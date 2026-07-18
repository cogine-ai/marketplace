# Upstream sources

Packaged on 2026-07-18. Skill directories are copied into this plugin so that
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

## Cogine local skill — 1 skill

- Skill: `cogine-power-gates`
- Source: Cogine-authored global Codex installation
- Snapshot date: 2026-07-18

## Matt Pocock skills — 7 skills

- Repository: https://github.com/mattpocock/skills
- Branch: `main`
- Pinned commit: `9603c1cc8118d08bc1b3bf34cf714f62178dea3b`
- License: MIT

## Frontend Design — 1 skill

- Repository: https://github.com/anthropics/claude-plugins-official
- Pinned commit: `81500db67345a66d99f8330eafff911553475217`
- License: Apache-2.0

## Build Web Apps — 1 skill

- Repository: https://github.com/openai/plugins
- Package: `build-web-apps` version `0.1.2`
- Skill: `shadcn`
- License declared by the package: MIT

## Explicit exclusions

- `superpowers` is intentionally excluded because this bundle favors lower
  prompt overhead and smaller, directly triggered workflows.
- iOS, macOS, Cloudflare, Lark, calendar, email, storage, and other
  platform/vendor companion packs are not part of the Coding Engineer core.
- Temporary, deprecated, in-progress, and one-repository-only skills are not
  included.

## Cross-platform compatibility adjustments

The current Codex skill schema does not accept `disable-model-invocation` or
top-level `arguments` frontmatter. Those fields were removed from four copied
skills. All skill descriptions were normalized into shorter trigger summaries
to reduce always-on plugin token cost; manually invoked skills retain explicit
invocation wording. One `diagnosing-bugs` handoff was generalized because the
larger architecture-audit skill is intentionally outside this core bundle.
`to-spec`, `to-tickets`, and `code-review` were adjusted to discover repository
tracker conventions directly, so they do not require a separate setup skill.
No other workflow steps or reference files were changed.
