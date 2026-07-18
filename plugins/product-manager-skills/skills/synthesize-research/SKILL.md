---
name: synthesize-research
description: Synthesize interviews, surveys, support feedback, usability notes, and product data into evidence-backed findings, opportunity areas, and recommendations. Use when raw research must inform a product decision or roadmap.
---

# Synthesize Research

Turn mixed research inputs into decisions without overstating the evidence.

## Workflow

1. Define the research question and decision the synthesis should inform. Use the supplied material; ask only for missing context that changes the analysis.
2. Extract observations by source: behavior, pain point, workaround, positive signal, segment, and any provided quote. Keep observed behavior separate from stated preference.
3. Cluster observations into themes. Count distinct participants or sources, not repeated mentions from one source.
4. Rate each theme by frequency, impact, and confidence. Note contradictions, outliers, missing segments, and sample limitations.
5. Triangulate qualitative and quantitative evidence when both exist. If sources disagree, show the disagreement instead of forcing consensus.
6. Tie each recommendation to findings and identify what still needs validation.

## Output

```markdown
## Research Synthesis

### Research Overview
Question, inputs, sample, timeframe, and limitations.

### Key Findings
| Finding | Evidence | Frequency | Impact | Confidence |
|---|---|---:|---|---|

### Segments
Only evidence-supported differences in needs or behavior.

### Opportunity Areas
Prioritized unmet needs, not feature requests copied verbatim.

### Recommendations
Actions linked to specific findings, with expected learning or outcome.

### Open Questions
Evidence gaps and the smallest follow-up research needed.
```

## Quality Gates

- Attribute claims to supplied sources; never invent quotes, counts, or participant traits.
- Label inference separately from evidence.
- Prefer high-impact findings over long theme lists.
- Redact personal or sensitive data from the synthesis.
