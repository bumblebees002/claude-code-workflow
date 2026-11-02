---
name: proposal
description: "Use when a job description needs a decision and a proposal — an Upwork/Contra/Fiverr post pasted in, a client brief, an RFP, or 'should I bid on this?'. Decides whether to bid at all, which category to bid into, what to charge, and drafts the proposal from evidence in the Obsidian vault. Never invents a claim. Also use to review a draft proposal for unsupported claims, or to log an outcome against a sent proposal. Triggers: 'should I bid', 'write a proposal', 'here's a job post', 'draft a cover letter', 'is this job worth it', '/proposal'."
trigger: /proposal
---

# /proposal

A proposal is a **claim about what you can do, made to a stranger who will check.** The
cost of one unsupported claim is not a lost bid — it is a bad contract you then have to
deliver, and a JSS hit that outlives it.

So this skill does the same thing your own agents do before they write to a database: it
**proposes, cites, and refuses to invent**. Every factual claim in a draft must trace to a
page in the vault. If the vault cannot support it, the skill says so instead of writing
it. That is [[deterministic-write-guard]] pointed at your reputation.

## The one hard rule

> **No claim without a citation.**

Every sentence asserting capability, experience or outcome carries a vault page behind it.
If a job needs something the knowledge base cannot support, the output says
**"cannot support: X"** and offers the nearest honest alternative. It never stretches.

Corollaries:
- Never state an outcome the vault records as unmeasured. "Not measured" is a real answer.
- Never claim a client relationship the vault does not name.
- Anything the vault marks *claimed, unverified* may be described as work done, never as a
  proven result.
- Never autopost. This skill drafts; the human sends.

## Vault paths

Source of truth is `$OBSIDIAN_VAULT`. Read in this order — stop as
soon as you have what the job needs:

| Purpose | Path |
|---|---|
| **Newest facts, demo links, internship, creativity story — read first** | `04-outputs/context/master-context.md` §0 |
| Positioning, honesty contract, evidence index | `03-wiki/maps/profile.md` |
| Wedges, categories, what never to lead with | `03-wiki/syntheses/upwork-wedge-selection.md` |
| Priced offers, scope, exclusions, proof assets | `03-wiki/maps/offers.md` |
| Capability tiers | `03-wiki/maps/capability-map.md` — **does not exist yet** (blocked on interview session 5). Until it does, use `04-outputs/context/master-context.md` §2/§3 instead |
| Portable summary: what he does / does NOT do | `04-outputs/context/master-context.md` |
| Per-project evidence | `03-wiki/entities/*.md` |
| Reusable techniques to cite | `03-wiki/concepts/*.md` |
| Market figures (dated — check decay) | `03-wiki/sources/upwork-market-2026.md` |

Never read the whole vault. Read `profile.md` first; it indexes the rest.

## Step 1 — Should you bid at all?

**A "don't bid" is a successful output.** Connects are $0.15 each and at a 2% reply rate a
contract costs ~$180 of them. Filtering is worth more than writing.

Score the post against `references/qualify.md`. Hard filters — any miss is a strong no:

- Payment verified? (only ~52% of AI postings are)
- Client lifetime spend **$1k–$5k**? That band replies at 8.15%. **$500k+ whales reply at
  3.85%** — chasing big spenders is the most expensive default on the platform.
- 2+ prior hires, 4.5+ rating
- **Fewer than 15 existing proposals**
- **Posted under 2 hours ago** — never bid past 24h
- Does it map to a wedge in `upwork-wedge-selection.md`, or is it a commodity category?

Red flags that override everything: "fully autonomous, no review step" (the client will
blame you for the model), unpaid test tasks, scope described only as an outcome with no
system named, or a budget below the offer floor in `offers.md`.

Output a verdict — **BID / SKIP / BID IF** — with the reason in one line.

## Step 2 — Which category, and which offer

Category selection moves the reply rate more than proposal quality does. Same work bid
into Information Security & Compliance replies at **11.21%**; bid into Web Development it
replies at **5.80%**.

Map the job to one offer in `offers.md`. If it maps to none, either propose the nearest
offer with an honest gap statement, or skip. Do not invent a new offer mid-bid.

## Step 3 — Bid position

**Never match the client's stated budget.** That is where 88% of bids land and it replies
at 8.8%. Two valid positions:

| Position | Reply rate | Use when |
|---|---|---|
| **Under 50% of stated budget**, tight scoped slice | **20.6%** | Default. Land small, escalate inside the relationship |
| **200–500% reframe**, materially larger scope | **16.4%** | The post underestimates its own problem and you can show why |

Hourly: the $35–49 modal band is the *worst*-performing (6.39%). Go clearly below or
clearly above it.

## Step 4 — Draft

Structure, in this order, **under 180 words**:

1. **Their problem, in their words.** Quote or mirror the phrasing from the post. Never
   open with "I am" or "I have".
2. **One specific detail** proving you read it — a constraint, a tool they named, a number.
3. **One proof point**, cited. Off-platform work counts fully. One, not three.
4. **A concrete first step** — what happens in the first 24–48 hours.
5. **One useful question** that shows domain understanding.

Banned: "leverage my expertise", "I'm passionate about", "I'm new to Upwork", "I have X
years of experience", em-dash-heavy AI cadence, any list of technologies as a wall.

Upwork enforces an AI-content policy with detection, and clients pattern-match generic AI
phrasing instantly. **Draft from evidence; the human edits before sending.**

If a Loom exists for the matched work, put the link in the proof point (table and
"which demo to link" rules in master-context §0). One link, the closest match. Never link a client's live product. Credit any open-source
project a build started from.

When the post asks about the person (about you, why you, how you think), one sentence of the
creativity story from master-context §0 plus one concrete case is allowed. Never more.

## Step 5 — Write out and log

Write to `04-outputs/proposals/YYYY-MM-DD-<client-or-slug>.md` containing: the verdict and
why · the matched offer · the category to bid into · bid position and number · the draft ·
**the citation list** · and any `cannot support:` lines.

Append one row to `04-outputs/proposals/ledger.md`:

```
| YYYY-MM-DD | slug | wedge | category bid into | offer | bid | position | verdict | sent | replied | won |
```

Eleven columns, in that order — match the header already in `ledger.md` exactly, and log
SKIP rows too. They are the cheapest data on the page.

The ledger is the point. It turns wedge selection from an argument into a measurement.
When a reply or outcome lands, come back and fill the row — that is a valid `/proposal`
invocation on its own.

## Reviewing someone else's draft

Given a draft, do one pass: flag every sentence making a factual claim, and for each,
either attach the vault page that supports it or mark it **unsupported**. Report the count.
Do not rewrite unless asked.

## When the vault is thin

If `profile.md` is still a seed, or the matched offer has an unfilled **proof asset**,
say so up front. The right move is often to fill the gap rather than send a weak bid —
point at [[00-system/interview-bank]] and name the session that would unblock it.

## References

- `references/qualify.md` — the full client/job scoring checklist
- `references/draft-patterns.md` — worked openers per wedge, and the banned-phrase list
- `references/market-figures.md` — the dated numbers this skill cites, and when they expire
