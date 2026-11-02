# Adapting a template into a project

Read this once a candidate is selected and approved. It applies to Route A (a built
template), Route B1 (source at a pin), and Route C step 5 (an open-source find).

## The method is a trim, not a rebuild

Lift the working feature and reshape it to fit. Do **not** clean-room reimplement from
the contract. Rebuild only the specific parts a critique flagged as defective.

The cost difference is measured, not theoretical: one template was trimmed and composed
from existing pieces and was cheap; one was rebuilt from a 207-scenario contract and
cost roughly 800k tokens for 3,569 lines. Correct output, wrong method.

What makes trimming safe is *composition*: shared concerns come from templates that
already exist rather than being copied alongside the feature. Nine source defects
disappeared structurally that way in one adapter — nobody hand-fixed them.

## Where "trim, do not rebuild" stops applying

The rule assumes two things: you own the source, and the language matches. Both hold when
lifting from your own products into a template.

Neither holds for a foreign-language open-source find. There is nothing to lift — a
mechanical translation drags in idioms that do not belong and produces code a reviewer
spots instantly. There, the method inverts: extract the contract and rebuild. See
[extracting-from-a-product.md](extracting-from-a-product.md).

So: **trim what you own, rebuild what you find.**

## Language conversion happens here

A template belongs to no product. It is written in the language its source was in, and
it is converted to the target's language and conventions **at adoption** — that is now.

What carries across the conversion:

- the behavior contract
- the test scenarios

Both are language-independent. A Python template going into a TypeScript project is not
harder to adopt than a TypeScript one; the source language costs nothing. The only real
difference is that tests in a foreign language are read for their scenarios rather than
executed directly.

## Order of work

1. **Read the contract first.** `TEMPLATE.md` gives behavior, extension points, security
   posture, non-goals, and verification. Non-goals matter as much as behavior — they say
   what the template deliberately refuses to do, and those refusals are usually load-bearing.

2. **Map the ports.** Templates achieve separation through dependency-injected structural
   ports with zero runtime dependencies, not through directory layout. Three have no
   `adapters/` directory at all. Find the ports; they are where the target project plugs in.

3. **Write the adapter, not a fork.** The target supplies concrete implementations of the
   ports — its database, its clock, its notifier. Keep that layer separate from the core
   you lifted, so a later version bump touches one side only.

4. **Port the tests.** Non-negotiable. The tests are the reason the template is worth
   anything; the implementation is the cheapest layer. Convert scenarios to the target's
   test runner. If a scenario cannot be expressed in the target, that is a finding to
   report, not a test to drop silently.

5. **Run them in the target.** Green in the library proves nothing about the target.

6. **Keep the layers apart.** Reusable core, adapters, generated files, product-specific
   overrides, migrations, and tests each stay distinct. Collapsing them is what makes the
   next upgrade impossible.

## Conflicts

`compatibility.json` carries `conflict_policy.owned_paths` — paths the template expects
to own. Before writing anything:

- List every collision against the target tree.
- Report them. Do not resolve one silently.
- A collision on a path the target actively maintains usually means the adapter layer
  should absorb the difference, not that the target's file should be overwritten.

## Dependencies are real

`template.yaml` declares dependencies with version ranges, and the composition graph is
not decorative:

```
pending-action-store (leaf)      conversation-store (leaf)
        ^ optional                       ^
proposal-approval-workflow  <----  omnichannel-agent-core
        ^          ^                     ^         ^          ^
  accounting-tool-pack     web-assistant-adapter   telegram-assistant-adapter

shared-board-core (leaf)
        ^                    ^                    ^
board-access-policy   board-realtime-sync   board-notifications-and-counts
                                                  ^ pending-action-store (outbox)
```

Adopting a channel adapter without the agent core it composes recreates the duplication
the library exists to prevent. If the user wants only the leaf, say what is being lost.

## Known defects to fix on the way in

Some are already fixed in the templates but still live in the source products, so they
matter for Route B:

- missing TTL and audit trail
- non-idempotent save
- executable endpoints held in React
- floating-point money — store integer cents, convert at the boundary only
- server-timezone dates

And carried *by* released templates, so they matter for Route A. Each already has a
consumer working around it:

- `shared-board-core` reads `AuthzDecision.via` as ownership when it names which layer
  permitted the action, so an authorizer reporting `via: "grant"` is refused on a board
  it owns.
- `shared-board-core` runs its notify step after the store transaction commits, so a
  notification cannot share the write's unit of work.
- `shared-board-core` does not pass the dedup key to `NotificationAudience.suppress`,
  and returns before `deliver` when everything is suppressed, so the key is never exposed.
- `pending-action-store` cannot enumerate — it answers "the one active proposal in this
  scope" and cannot express a drain batch, a recipient inbox, or a dead-letter list.

Releases are immutable. If one of these bites during adoption, work around it in the
adapter layer and report it; never edit a released version in place.

## Reporting

State plainly:

- what was adopted, at what version, from what route
- every file created or modified in the target
- every deviation from the template's contract, and why
- which tests were ported, which were not, and what that leaves uncovered
- any dependency implied but not adopted
