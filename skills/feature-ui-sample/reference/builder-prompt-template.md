# Builder prompt template (one per sample)

Launch with `Agent`, `subagent_type: "claude"`, `run_in_background: true`. Send all builders
in one message, or two if there are more than ~8. Fill every `{{…}}`.

````
You are building ONE HTML design sample. Do the work yourself; do not launch subagents.

FIRST read, in full: {{SCRATCHPAD}}/shared-contract.md. Follow it exactly: the build contract,
the shared token names, the 8 ingredients, the anti-slop rules, the bottom section (Design DNA,
How it would work, Ideas not built yet) and the receipt format. Then read
~/.claude/skills/ui/reference/sample-recipe.md, your design source (paths in
~/.claude/skills/feature-ui-sample/reference/design-sources.md), and
~/.claude/skills/feature-ui-sample/reference/lessons.md.

## Your assignment: {{NN}}
- File: {{SAMPLES_DIR}}/{{NN}}-{{slug}}.html
- Feature (NEW): **{{feature name}}.** {{one sentence: what it lets the user do}}
- Design source label: **{{exact label}}**. {{what to read, and 4–8 concrete things to take
  from it: materials, radius, shapes, motion; plus what NOT to do, e.g. "restrained: no neon"}}
- Layout frame: **{{layout frame}}.** {{how it reflows on mobile}}
- Palette ({{dark|WARM LIGHT default}}): bg {{hex}}, surface {{hex}}, surface-2 {{hex}},
  line {{rgba}}, ink {{hex}}, muted {{hex}}, accent {{hex}}, accent-2 {{hex}}, good {{hex}},
  warn {{hex}}, bad {{hex}}. {{how the other theme derives, incl. an accent readable on it}}
- Fonts: typography.csv row {{N}}, {{Display}} / {{Body}}. Link: {{exact Google Fonts URL}}
- Primary chart: **{{form}}**, plus **{{second form}}**.

## Concept brief
{{A PARAGRAPH-LEVEL SPEC, never a category. It must include:
  - what the screen LEADS WITH (the hero), and the primary button with its exact label
  - the named entities from the shared data, with the exact figures, and CHECK THEY ADD UP
  - 3–4 stat tiles, each with its delta, sparkline or target
  - a "Proposed block to include:" that the user didn't ask for
  - what is "Demoted:"
  - "Motion:" entry, one live loop, and the cursor interaction
  - relevant pre-emptive lines from lessons.md
  - "How it would work": 3–5 plain steps
  - "Seed ideas for 'Ideas not built yet'": 4–6 (features + animation). Add your own too.}}

Reply with only the receipt from the shared contract.
````

---

## Worked example: the brief the user loved (ai-freelancer #01)

````
## Your assignment: 01
- File: /…/design-samples/01-contest-race.html
- Feature (NEW): **Contest mode.** One brief, several agents working on it at the same time;
  the buyer picks the winner and pays only that agent.
- Design source label: **UI UX Pro Max · #51 HUD / Sci-Fi FUI**. Use it RESTRAINED: thin line
  work, corner brackets on panels, mono readouts, precise tick marks. No neon overload,
  scanlines, glitch or fake sci-fi jargon. Read row No=51 of styles.csv.
- Layout frame: **three equal live lanes across the full width + a sticky bottom "judge dock".**
  No sidebar.
- Palette (dark): bg #07090c, surface #0d1117, surface-2 #131922, line rgba(94,234,212,.14),
  ink #e6edf3, muted #8b98a5, accent #5eead4, accent-2 #fbbf24, good #34d399, warn #f59e0b,
  bad #f87171. Derive a light theme (cool pale grey ground, accent darkened to stay readable).
- Fonts: typography.csv row 47, Exo / Roboto Mono.
  Link: https://fonts.googleapis.com/css2?family=Exo:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap
- Primary chart: **an arc gauge per lane** (checks passed), plus **race bars** (time to finish
  against the 8-minute deadline).

## Concept brief
The screen leads with the race itself. Alice Buyer posted a contest brief: "Company research
brief on Northwind Robotics, Standard (10 sources)", max price $29.00 held in escrow.

Three lanes, shown at a snapshot 1m 52s in:
- Lane 1, Company Research Brief (AF Labs, $29, success 91%, ★ 4.6): succeeded, 4/4 checks,
  finished in 1m 52s (its median is 2m 10s), 10 sources.
- Lane 2, "Scout Brief" by Sam Both ("New" badge, bid $24): validating, 3/4, llm_rubric
  still scoring.
- Lane 3, "Lens Research" by Bob Builder ("New", bid $27): running (auto-retry), because
  `regex $.sources[0].url` failed on the first attempt.

Each lane shows the run-state chip, an elapsed timer against the deadline, the arc gauge, a
sources-found counter, a live step line, and a short output snippet labelled
"AI-generated output".

Stat tiles:
- Escrow held $29.00
- Entries 3
- Fastest 1m 52s (−14% vs median)
- Checks passing 9/12, with a small progress bar

Hero: the lanes plus the judge dock. The dock reads "Pick the winner", with a side-by-side
compare toggle and the rule: "You pay only the winner. The other entries are not charged."
The primary button is "Choose Company Research Brief · $29.00".

Proposed block to include: a "Where they disagree" diff lens that highlights conflicting
facts across the outputs (founded 2016 vs 2017, HQ Pittsburgh vs Boston).

Demoted: agent profile details and reviews, one line each.

Motion: the lanes stagger in, lane 3's progress fill loops, and the elapsed timer ticks. The
cursor interaction is a spotlight across the lanes.

How it would work:
1. You post one brief.
2. Up to three agents work on it at once.
3. You compare the results side by side.
4. You pay only the one you pick.

Seed ideas for "Ideas not built yet":
- Let buyers set a "first to pass wins" rule.
- Show a replay of the race.
- When a lane finishes, it slides up with a soft glow.
- A tie-break vote from a second AI judge.
- The diff lens could animate the conflicting words like a highlighter.
````
