# Examples

Use these examples to calibrate routing. Apply their decision pattern, not their wording.

## Canonical Routes

| Request or new fact | Mode | Behavior |
|---|---|---|
| Explicit typo fix with no other changes | `fast` | Change only the target and inspect the diff. If activation was implicit, exit the protocol silently. |
| Review a prompt for blind spots; do not implement | `blind-spot-only` | Produce the blind-spot artifact and stop. |
| Implement a bounded feature in an unfamiliar, non-sensitive module | `standard` | Inspect the module, choose the relevant discovery method, commit to a bounded path, then execute. |
| Read and compare architecture across repositories | `standard` | Inspect and compare; raise the floor only if another high-risk consequence appears. |
| User requests `fast` for a production deploy | `high-risk` | Enforce the safety floor; confirm target, revision, preflight, rollback, authorization, and read-back. |
| Local reversible edge case inside an accepted plan | Existing mode | Take the conservative path, record it when notes were requested, and continue. |
| New schema semantics invalidate the accepted plan | Existing mode -> Deviation | Pause, explain the new fact and options, and obtain the material decision. |
| HTML report and quiz requested after implementation | `standard` unless another boundary raises it | Produce the requested artifact; HTML is a format, not a mode. |

Never route to undefined labels such as `review`, `research`, or `prototype` modes.

## Unknown-Heavy Design Example

Request: "Make this dashboard feel premium. I do not know what good looks like."

1. Frame the audience, decision the dashboard supports, and non-goals. Ask only if an answer changes the prototype directions.
2. Use `standard`. Treat visual taste as an unknown known.
3. Produce one HTML artifact with several meaningfully different directions using representative data; do not wire production behavior.
4. Let the user's reaction become Discovery evidence.
5. Commit only after the selected direction and production scope are clear.

The prototype is the requested work, not merely a proposal to create one.

## State Traces

```text
fast:         unframed -> verifying -> complete
standard:     unframed -> discovering -> ready-to-commit -> executing -> verifying -> transfer-ready -> complete
material drift: executing -> deviation-found -> ready-to-commit | blocked | stopped
```

Track state only for long, high-risk, blocked, or materially deviating work.

## Transfer Calibration

- Ordinary handoff: outcome, evidence, material decisions/deviations, residual risk, owner actions.
- Pitch/explainer: lead with the result or demo, then context, decisions, proof, and anticipated reviewer concerns.
- Quiz: teach the changed behavior first, then test the user's understanding of consequences and edge cases before acceptance.
