# Skill updates — 2026-09-15

Refresh upstream content while retaining the documented Cogine adaptations.
The Codex and Claude Code manifests share the same release versions and skill
directories, replacing the temporary local Codex build suffixes.

| Plugin | Version | Changes |
| --- | --- | --- |
| Coding Engineer | 0.2.2 | Refresh `to-spec` and `to-tickets` from Matt Pocock; preserve tracker discovery, local fallback, labels, and invocation policy. PowerGates reuses authorization already granted in the current session. |
| Design Engineer | 0.1.3 | Synchronize the seven changed Emil Kowalski skill bodies; preserve the existing host metadata and invocation policy. |
| Product Manager | 0.2.2 | Apply the same Matt Pocock spec and ticket updates with the existing product-plugin adaptations. |
| Growth and GTM | 0.1.4 | Complete eight upstream refreshes, including missing evaluations and a tool benchmark reference. Preserve concise triggers, bundled routes, contextual sampling and pricing, and existing customer commitments. |
| Founder and CEO | 0.1.2 | Let `startup-finance` answer a single metric directly; use full scenarios when the requested decision needs them. |

## Source and local differences

The four upstream-derived plugin updates record their source commits and each
retained adaptation in `plugins/*/UPSTREAM_SYNC_2026-09-15.json`. Unmodified
sources retain their prior attribution and license files. The Founder/CEO
change is a small edit to Cogine-authored material.

The refresh does not import unrelated new skills or undo the simplifications
approved on September 8. Growth evaluations are imported as evaluation
fixtures; their presence does not claim an LLM behavior evaluation was run.

## Validation

- Coding bundle checks cover its 30 skills, cross-skill routing, invocation
  policies, synchronized manifests, and 33 upstream-locked files.
- Bundle contract tests cover the supported Codex and Claude layouts.
- Release checks verify all plugin manifests, catalog versions, evaluation JSON,
  and the installed copies of the four previously installed plugins.
- Generic OpenAI validators reject several existing upstream or Claude-specific
  frontmatter fields. Those fields remain intact; the baseline mismatches are
  tracked separately from the bundle and release checks.

Individual global skill installations and CLI updates are recorded separately
in the local maintenance report. This release does not automatically install
the Founder/CEO plugin for users who have not selected it.
