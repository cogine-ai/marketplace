---
name: cogine-power-gates
description: "Use for Cogine gated execution when material risk, unknowns, deviation, or unverified completion requires a pause."
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
| `high-risk` | Actions changing architecture/contracts, production/customer state, security/permissions, billing/cost, release/public or consequential remote/live state, or that are destructive, irreversible, cross-repo contract/state changes, or hard to verify | All; confirm material decisions and remote/live actions unless explicitly authorized |

Route in order:

1. Use `blind-spot-only` only for its named discovery/critique scope.
2. Set the floor from consequences; read-only analysis stays `standard` absent another high-risk consequence.
3. Honor a named mode only at or above that floor.
4. Without one, use `fast` only when every fast predicate holds; otherwise use `standard`.

Read `references/task-modes.md` for boundaries.

## Gate Rule

Interrupt only if unresolved issues could materially change the next action; otherwise pass silently. Announce mode only when behavior changes.

## Discovery

| Unknown | Response |
|---|---|
| Known known | Verify the prompt's map against code, evidence, or live state when relevant. |
| Known unknown | Ask, research, or interview when the answer could change the path. |
| Unknown known | Expose tacit preference with options, brainstorms, references, or prototypes. |
| Unknown unknown | Blind-spot pass, reference scan, or plan review before expensive work. |

Resolve, accept, or escalate only material unknowns.

## Gates

| Gate | Pass or interrupt condition |
|---|---|
| Frame | Objective, limits, and inspectable success make the next action clear. Ask only when missing input could materially alter it; otherwise state the assumption and continue. |
| Discovery | The relevant method was used; no unresolved unknown can materially change the path unless accepted or escalated. |
| Commit | Path, scope, verification, and stop triggers are bounded. Get a human decision for material changes to meaning, scope, architecture/contracts, data, permissions, security, cost, release/public state, or remote/live state unless already authorized in this session. |
| Deviation | Continue and log local, reversible, in-scope variation. Pause when new facts change the accepted path, material semantics/risk, remote/live state, or validation. |
| Evidence | Map every material completion claim to direct evidence. If proof is missing, use `implemented but not fully verified`, `blocked on validation`, or `not complete`. |

During Execute, maintain any requested implementation-notes artifact and record material assumptions, decisions, and deviations.

## Artifacts And Transfer

Use Markdown for operational/copyable artifacts and HTML for UI, visual, or interaction prototypes; consider HTML for rich explainers, pitches, quizzes, walkthroughs, and comparisons. Preserve a named format. Ask once only when Markdown versus HTML materially affects usefulness. Never replace the requested artifact with a gate report.

Transfer ordinary work with outcome, evidence, material decisions/deviations, residual risk, and owner actions. When understanding or buy-in is a goal, produce the requested explainer, pitch, or quiz.

## Output And Completion

Do not report passed gates. On interruption, report `Gate`, `Reason`, `Options`, `Recommendation`, and `Need`. Read `references/gate-reports.md` for contracts and `references/examples.md` for routes and state traces.

Claim complete only when the objective is met, non-goals are respected, material unknowns/deviations are resolved, accepted, or escalated, each material claim has direct evidence, residual risk is explicit, and the human can understand what changed and remains.
