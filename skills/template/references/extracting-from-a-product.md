# Extracting one feature out of a whole product

Read this when the thing you need is **not** a standalone repository — it lives inside a
larger product, yours or someone else's. That is the normal case, not the exception:
virtual-office's CSV export lives inside its attendance feature, and ai_accountant's
Stripe handling lives inside its webhook routes. Neither is a "CSV library" or a
"payments library". Features are rarely isolated.

## Never clone to evaluate

Cloning is the expensive step, so it happens **after** a decision, never before.

1. Screen 3–5 candidates from the web and the GitHub API only: license, activity, test
   presence, stars, and roughly where the feature lives. See [screening.md](screening.md).
2. Present them. **Stop for approval.**
3. Shallow-clone only the one chosen:
   ```bash
   git clone --depth 1 <url> "$SCRATCH/<name>"
   git -C "$SCRATCH/<name>" rev-parse HEAD    # record this immediately
   ```

Record the commit *before* doing anything else. A throwaway clone whose commit was never
written down is unreproducible, and the provenance record depends on it.

## Survey the whole product before you delete it

**This is the step that pays for the clone.** You have the entire product on disk exactly
once. Before deleting it, write down what *else* is in there.

The feature you came for is one of many. Six months from now the question will be "didn't
we see something that did X?" — and the answer should be a note, not another clone.

Produce a survey covering:

- What the product is, and its license.
- The feature you took.
- **Other features worth remembering**, one line each, with the path they live in.
- Anything notably good — a pattern, a test approach, a boundary worth copying later.
- Anything notably bad — so a future search does not re-evaluate it hopefully.

Write it to `$OBSIDIAN_VAULT/03-wiki/entities/<product>.md` as an entity page, and
add a line to `Research/Tools & Repos Radar.md`. Then delete the clone.

The survey outlives the clone. That is the whole point.

## Locate the feature

Find the real boundary, not the file with the matching name:

- Start from tests. A well-named test names the behaviour and shows the entry points.
- Follow imports **outward** from the core file. Where they stop being about the feature
  and start being about the host product, you have found the edge.
- Note every import that reaches into product internals — config, DI container, logger,
  auth, database session. Each one becomes a port or a decision.

Judge the boundary by reading imports, never by counting files. "3 files, no coupling"
has been wrong before: one of those files reached into sixteen modules of its host and
was roughly 70% product wiring.

## The feature will not be what you asked for

It never is. Sort what you found into four buckets and **bring them back as questions**:

| Bucket | Meaning | Question to ask |
|---|---|---|
| **Core** | the behaviour you actually wanted | — |
| **Bundled extras** | things that came attached, unasked | keep, trim, or defer? |
| **Host wiring** | dependencies on *their* product | replace with what, in ours? |
| **Gaps** | what you needed and it does not do | build now, or accept? |

Do not silently trim, and do not silently keep. Both decisions are the user's, because
both change what the feature costs to own.

State each extra concretely: what it does, what it drags in, and what keeping it would
cost *in this project*. "It also ships a Redis-backed store and a Prometheus exporter;
you run Postgres and have no metrics, so keeping the store means writing a Postgres
adapter and keeping the exporter means adding a dependency you have no use for."

Then recommend. A list of options with no recommendation is not help.

## When the language is different

It usually is. **Do not port code across languages.**

The library's standing rule is *trim, do not rebuild* — and this is exactly where that
rule stops applying. Trimming works when you own the source and the language matches. A
foreign-language find has nothing to lift: a mechanically translated file drags in idioms
that do not belong and produces code a reviewer can spot instantly.

So:

1. Read the source for **concepts**, not syntax. What algorithm, what guarantees, what
   happens at the edges — concurrency, clock, failure, retry, ordering.
2. Write the **test scenarios first, in the target language**. These carry across
   unchanged; they are language-independent and they are the part worth having.
3. Implement idiomatically in the target until they pass. Use the target's conventions,
   not a transliteration of theirs.
4. Cite the original repository, commit, and paths in the provenance record. You rebuilt
   the behaviour, but the idea has an origin and it gets credited.

This is slower per feature than copying, and it is the only method that produces code
which belongs in the project.

## Then

- Adapt into the project per [adapting.md](adapting.md).
- Write the harvest brief per [harvest-brief.md](harvest-brief.md), including the
  survey and the trim decisions — the extras you rejected are part of the record.
- Log the adoption in `04-outputs/tables/template-adoptions.md`.
- Delete the clone. Confirm the survey is written first.
