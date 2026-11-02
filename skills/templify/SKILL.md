---
name: templify
description: "Use when an existing, already-built project should be turned into reusable templates — break the whole project into features, judge each one for reusability, and write one harvest brief per feature (plus a master map) into the private template library. Consumer-side only: it analyses and briefs, it never extracts. Triggers: 'templify this project', 'turn this into templates', 'break this project into features', 'what in this project is reusable', 'harvest everything from this project', '/templify'."
trigger: /templify
---

# /templify

Take a finished project, split it into features, decide which are worth keeping as
templates, and write a brief for each one. The extraction itself happens later, inside the
library repo, with the maintainer skill (`feature-template-library`).

`/template harvest <thing>` handles ONE feature. `/templify` handles the WHOLE project:
it finds the features first, then runs the harvest-brief process on each.

## Usage

```bash
/templify                    # templify the project I'm standing in
/templify <path>             # templify another project
/templify map                # stop after Phase 2: show the feature map, write nothing
/templify <feature>          # one feature only (same as /template harvest)
```

## Hard rules

- **Brief, never extract.** The only files this skill *authors* in the library are the
  briefs in `$LIB/.planning/`. Never create `templates/<id>/`, never edit `catalog/`,
  manifests or the library `CLAUDE.md`.
  (Same rule as `~/.claude/skills/template/references/harvest-brief.md` — read it first.)
- **But it does sync what already exists.** Templates and catalog changes made by
  maintainer sessions sit uncommitted in the library checkout; Phase 5 validates them and
  commits/pushes them with the briefs, so the `templates/` folder on GitHub never lags
  behind this Mac. Syncing is not authoring.
- **A templify is not finished until it is in BOTH places**: the Obsidian vault AND the
  private GitHub library. `/template` reads the briefs back (its Phase 1b), so a brief
  that is missing from either place is a feature the next search will not find.
- **Read-only on the source project.** No refactors, no moving files to "prepare" them.
- **No versions, no lifecycle status, no "proven" claims.** One project is evidence, not a
  contract.
- **`reject` is a valid answer.** A feature too entangled to extract is recorded with
  reasons, not forced into a template.
- Never write secrets, `.env` values, or customer data into a brief.

## Phase 0 — Locate both ends

```bash
LIB="${FEATURE_TEMPLATE_LIBRARY:-$HOME/projects/Aclaude/template}"
test -f "$LIB/catalog/index.json" || echo "library missing"   # if missing: say so and stop
```

Identify the source project's stack (`package.json`, `pyproject.toml`, `go.mod`,
`Cargo.toml`): language, runtime version, test runner, persistence, auth, deploy target.
Record the git remote and HEAD commit — provenance is mandatory. Find the license; if there
is none, say so (the project is then not freely harvestable and the user must decide).

## Phase 1 — Inventory the project

Cheapest source first:

1. `graphify-out/` exists → query it for communities / god nodes.
2. Otherwise read: README, route/page tree, API route list, DB schema/migrations, env
   var names (names only), `package.json` dependencies, top-level folder layout.
3. Only then open source files, and only to settle a boundary question.

Do not read the whole repo. The output of this phase is a flat list of candidate
**features** stated as behavior ("a user can approve a pending action"), never as technology
("uses Redis").

## Phase 2 — Decompose into features

A feature is one user-visible capability with its own data and its own tests. Rules:

- Split until each feature has **one reason to exist**. "Auth + billing + email" is three.
- Separate **product wiring** (routes, branding, copy, config) from **reusable core**.
- Cross-cutting concerns (auth, persistence, logging, notifications, jobs) are features in
  their own right — they are usually what other features should *compose from*, not copy.
- Record dependencies between features. This is the build order for extraction.

Produce the **feature map** table:

| # | feature (behavior) | files/dirs | depends on | external deps | tests exist? |
|---|---|---|---|---|---|

If invoked as `/templify map`, stop here and show the table.

## Phase 3 — Judge each feature

For every row, in this order:

1. **Already in the library?**
   ```bash
   python3 "$LIB/skills/feature-template-library/scripts/search_catalog.py" \
     "<behavior in plain language>" --json --prefer-built --min-score 20
   ```
   - Score 40+ and status `ready`/`verified` → verdict **already-templated**. Note whether
     this project should *adopt* the template instead (a clean-up, not a harvest).
   - Hit at `mapped`/`discovered` → verdict **upgrade-candidate**: the brief feeds that
     existing family rather than starting a new one.
   - No hit → **new**.
2. **Reusability test** — all must be answerable:
   - Does it work with the product wiring stripped off? Which files break?
   - What would have to become an injected **port** (persistence, clock, delivery, auth, HTTP)?
   - Does it carry business rules specific to this product's domain?
   - Are there tests? Without them the test scenarios must be written from behavior.
   - Defects visible in the code that must be fixed during extraction, not carried over.
