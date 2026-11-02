# Qualifying a job post

A "don't bid" is a successful output. Connects cost $0.15; at a 2% reply rate a single
contract costs roughly $180 of them. Filtering beats writing.

## Hard filters — any miss is a strong no

| Signal | Threshold | Why |
|---|---|---|
| Payment verified | required | Only ~52% of AI postings are |
| Client lifetime spend | **$1k–$5k** | Replies at 8.15%, the best band |
| Prior hires | 2+ | Knows how to run a contract |
| Client rating | 4.5+ | Below this, JSS risk is theirs and becomes yours |
| Existing proposals | **< 15** | Above 20 the read-rate collapses |
| Age of post | **< 2 hours** | Never past 24h; by hour 36 there are 50+ applicants |
| Maps to a wedge | required | See `upwork-wedge-selection.md` |

**Counter-intuitive:** clients with **$500k+ lifetime spend reply at 3.85%** — worse than
half the small-client rate. Filtering *for* big spenders is the most expensive default on
the platform. Prefer the $1k–$5k band.

## Timing windows

| Minutes after posting | Reply rate |
|---|---|
| 4–5 | **8.99%** |
| 5–10 | 6.91% (the trough) |
| 12–15 | **8.07%** (real second wave) |
| > 24h | don't |

## Red flags — override everything above

- **"Fully autonomous, no human review"** — the client will blame you for the model's
  behaviour. Experienced bidders treat this as a hard no.
- Unpaid test tasks or "build a quick demo first"
- Scope stated only as an outcome, with no system named
- Budget below the floor of the matched offer in `offers.md`
- Client asking to move off-platform before a contract exists
- A post that reads as a rewritten version of another post (template farming)
- "Simple", "quick", or "should take a few hours" attached to anything touching auth,
  payments, tenancy or migrations

## Green flags — worth bidding even if one hard filter misses

- They name the specific tool that broke (Lovable, Bolt, Cursor, Replit, Supabase)
- They describe a *symptom* rather than requesting a *technology* — symptoms mean they
  need judgment, which is the expensive kind of work
- They mention a previous developer who left or disappeared
- Security, compliance, isolation, or "before we launch" language
- They have posted and hired for this same problem before and it's still not solved

## Category routing

The single highest-leverage decision. Same work, different category, roughly double the
reply rate at identical Connects cost.

| If the job is really… | Bid it into | Not |
|---|---|---|
| Fixing/hardening an inherited or AI-generated app | **Information Security & Compliance** (11.21%) | Web Development (5.80%) |
| Lead pipeline with LLM enrichment | **Lead Generation** (14.38%) | AI & Machine Learning (7.21%) |
| Multi-channel bot | AI Chatbot / Conversational | Generic "AI agent" |
| Claude Code / team AI workflow | AI Consulting / Process | Web Development |

Never bid into AI & Machine Learning or Web Development by default. They are the two
worst-performing categories on the platform.

## Output format

```
VERDICT: BID | SKIP | BID IF <condition>
WHY: <one line>
CATEGORY: <where to bid it>
OFFER: <which offer in offers.md, or "no match">
FLAGS: <any red/green flags worth naming>
```

*Figures dated 2026-08-15 from `03-wiki/sources/upwork-market-2026.md`. Re-verify after
roughly six months.*
