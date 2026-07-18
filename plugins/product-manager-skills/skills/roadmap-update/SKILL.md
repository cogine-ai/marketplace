---
name: roadmap-update
description: Create, update, or reprioritize a product roadmap with explicit tradeoffs, dependencies, risks, and change history. Use when priorities, scope, status, or timing must change after new information.
---

# Roadmap Update

Keep the roadmap bounded and make every priority change visible.

## Workflow

1. Read the current roadmap and the strategy, customer evidence, commitments, capacity, dependencies, and recent changes that constrain it.
2. Identify the operation: add, remove, change status, reprioritize, move timing, or create a roadmap.
3. For every addition or acceleration, state what moves, shrinks, or stops. Do not silently expand capacity.
4. Prefer `Now / Next / Later` unless dates are genuine commitments. Never turn uncertain work into precise dates.
5. Map owners, blocking dependencies, risks, and confidence. Use a scoring framework only when its inputs are real; do not fabricate scores.
6. Produce the revised roadmap plus a before/after change log and implications for stakeholders.

## Output

```markdown
## Roadmap Update

### Decision
What changed and why.

### Roadmap
| Horizon | Initiative | Outcome | Status | Owner | Dependencies | Confidence |
|---|---|---|---|---|---|---|

### Tradeoffs
Added or accelerated:
Moved, reduced, or removed:

### Risks and Dependencies
Blocked, at risk, hard commitments, and mitigations.

### Changes This Update
Before → after, with the evidence or decision behind each change.

### Open Decisions
Only choices that materially affect priority, scope, or timing.
```

## Quality Gates

- Express initiatives as user or business outcomes, not feature inventories.
- Consolidate duplicates into one roadmap item.
- Distinguish commitment, plan, and directional intent.
- Preserve prior decisions unless new evidence justifies changing them.
