# Worked example: ai-freelancer, round 1 (2026-09-28)

The round the user loved: "I am very surprised after watching all the UI designs."

**Project:** an AI-agent freelance marketplace (Next.js monorepo). Every seller is an AI
agent; buyers pay only if the result passes its checks. The app before this round was stock
shadcn, greyscale, light-only, with no charts and no motion.

## What the user asked, and how it was read
- "Only the new features to explore" plus "new skin also". **Every sample = a new feature + a new skin.**
- "Setting of the sixth, colour like the fifth": the **mix-and-match** requirement, which led to shared token names.
- "Classify: this is from Apple Design, this from UI Pro Max…": the **source badge** on every sample, plus gallery filters.
- "A different sample for graphs": the **chart gallery**.
- "At the bottom, very simple English": the **"How it would work"** line. Round 2 onward expands it into steps plus "Ideas not built yet".
- Feedback afterwards: "I especially like Apple. You made 2 Apple designs; increase to 4."

## Questions asked (one AskUserQuestion)
1. Feature groups (multiSelect): Hiring reimagined / Watching the work / Trust & reputation / Builder business. The user picked all four and added "bring something else to the table".
2. Chart gallery: a separate page.
3. Mood: mostly dark, with one or two light.

## Exploration outputs used
- 23 candidate features from the feature inventory, todo.md and the architecture milestones.
- The real seed data:
  - users: Alice Buyer, AF Labs, Sam Both, Bob Builder, Carol Admin
  - 6 agents with their tiers and prices
  - example companies and products
  - the order and run state machines
  - fee 15%, auto-accept 72 h, reserve 7 days
- The current UI: shadcn neutral, no fonts, no dark mode, no charts.

## The assignment grid that shipped (13 files)

| # | File | Feature | Leads with | Source | Layout | Palette bg / accent / accent-2 | Primary chart | Fonts | Review |
|---|---|---|---|---|---|---|---|---|---|
| 01 | 01-contest-race | Contest mode | 3 agents racing on one brief | UIPM #51 HUD (restrained) | 3 lanes + judge dock | #07090c / #5eead4 / #fbbf24 | arc gauges + race bars | 47 Exo / Roboto Mono | 8 |
| 02 | 02-team-pipeline | Hire a team | a chain of agents, one price | Apple · visionOS Spatial | node canvas + glass inspector + ornament | #0b0d12 / #0a84ff / #bf5af2 | budget flow + step rings | SF + Inter (55) | 8 |
| 03 | 03-brief-builder | AI brief builder | a spec writing itself | Anthropic frontend-design | chat + living document | warm light #f5f1ea / #c2410c / #4d7c0f | radial bar set + confidence ring | 35 Libre Bodoni / Public Sans | 8 |
| 04 | 04-run-trace | Live run trace | a waterfall of steps | In-house Dark-Glass | rail + waterfall + drawer | #030303 / #818cf8 / #22d3ee | gantt + cost donut | 42 Fira Sans / Code | 8.5 |
| 05 | 05-agent-asks | Agent asks mid-run | the one question + countdown | Apple · Liquid Glass | glass sheet over blurred page | #05060a / #64d2ff / #ff375f | countdown ring + progress arc | SF + Inter (63) | 7.5 |
| 06 | 06-leaderboard | Leaderboard + levels | giant rank numerals | UIPM #47 Exaggerated Minimalism | top nav + poster list | #000 / #c6f432 / #fff | slope + level ring + pass^k dots | 49 Barlow Condensed | 8 |
| 07 | 07-ai-judge-dispute | AI-judge dispute | the verdict | Impeccable | two cases + verdict spine | #14110f / #c9a45c / #8fb4d9 | radar + confidence gauge | 29 EB Garamond / Lato | 8 |
| 08 | 08-builder-funnel | Builder funnel | the biggest leak | UIPM #33 Comparative | icon rail + bento | #0e1116 / #7c5cff / #22d3ee | funnel + refund donut + A/B bars | 3 Space Grotesk / DM Sans | 7 |
| 09 | 09-payouts-flow | Payouts timeline | money moving through stations | UIPM #36 Financial | top nav + money-flow hero | warm light #f6f3ee / #0f766e / #9a3412 | stacked area + reserve rings + calendar heatmap | 31 IBM Plex | 8 |
| 10 | 10-demand-insights | Demand insights | what buyers asked that you can't do | UIPM #43 AI-Native | bubble map + feed rail | #0b0a14 / #8b5cf6 / #2dd4bf | packed bubbles + day×hour heatmap | 18 Syne / Manrope | 7 |
| 11 | 11-marketplace-pulse | (proposed) admin pulse | the one incident | UIPM #31 Real-Time Monitoring | full-bleed wall + ticker | #050807 / #2dd4bf / #a78bfa | health heatmap + live line + GMV arc | 16 Lexend / Source Sans 3 | 8 |
| 12 | 12-recurring-jobs | (proposed) recurring hires | the next run | UIPM #65 Gradient Mesh | week spine + 24 h clock | #0a0b1a / #ff7a59 / #7a5cff | radial clock + bullet bars | 11 Outfit / Work Sans | 7.5 |
| 13 | 13-chart-gallery | Chart gallery | 14 charts, each tagged with where it lives | dataviz + UIPM charts | varied-span card grid | #0c0d10 / #7c9cff / #5eead4 | all 14 | 44 Archivo / Space Grotesk | 7.5 |

That round had only 2 Apple samples. **From round 2 on, use 4 Apple samples** (A1–A5 in
`design-sources.md`). For example, in this project 06 → Apple · Keynote Bento, 11 → Apple ·
macOS Sidebar (HIG), and 12 → Apple · Widgets & Live Activities.

## How it ran
1. Two Explore agents in parallel, then one AskUserQuestion, then a plan with the grid.
2. The shared contract was written to the scratchpad, and 13 builder agents ran in parallel
   (two launch messages).
3. The gallery `index.html` was built while they ran. Gallery cards were corrected when
   receipts showed different shipped hexes (04 shipped #030303 / #818cf8).
4. Receipts checked: the colors.csv rows and the typography rows existed and matched; the
   dataviz `validate_palette.js` existed at the claimed path.
5. The gate ran clean on all 13 files.
6. Four reviewer-fixer agents (01–05, 06–10, 11–12, 13) fixed about 60 real defects, now
   recorded in `reference/lessons.md`. Scores were 7–8.5.
7. Final checks: 13/13 links resolve, one theme key per file, every script parses, and git
   shows only `design-samples/` as new.
8. Hand-off: a table with scores, mix-and-match instructions, honest open issues, and a
   request for keep/kill picks.

## Example "How it would work" lines (round-1 style, one line each; round 2+ uses 3–5 steps)
- **Contest:** "You post one brief and up to three agents work on it at the same time. You
  compare the results and pay only the one you pick; the others cost you nothing."
- **Agent asks:** "Sometimes an agent needs a quick decision to do the job right. It pauses
  and asks you here; you answer in one tap, and it carries on. If you don't answer in time,
  it uses its default."
- **Payouts:** "When a buyer accepts your agent's work, the money waits 7 days in case of
  problems, then becomes available. You can send it to your bank whenever you want, and
  download a statement every month."
