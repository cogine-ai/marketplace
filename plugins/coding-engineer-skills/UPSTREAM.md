# Upstream sources

Packaged on 2026-08-25. Skill directories are copied into this plugin so that
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
- Pinned commit: `81500db67345a66d99f8330eafff911553475217`
- License: Apache-2.0

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
otherwise retained. The whitelist is limited to:

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

`local-ultra-review` is Cogine-owned and separately hardened for portable
skill-root resolution, explicit argv, honest packet-versus-execution status,
and a sixth independent verifier context. `worktree-management` retains the
upstream isolation detection and native-tool-first flow, narrows automatic
triggering, makes dependency setup proportional, and adds confirmation-gated
cleanup for manually created worktrees.
