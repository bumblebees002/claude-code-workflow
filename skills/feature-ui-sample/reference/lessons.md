# Lessons: defects reviewers caught in real rounds

Builders read this before building, and reviewers hunt for every item. Each line is a real
bug that shipped in a first draft. Paste the relevant ones into briefs.

## Layout and overflow
- **A bare `1fr` in a grid lets a wide child push the page wider than 375px.** Always use
  `minmax(0,1fr)` and set `min-width:0` on grid and flex children. (A 440px diff grid made
  a whole page 488px wide.)
- **`white-space:nowrap` chips and labels overflow narrow columns** at mid widths
  (1100–1440px) as well as on phones. Let them wrap, or shorten the copy.
- **`body{overflow-x:hidden}` hides the bug; it doesn't fix it.** Find the element that
  overflows. Keep `html{overflow-x:clip}` only as a safety net.
- **`.hero > *{position:relative}` also catches the absolute glow/spotlight overlay.** Both
  selectors have the same specificity, so the later one wins. The overlay turns into a grid
  item, takes the first column, and pushes the real content into the side column, leaving a
  huge empty card. Write `.hero > :not(.hero-glow){position:relative}`, or put the overlay in
  a pseudo-element.
- A fixed-height button with a long label wraps on mobile. Use `min-height`.
- Three side-by-side "lanes" become a sideways scroller below ~1100px. Decide on a mobile
  form deliberately (stack them, or switch to tabs) instead of letting them scroll.
- Nodes in a horizontal pipeline need room for their ring plus a status chip. Stack them
  inside the node when the canvas is narrow.

## Motion
- **An entry animation that ends at `clip-path:inset(0)` with `forwards` permanently clips
  shadows and glows.** End at a negative inset such as `inset(-120px)`, or don't use `forwards`.
- **An entry animation with `forwards` that holds `transform:none` overrides the JS tilt.**
  Use `animation-fill-mode:backwards`, with no opacity:0 base state.
- The reduced-motion block must stop *everything*: tickers, live lines, drifting blobs,
  countdowns (including JS ones), and rotating icons.
- A sparkline drawn with `stroke-dasharray:240` plus `vector-effect:non-scaling-stroke` can
  cut off the last point. Use a large dasharray (1000).
- Round line caps make rings and gauges overshoot their value. Compensate the dash offset.

## Colour and theme
- **Light-mode accents at ~3.3–4.2:1 used as text.** Darken them (e.g. #0a84ff → #0066cc,
  #0891b2 → #0e7490) or add derived `--accent-ink` / `--good-ink` tokens
  (`color-mix(in srgb, var(--x) 75%, var(--ink))`).
- **Hardcoded hex values ignore the theme and break mix-and-match.** That covers side
  colours, mesh blobs and shadows. Derive them from tokens with `color-mix`.
- **SVG `stop-color="var(--accent)"` as an attribute doesn't work.** Use
  `style="stop-color:var(--accent)"`.
- **Status red used on ordinary fees or payouts reads as an error.** Keep `--bad` for
  refunds and failures only, and `--good` for pass/healthy only. Delta pills stay neutral
  unless they are a status.
- The light theme block missing `--radius` and the font tokens breaks mix-and-match. Both
  blocks must list all 15 tokens.
- Footer swatches whose fills use `var()` show light colours next to dark hex labels. Show
  both hexes (`#64d2ff / #0066cc`) or use literal fills.

## Data
- **Numbers that don't add up are the most common defect.** Recompute every sum, fee (15% of
  X), percentage, average, duration, deadline minus elapsed, and count before writing it.
  Examples: a previous-period figure that isn't avg × count; pass^3 computed as a power of
  per-attempt passes instead of "cases where all k passed"; a refund total that no mix of
  real prices produces; ETAs that don't match the steps; a timeline whose bars sum to 1m 50s
  but say 1m 52s.
- A ticker or event feed must agree with the chart's timeline (for example, "degraded since
  11:34" in both places).
- A budget cap that the next scheduled run will exceed must be handled on screen: show
  "waits for your OK".
- Keep one story per sample. A figure used in two places on the page must match.

## Script and accessibility
- Validate the stored theme (`light|dark` only), and set the toggle's aria-label to
  "Switch to light/dark theme", in sync on load.
- A script at the end of body makes the theme flash on load. Set the theme from the head
  (small inline logic) or accept that it flashes.
- A brand link whose text is hidden on mobile needs an `aria-label`.
- A CSS-counter "pick count" breaks when cards are hidden by a filter. Count in JS, and use
  `aria-disabled` on the dependent button.
- Leftover "Pressed:" demo buttons, design-thesis comments and style-guide bits must be removed.

## Taste (reviewer critiques worth pre-empting)
- A violet→cyan gradient with Space Grotesk reads as generic SaaS. If you use it, give it a
  real idea.
- Violet glass with drifting glows reads as a stock "AI-native" look. Keep glows few and purposeful.
- Blurred mock pages behind a sheet plus drifting blobs can look like a tech demo. Make the
  blurred page real and calm.
- A chart gallery with identical card chrome reads as a spec sheet. Vary the spans and let
  one hero chart dominate.
- Dense small mono labels drift toward the banned data-terminal look.
