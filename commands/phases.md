---
description: Execute a multi-phase plan as a dependency graph — parallel subagents in git worktrees where independent, sequential where phases share files or depend on each other, with a single serialized verification gate before every commit.
argument-hint: [phase list, or leave blank to use the phases from the current plan]
---

# Execute phases as a dependency graph

You are the **orchestrator** of a multi-phase plan. The phases are:

$ARGUMENTS

If the section above is empty, use the phases from the current plan / recent conversation instead.

Follow these four steps **in order**. Do not skip the scout step.

---

## THE THREE RULES

Everything below depends on these. Never break them.

1. **Never nest agents.** You do all the fan-out yourself, at **every depth**. A subagent must
   never spawn another subagent.
2. **Subagents never commit.** No `git add`, `git commit`, `git merge`, or any writing git command.
   Concurrent git in one worktree collides on `.git/index.lock`. You make every commit yourself.
3. **Subagents never run the full gate.** No full build, no test suite, no dev server. You run
   every verification gate yourself, one at a time. This is what makes concurrent gates
   *impossible* rather than merely discouraged — and it is what keeps the machine cool.

---

## THE RECURSIVE RULE

The plan is a graph of **nodes**. A phase is a node. Everything below applies to a node at **any
depth** — there is no special "phase level" and "sub-task level", just the same rule applied again.

**Decompose:** any node too large for one agent's context is replaced by a sub-graph of child
nodes. Each child is scouted exactly like its parent — its own files, its own dependencies — and
may itself be decomposed. Recurse as deep as the work actually goes.

**Schedule:** two nodes may run **in parallel** if and only if **both** hold:

- no dependency path between them, **and**
- their file sets are **disjoint**.

If either fails → **serialize** them in dependency order. A node that touches the same file as
another node is never parallel with it, at any depth.

**Stop decomposing** when a node fits comfortably in one agent — roughly a handful of files and one
coherent change. Splitting past that point costs more in scouting and coordination than it returns.

### Worktrees mark commit boundaries — and are never nested

A worktree exists so that **independent commit histories don't collide.** So:

- **A node that produces a commit gets its own worktree.** In practice that is a top-level phase.
- **Its descendants share that one worktree.** They never commit, so they need no branch of their
  own, and disjoint files mean they never collide. A dependent child simply finds its
  prerequisite's files already on disk — no commit, no merge, no gate between children.

**Do not create worktrees inside worktrees.** Three reasons, and they all bite:

1. Git has no worktree hierarchy — every worktree is a flat sibling registered in the main repo, so
   "nested" is a directory illusion, not a real structure.
2. A worktree directory physically placed inside another shows up as untracked junk in the outer
   tree's `git status`, and is easy to sweep into a commit by accident.
3. **Every extra worktree is another commit boundary, and every commit boundary is another full
   verification gate.** Gates run one at a time, so more worktrees means a longer serial queue and
   a hotter machine — the opposite of what you want.

So: **recurse the task graph as deep as you like; keep the worktrees flat.** That is what gives
maximum safe parallelism — the decomposition buys you concurrency, while the flat worktree set
keeps the serial gate queue as short as possible.

---

## STEP 1 — Scout only (do NOT build yet)

Scout **every node, recursively**. For each one determine:

- The exact files it will **create or modify**.
- Its **dependencies** — which sibling nodes must finish before it can start.
- Its **size** — does it fit in one agent, or must it be decomposed further?

If it must be decomposed, name its children and scout each of them the same way. Keep going until
every leaf fits one agent. Decompose a node when it spans several independent modules, touches many
files, or is plainly more than one agent's context.

Scale exploration to the task: if a node's files are already obvious or I named them, don't launch
a scout for it. Only spin up exploration subagents where the files are genuinely unknown, and let
them return a **compressed summary** so the main context stays clean. Don't recurse for its own
sake — a node that already fits one agent is a leaf, however shallow that makes the tree.

Present the result as a table, one row per **leaf**, indented to show the tree:

| Node | Files touched | Depends on | Runs parallel with | Worktree |
|------|---------------|------------|--------------------|----------|

Use dotted paths for depth (`B`, `B.1`, `B.1.a`) and name the **worktree** each leaf executes in —
descendants of the same phase all show the same worktree, which is what makes the sharing visible
and reviewable.

Then state the **max useful parallelism**, work out a **recommended concurrency**, and **ask me how
many agents to run this run** with AskUserQuestion — the recommendation first, labelled
"(Recommended)", plus 2–3 alternatives from 2 / 3 / 4 / 5 / all. Skip the question only if I
already named a number (in this prompt or when I approved the plan) or the width is 1.

Recommend **min(max useful parallelism, 4)**, then adjust: go lower when most leaves are tiny
(1–2 files — setup costs more than it saves) or share a hot area of the repo; go higher than 4 only
when the width is bigger and the leaves are heavy. Give the reason in one line, e.g. "Recommended 4:
widest layer is 6 leaves, 4 keeps disk and noise sensible." Agents are mostly network-bound, so a
high number costs disk and noise rather than heat, and the gate stays serial either way.

Max useful parallelism is the **width of the leaf graph** — the largest number of leaves that are
mutually independent and file-disjoint — not the total node count. A chain of 3 contributes 1.

Also report, so I can sanity-check the shape as it runs:

- total leaves, and the **depth** of the deepest branch
- number of worktrees (= number of gate runs, = the serial queue length)
- any node you decomposed that turned out to be a pure serial chain

