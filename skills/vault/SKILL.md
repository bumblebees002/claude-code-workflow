---
name: vault
description: "Use when working in any project that has (or should have) an Obsidian page — to read what is already known before exploring the repo, to record a decision or a lesson so it survives the session, to refresh a project's page after changes, or to document a project for the first time. Also use to answer 'why did we do it this way?', 'have we hit this before?', or 'what did we decide about X?'. Triggers: 'document this project', 'add to obsidian', 'remember this decision', 'why did we choose', 'what do we know about', '/vault'."
trigger: /vault
---

# /vault

The vault is not a copy of the code. Git already stores the code, and each repo's own
`CLAUDE.md` already stores its rules. **The vault stores the *why*** — decisions, dead
ends, and lessons — because that is the only part that transfers between projects, and
transfer is the entire return on writing anything down.

## Usage

```bash
/vault                      # status: what is registered, stale, or missing prose
/vault sync                 # refresh this project's machine facts (free)
/vault add                  # first page for this project: facts + prose
/vault next                 # propose the next project to document, then ask
/vault ask <question>       # answer from the vault before reading code
/vault note <decision>      # append one durable decision or lesson
```

## The economics — respect them or this stops being worth running

Every page has two halves, and confusing them is the failure mode.

| Half | Written by | Cost | Regenerated |
|---|---|---|---|
| Between `<!-- project:start -->` and `<!-- project:end -->` | `sync_project.py`, from git and manifests | **~0 — never read source to produce it** | every sync |
| Everything outside | you, rarely | real | **never** |

**Never spend model tokens producing anything that belongs in the generated block.** If a
fact can be derived from `git`, `package.json`, or the project's `CLAUDE.md` headings, the
script already has it. Reading the codebase to restate it is pure loss, and it is what
makes people stop syncing, which is what lets pages rot.

## Phase 0 — Locate both ends

```bash
LIB="${FEATURE_TEMPLATE_LIBRARY:-$HOME/projects/Aclaude/template}"
VAULT="${OBSIDIAN_VAULT_PATH:-$HOME/obsidian-vault}"
```

The repo is `git rev-parse --show-toplevel`; the page is its basename lowercased with
`_` → `-`. So `ai_accountant` is `03-wiki/entities/ai-accountant.md` — **check before
creating, or you get a second page for a project that already has one.**

## `sync` — refresh the machine facts

**This is usually already done.** The `SessionStart` hook (`~/.claude/hooks/vault-context.py`)
regenerates a registered project's machine block whenever HEAD has moved — 78 ms when the
page is current, ~240 ms when it actually resyncs. So never end a turn by suggesting the
user run a sync: if the session started in that repo, the facts are current.

Run it by hand only for a repo you are **not** sitting in, or to verify:

```bash
python3 "$LIB/scripts/sync_project.py"                    # the repo you are in
python3 "$LIB/scripts/sync_project.py" --all              # every registered project
python3 "$LIB/scripts/sync_project.py" --check            # verify, write nothing
```

That is the whole operation. Report which pages changed. Do not read the codebase, do not
"improve" the block by hand — it is regenerated, so hand edits inside the markers are lost
on the next run, silently.

**What automation cannot do.** Only the machine half self-heals. Prose — the *why* — has no
derivation, so nothing regenerates it and nothing can tell you it is wrong; the hook only
warns that a page moved by 25+ commits, which makes staleness *likely*, not certain. When
you have just learned something durable about a project, `note` it. That is the half that
needs a human trigger, and it is the half that carries the value.

## `add` — the one expensive operation, done once per project

1. **Generate the facts first**: `python3 "$LIB/scripts/sync_project.py"`. Now you have
   the stack, shape, commands, and the project's own rules for free.
2. **Read the generated block and the project's `CLAUDE.md`.** Usually that is enough.
   Read source only where the *why* is genuinely unclear, and read narrowly.
3. **Write only the four prose sections**, replacing the `_Not yet written._` placeholders:

   - **Summary** — what it is and who it serves, in two or three sentences. Not a
     feature list; the block already carries the structure.
   - **Relevance** — why it exists, and what depends on it.
   - **Related Concepts** — `[[links]]` to other projects, concepts, and templates.
     **This is the part that makes the graph a brain.** A project with no links is a
     document; a project with links is knowledge that transfers.
   - **Open Questions** — decisions pending, dead ends already tried, what broke last time.
     Highest-value section by a wide margin. Everything else can be re-derived from code.

4. **Prefer linking over restating.** If a fact lives in a template page, a concept page,
   or the project's `CLAUDE.md`, link to it. Two copies of a fact means one will be wrong
   later and nothing will say which.
5. Update `index.md`. The script already appends to `log.md`.

## `next` — one project at a time, never a batch

Rank the unregistered repos under `~/projects/Aclaude/` by (no page yet) × (recent commit
activity) × (size), **propose exactly one, and stop for a yes or no.** Do not chain into a
second without being asked. Documenting fourteen projects in one sitting produces fourteen
pages nobody read.

## `ask` — read before you explore

1. Read the project's page first, then `index.md`, then search the vault.
2. Answer with citations to the pages used.
3. **If the vault contradicts the code, the code wins and the page is stale** — say so
   plainly, and offer `/vault sync`.
4. If the answer was durable and not already recorded, offer to `note` it.

## `note` — how the vault gets smarter

Append to **Open Questions** or **Relevance** on the relevant page. One entry, dated, with
the reasoning, not just the conclusion — a decision without its reason cannot be revisited
when circumstances change. Cross-link it from any other project it affects; that link is
the mechanism by which project #2 goes faster than project #1.

## Guardrails

- **Never write inside the markers.** It is generated; your edit is lost on the next sync.
- **Never read source to produce facts the script already derives.** That is the cost that
  kills the habit.
- **Never batch-document projects.** One, proposed, approved.
- **Never let a page assert something you did not verify.** A page that is wrong is worse
  than a page that is missing, because it gets believed. `ai-accountant.md` sat 101 commits
  stale pointing at a directory that no longer existed — that is the failure being fixed.
- **Never invent folders.** The vault schema is `claudd.md`; entity pages need its six
  required sections and its frontmatter. Every durable change updates `index.md` and
  appends to `log.md`.
- **Never write to the vault from a script that is not `sync_project.py`** for machine
  facts — two writers means drift.
- **Do not document a project just because it exists.** A repo with no decisions worth
  recording earns a generated block and nothing else. That is a complete, honest outcome.
