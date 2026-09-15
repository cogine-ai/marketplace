# Upstream sources

Packaged on 2026-08-25; selectively updated on 2026-09-08. Skill directories are copied into this plugin so that
Codex and Claude Code can discover the same bundle from one Marketplace entry.

## Cogine Dev Skillset — 13 skills

- Repository: https://github.com/cogine-ai/cogine-dev-skillset
- Branch: `main`
- Pinned commit: `a823bcaef7e932a06ecd86e57d0354c4814539b2`
- License: Apache-2.0, with per-skill third-party notices where applicable

## Auto Agents — 2 skills

- Repository: https://github.com/cogine-ai/auto-agents
- Branch: `main`
- Pinned commit: `f3c21e6ddbe52d4a0c47777c5a9fec2233468fac`
- Skills: `cogine-orchestrator`, `cogine-multirepo-worker`
- Maintainer: Cogine AI

## Cogine local skills — 4 skills

- Skill: `cogine-power-gates`
- Source: Cogine-authored global Codex installation
- Snapshot date: 2026-07-18
- Skills refreshed from newer global Codex installations on 2026-07-22:
  `fix-ci`, `loop-on-ci`, and `review-and-ship`

## Matt Pocock skills — 12 skills

- Repository: https://github.com/mattpocock/skills
- Branch: `main`
- Current pinned commit: `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`
- License: MIT

`code-review`, `codebase-design`, `diagnosing-bugs`, `domain-modeling`,
`grilling`, `implement`,
`improve-codebase-architecture`, `setup-matt-pocock-skills`, and `tdd`
are synchronized from the current pinned commit. `fix-merge-conflicts` is
the same upstream workflow as `resolving-merge-conflicts`, under the plugin's
established public name.

`to-spec` and `to-tickets` remain the previously reviewed Matt-derived
local adaptations based on commit
`2ab958093e83e0ec752e6c1c5932da465bf23e0c`. They continue to prefer
`docs/agents/issue-tracker.md` when present and fall back safely when setup
has not run.

`backlog-ready-spec` is not a Matt Pocock skill: it is a Cogine-authored
adaptation from Cogine Dev Skillset, informed by GStack's `spec` workflow.
On 2026-07-29, `backlog-ready-spec` and `devex-review` selectively absorbed
current GStack checks without importing its runtime or preamble.

The machine-readable file [UPSTREAM_LOCK.json](./UPSTREAM_LOCK.json) records
the current Matt commit, upstream and packaged SHA-256 hashes for all 33 files
in the 10 current imports, and the complete adaptation whitelist.

## Frontend Design — 1 skill

- Repository: https://github.com/anthropics/claude-plugins-official
- Baseline commit: `81500db67345a66d99f8330eafff911553475217`
- Selective update: `85cce0381e7860082641b59d961a2b8c368b8b79`
- License: Apache-2.0

The update adopts typography roles, reading measure, explicit alignment,
information-led grouping, and action-responsive motion. It retains brief/brand
priority without importing blanket aesthetic bans or mandatory reconfirmation
of a supplied subject. This is an adaptation, not a byte-identical snapshot.

## Build Web Apps — 1 skill

- Repository: https://github.com/openai/plugins
- Package: `build-web-apps` version `0.1.2`
- Skill: `shadcn`
- License declared by the package: MIT

## Vercel React Best Practices — 1 skill

- Source: Vercel Engineering agent skill snapshot
- Skill: `vercel-react-best-practices`
- Snapshot version: `1.0.0` with 70 rules
- Snapshot date: 2026-07-22
- License declared by the skill: MIT

## Superpowers — 1 adapted skill

- Repository: https://github.com/obra/superpowers
- Package version: `6.1.1`
- Source skill: `using-git-worktrees`; packaged as `worktree-management`
- License: MIT

## Explicit exclusions

- The full `superpowers` workflow pack is intentionally excluded. Only its
  worktree isolation workflow is adapted as a narrowly triggered lifecycle.
- Matt's `ask-matt` router, `wayfinder`, `research`, `prototype`, and
  `triage` are intentionally excluded from this P0/P1 bundle.
- Matt's `grill-with-docs` is intentionally excluded because it is only a
  cross-skill alias for the separately bundled `grilling` and
  `domain-modeling` skills and has no independent workflow contract.
