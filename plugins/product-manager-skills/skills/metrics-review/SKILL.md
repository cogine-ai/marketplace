---
name: metrics-review
description: Review product metrics against prior periods and targets, diagnose meaningful changes, and recommend actions. Use for weekly, monthly, or quarterly reviews and investigations of spikes, drops, funnels, cohorts, or experiments.
---

# Metrics Review

Turn numbers into product decisions while preserving data and causal uncertainty.

## Workflow

1. Confirm each metric's definition, population, period, comparison, target, source, and known data-quality issues.
2. Organize metrics as a North Star, product-health indicators, and diagnostic metrics. Use acquisition, activation, engagement, retention, monetization, and satisfaction only where relevant.
3. Calculate absolute and relative changes correctly. Inspect trends, rate of change, anomalies, cohorts, and segments rather than relying on one aggregate snapshot.
4. Connect changes to launches, incidents, campaigns, seasonality, or experiments, but label correlation and hypotheses separately from demonstrated causation.
5. Prioritize a small set of investigations, experiments, investments, or alerts. Give each action an owner or next decision when context allows.

## Output

```markdown
## Metrics Review

### Summary
Overall health, most important change, and main caveat.

### Scorecard
| Metric | Current | Previous | Change | Target | Status |
|---|---:|---:|---:|---:|---|

### Findings
Material trends, segments, anomalies, and confidence.

### Bright Spots and Concerns
What to sustain and what needs attention.

### Hypotheses
Possible explanations, evidence for and against, and validation needed.

### Actions
Investigation, experiment, investment, or alert; expected decision unlocked.

### Data Caveats
Definition changes, missing data, bias, and comparability limits.
```

## Quality Gates

- Never invent missing targets, baselines, or causal explanations; mark them `TBD`.
- Avoid vanity metrics without a link to user value or a decision.
- Show denominators for rates and sample sizes when available.
- Keep the action list smaller than the finding list.
