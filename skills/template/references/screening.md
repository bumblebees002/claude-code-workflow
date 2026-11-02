# Screening an external candidate

Read this in Route C, after the private catalog missed and before presenting options.

## Before searching at all, write the checklist

Do not open a browser until these five are written down. Without them "which is better?"
has no answer, and every candidate looks fine.

1. **Required user-visible behavior.** What must actually happen, in the user's words.
2. **Target stack and deployment constraints.** Language, runtime version, persistence,
   hosting, whether a background worker exists.
3. **Security boundaries.** Data sensitivity, auth, payments, tenant isolation, PII.
4. **Required tests and clean-install proof.** What would convince you it works here.
5. **Acceptable licenses.** Decided before you see a candidate you like.

## Search order

1. `$OBSIDIAN_VAULT/Research/Tools & Repos Radar.md` — already vetted, already
   written up, and the entries carry a "How I can use it" section stating the intended fit.
2. `$OBSIDIAN_VAULT/03-wiki/entities/` — tools and libraries already in the wiki.
3. Only then `mcp__exa__web_search_exa` / `mcp__tavily__tavily_search`.

A radar hit is worth more than a fresh search result: it has already been judged once,
and the judgment is recorded.

## Rubric

Score each candidate. Do not average into a single number — the disqualifiers are
disqualifiers regardless of how good the rest looks.

| Dimension | Look for | Disqualifying |
|---|---|---|
| **License** | MIT, Apache-2.0, BSD, ISC | GPL/AGPL without explicit acceptance; **no license file at all** |
| **Maintenance** | commits within ~6 months, issues answered, releases tagged | archived, last commit years old, maintainer explicitly stepping away |
| **Tests** | a real suite, CI that runs it, tests that assert behavior | no tests, or tests that only assert the code imports |
| **Boundary** | the feature is separable; few imports reaching into app internals | feature is 70% product wiring — see below |
| **Stack fit** | matches the target's language/runtime, or converts cleanly | needs a runtime the target cannot host |
| **Size** | small enough to read fully before adopting | you cannot read it, so you cannot vouch for it |
| **Security** | input validation, no obvious injection or SSRF surface | handles secrets or network egress carelessly |

**No license means no permission.** A public repository without a license grants nothing.
This is the one dimension with no judgment call in it.

## The file-count trap

"Three files, no internal coupling" is not an extractability measure and has been wrong
before. In one measured case it held for one file and failed for the other two — one of
them reached into sixteen modules of its host and was roughly 70% product wiring.

Judge the boundary by reading the imports, not by counting files.

## Contract density beats popularity

Rank on tests per unit of source, boundary tightness, and generality — not on stars.
A 947-line project with 70 tests covering a complete defense is a better adoption target
than a 20k-star framework you would use 5% of.

Never rank a candidate up or down for the language it is written in. Conversion happens
at adoption and the source language costs nothing.

## Presenting

Give 3–5 candidates in a table with: name, license, last commit, test count, size, and a
one-line "what you would actually take from it". Then a recommendation with the reason,
and the honest downside of that recommendation.

Then stop. Adoption needs approval.

## After approval

Adapt per [adapting.md](adapting.md), then harvest per
[harvest-brief.md](harvest-brief.md). Record the find in the vault either way — even a
rejected candidate is worth an entity page, because the next search should not
re-evaluate it from scratch.
