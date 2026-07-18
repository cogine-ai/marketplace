# Gate Reports

Use an output contract only when a gate interrupts, validation is incomplete, or the user requested a blind-spot artifact. Passed gates stay silent.

## Decision Or Deviation

Use for a material Frame, Discovery, Commit, or Deviation decision:

```markdown
**Gate:** Frame | Discovery | Commit | Deviation
**Reason:** The material issue or new fact.
**Options:** Only viable choices and their trade-offs.
**Recommendation:** The preferred bounded path and why.
**Need:** The exact decision, authorization, or input required.
```

Do not ask for confirmation when the choice is local, reversible, in scope, and cannot change material semantics, risk, remote/live state, or validation.

## Evidence Status

Map claims to evidence rather than listing unrelated commands:

```markdown
**Evidence Gate**
| Material claim | Direct evidence | Status |
|---|---|---|
| ... | test, diff, screenshot, live read-back, CI, log, or artifact | proven / missing |

**Missing validation:**
**Residual risk:**
**Completion:** complete | implemented but not fully verified | blocked on validation | not complete
```

One passing check does not prove an unrelated claim. UI rendering needs visual/browser evidence; remote-state changes need live read-back or equivalent provider evidence.

## Blind-Spot Artifact

```markdown
**Current map:** What the user supplied and their stated starting point.
**Material unknown unknowns:** Risks or possibilities they may not know to ask about.
**Questions that change the path:** Prioritized, not exhaustive.
**References or prototypes:** The cheapest evidence that would reduce uncertainty.
**Better next prompt:** A bounded request using what was learned.
```

Stop after the artifact unless the user explicitly expands the scope.
