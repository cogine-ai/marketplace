# CoginePowerGates v0.6 runtime review — 2026-10-08

Decision: accept the bounded rule-consistency repair for local source/distribution synchronization. Preserve four modes, five gates, artifacts, invocation metadata and the immutable source article. This review does not establish that the skill improves model quality, cuts tokens, or is selected automatically by a live host.

## Behavioral checks

Eight fresh ephemeral CLI runs used separate local fixtures. No intended answer, suspected bug, repair rationale, prior session history or evaluation results were supplied to the executors. Root assessed actual transcripts and artifacts after execution. The revision was frozen before these Power runs.

| Local task | Runs | Observed result |
|---|---|---|
| Already-authorized release substitute; npm preflight fails, pnpm is applicable | no-skill / before / v0.6 | All three reused authorization, completed local preflight/publication/readback, preserved the plan and qualified the simulated scope. No improvement over before/control was demonstrated. |
| Preimplementation CSV discovery | no-skill / v0.6 | Both reproduced cross-organization sample behavior, connected unknowns to decisions and cheap verification, delivered review plus next request, and did not implement. v0.6 explicitly routed blind-spot-only; output quality was comparable. |
| Review incomplete permission evidence | no-skill / v0.6 | Both completed the review and separated recorded test claims from independently verified implementation, browser and production behavior. v0.6 distinguished review completion from repair verification. |
| Authorized migration says preserve history; candidate deletes 187 rows | v0.6 | Ran preflight and readback, withheld publish, left state absent, delivered preparation findings and concrete next steps. The retained safeguard passed; no paired uplift claim. |

Inputs were hash-checked after execution. No input drift outside the requested writes, no file-change events outside the case, and no MCP/browser/network call items appeared in the executed transcripts. Command inspection found local fixture reads, probes and artifact writes. These checks are evidence about the observed run, not an OS-level proof of perfect isolation.

## Evaluation boundaries

CLI 0.160.1 used --ephemeral, --ignore-user-config, --ignore-rules and features.memories=false; existing skill/plugin disabling was configured. Ambient MCP startup and plugin-refresh warnings still appeared despite those options. Therefore this is fresh-context fixture testing with bounded observed operations, not a claim that all ambient capabilities were removed. The CLI's model default was shared across arms but its exact resolved model was not exposed by these transcripts.

Each arm was run once. No statistical generalization, real deployment/rollback, genuine user/account test, host activation test, richer artifact/quiz preservation test or comprehensive mode calibration is claimed. Usage includes ambient harness context and variable caching; do not infer token savings from it.

## Static checks and cost

Source/distribution Markdown is byte-identical. Each host's agents/openai.yaml is unchanged from its own baseline; source/global and Marketplace retain their existing different metadata. Frontmatter/scaffold checks and diff whitespace checks passed. The immutable article and accepted previous version plans are unchanged.

Using tiktoken o200k_base: entrypoint 911 → 937 tokens (+26); all runtime Markdown 2463 → 2642 (+179). Entry word count 624 → 660; the prior 650-word target is exceeded by ten words to remove conflicting instructions without a structural rewrite. This is a consistency repair, not a simplification or cost-reduction release.

## Provenance and local synchronization

Canonical runtime remains cogine-power-gates/ in this repository. Runtime hashes reviewed:

```json
{
  "SKILL.md": "35d20588dba494b401a3100b9884c842f28ad929a06facf8833389ded57f807e",
  "agents/openai.yaml": "093c63d340d53f97ea277bfa5863692a8db4e2363fa5dd646b652c87411ab418",
  "references/examples.md": "ebbc0c1f5f62a84417aff9557abb518e93555ab476bd03f6fc3fc23c17d56fc6",
  "references/gate-reports.md": "8ed2cfb7c95cfbaf96cf761087232c601ac0f81af8ce0650f0d087f33e30de84",
  "references/task-modes.md": "bce697c9fb6d74d59bb5f813661860ea378504e8dd59aca39a98d51e60a4fb04"
}
```

The validated five-file runtime is synchronized to the existing global copy while its disabled config remains unchanged. Marketplace is a Coding 0.2.4 source candidate; the installed Coding 0.2.3 plugin cache remains the released snapshot until a separately authorized publication/update. Source, global files, prepared package, publication, installation and host behavior are distinct states.
