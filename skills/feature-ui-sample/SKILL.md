---
name: feature-ui-sample
description: "Explore a project end to end, then generate a gallery of ~13 self-contained HTML samples where EVERY sample is a NEW feature the app doesn't have yet AND a NEW visual skin, each labelled with the installed design system it came from (Apple · Liquid Glass / visionOS / macOS HIG / Keynote Bento / Widgets, UI UX Pro Max #N, Anthropic frontend-design, Impeccable, in-house Dark-Glass, dataviz). Four Apple samples per round, one chart gallery, shared token names so any layout can take any palette, and a plain-English 'How it would work' + 'Ideas not built yet' section at the bottom of every sample. One builder subagent per sample, a grep gate, adversarial reviewer agents, then a filterable index.html. Never touches the real app. Triggers: '/feature-ui-sample', 'feature ui sample', 'make feature samples', 'show me new feature ideas as UI', 'explore new features with designs', 'design samples of new features'."
trigger: /feature-ui-sample
---

# /feature-ui-sample

Make the user go "wow" in a new project: explore the codebase, invent the features it
doesn't have yet, and show each one as a finished, futuristic HTML screen in a different
design language, all in one gallery.

This is the exact process from the ai-freelancer round of 2026-09-28, which the user loved.
**Follow it step by step, and don't simplify it.** The worked example in
`examples/ai-freelancer-round1.md` is the quality bar.

## What the user loved (keep all of it)

1. **Feature + skin in one.** Every sample is a NEW feature (something the product doesn't
   do yet) drawn in a NEW design language. It is never a re-skin of an existing screen.
2. **Classified by design source.** Every sample carries a badge naming the installed design
   system it came from, and the gallery can be filtered by those sources.
3. **Apple gets more room.** Build **4 Apple samples per round**, each a *different* Apple
   variant (see `reference/design-sources.md`).
4. **Mix and match.** Every sample uses the same token names, so "the layout of #06 with the
   colours of #05" means pasting one `:root` block.
5. **Charts everywhere, plus a separate chart gallery.** It shows ~14 chart types, each
   tagged with the page it would live on.
6. **Plain English at the bottom.** Every sample ends with "How it would work" and
   **"Ideas not built yet"**: more features, plus animation and interaction ideas that were
   in mind but not built. The ideas are short, simple and easy to understand. See the footer
   spec in `reference/shared-contract-template.md`.
7. **Futuristic, minimal, professional, never AI slop.** Mostly dark, with 1–2 warm light
   samples.
8. **Always excluded:** neumorphism, skeuomorphism and claymorphism. The permanent global
   bans in `~/.claude/skills/ui/reference/banned-styles.md` also apply.

## Files in this skill

| File | What it is |
|---|---|
| `reference/design-sources.md` | Every design source: label, path to read, what to take from it, the 5 Apple variants, and the round mix |
| `reference/shared-contract-template.md` | The contract every builder reads. Fill the `{{…}}` slots and save it to the scratchpad |
| `reference/builder-prompt-template.md` | The per-sample prompt skeleton, with one full worked brief |
| `reference/reviewer-prompt-template.md` | The adversarial reviewer-and-fixer prompt |
| `reference/lessons.md` | Defects the reviewers caught last time. Paste the relevant ones into builder briefs so they don't happen again |
| `reference/gate.sh` | The automated ingredient gate. Run it with the samples folder as its argument |
| `examples/ai-freelancer-round1.md` | The full assignment grid and briefs from the round the user loved |
| `examples/gallery-index.html` | The finished gallery page. Copy it and swap in the new cards |

It also depends on the `/ui` skill's references (read them, don't copy them):
- `~/.claude/skills/ui/reference/sample-recipe.md`: donut, sparkline, tilt/spotlight, stagger and theme-toggle code
- `~/.claude/skills/ui/reference/banned-styles.md`
- `~/.claude/skills/ui/reference/dark-glass-system.md` and `components/tokens.css`

---

## Step 0: Rules that never change

- **Never modify the real app.** Everything goes in `design-samples/` at the repo root. If
  that folder already holds an earlier round, use `design-samples/round-N/`.
- **Don't open a browser to verify** unless the user asks. Many of the user's projects
  forbid it. Verification is by grep, script parse and reading the code.
