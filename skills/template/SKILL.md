---
name: template
description: "Use when a project needs a feature that might already exist — search the private template library first, then the vetted Obsidian repo radar, then the open internet, and adapt what is found into THIS project rather than rebuilding it. Also use to check whether a feature is already extracted, to compare an open-source implementation before adopting it, or to harvest a feature back into the library. Triggers: 'do we already have this?', 'can we reuse', 'add telegram/whatsapp/voice to this', 'find an open source X', 'is there a template for', '/template'."
trigger: /template
---

# /template

Never rebuild what already exists. Search in a fixed order — private library, then
your own vetted radar, then the open internet — and adapt the winner into the project
you are standing in.

## Usage

```bash
/template                                  # ask what feature is needed
/template do we have a kanban board?       # search only, report honestly
/template add telegram notifications       # search, then adapt into this project
/template receipt OCR                      # likely Route C (open source)
/template harvest <thing>                  # push something back into the library
```

## What this is not

This is the **consumer** skill. It adapts features *into* the project you are in.

Library maintenance — extracting a new template, releasing a version, regenerating the
catalog, validating hashes — belongs to the `feature-template-library` skill inside the
library repo. Never do that work from a consumer project. See
[harvest-brief.md](references/harvest-brief.md) for the hand-off.

---

## Phase 0 — Locate both ends. Do not skip.

**The library.** In precedence order: `$FEATURE_TEMPLATE_LIBRARY`, then
`~/projects/Aclaude/template`. Confirm `catalog/index.json` exists there. If it does
not, say so and stop — do not silently fall through to a web search.

```bash
LIB="${FEATURE_TEMPLATE_LIBRARY:-$HOME/projects/Aclaude/template}"
```

**The target.** Identify the current project and its stack from `package.json`,
`pyproject.toml`, `go.mod`, or `Cargo.toml`. You need the language, the runtime version,
the test runner, and the persistence layer before you can judge any candidate. Record
them; every later phase depends on them.

**Restate the request as behavior, not technology.** "Add Telegram" is a channel
adapter, a delivery path, and an identity link. "Remember clients" is persistence,
tenant isolation, and retention. Search on behavior.

## Phase 1 — Search the private catalog. Always first.

```bash
python3 "$LIB/skills/feature-template-library/scripts/search_catalog.py" \
  "<the behavior, in plain language>" --json --prefer-built --min-score 20
```

`--prefer-built` ranks families that have real code above discovery pointers.
`--min-score 20` is what makes Route C reachable: the scorer returns *something* for
almost any query, so without a floor a coincidence gets reported as a candidate. A
confident hit scores 40+; incidental single-token overlap scores under 15.

Add `--stack`, `--category`, or `--status` only when the request supplies that
constraint. If you want to see the near-misses under the floor, re-run without
`--min-score` — but present them as near-misses, never as answers.

Read the `status` of the top hits and branch. **The status is the whole decision** —
49 catalog entries exist but only 12 have code.

| status | count | what it means | route |
|---|---|---|---|
| `ready` | 2 | built, plus a clean-fixture production proof | **A** |
| `verified` | 10 | built, contract tests pass | **A** |
| `mapped` | 18 | located in a source product, nothing built | **B** |
| `discovered` | 19 | located in upstream evidence, nothing built | **B** |

If nothing scores, **do not go to the internet yet — go to Phase 2.**

Report matches with status, what the template actually does, and its license. Stop here
if the user only asked "do we have it?" — do not start adapting uninvited.

### Phase 1b — Briefs written by `/templify` and `/template harvest`

The catalog only lists features someone has seeded. `/templify` records whole projects as
briefs in `$LIB/.planning/` first, so a feature can be known there before the catalog
has it. Search them every time Phase 1 is done, hit or miss:

```bash
grep -ril "<behavior keyword>" "$LIB"/.planning/harvest-*.md "$LIB"/.planning/templify-*.md 2>/dev/null
```

Each brief opens with front-matter (`status: briefed`, `source_repo`, `source_commit`,
`extraction_mode`, `priority`, `keywords`). Read only that front-matter and the behavior
checklist to judge a hit.

