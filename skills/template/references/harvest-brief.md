# Harvesting a feature back into the library

Read this after a Route C adoption succeeds, or whenever something generic proves itself
in a project and should stop being project-specific.

## The rule

**Write a brief. Do not extract from the consumer project.**

A real extraction produces a template directory, four manifests, a contract document, a
test suite, content-integrity hashes, a catalog entry, and a release record — and every
one of those is validated against the library's own tooling. Producing them from a
consumer project means producing them without that tooling, which means producing them
wrong.

So: this skill writes a brief into the library, and the extraction happens there, in a
session that has the maintainer skill and the five checks available.

## Where the brief goes

```
$LIB/.planning/harvest-<slug>.md
```

Writing into `.planning/` — and committing/pushing exactly those files — is the *only*
write this skill makes to the library. Never create `templates/<id>/`, never edit
`catalog/`, never touch a manifest, never edit `CLAUDE.md` from a consumer project.

Every brief starts with front-matter so `/template` Phase 1b can find it by grep:

```yaml
---
status: briefed
feature: <slug>
source_repo: <git remote url>
source_commit: <exact sha>
extraction_mode: service | package | generator | reference | reject
priority: high | medium | low
keywords: [<plain-language synonyms for the behavior>]
---
```

Publish it to GitHub too (see `/templify` Phase 5 for the safe procedure: path-limited
commit, private-repo check, no force-push). A brief that exists only on this Mac is not
harvested.

Every vertical in this library starts with a pre-execution critique written *before*
implementation. The brief is the raw material for that critique — it is not the critique
itself, and it does not authorize an extraction.

## What the brief must contain

1. **Behavior checklist.** What the feature does, in user-visible terms. One line per
   behavior. This becomes the contract, so vagueness here is expensive later.

2. **Where it came from.** Repository URL, the exact commit adopted, the license and where
   the license file lives, and the specific paths taken. Provenance is not optional; every
   template records it and it is hash-verified.

3. **Proposed boundary.** What is genuinely reusable versus what was product wiring.
   Be specific about the second part — it is the thing most likely to be wrong, and
   "3 files, no coupling" has been wrong before.

4. **Ports.** Which dependencies must become injected structural ports for the feature to
   work in a different product: persistence, clock, delivery, auth, HTTP.

5. **Test scenarios.** Every behavior worth asserting, language-independent. This is the
   most valuable section by a wide margin — the implementation is the cheapest layer.
   Include scenarios the original lacked; a gap you found while adapting is exactly the
   kind of defect the library exists to stop propagating.

6. **Defects found while adapting.** Anything wrong in the source that you worked around.
   These *must* be fixed during extraction rather than trimmed in — trimming a known
   defect means every future product inherits it, which is the precise failure this
   library was built to prevent.

7. **Composition.** Which existing templates should supply shared concerns instead of the
   feature carrying its own copy. Check the catalog before claiming there is nothing.

8. **What it would depend on**, and whether any of those are unreleased. An unreleased
   family must never become a required dependency.

9. **Proposed extraction mode.** `service`, `package`, `generator`, `reference`, or
   `reject` — and "reject" is a real, respectable outcome. A feature too entangled to
   extract cleanly is better recorded as a rejection with reasons than forced into a
   template nobody can adopt.

## What the brief must not claim

- Do not assign a version. Versions are assigned at release.
- Do not assign a lifecycle status. `discovered → mapped → extracted → verified → ready`
  is gated by the library's own checks, and `ready` additionally needs a production
  adapter proven in a clean fixture.
- Do not assert the feature is proven because it works in one project. One consumer is
  evidence, not a contract.

## Also record it in the vault

A harvest is a durable change. Per the vault schema:

- entity page under `03-wiki/entities/` for the source project, if new
- an entry in `Research/Tools & Repos Radar.md`
- the adoption row in `04-outputs/tables/template-adoptions.md`
- append to `log.md`, update `index.md`

## Then hand off, explicitly

Tell the user, in plain words: the feature is working in their project, the brief is
written at `<path>`, and the extraction itself is a separate session's work in the
library repo. Do not imply the template now exists. It does not.
