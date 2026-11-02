---
name: compact-prompt
description: Write a ready-to-paste `/compact <instructions>` command tailored to what THIS session is doing right now, so compaction keeps what matters and drops what doesn't. Detects the situation itself — a plan not yet executed, subagents mid-flight across waves/worktrees, a change of direction, mid-implementation, debugging, or research — and writes the matching preservation instructions. Use when the user asks for a compact prompt, says the context is getting full, gets the strategic-compact reminder, or types '/compact-prompt'. Optional argument forces a scenario: plan | agents | pivot | build | debug | research.
---

# Compact Prompt

`/compact` accepts free-text instructions: `/compact <what to keep>`. A bare
`/compact` summarizes generically and loses the things this session depends on.
Your job: read the current session, work out which situation it is in, and
write the instructions that make the summary carry everything needed to keep
going without re-asking the user.

You are writing for the summarizer, which sees the whole conversation. Name the
concrete things to keep: real paths, branch names, agent names, commit SHAs,
counts. Do not write "keep the important details".

## Step 1: Detect the scenario

If the user passed an argument, use it. Otherwise read the recent turns and
pick every scenario that applies. They combine; a session is often
`agents + pivot`.

| Scenario | Signals in the session |
|---|---|
| **plan** | A plan was written or agreed (plan file, numbered steps, "the plan is…") and execution has not started or has barely started. |
| **agents** | Agent/Task calls were made; background agents are running or have reported; work is split into waves, phases or worktrees; more launches are still due. |
| **pivot** | The user changed direction after work was done: "change this", "redo", "plan again", a rejected approach. |
| **build** | Files are being edited now; tests or builds are being run; uncommitted changes exist. |
| **debug** | A bug is being chased: hypotheses, repro steps, things ruled out. |
| **research** | Mostly reading, searching and answering, with conclusions but no edits. |

If nothing clearly matches, use **build** plus whatever is closest, and say
which you picked.

## Step 2: Gather the facts before writing

Check live state instead of trusting memory. Checks are cheap; getting them wrong is not.

- `git status --short`, `git branch --show-current`, `git log --oneline -5` in each repo touched.
- If agents or worktrees are involved: `git worktree list`, and which agents are still running versus returned (from the task notifications in this session).
- The path of any plan file, and whether it is current or superseded.

## Step 3: Write the instructions

Always include these, in every scenario:

- **Goal**: one line on what the user is ultimately trying to get done.
- **Where things live**: repos, branches, key files, and plan-file paths.
- **Decisions and user preferences made in this session**, including things the user rejected or banned. These are the most expensive to lose.
- **Next action**: the exact next step after compaction, as a command, not a vibe.
- **After compaction, verify with git before acting**: state may have moved while compacting (agents finish, files change).

Then add the scenario blocks.

**plan**
- Keep the full plan verbatim: every step, its order, the files each step touches, and its verification check.
- Keep why this plan beat the alternatives, in one line per rejected option.
- Mark it clearly: NOT STARTED, or done through step N.
- Next action: "execute step 1 (or N+1) of the plan".

**agents**
- A roster table with one row per agent: name/id · task · worktree + branch · status (done / running / not launched) · result or blocker · merged? (y/n).
- Totals: X done, Y running, Z still to launch, and which wave is next.
- The launch rules in force: dependency order, what can run in parallel, the verification gate before merge or commit, the model or agent type used.
- Running agents: keep their names/ids so they can be messaged, and note that their completion notifications will still arrive.
- Next action: which agents to launch next, with their assignments.

**pivot**
- What was finished and is still valid, so it is not redone.
- What changed and why, in the user's own words where possible.
- The old plan, marked SUPERSEDED in one line; do not carry its details forward.
- The new plan in full.

**build**
- Files changed so far and what each change does.
- What is left, in order.
- Last test/build result, with the exact command and pass/fail.
- Uncommitted or unpushed state.

**debug**
- Symptom, exact error text, and the repro command.
- Hypotheses tested and RULED OUT, with evidence, so they are not re-tested.
- The current leading hypothesis and the next experiment.

**research**
- Conclusions reached, each with its source (URL, file, command output).
- Open questions still unanswered.

## Drop list

Tell the summarizer to drop: raw tool output already acted on, full file
contents that can be re-read, superseded plans, dead-end exploration beyond
one line each, and chit-chat.

## Output format

Reply with exactly:

1. One line: `Scenario: <detected scenarios>`. If a scenario was guessed, add why.
2. A single fenced code block containing the whole command, starting with
   `/compact ` and ready to paste. Keep it under ~350 words: dense bullet
   fragments, not prose.
3. Nothing else. Do not run `/compact` yourself; the user pastes it.