- **Don't commit** unless the user asks. If they do, follow the project's pre-commit rules.
- Read the project's `CLAUDE.md`, and any Obsidian vault page a hook points to, before
  exploring.

## Step 1: Explore the whole project (plan mode is fine)

Launch **two `Explore` agents in parallel** (thoroughness "medium"):

**Agent A: features and roadmap.** Report:
1. Every screen or feature that exists today, one line each, grouped by user role.
2. **15–25 candidate NEW features**, pulled from roadmap and todo files, architecture docs,
   research docs and "later/V1" lists. For each: one line on what it is, plus file and section.
   Prioritise the ones that make visual screens: live views, comparisons, analytics,
   money flow, reputation, workflows, AI-assisted flows, admin monitoring.
3. **Real data to reuse word for word:** seeded users, entity names, prices and tiers,
   state-machine state names, enums, fee constants, example inputs, review text.

**Agent B: the current look.** Report:
1. Design tokens: colours, radius, fonts actually loaded, dark mode (yes or no).
2. The app shell: header, nav labels per role, footer.
3. The structure of the flagship screens, with exact labels quoted.
4. Existing charts, animation and icon library.
5. Any existing `design-samples/` folder, `rejected.md`, or UI conventions section.

At the same time, read `design-samples/rejected.md` if it exists, and `banned-styles.md`.

For a greenfield project with no code, derive the features and data from the user's
request and the docs, and say so.

## Step 2: Ask once (one `AskUserQuestion`)

Ask at most 4 questions and skip any the request already answers:
1. **Feature groups** (multiSelect). Offer 4 groups of 2–3 candidate features each, named
   for the product, e.g. "Buying, reimagined", "Watching the work", "Trust & reputation",
   "Business / money". In each description, list the actual features in one line.
2. **Chart gallery:** a separate page (recommended), or charts inside the features only.
3. **Mood:** mostly dark with 1–2 warm light (recommended), half and half, or mostly light.
4. Only if unclear: anything the user specifically wants to see or avoid.

Always add **2 proposed extras** of your own on top of the groups the user picks. The user
explicitly likes it when you "bring something else to the table".

## Step 3: Write the assignment grid

The default round is **~12 feature samples + 1 chart gallery = 13 files**.

| Rule | Detail |
|---|---|
| Source mix | **4 Apple** (4 *different* variants) · ~5 UI UX Pro Max (different rows) · 1 Anthropic frontend-design · 1 Impeccable · 1 In-house Dark-Glass · chart gallery = dataviz + UIPM charts. See `design-sources.md` |
| Uniqueness | No two samples share a **layout frame**, a **primary chart form**, or a **palette** |
| Light | 1–2 warm light samples (paper or cream, layered; never white-and-hairline). The rest are dark |
| Fonts | Pick a real row from `…/ui-ux-pro-max/2.6.2/cli/assets/data/typography.csv` for each sample and paste its row number and the exact Google Fonts `<link>`. Apple samples use the system SF stack first, then Inter (rows 55 or 63). Never name a font that isn't in a real row, or say "not in typography.csv" |
| Palette | Give all 11 colour hexes for the dark theme and say how the light theme should derive |

Write the grid into the plan file, or show it to the user, before fanning out. Columns:
`# · file · feature (group) · what it leads with · design source · layout frame ·
palette (bg / accent / accent-2) · primary chart · fonts (row)`.

## Step 4: Write a real brief for every sample

This step decides the quality. Use `reference/builder-prompt-template.md`. Each brief is a
**paragraph-level spec**, never a category. It must name:
- the specific entities it shows, **by name**, taken from the real data
- the **exact figures**, and check that they add up (fees, percentages, totals, durations)
- what the screen **leads with** (the hero), and the primary button with its label
- 3–4 stat tiles, each with a delta, sparkline or target
- one **proposed block** the user didn't ask for
- what it **demotes**
- the motion: entry, one live loop, and the cursor interaction
- the plain-English "How it would work" (3–5 short steps)
- 4–6 seed ideas for "Ideas not built yet" (features + motion). The builder adds its own.

Pre-empt known defects by pasting the relevant lines from `reference/lessons.md`. If a brief
could be pasted into another sample without editing, it is too generic. Rewrite it.

## Step 5: Fan out the builders