A brief is a **pointer, not a template** — treat it exactly like a `mapped` entry
(Route B): it names a working implementation, its project, commit and paths, and what to
strip. It is never installable and never described as such. If a brief matches, offer
Route B1 (adapt from the source at the pinned commit via `git show <commit>:<path>`) or
B2 (extract it properly in the library repo).

## Phase 2 — Search the source itself. The catalog only knows what someone wrote down.

The catalog indexes 49 hand-seeded families. A feature only becomes findable there once a
human writes it up, so **anything buried inside a larger feature is invisible to Phase 1**.
virtual-office exports CSV from `apps/web/src/attendance/attendanceView.ts`, with a test
beside it, and no catalog family mentions csv at all.

So before going outward, search the code you already own:

```bash
python3 "$LIB/scripts/search_sources.py" "<the behavior>" --json
```

It reads the pinned products at their commits (never the working tree) and returns
directory clusters, not grep lines, with:

- `implementation` and `tests` — a feature is a file that does the thing, with a test
  beside it. **A test-only cluster is a passing mention, not a feature**, and is demoted.
- `covered_by` — whether a catalog family already cites those paths.

Read the result honestly. A hit means *behaviour like this exists in your code*; it does
not mean a reusable boundary exists. Offer:

- **adapt from there** — treat it like Route B1, reading at the pin, and
- **seed a family** so the next search finds it in Phase 1 instead of Phase 2. This is
  how the catalog grows from your own code rather than only from hand-authoring.

Only when Phase 1 and Phase 2 both come up empty does the request go outward.

---

## Route A — a built template exists

1. **Load only the contract.** `templates/<id>/TEMPLATE.md`, `template.yaml`, and
   `compatibility.json`. Not the source, not the tests, not the catalog. Both manifests
   are **JSON despite the `.yaml` extension** — parse with `json`.
2. **Check dependencies.** `template.yaml` declares them and they are real:
   `board-notifications-and-counts` needs `pending-action-store`; the board siblings need
   `shared-board-core`. Adopting one may mean adopting two.
3. **Check conflicts.** `compatibility.json` carries `conflict_policy.owned_paths`.
   Compare against the target tree and name every collision.
4. **Report, then stop for approval.** Cover: behavior, dependencies, conflicts,
   language conversion required, and — if status is `verified` rather than `ready` —
   say plainly that it has contract tests but no production adapter proof.
5. **Adapt.** Convert to the target's language and conventions *now*; that is when
   conversion is supposed to happen. Carry across the behavior contract and the test
   scenarios, which are language-independent. **Port the tests.** A template without its
   tests is just code, and the tests are the part worth having.
6. **Record it** — see Phase 3.

Full procedure: [adapting.md](references/adapting.md).

## Route B — the catalog knows where it lives, but nothing is built

Say that plainly. A `mapped` or `discovered` entry proves relevant source exists; it
proves nothing about a reusable boundary. Then offer two options and let the user pick:

**b1 — adapt straight from the pinned source.** Cheaper, no library artifacts produced.
- Read **at the pin**, never from the working tree:
  ```bash
  git -C <product> show <pin>:<path>      # never `cat <product>/<path>`
  ```
  The source products are actively developed; one moved through four HEADs in a single
  session. Reading the checkout can put behavior into your project that does not exist
  at the pin.
- **Verify the family's declared paths before quoting any evidence:**
  ```bash
  git -C <product> ls-tree -r <pin> --name-only | grep <pattern>
  ```
  Seed globs have silently matched nothing twice — once too narrow, once because `[` in
  a Next.js `[token]` route was read as a character class. An unverified glob means an
  invented contract.
- **Critique before you copy.** These products carry known defects: missing TTL and audit
  trail, non-idempotent save, floating-point money, server-timezone dates, executable
  endpoints held in React. Do not assume source behavior is correct.

