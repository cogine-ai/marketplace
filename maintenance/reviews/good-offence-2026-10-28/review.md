# Good Offence: forward evaluation receipt

The first frozen policy produced a behavioral false positive. After a focused policy revision, the same five cases had the intended decisions and mechanisms, but the runner rejected the revised response for violating its strict schema. **Neither run is an unqualified end-to-end pass.**

| Frozen policy | Model session | Behavioral result | Strict schema |
| --- | --- | --- | --- |
| v1, `c41abe8bbc8e32f89c056244b4c05cb01ce2473431c74ef2fbe543e4c67a3a66` | `ses_e7e4ab216ffeFMYdfhE8pLu2l9` | 4/5 | Pass |
| v2, `d6970d4db1159429d728233813b0c039a19dc6f9ef97c759169147cedfeaae78` | `ses_e7e41eff3ffePZSvNEtD3Q168S` | 5/5 intended decisions/mechanisms, with one narrative error | **Fail; rejected** |

Both used local OpenCode CLI with requested model `zhipuai-coding-plan/glm-5.3-flash`, classifier access, a 600-second timeout, and one model invocation per frozen policy. Recorded durations were 403.155 and 240.316 seconds. The provider-side model identity was not independently verified. There was no third invocation or post-failure schema relaxation.

Each prompt included the canonical skill, its required premise/defensive/principles context, and five complete synthetic code changes with neutral case IDs. Expected answers were separate from model input. A separate fresh-context Codex agent received only the policy, references and neutral inputs, with no parent history or expected answers. Its five decisions matched the held-out expected results. This was on frozen policy v1; a later static review also confirmed the v2 contract rule. The revised-policy run reused known fixtures and is a regression check, not a new holdout evaluation. A local preflight invocation failed before any model call because of a relative schema path; it was preserved and corrected without changing the prompt.

## Decisions and evidence

| Case | Intended result | v1 | v2 | Evidence inspected |
| --- | --- | --- | --- | --- |
| case-01 | Report duplicate validation | Correct | Correct, narrative error noted below | `catalog.py:build_record`: the sole outer caller validates the exact builtin immutable string; the inner identical nonblank guard is unreachable. Remove only that inner guard. |
| case-02 | Withhold orphan UI cleanup | Correct | Correct | Functional progress state and handlers remain out of scope after losing callers. An incidental Array.isArray fallback does not justify deleting the whole feature. |
| case-03 | Retain authorization layers | **Incorrect finding** | Correctly withheld | Removing the preparse guard changes the reviewed head's denied malformed request from 403/plain to 400/JSON, and a denied valid request from 403/plain to 403/JSON. Independent awaited authorization reads do not share a snapshot. |
| case-04 | Retain real I/O recovery | Correct | Correct | The bounded, narrow retry has a named transient remote failure, an actual third-attempt recovery, no other retry layer, and final exception propagation. |
| case-05 | Report sentinel cascade | Correct | Correct | Jointly remove the catch-to-empty sentinel in `items.py:load_items` and the compensating rethrow in `render_items`. Keep the nonempty source guarantee and fixed HTTP503 response. |

Decision and source-location scores were checked automatically, then each mechanism, caller premise, proposed deletion, and preservation claim was inspected against the raw source. The scores do not stand in for that semantic inspection.

The v1 case-03 false positive was substantive: the model acknowledged the changed error order and response shape, then treated absence of an explicit requirement and the base implementation's behavior as permission to discard the reviewed head's behavior. The narrow v2 revision makes the reviewed head the equivalence baseline and rejects that inference. In v2 the model explicitly used those observable differences to withhold the finding, also rejecting deletion of the inner check because it changes which independent authorization snapshot is consulted.

V2 case-01 inaccurately states that a missing `name` raises ValueError. The source actually raises KeyError at `payload["name"]` before either guard. This does not invalidate deletion of the unreachable inner guard; it is still a preservation-description error and prevents claiming flawless reasoning.

## Protocol failure and containment

V2 added `preserved_behavior_note: null` to the case-01 finding, although the schema disallows additional properties. The adapter exited nonzero and returned no accepted result. The complete original text and events were preserved, and the JSON was extracted offline for semantic assessment **without removing or repairing that invalid field**. This observes rejection on a schema violation; it does not make the run a protocol pass or establish every publication gate end to end.

V2 also attempted one builtin `skill` lookup for `good-offence`; it failed with `Unable to load skill good-offence` and recorded `executed: false`. The model then used the full policy already supplied inline and completed all cases. No repository/GitHub tools, edits, or publication were used. The first run had no tool calls.

## Packaging and limits

Independent packaging checks passed for both policies: one SKILL.md entrypoint; consistent `good-offence` name and invocation metadata; six pinned upstream source/license files matching their recorded Git blobs; valid relative principles links; license and NOTICE present; neutral fixtures separated from expected answers; no source symlinks, machine-specific paths, runtime database/log artifacts, or nested upstream skill entrypoint.

This is a small repeated synthetic suite, not a measured production false-positive rate. No actual Claude-host behavior, marketplace installation, live-repository review, runtime verifier end-to-end publication gate, or GitHub output was tested by this evaluation. No broad cross-host or deployment safety claim follows. The accompanying JSON receipt records prompt, policy, raw-input, and evidence hashes. Full original artifacts are retained by the maintainer; this curated report contains no production review material or local absolute paths.
