# Design sources: the label on every sample

Each sample shows ONE source label, exactly as written below. It appears in the sample's
Design DNA footer and as the gallery badge. Every builder must read its source before
designing, and say in the receipt what it took from it.

Be honest. If no installed skill covers a variant (for example, macOS HIG), the label says
where the guidance really came from. Never invent a skill, palette row or tool.

`UIPM` = `~/.claude/plugins/cache/ui-ux-pro-max-skill/ui-ux-pro-max/2.6.2/cli/assets/data/`,
which holds `styles.csv`, `colors.csv`, `typography.csv`, `charts.csv` and more. If the
version folder differs, `ls` the parent to find it.

---

## Round mix (default 13 files)

| Family | Count | Gallery filter chip |
|---|---|---|
| **Apple**: 4 *different* variants from the 5 below | **4** | Apple |
| UI UX Pro Max: different styles.csv rows | ~5 | UI UX Pro Max |
| Anthropic frontend-design | 1 | Anthropic frontend-design |
| Impeccable | 1 | Impeccable |
| In-house Dark-Glass | 1 | In-house Dark-Glass |
| Chart gallery: dataviz + UIPM charts.csv | 1 | dataviz |

For fewer samples, shrink UIPM first and keep 4 Apple. For more samples, add Apple variant 5
and more UIPM rows.

---

## Apple: the five variants (pick 4 per round, all different)

Always use the SF system stack first:
`-apple-system, "SF Pro Display", "SF Pro Text", BlinkMacSystemFont`. After it, load Inter
from Google Fonts: typography.csv row 55 "Spatial Clear" or row 63.

### A1 · Apple · Liquid Glass
- **Read:** `~/.claude/plugins/marketplaces/ecc/skills/liquid-glass-design/SKILL.md`, and UIPM `styles.csv` row No=14 "Liquid Glass".
- **Take:**
  - translucent material: `backdrop-filter: blur(24–30px) saturate(180%)`
  - a bright specular edge (a gradient border, brighter at the top-left)
  - a content-adaptive tint
  - `.interactive()` capsules that squash and scale on press
  - `.glassProminent` primary buttons
  - bottom sheets with a grabber
  - radius 28–34px
  - vibrancy on secondary text
  - a specular highlight that follows the pointer
