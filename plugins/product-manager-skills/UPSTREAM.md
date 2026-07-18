# Upstream sources

Packaged on 2026-07-19. Skill directories are copied or adapted into this
plugin so Codex and Claude Code can discover the same bundle.

## Cogine Dev Skillset — 2 skills

- Repository: https://github.com/cogine-ai/cogine-dev-skillset
- Branch: `main`
- Pinned commit: `a823bcaef7e932a06ecd86e57d0354c4814539b2`
- Skills: `founder-office-hours`, `backlog-ready-spec`
- License: Apache-2.0

## Matt Pocock skills — 5 skills

- Repository: https://github.com/mattpocock/skills
- Branch: `main`
- Pinned commit: `9603c1cc8118d08bc1b3bf34cf714f62178dea3b`
- Skills: `grilling`, `grill-me`, `prototype`, `to-spec`, `to-tickets`
- License: MIT

## Anthropic Knowledge Work Plugins — 4 adapted skills

- Repository: https://github.com/anthropics/knowledge-work-plugins
- Branch: `main`
- Pinned commit: `74d516ad8d4026b314bb1c0ee47f4516104c32cc`
- Skills: `synthesize-research`, `competitive-brief`, `roadmap-update`,
  `metrics-review`
- License: Apache-2.0

## GitHub Awesome Copilot — 1 adapted skill

- Repository: https://github.com/github/awesome-copilot
- Branch: `main`
- Pinned commit: `26fe2d126bf79aafb38f43344d450b69632200f8`
- Source skill: `prd`; packaged as `write-prd`
- License: MIT

## Interface Design — 1 skill

- Repository: https://github.com/Dammyjay93/interface-design
- Branch: `main`
- Pinned commit: `2f9be3206855bcb2d1d0af262c8bae25cba6658d`
- License: MIT

## UI UX Pro Max — 1 skill

- Repository: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- Branch: `main`
- Pinned commit: `f8ac5e1266dba8354ea96e19994d9f4345e7ec31`
- License: MIT

## Cross-platform compatibility adjustments

Unsupported frontmatter and Claude-only command syntax were removed. Matt
Pocock's tracker-aware skills reuse Cogine's portable adaptations. The four
Anthropic workflows and GitHub PRD workflow were condensed and made
connector-independent. `prototype` gained four concise design gates and a
standalone HTML fallback. `ui-ux-pro-max` resolves its own skill directory
instead of relying on `CLAUDE_PLUGIN_ROOT`, and Codex treats it as explicit-only.