- iOS, macOS, Cloudflare, Lark, calendar, email, storage, and other
  platform/vendor companion packs are not part of the Coding Engineer core.
- Temporary, deprecated, in-progress, and one-repository-only skills are not
  included.

## Cross-platform compatibility adjustments

Invocation policy is expressed natively for both hosts:

- The 12 explicit-only workflow commands retain
  `disable-model-invocation: true` for Claude Code and set
  `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for
  Codex.
- The 18 model-invokable skills omit both controls and use the host defaults.
- Every skill has `agents/openai.yaml`.

For the 10 current Matt imports, upstream bodies and supporting files are
otherwise retained. The adaptation whitelist is limited to local namespace and
host-safety requirements plus verified functional corrections:

1. Fully qualifying operational cross-skill calls as
   `coding-engineer-skills:<skill>`.
2. Retaining the local `implement` pre-commit review against the originating
   spec and repository standards instead of chaining the fixed-point
   `code-review` workflow.
3. Scoping `code-review` discovery to committed changes since a fixed point,
   matching the diff it actually reviews.
4. Removing setup-document references to the excluded `grill-with-docs`
   alias while keeping direct `domain-modeling` routing.
5. Keeping the established `fix-merge-conflicts` folder/frontmatter name for
   upstream `resolving-merge-conflicts`.
6. Adjusting the corresponding user-facing display name.
7. Resolving `CONTEXT-MAP.md` before domain reads and writes, and preserving an
   existing multi-context setup.
8. Keeping conflict resolution recoverable, staging only verified conflict
   files, and requiring confirmation before changing Git history.
9. Correcting the GitHub triage command, dependency query, local issue path,
   and ADR zero-padding instructions so their documented contracts execute as
   written.
10. Creating architecture reports through a secure unique temporary file,
    stating their CDN requirement, HTML-escaping repository-derived content,
    and using Mermaid's strict security mode.

`local-ultra-review` is Cogine-owned and separately hardened for portable
skill-root resolution, explicit argv, honest packet-versus-execution status,
and a separate independent verifier context. `worktree-management` retains the
upstream isolation detection and native-tool-first flow, narrows automatic
triggering, makes dependency setup proportional, and adds confirmation-gated
cleanup for manually created worktrees.

## Approved selective update — 2026-09-08

- `backlog-ready-spec` adopts issue-data trust boundaries and the distinction
  between successful zero matches, successful matches, and failed lookups from
  [GStack spec](https://github.com/garrytan/gstack/blob/0530392821c277b95e5cd65aa9d9fda4248718b2/spec/SKILL.md.tmpl).
  This is a secondary upstream reference, not a wholesale GStack sync. The
  Product Manager copy remains identical; no GStack runtime is imported.
- `shadcn` replaces the Claude-only dynamic shell injection with an explicit
  project-runner command and distinguishes lookup failures from an absent
  project. Its source snapshot is otherwise retained.
- `local-ultra-review` defaults every target, including a current-repo PR URL,
  to local output. Posting requires explicit arguments reflecting user
  authorization; the existing independent execution and verification contract
  is retained.

The Matt lock and the other skill entries are unchanged. See the marketplace
[update record](../../docs/skill-updates-2026-09-08.md) for scope and validation.

## Complete upstream refresh with retained local adaptations — 2026-09-15

`to-spec` and `to-tickets` are refreshed from Matt `3cca18b368ae95cdbdebbff572ccafa662551015`. Preserve short explicit triggers, native host policies, repository tracker discovery, safe local fallback, and existing-label-only publication. The 33-file lock for the ten other Matt imports is unchanged. Worktree management was reviewed against Superpowers v6.3.0 (`b36e0829c6d0140e93cfef2ca599b1b07d4a7797`); the upstream rationalization-table rewrite does not add behavior missing from the deliberately shorter local flow. The five GStack-derived workflows were reviewed against `4a3c6a8a3cad82cfffdaa4d152e1c5ae5c4af659`: redaction, failed-evidence handling, live-vs-untested reporting and portable review already cover the applicable deltas. Provider-specific reviewer/Aside runtime changes remain outside these documented portable adaptations.

See `UPSTREAM_SYNC_2026-09-15.json` for the per-entry overlay ledger. The refresh ships as version 0.2.2 in both Codex and Claude Code manifests and the Claude marketplace catalog.