Once I answer the concurrency question, **go straight to Step 2** — no second confirmation.
**STOP and ask instead** if the shape looks wrong: more than 12 leaves, depth over 3, two leaves
you cannot make file-disjoint, or a precondition in Step 2 fails.

---

## STEP 2 — Build the execution graph and launch

### Preconditions — check before creating any worktree

- The repo is a git repo.
- The working tree is clean.
- Resolve the **base branch** from the repo (`main`, `master`, or the current branch). Never assume
  `main`.

### Create one worktree per phase

Create it **yourself** rather than using `isolation: "worktree"`. That flag gives each agent its
*own* worktree, so it cannot be the mechanism for several agents sharing one — and sharing is what
lets a decomposed phase run in parallel:

```
git worktree add ../wt-<phase> -b phase/<phase> <base-branch>
```

Independent phases get independent worktrees and run side-by-side. Phases that share files or have
a dependency are **serialized** — a dependent phase starts only after its prerequisite has passed
its gate, been committed, and merged.

Two phases touching the same file must **never** run in parallel.

Independent chains run side-by-side: `A→B` and `C→D` and `E` all progress at once, then a final
join phase (if any) runs last.

### Launch the leaves — flat, at every depth

You launch **leaves only**. Interior nodes are just structure; they never get an agent of their
own. Every leaf under a phase runs in **that phase's single worktree**, launched as a flat sibling,
each told its working directory and exactly which files it exclusively owns.

Walk the graph and launch a leaf the moment two things are true:

1. every node it depends on has reported done, **and**
2. a concurrency slot is free.

That is the whole scheduler. It naturally produces the behaviour you want at any depth — leaves
from *different* phases, and independent leaves from the *same* phase, all run at once, while
dependent ones queue behind their prerequisites.

The handoff between leaves in one worktree is **much lighter than between phases**: they share a
working tree and never commit, so a dependent leaf simply finds its prerequisite's files already on
disk. No commit, no merge, and **no gate between leaves** — the full gate runs once, for the whole
worktree, at the end.

**Decompose even when the children form a pure serial chain.** Zero parallelism is still worth it:
three sequential agents each get a fresh context, which is the whole reason for decomposing — one
agent doing all three would exhaust itself. Speed is the bonus, not the point.

### Concurrency

Respect the number I chose in Step 1. Queue the remainder and start each as a slot frees.

---

## STEP 3 — Implementation, then the serialized gate

### What each subagent does

1. **Explore** its assigned files (only if not already known).
2. **Implement** its leaf.
3. Run a **cheap check only** — lint / typecheck limited to the files it changed.
4. **Report back**: its node id, the files it changed, and a short summary.

Give every agent its **absolute worktree path** in the prompt, and have it confirm the path back in
its report — that confirmation is your check that two leaves you believed were in the same worktree
actually were, and that no agent wandered into the main checkout.

State explicitly in every agent prompt what it must **not** do:

- run the full build, the test suite, or a dev server
- commit, or touch any file outside its assigned set
- spawn another subagent
- open a browser, take screenshots, or navigate pages — verification is automated only

### What you (the orchestrator) do

Once **every leaf** belonging to a worktree has finished — at every depth, the parallel ones and
every serialized chain — run the **full gate** on that worktree.

**One worktree at a time. Never two gates in parallel.** This is a plain serial loop; a worktree
still mid-chain is simply not yet eligible for the queue. Running several builds at once overheats
the machine, so this ordering is mandatory, not advisory.

Resolve the gate commands from the project — do **not** assume npm:

| Detected | build | lint | test |
|---|---|---|---|
| `package.json` | `npm run build` | `npm run lint` | `npm run test` |
| `pyproject.toml` / `requirements.txt` | — | `ruff check` (+ `mypy` if configured) | `pytest -n2` |
| `Cargo.toml` | `cargo build` | `cargo clippy` | `cargo test -- --test-threads=2` |
| `go.mod` | `go build ./...` | `go vet ./...` | `go test ./...` |
| `Makefile` | `make build` | `make lint` | `make test` |

Only run the scripts that actually exist. **If no gate commands can be detected at all, STOP and
ask me — never report a pass on an empty gate.**

Pin test-runner parallelism so the one serial gate stays cool: `jest --maxWorkers=2`,
`vitest --maxThreads=2`, `pytest -n2`, `cargo test -- --test-threads=2`.

Report **pass/fail** for each step.

- If tests don't exist yet for what this phase touches, **write them now** so verification stays
  automated and cheap.
- **On failure:** send that worktree's agent back with the failure output to fix it, then re-run
  the gate for that worktree — still serially, still one at a time.
- If it can't be fixed, **stop that chain**, leave the base branch untouched, and report it — do
  **NOT** merge broken code.

**Commit only after the gate passes, and make the commit yourself.**

---

## STEP 4 — Merge, clean up, report

- Merge each **passing** phase into the resolved base branch in **dependency order**.
- Resolve or clearly flag any merge conflicts.
- **Clean up**: `git worktree remove` each merged worktree and prune its branch. Treat "already
  removed" as success, not an error. Finish with `git worktree prune`.
- **Never remove a worktree whose phase failed its gate** — leave it for inspection and say so.
- Give a final summary:
  - ✅ merged (with commit refs)
  - ❌ failed the gate (with the failing step)
  - ⚠️ conflicts or anything needing my attention
  - 🌳 any worktrees deliberately left in place for inspection

Keep me informed at each phase boundary, not just at the end.
