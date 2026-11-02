# Draft patterns

Under 180 words. Their problem first, one proof point, one first step, one question.

## The shape

```
<Their problem, mirrored in their words — 1–2 sentences>

<One specific detail from the post proving you read it>

<ONE proof point, cited to a vault page>

<What happens in the first 24–48 hours — concrete>

<One question that shows domain understanding>
```

## Worked openers per wedge

**Wedge 1 — rescue / audit.** The client is scared and does not want a lecture.

> Your app works for the people who signed up first and breaks for the ones who came
> later — that pattern is almost always tenant scoping, not load.
>
> You mentioned it's on Supabase with organisations. I've audited exactly that shape: a
> 49-table schema where 30 tables carried the org key and 19 reached it by join. One
> unscoped in-memory map produced one critical and four serious findings — caught before
> anything leaked.
>
> First 48 hours: I enumerate every table and route, mark which ones can be reached
> across orgs, and ship one fix so you can see it working. Report either way.
>
> One question — when a user hits another org's record today, do they get a 403 or a 404?

**Wedge 2 — conversational agent.** The client wants to see it, not read about it.

> You want customers to book by texting instead of using the portal — and you're worried
> the bot will confirm something that never happened.
>
> That's the right worry. I build these so the agent *proposes* and the write only happens
> on confirmation; the model never touches the database directly. Two production systems
> run this way, one for bookkeeping and one for a retail shop across WhatsApp, Telegram
> and web.
>
> First 48 hours: one channel live against a test calendar, so you can text it yourself.
>
> One question — when it can't handle something, who should it hand off to?

**Wedge 3 — Claude Code / AI workflow.** The client's team is producing inconsistent output.

> "Works on the first try, breaks on the third" is usually not the model — it's that
> nothing fails loudly when the AI is wrong.
>
> You mentioned your tests pass but bugs still ship. I run a four-command gate before
> every commit, separately from the build, because bundlers strip types without checking
> them — that exact gap shipped a real type error past a green build and 3,500 passing
> tests on one of my projects.
>
> First 48 hours: a repo-specific CLAUDE.md and a pre-commit gate wired up, so bad output
> stops at the commit instead of at your users.
>
> One question — what's the last thing AI broke that you only found in production?

## Banned

Phrases that mark a proposal as generic or AI-written:

- "I am", "I have X years of experience", "Allow me to introduce myself"
- "leverage", "utilize", "robust", "cutting-edge", "seamless", "end-to-end solution"
- "I'm passionate about", "I would love the opportunity"
- "I'm new to Upwork but"
- "As an experienced <title>"
- A wall of technology names with no sentence around them
- Three proof points where one would do
- Any sentence that would read identically for a different job post

Structural tells to avoid: heavy em-dash cadence, tricolon lists ("faster, cleaner, and
more reliable"), a closing paragraph that restates the opening.

## Proof-point selection

Pick **one**, matched to their fear, not to your favourite project:

| Their fear | Cite |
|---|---|
| "Our data will leak between customers" | the isolation audit — one critical, four serious findings |
| "The AI will do something stupid" | propose-and-approve; the model never writes directly |
| "It'll pass tests and still be broken" | typecheck separate from build; the type error that shipped through green |
| "Our last developer disappeared" | documented dead-ends and handover notes per repo |
| "Our AI bill is out of control" | the gateway over ~100 providers with cost tracking; the 2–3× faster and 8–15× cheaper bake-off |
| "It'll be slow" | measured, not guessed: 0.011ms → 311ms → 0.053ms cached |

## Citation block

Every draft is written out with its citations attached, so a claim can be traced later:

```
CITATIONS
- "one critical and four serious findings" → 03-wiki/concepts/ephemeral-state-is-not-authorization.md
- "two production systems" → 03-wiki/entities/ai-accountant.md, 03-wiki/entities/groceries.md

CANNOT SUPPORT
- <claim the job invited that the vault can't back, and the honest alternative offered>
```
