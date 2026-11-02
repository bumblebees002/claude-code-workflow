---
name: tutor
description: Teach me any codebase systematically, like you did with ai_accountant — skeleton first, no code reading required
version: 1.0.0
trigger: "teach me this project", "how does this codebase work", "explain this repo structure", "/tutor"
---

# Tutor — Codebase Teaching Skill

When invoked with a project directory, this skill analyzes the codebase and teaches it the way you learned ai_accountant: one concept at a time, in very short sentences, waiting for your feedback before moving forward.

## What This Skill Does

1. **Scans the project structure** — finds the main pattern (4-layer chains, API routes, libraries, etc.)
2. **Identifies the skeleton** — what are the 12 files that explain 80% of the codebase?
3. **Traces one feature end-to-end** — picks a concrete example and walks through it
4. **Teaches systematically** — breaks knowledge into chunks, waits for your confirmation
5. **Connects all dots** — shows how everything fits together

## Teaching Methodology

The skill follows this exact pattern:

### Phase 1: The Shape (5 minutes)
- Identify the main architecture (e.g., frontend → API → brain → database)
- Show it works the same way for every feature
- Wait for confirmation before moving on

### Phase 2: The Files (10 minutes)
- Name the 12 core files (the 80%)
- For each, explain in ONE sentence what it does
- Have the user open them in their IDE

### Phase 3: One Example (15 minutes)
- Pick one feature (e.g., "create an expense")
- Trace it through all layers
- Show how data flows from screen → database → back to screen

### Phase 4: The Repeating Pattern (5 minutes)
- Show that this pattern repeats 20+ times
- User confirms: "I can guess the file names for any feature"
- Proof: pick another feature, they predict the files

### Phase 5: Integration & Special Parts (10 minutes)
- External integrations (Stripe, API calls, webhooks)
- The AI part (if the project has it)
- Debugging approach

### Phase 6: Complete Skeleton (2 minutes)
- One-line summary of everything taught
- The three files that explain it all

## How to Use This Skill

```bash
/tutor                                    # Current directory
/tutor /path/to/project                   # Specific project
/tutor --project my-app --interactive     # Interactive mode (default)
```

## Detection Logic: Identifying the Pattern

The skill automatically detects the architecture type:

| Pattern | Detection |
|---------|-----------|
| **Next.js API + React** | `app/page.tsx`, `app/api/*/route.ts`, `lib/` |
| **Express + React** | `routes/`, `controllers/`, `middleware/`, `src/components/` |
| **Django + Templates** | `urls.py`, `views.py`, `models.py`, `templates/` |
| **Rails** | `app/controllers/`, `app/models/`, `app/views/`, `routes.rb` |
| **Microservices** | Multiple `src/` dirs, `docker-compose.yml`, `proto/` files |

## Output

The skill produces:

1. **A teaching session** (live, in the terminal)
2. **A skeleton map** (written to `PROJECT_SKELETON.md` in the project)
3. **A checklist** (what was taught, what wasn't, what to learn next)

## The 80/20 Rule

For every codebase, the skill identifies:

- **The skeleton**: 12 core files (the 80%)
- **The pattern**: The repeated structure that makes the other 200+ files predictable
- **The 3 files**: The ones that explain everything
- **The debuggging map**: Where to look when something breaks

## Teaching Rules

The skill ALWAYS:

1. **Uses very short sentences** — one concept per message
2. **Shows file paths** — so the user can open them
3. **Waits for confirmation** — "Does this make sense?" before moving on
4. **Builds on prior knowledge** — "Like we just learned..."
5. **Asks questions** — forces the user to predict, not just listen
6. **Never explains code** — only the shape and connections
7. **Uses one working example** — traces it completely, then shows it repeats
8. **Saves output locally** — they own the skeleton map

## Phase Checklist

- [ ] **Phase 1** — Identified the main pattern (frontend → API → brain → database or equivalent)
- [ ] **Phase 2** — Named the 12 core files
- [ ] **Phase 3** — Traced one feature end-to-end
- [ ] **Phase 4** — User confirmed the pattern repeats
- [ ] **Phase 5** — Explained integrations / AI / special parts
- [ ] **Phase 6** — Generated complete skeleton

## Tracking Progress

The skill tracks:

- **Files taught**: 12 (the skeleton)
- **Patterns identified**: (3-5, depending on project)
- **Example traced**: (1 full feature)
- **Confirmations received**: (how many times did they say "yes"?)

## Related Commands

- `/code-review` — Once you understand the skeleton, review code changes
- `/debug` — Use the skeleton to debug issues
- `/plan` — Plan changes using the architecture you learned

---

**Version**: 1.0.0  
**Last Updated**: 2026-08-23  
**Works With**: Any codebase (detected automatically)
