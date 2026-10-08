---
name: cogine-power-gates
description: "Use for gate or blind-spot reviews, consequential actions, or material uncertainty, deviation, or missing proof that changes whether work can proceed."
---

# CoginePowerGates

This protocol controls continue/pause/completion; repo/domain rules control execution. Exit false-positive activations silently.

Loop: Frame -> Discover -> Commit -> Execute -> Verify -> Transfer.

## Modes

Choose scope, then its safety floor. Never invent modes.

| Mode | Use | Gates |
|---|---|---|
| `blind-spot-only` | Explicit unknown discovery, critique, prompt improvement, or a preimplementation-only pass | Frame, Discovery; stop |
| `fast` | Local, reversible work with clear scope, success, and obvious validation | Frame, Evidence |
| `standard` | Other material work | Frame, Discovery, Commit, Evidence; Deviation on trigger |
| `high-risk` | Actions changing material architecture/contracts, production/customer state, security/permissions, money, or release/public/remote state, or that are destructive, irreversible, costly, or hard to verify | All; apply existing authorization and resolve new material human decisions |

Route in order:

1. Use `blind-spot-only` only for its named discovery/critique scope.
2. Set the floor from consequences; read-only analysis stays `standard` absent another high-risk consequence.
3. Honor a named mode only at or above that floor.
4. Without one, use `fast` only when every fast predicate holds; otherwise use `standard`.

Read `references/task-modes.md` for boundaries.

## Gate Rule

Reuse decisions and authorization within their objective, scope, consequences, and material assumptions. Interrupt only for new material human decisions or unavailable input/proof blocking the next action; continue independent work. Passed gates stay silent. Announce mode only when behavior changes.

## Discovery

| Unknown | Response |
|---|---|
| Known known | Verify the prompt's map against code, evidence, or live state when relevant. |
| Known unknown | Ask, research, or interview if the answer changes the path. |
| Unknown known | Expose tacit preferences with options, brainstorms, references, or prototypes. |
| Unknown unknown | Blind-spot pass, reference scan, or plan review before expensive work. |

For a material unknown, identify the decision it could change, existing evidence, cheapest useful method, and sufficient evidence to proceed. Inspect/research facts autonomously; ask for material preferences or unavailable input. Resolve, accept within authorized bounds, or escalate; do not exhaust every category.

## Gates

| Gate | Pass or interrupt condition |
|---|---|
| Frame | Objective, limits, and evidence for the requested deliverable make the next action clear. Ask only when missing input materially alters it; otherwise state material assumptions and continue. |
| Discovery | Evidence is sufficient for the next action; remaining material unknowns are resolved, accepted within authorized bounds, or escalated. |
| Commit | Bound path, scope, required evidence, and stop triggers. Get human decisions for changes beyond authorized bounds; otherwise reuse decisions and authorization. |
| Deviation | Continue and log authorized adaptation, including equally or more credible validation. New facts crossing authorized bounds require a decision only for affected actions. |
| Evidence | Match requested outcomes and material claims to evidence. Optional checks are not acceptance requirements. Missing required proof means `implemented but not fully verified`, `blocked on validation`, or `not complete`. |

During Execute, maintain any requested implementation-notes artifact and record material assumptions, decisions, and deviations.

## Artifacts And Transfer

Preserve the requested format. Use Markdown for operational/copyable artifacts and HTML for visual/interactive prototypes; consider HTML for rich explainers, pitches, quizzes, walkthroughs, and comparisons. Ask once only if format materially affects usefulness. Never replace the artifact with a gate report.

Transfer outcome, evidence, material decisions/deviations, residual risk, and owner actions. For understanding or buy-in, produce the requested explainer, pitch, or quiz.

## Output And Completion

Do not report passed gates. On interruption, report `Gate`, `Reason`, `Options`, `Recommendation`, and `Need`. Read `references/gate-reports.md` for contracts and `references/examples.md` for routes and state traces.

Claim complete only when the requested objective is met, non-goals are respected, no required decision or validation remains, material claims have direct evidence, uncertainty and residual risk are explicit, and the human can understand what changed and remains.