3. **Extraction mode**: `service` · `package` · `generator` · `reference` · `reject`.
4. **Priority**: `high` (reusable core, no tests needed to start, many future products
   would want it), `medium`, `low`, `skip` (already templated or rejected).

Parallelism: for projects with 5+ features, the per-feature analysis in step 2 may be
fanned out to read-only `Explore` agents, one per feature, each handed only that
feature's files and the brief checklist. Agents report; the main session writes the briefs.

## Phase 4 — Write the briefs

For each feature with verdict `new` or `upgrade-candidate` and priority ≠ `skip`, write

```
$LIB/.planning/harvest-<project>-<feature-slug>.md
```

starting with the `status: briefed` front-matter block defined in `harvest-brief.md`
(that is what `/template` Phase 1b greps), then the nine-section structure (behavior checklist · provenance ·
proposed boundary · ports · test scenarios · defects found · composition · dependencies ·
extraction mode). Provenance is the project's remote + the exact commit + license + paths.

Then write the master map:

```
$LIB/.planning/templify-<project>.md
```

containing: the project's stack and commit, the full feature map table with verdicts and
priorities, the recommended **extraction order** (dependencies first, shared concerns
first), and the list of rejected features with reasons.

Check that a brief file does not already exist before writing; if one does, show a diff
summary and ask — do not overwrite.

## Phase 5 — Publish to GitHub (mandatory)

The library is the private repo `bumblebees002/feature-template-library`, branch `main`.
The library checkout is usually **dirty** (modified catalog files, untracked templates) and
often **ahead of origin** with commits that are not part of this templify. So publish with
path-limited git, never a blanket add. Two commits, so history stays readable:

```bash
cd "$LIB"
gh repo view bumblebees002/feature-template-library --json isPrivate   # must be true; if not, STOP
gh auth status                                  # active account must be bumblebees002; if not, STOP and say so

# 1. the briefs this run wrote
FILES=".planning/templify-<project>.md .planning/harvest-<project>-<slug>.md ..."
git add -- $FILES
git commit -m "Templify <project>: <N> feature briefs" -- $FILES

# 2. the templates folder + catalog, only if they have uncommitted changes
git status --short -- templates catalog          # nothing listed -> skip step 2
python3 scripts/build_catalog.py --check         # catalog must match the templates
python3 scripts/validate_catalog.py              # add --require-vendor only if vendor/ exists
python3 -m unittest discover -s tests            # all must pass
git add -- templates catalog
git commit -m "Sync templates folder and catalog" -- templates catalog

git rev-list --left-right --count HEAD...origin/main   # first number = local commits not on GitHub
```

- **If any step-2 check fails, do not commit templates/catalog.** Push the briefs alone,
  and tell the user which check failed and which template is inconsistent.
- Scan the new/changed template files for secrets before committing (key/token/password
  assignments, `.env`, `.pem`). Test fixtures with obviously fake values are fine; say so.
- Leave unrelated changes alone — e.g. a deleted `vendor/README.md`. Report them; do not
  commit or restore them.
- If the first rev-list number is more than the commits this run just made (other
  unpushed commits), **list them with `git log origin/main..HEAD --oneline` and ask before
  pushing** — a push would publish them too. A standing "yes, push everything" from the
  user in this conversation counts; one from an earlier session does not.
- Otherwise `git push origin main`.
- Never `git add -A` / `git add .`, never `--force`, never stash or reset the user's
  uncommitted work. If the push is rejected, report why and stop.
- Verify, don't assume: `git fetch origin && git rev-list --left-right --count HEAD...origin/main`
  must print `0 0`, and `git log origin/main -2 --stat` must show the brief files (and the
  templates/catalog files if step 2 ran). Quote the commit hashes and the GitHub URL in
  the handoff.
- Never put secrets, `.env` values, or customer data in a brief — the repo is private, but
  it is still a remote copy.

## Phase 6 — Record in the vault (mandatory)

Per the vault schema (`$OBSIDIAN_VAULT/claudd.md`; see the `vault` skill):

- entity page under `03-wiki/entities/` for the project if new, listing its features
- an entry in `Research/Tools & Repos Radar.md`
- rows in `04-outputs/tables/template-adoptions.md` for any feature that already maps to
  a template
- append to `log.md`, update `index.md`

Each vault entry links the GitHub commit from Phase 5. Do not invent folders.

## Phase 7 — Hand off, in plain words

Report in this shape, short:

1. **N features found**, X already templated, Y new, Z rejected.
2. The ranked list: feature → mode → priority (one line each).
3. **Where it lives, both places:** GitHub commit + URL, and the vault pages written.
4. "`/template` will now find these as briefs. Nothing is extracted yet. Next step is a
   separate session in `$LIB` with the `feature-template-library` skill, starting with
   `<first feature in extraction order>`."

Done means: briefs written, committed and pushed (verified on `origin/main`), the
`templates/` folder and catalog in sync with GitHub (or the reason they are not), vault
updated. If any one of the three did not happen, say which, not "done".

Do not imply a template now exists. It does not.
