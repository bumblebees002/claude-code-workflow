# Shared contract for every design sample (read ALL of this)

<!-- ORCHESTRATOR: fill every {{…}} slot, delete these comments, and save the result to the
     scratchpad as shared-contract.md. Builders get its absolute path. -->

## The product
{{PRODUCT_SUMMARY}}
<!-- 3–5 sentences: what it is, who uses it (the roles), and what makes it different. Name the
     app sections and the header toggles exactly as they exist. -->

You are designing a **NEW feature screen that the app does not have yet**, in a **NEW visual
skin**. The user will mix and match across samples ("the layout of #06 with the colours of
#05"), so both the layout and the palette must be strong on their own.

## Mood
Futuristic, minimal and **professional**. It must NOT look like AI slop or a template.
Minimalism is a quality here, not the concept.

**Banned outright:** neumorphism, soft-UI, skeuomorphism, claymorphism, hairline-only Swiss
minimal, neubrutalism, dense data-terminal or ledger tables, radius 0. Also banned: anything in
`{{SAMPLES_DIR}}/rejected.md` and `~/.claude/skills/ui/reference/banned-styles.md`.

## Build contract
Create ONE self-contained HTML file at the EXACT path given in your assignment, under
`{{SAMPLES_DIR}}/`.

**Allowed:**
- One inline `<style>`.
- One inline `<script>` of **40 lines or fewer**, used only for the cursor interaction and the theme toggle.
- Inline SVG for charts and icons.
- Google Fonts `<link>` tags with preconnect. These are the ONLY external references.

**Not allowed:** frameworks, a build step, `<script src>`, `fetch`, web images, or
reading or modifying any other repo file.

**It must:**
- Render from `file://`.
- Have no horizontal page scroll at 375, 768 or 1280px. Wide things scroll inside their own `overflow-x:auto` box.
- Store the theme in localStorage under `{{THEME_KEY}}-NN` (NN is your number), wrapped in try/catch, accepting only `light` or `dark`.

**Read these first and reuse them:**
- `~/.claude/skills/ui/reference/sample-recipe.md`: the donut ring, sparkline, tilt/spotlight, stagger and theme-toggle code. Re-colour it; don't re-derive it.
- Your design source, using the paths in `~/.claude/skills/feature-ui-sample/reference/design-sources.md`. Read enough of it to design faithfully in that language, and say what you took from it in your receipt.
- `~/.claude/skills/feature-ui-sample/reference/lessons.md`: the defects previous reviewers caught. Don't repeat them.

## Shared token names (REQUIRED, for mix-and-match)
Define ALL of these in `:root` (the default theme) and override them in the other theme
(`[data-theme="light"]` or `[data-theme="dark"]`). Both blocks must list all 15. Use only these
variables for colour, radius and fonts. You may add more tokens only if they are derived from
these (for example `color-mix(in srgb, var(--accent) 75%, var(--ink))`).

```
--bg --surface --surface-2 --line --ink --muted --accent --accent-2 --good --warn --bad --radius --font-display --font-body --font-mono
```

The test: pasting another sample's `:root` block into yours must fully re-colour your screen.

## The eight required ingredients (checked by grep and by a reviewer)
1. **A named concept.** Say what the screen *leads with*, not a style name.
2. **Two or more visualisations, at least one radial.** A donut, ring or arc gauge in inline SVG using `stroke-dasharray`.
3. **A hero element.** One dominant block that carries the primary action, with real elevation or glow.
4. **Stat tiles that mean something.** Each has a delta, trend arrow, sparkline or progress to a target. Never a bare label and number.
5. **At least one cursor-reactive interaction** using `pointermove`: tilt, spotlight or magnetic.
6. **Entry motion.** A staggered fade-up with `@keyframes`, plus one purposeful live loop (a progress fill, a ticking counter, a pulse). Honour `prefers-reduced-motion` so that it actually stops everything.
7. **A working light/dark toggle.** Both modes legible, and the accent readable in both (about 4.5:1 where it is used as text).
8. **Fonts actually loaded.** A preconnect plus a `<link>` for every webfont you name.

Also required: `:focus-visible` rings, and hover, active and disabled states on buttons.

## Anti-slop rules
- No gradient text, except at most one display number or headline.
- No emoji. Inline SVG line icons only, in one stroke style.
- No uniform grid of equal cards. Size encodes importance.
- No "Lorem", "Card title", "User 1", or stats that contradict the shared data. **The numbers must add up.**
- Figures use tabular-nums. Money is shown like `$29.00`, durations like `1m 52s`.
- One radius scale, one elevation scale and one type scale, on a 4/8px rhythm. No half-pixel font sizes.
- Status colours (`--good`, `--warn`, `--bad`) are for status only. Never use them on ordinary fees, chrome or decoration.
- Copy is short and human, the way a real product writes it.

## Required bottom section: Design DNA + How it would work + Ideas not built yet
At the very bottom of the page, put `<footer id="design-dna">` containing three parts.

**1. Design DNA** (one compact row or grid):
- **Design source:** your label exactly as given (e.g. "Apple · Liquid Glass", "UI UX Pro Max · #47 Exaggerated Minimalism").
- **Layout:** the name of your layout frame.
- **Palette:** 5 swatches, showing the hex for BOTH themes (e.g. `#64d2ff / #0066cc`).
- **Fonts:** the names.

**2. "How it would work"** (heading with that literal text): **3 to 5 short numbered steps**
in very simple, plain English. Write it the way you'd explain it to a friend, with no
jargon, no code words and no state-machine names. Each step is one short sentence.
Example:
1. You post one brief.
2. Up to three agents work on it at the same time.
3. You compare the results side by side.
4. You pay only the one you pick. The others cost you nothing.

**3. "Ideas not built yet"** (heading with that literal text; the wrapper has `id="ideas-next"`).
These are things you had in mind but did not build into this sample. Keep them simple, one
or two short sentences each, easy to understand:
- **"More features we could add"**: 3 to 5 ideas for what this feature could also do.
- **"Animation & interaction ideas"**: 3 to 5 motion or interaction ideas that would make
  it feel more alive, described so a non-designer can picture them (e.g. "When an agent
  finishes, its lane could flash softly and slide to the top.").
- **"Where else this could show up"** (optional): 1 to 3 other screens or moments where this
  idea would also help.

Style this section so it is readable but quiet: muted text, a small heading per list, two
or three columns on desktop and one on mobile. It should read like a designer's note, not a
second page.

## Product rules that stay true in every screen
{{PRODUCT_RULES}}
<!-- e.g. required badges/labels (AI disclosure), trust rules, money rules, state names -->

## Shared data (use these names and numbers exactly; invent only what your feature needs, consistent with them)
{{SHARED_DATA}}
<!-- Real names from the seed/fixtures: users and roles, main entities with prices/tiers/stats,
     example inputs, real review text, state machines, enums, fee and limit constants. -->

## Reply with EXACTLY this receipt and nothing else
```
file: <samples dir>/NN-slug.html
concept: <one line: what this screen leads with>
proposed: <the one block you added that was not asked for>
source: <design source label>; what I took from it: <one line>
palette: shipped <accent hex> / <bg hex>; nearest colors.csv row: <N> (<name>) or "no comparable row"
fonts: <names>; typography.csv row <N>, or "not in typography.csv"; linked: yes
viz: <chart forms used>
ideas: <count of "Ideas not built yet" items>
lines: <wc -l of the file>
ingredients: 1..8 all present
```
Every line must be checkable. Don't claim a tool or row you can't point to.