- **Best for:** one focused decision or moment, such as a question, a confirmation or a checkout sheet over a blurred page.
- **Palette hint:** a near-black ground with slow iridescent blobs (#ff375f, #5e5ce6, #64d2ff). Accent #64d2ff; system good/warn/bad are #30d158 / #ffd60a / #ff453a.

### A2 · Apple · visionOS Spatial
- **Read:** UIPM `styles.csv` row No=55 "Spatial UI (VisionOS)", plus the material notes in the liquid-glass skill.
- **Take:**
  - glass windows floating at different depths, with the selected one closer and the others receded
  - soft layered shadows and generous padding
  - radius 24–32px
  - **ornaments**: small floating toolbars attached below a window
  - a gaze-style specular glow on hover
  - calm, spacious and never dense
- **Best for:** canvases, pipelines, multi-object workspaces and spatial overviews.
- **Palette hint:** bg #0b0d12 with 2–3 very soft colour fields. Accent #0a84ff, accent-2 #bf5af2.

### A3 · Apple · macOS Sidebar (HIG)
- **Read:** there is no installed skill for this. Use Apple Human Interface Guidelines knowledge and borrow the material rules from the liquid-glass skill. The label adds the suffix: "Apple · macOS Sidebar (HIG, from built-in knowledge)".
- **Take:**
  - a translucent source-list sidebar with SF Symbols-style line icons
  - a unified toolbar with a centred title and a search field
  - a content area plus an optional inspector pane
  - grouped inset lists and segmented controls
  - small radius (8–12px) on controls and 16px on panels
  - restrained accent (system blue or tinted)
  - quiet depth and very precise alignment
- **Best for:** dense "pro" tools such as settings, libraries, admin, builder consoles and file-like lists.
- **Palette hint:** window #1e1e1e / sidebar rgba(40,40,40,.72) / hairline rgba(255,255,255,.08). Accent #0a84ff; the light theme is macOS light (#f5f5f7 window, white content).

### A4 · Apple · Keynote Bento
- **Read:** UIPM `styles.csv` row No=53 "Bento Grids", and `~/.claude/skills/ui/reference/style-catalog.md` → "Bento Grids (disciplined)".
- **Take:**
  - an Apple-keynote bento of unequal tiles on a near-black stage
  - one huge number or phrase per tile
  - product-page typography with tight tracking on huge SF display sizes
  - one graphite or blue accent
  - tiles that reveal on scroll or in a staggered entry
  - radius 20–28px
  - every tile makes exactly one point
- **Best for:** summaries, "year in review", analytics overviews, launch pages and marketplace pulse.
- **Palette hint:** stage #000 / tile #111113 / tile-2 #1d1d1f, ink #f5f5f7, accent #2997ff. The light theme is #f5f5f7 with white tiles.

### A5 · Apple · Widgets & Live Activities
- **Read:** the WidgetKit and Live Activity parts of the liquid-glass skill, and UIPM row 14.
- **Take:**
  - iOS home-screen widget sizes (small 2×2, medium 4×2, large 4×4) arranged as a stack
  - a **Dynamic Island / Live Activity** pill that expands
  - the lock-screen notification stack
  - glanceable single numbers and rings (Activity-rings style)
  - radius 22–26px, continuous corners
- **Best for:** anything live or ambient: a running job, a countdown, a delivery, a streak or a schedule.
- **Palette hint:** wallpaper gradient (deep indigo to violet), widget glass rgba(28,28,30,.72). Accents #30d158 / #0a84ff / #ff9f0a (Activity-ring colours only for rings, never for status).

---

## UI UX Pro Max (styles.csv rows): futuristic-friendly picks

Label format: `UI UX Pro Max · #N <Style Category>`. Read that row before designing.

| Row | Style | Good for |
|---|---|---|
| 51 | HUD / Sci-Fi FUI (use it **restrained**: thin lines, corner brackets, mono readouts, no neon, glitch or scanlines) | races, live comparisons, mission control |
| 47 | Exaggerated Minimalism | leaderboards, one giant number, manifesto pages |
| 43 | AI-Native UI | AI assistants, insights, concierge flows |
| 33 | Comparative Analysis Dashboard | versions, A/B tests, benchmarks |
| 36 | Financial Dashboard | payouts, wallets, invoices, pricing |
| 31 | Real-Time Monitoring | admin walls, ops, health |
| 65 | Gradient Mesh / Aurora Evolved | schedules, onboarding, calm ambient screens |
| 10 | Aurora UI | hero moments, launches |
| 46 | Dimensional Layering | stacked objects, drawers over drawers |
| 30 | Executive Dashboard | one-screen summaries |
| 32 | Drill-Down Analytics | hierarchies and zooming in |
| 62 | Interactive Cursor Design | playful explorers, maps |
| 66 | Editorial Grid / Magazine | reports, briefs, public pages (warm light) |
| 7 | Dark Mode (OLED) | true-black cockpits |

**Never use** rows 2 (Neumorphism), 9 (Claymorphism), 13 (Skeuomorphism), 19 (Soft UI Evolution), 4/38/77 (Brutalism family), 1/50 (Swiss minimal), 73 (Terminal), or any row in `rejected.md`.

## Anthropic frontend-design
- **Read:** `find ~/.claude/plugins/cache/claude-plugins-official/frontend-design -name SKILL.md`.
- **Take:** commit to one bold, intentional direction. Type does the work. Have one
  orchestrated load moment and one bold element, keep everything else quiet, and nothing
  templated. It works well as the **warm light** sample (paper tones, a serif display face).

## Impeccable
- **Read:** `~/.claude/plugins/cache/impeccable/impeccable/*/skills/impeccable/SKILL.md`, then
  `reference/craft-floor.md` and `reference/new-work.md`. **Do not run** its npx/node scripts.
  Just apply the guidance.
- **Take:**
  - the quality floor and the absolute bans: no eyebrow kickers, no gradient text, no side-stripe borders over 1px
  - offset-and-blur shadows only
  - contrast of at least 4.5:1
  - one authored motion moment
- **Best for:** serious, high-stakes screens: disputes, legal, trust and money decisions.

## In-house Dark-Glass (the `/ui` skill's default system)
- **Read:** `~/.claude/skills/ui/reference/dark-glass-system.md` and `components/tokens.css`.
- **Take:**
  - the #030303 ground
  - the white-at-alpha elevation ladder (.02/.04/.06/.09)
  - accent at 8/20/100% only
  - the six motion variables
  - a 2px accent top rule on the hero
  - near-monochrome charts
  - scale(.97) on press
- Map its colours onto the shared token names.

## Chart gallery: dataviz + UIPM charts.csv
- **Read:** load the `dataviz` skill with the Skill tool, and UIPM `charts.csv`.
- **Take:**
  - the categorical slots `--c1…--c5` in dataviz's fixed order
  - validate them with `validate_palette.js` under `/private/tmp/claude-*/bundled-skills/*/dataviz/scripts/`
  - 2px lines, rounded bar ends, one-hue sequential heatmaps, no dual axes
  - text never drawn in a series colour
  - form-per-job choices taken from the charts.csv rows

## Honesty rules for receipts
- A `colors.csv` row is cited by its **number and name**, and the orchestrator reads it back.
- A typography row is cited by its number. If a font isn't in the file, say
  "not in typography.csv".
- A tool is claimed only if its path exists afterwards.
