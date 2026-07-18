---
name: write-prd
description: Write a concise, measurable product requirements document for a new product, feature, or AI capability. Use when a validated product direction needs a shared contract for users, scope, outcomes, requirements, rollout, and risks.
---

# Write PRD

Translate a product decision into a product contract. Keep implementation detail proportional to the decision being made.

## Workflow

1. Gather the problem, target user, current workflow, desired outcome, evidence, constraints, and decision owner from the conversation and available artifacts.
2. Ask only for missing decisions that materially change the product, scope, or success criteria. Otherwise state assumptions and draft.
3. Inspect the existing product or repository when relevant so the PRD uses its domain language and does not propose something already present.
4. Define goals, measurable success criteria, user flow, requirements, acceptance criteria, and explicit non-goals.
5. For AI features, define the human outcome, failure modes, evaluation set, quality threshold, latency/cost boundaries, fallback, and data handling. Mark unknown targets `TBD`; do not invent numbers.
6. Define rollout, instrumentation, dependencies, risks, and unresolved product decisions.
7. Return or save the PRD where the repository already keeps product documents. Do not publish to a remote tracker unless the user asked.

## Output

```markdown
# <Product or Feature> PRD

## Executive Summary
Problem, target user, proposed outcome, and why now.

## Evidence and Current Workflow
Observed pain, existing alternatives, and source evidence.

## Goals and Success Criteria
Measurable outcomes, baselines, targets, and timeframe where known.

## Users and User Flow
Primary user, context, happy path, and important failure paths.

## Scope
In scope:
Out of scope:

## Requirements and Acceptance Criteria
Observable product behavior, ordered by priority.

## AI Requirements
Include only when applicable: evaluation, failure handling, cost/latency, privacy, fallback.

## Rollout and Instrumentation
Release stages, safeguards, events, dashboards, and decision gates.

## Dependencies and Risks
Product, design, engineering, policy, and go-to-market dependencies.

## Open Decisions
Owner and consequence of each unresolved choice.
```

## Quality Gates

- Replace vague words such as "fast", "easy", or "intuitive" with observable behavior.
- Keep product requirements separate from speculative architecture.
- Make non-goals strong enough to prevent scope creep.
- Use `$backlog-ready-spec` after the PRD when implementation readiness must be verified.