1. Fill `reference/shared-contract-template.md` (product summary, shared data, product rules,
   paths) and write it to the **scratchpad** as `shared-contract.md`.
2. Launch **one `Agent` per sample** (`subagent_type: "claude"`, `run_in_background: true`),
   all in one message, or two messages if there are more than ~8. Each writes exactly one file.
3. Each builder replies with the receipt defined in the contract.
4. While they run, build the gallery (Step 8) and copy `reference/gate.sh` to the scratchpad.
5. As receipts arrive, check them:
   - The cited `colors.csv` row exists and has that name.
   - The typography row matches.
   - Any claimed tool path exists. The dataviz `validate_palette.js` lives under
     `/private/tmp/claude-*/bundled-skills/*/dataviz/scripts/`.
   - If a receipt reveals shipped hexes different from the grid, update that gallery card.

## Step 6: Gate

```bash
zsh <scratchpad>/gate.sh <repo>/design-samples
```

Silence per file means pass. Any FAIL means the sample is regenerated or fixed before review.

## Step 7: Adversarial review

Launch reviewer-fixer agents with `reference/reviewer-prompt-template.md`, **4–5 files each**,
as soon as a group of builders has finished. Don't wait for all 13, and never review a file
that is still being written. The reviewers fix in place and return a 1–10 score plus one line
of honest critique per file. Keep those scores and critiques for the hand-off.

After the reviews, act on anything small that they flagged but left alone, such as a demo
leftover or a stale label.

## Step 8: The gallery `design-samples/index.html`

Copy `examples/gallery-index.html` and replace the cards. Keep:
- the hero, with a count meta row (feature screens + chart gallery · dark/light split ·
  number of sources · "self-contained, zero build")
- the **"How to mix and match"** box (the shared token names plus 3 steps)
- the **sticky filter chips by design source**: All · Apple · UI UX Pro Max · Anthropic
  frontend-design · Impeccable · In-house Dark-Glass · dataviz (the small script at the bottom)
- the **bands per feature group**, then "Proposed extras", then "Chart gallery"
- **each card:** a CSS-only mini preview tinted with the sample's palette, the name, the role
  and number, the **source badge**, a "Leads with …" pitch, a one-line "how" note, tags
  (layout · charts · fonts), 5 swatches and Open. Add a small "+N ideas inside" tag
  showing how many ideas the sample's bottom section holds.

## Step 9: Verify

```bash
zsh <scratchpad>/gate.sh <repo>/design-samples          # silence = pass
cd <repo>/design-samples
grep -oE 'href="[0-9][^"]*\.html"' index.html | sed 's/href="//;s/"//' | while read f; do [ -f "$f" ] || echo "MISSING $f"; done
grep -ohE "[a-z]+-theme-[0-9]+" [0-9]*.html | sort | uniq -c   # one key per file
# every inline script parses:
for f in [0-9]*.html index.html; do python3 -c "import re;s=open('$f').read();open('/tmp/_s.js','w').write('\n'.join(re.findall(r'<script>(.*?)</script>',s,re.S)))" && node -e "new Function(require('fs').readFileSync('/tmp/_s.js','utf8'))" || echo "$f: script error"; done
cd .. && git status --short        # only design-samples/ is new
```

## Step 10: Record and hand off

1. Write `design-samples/rejected.md`, listing the excluded styles and a "Kept" section.
2. Save a project memory: where the round lives, that the samples use the shared tokens, and
   that it is waiting for picks.
3. The hand-off message:
   - A table with `# · feature · design source · layout · main charts · review score`.
   - "Mix and match": the one-sentence instruction.
   - **Honest open issues:** not browser-tested (if so), the reviewers' weakest-sample
     critiques, anything left unfixed.
   - Ask the user to keep, kill or mix ("keep 04 and 06, kill 10", "layout of #6 with the
     colours of #5"). Record kills in `rejected.md`. A kill with "never again" goes into
     `~/.claude/skills/ui/reference/banned-styles.md`.
   - Moving a direction into the real app is `/ui build`, and needs explicit approval.

## Next rounds

- Read `rejected.md` first. Never re-pitch a killed style or a close sibling of it.
- Bias new directions toward the families the user kept. The user loves Apple, so keep 4 or
  more Apple variants.
- Keep the shared token names identical across rounds, so palettes from round 1 still fit
  round 2 layouts.