**b2 — extract it properly first.** Hand off to the library repo. Costly (a real
extraction is a session's work), but the result is reusable forever.

## Route C — nothing local, go outward

**Expect the feature to be buried inside a whole product, not to be its own repo.** That
is the normal case. Full procedure:
[extracting-from-a-product.md](references/extracting-from-a-product.md).

1. **Search your own radar first.** These are repos already vetted, and they are what
   "the open-source project we talked about" means:
   ```
   $OBSIDIAN_VAULT/Research/Tools & Repos Radar.md
   $OBSIDIAN_VAULT/03-wiki/entities/
   ```
   Grep both before touching the internet.
2. **Then the open web**, via `mcp__exa__web_search_exa` or `mcp__tavily__tavily_search`.
   Search for the *behaviour*, and accept products that merely contain it.
3. **Screen without cloning** — license, maintenance, tests, boundary, stack fit, and
   roughly where inside the product the feature lives. Rubric:
   [screening.md](references/screening.md). Reject GPL/AGPL unless the user explicitly
   accepts the obligation. **No license means no permission**, not "public".
4. **Present 3–5 as a comparison table. Stop for approval.**
5. **Shallow-clone only the approved one**, and record its commit immediately —
   a throwaway clone whose commit was never written down is unreproducible.
6. **Locate the feature** by following tests and imports outward until they stop being
   about the feature and start being about the host product.
7. **Survey the whole product before deleting the clone.** You have it on disk exactly
   once. Write down what *else* is in there, one line per feature with its path, so the
   next time the answer is a note instead of another clone. This is the step that pays
   for the clone.
8. **Come back with the trim questions.** Sort what you found into core / bundled extras
   / host wiring / gaps, and ask. Never silently trim, never silently keep — both change
   what the feature costs to own. State each extra concretely and then recommend.
9. **Rebuild, do not port,** when the language differs — which it usually does. Read for
   concepts, write the test scenarios in the target language first, implement
   idiomatically. See the boundary note in [adapting.md](references/adapting.md).
10. **Delete the clone** once the survey is written.
11. **Harvest back into the library** — both halves. The project is unblocked now, and a
    brief goes to the library so the next project does not repeat any of this. Write the
    brief; do not create template directories from a consumer project. Format:
    [harvest-brief.md](references/harvest-brief.md).
12. **Record it** — Phase 3, plus the product survey as its own entity page.

---

## Phase 3 — Write it down, or it did not happen

There is no installer and no lockfile, so this ledger is the only thing that can answer
"which projects need the 0.2.0 fix?" Append one row to
`$OBSIDIAN_VAULT/04-outputs/tables/template-adoptions.md`:

```
| date | template | version | project | route | adaptations |
```

Record what you *changed* during adaptation, not just what you took — that column is
what tells a future upgrade whether it can be applied cleanly.

For a Route C find, also add an entity page under `03-wiki/entities/` and a section in
`Research/Tools & Repos Radar.md`.

The vault has a strict schema (`$OBSIDIAN_VAULT/claudd.md`): entity pages need
frontmatter and the required sections, and **every durable change appends to `log.md`
and updates `index.md`**. Follow it. Do not invent folders.

---

## Guardrails

- **Never call a `mapped` or `discovered` entry installable.** It is a pointer, not a
  template. Saying otherwise is the single most damaging thing this skill can do.
- **Never read a source product from its working tree.** `git show <pin>:<path>` only.
- **Never write to `templates/`, `catalog/`, or any manifest from a consumer project.**
  Harvesting is a hand-off, not an edit.
- **Never write code into the target before the approval gate.** Report first.
- **Never adopt GPL/AGPL or unlicensed code without explicit approval.**
- **Never skip Phase 1 or Phase 2.** Searching the web before searching the catalog *and*
  your own source is the exact failure this library was built to prevent. The catalog
  only knows what someone wrote down; your code knows more than the catalog does.
- **Never port code across languages.** Read for concepts and rebuild from the contract.
  "Trim, do not rebuild" assumes you own the source and the language matches — a foreign
  find has nothing to lift.
- **Never delete a clone before its survey is written.** You have the product on disk
  exactly once; the survey is what outlives it.
- **Never trim or keep a bundled extra silently.** Both are the user's call.
- **Never copy agent, proposal, or conversation logic into a channel adapter.** Compose
  from the existing template instead — that duplication is the original sin here.
- **Do not recursively read the catalog, every template, or all upstream source.** The
  library is built on progressive disclosure; one search should read one index.

## Verification

Before reporting an adoption complete:

- The ported tests run **in the target project** and pass.
- No file outside the reported conflict list was modified.
- The ledger row is written and `log.md` appended.
- If a dependency was implied but not adopted, that is stated, not hidden.
