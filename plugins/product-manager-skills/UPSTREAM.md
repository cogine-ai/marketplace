# Upstream sources

Packaged on 2026-07-19 and selectively updated on 2026-09-08. Skill directories are copied
or adapted into this plugin so Codex and Claude Code can discover the same
bundle.

## Cogine Dev Skillset — 2 skills

- Repository: https://github.com/cogine-ai/cogine-dev-skillset
- Branch: `main`
- Pinned commit: `a823bcaef7e932a06ecd86e57d0354c4814539b2`
- Skills: `founder-office-hours`, `backlog-ready-spec`
- License: Apache-2.0

`backlog-ready-spec` is a Cogine-authored adaptation informed by GStack's
`spec` workflow; it is not derived from Matt Pocock's `to-spec`.
On 2026-07-29, `founder-office-hours` and `backlog-ready-spec` selectively
absorbed current GStack checks without importing its runtime or preamble.

## Matt Pocock skills — 4 skills

- Repository: https://github.com/mattpocock/skills
- Branch: `main`
- Pinned commit: `6654f6b60cd9d5be8b54c6fafe44346dabeb3b76`
- Skills: `grilling`, `prototype`, `to-spec`, `to-tickets`
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
- Pinned commit: `4aad0584d92131626b16d4ff4d77f0455385013c`
- Previous snapshot: `f8ac5e1266dba8354ea96e19994d9f4345e7ec31`
- License: MIT

The runtime, data, and two reference files match the pinned
`.claude/skills/ui-ux-pro-max` snapshot, except 46 added blank-line trailing
spaces removed from `design_system.py` for diff validation (no executable AST
change; only docstring whitespace differs). The entry retains absolute skill-root
resolution and an explicit project output directory, and is explicit-only in
both hosts. Ten portable upstream test modules are included; the script-path
test is adapted to this package's layout. Upstream repository-maintenance tests
for catalog refresh, catalog generation line endings, and the relevance
evaluator depend on unshipped root tools and are not included. No sibling
design skills or CLI asset-mirroring machinery is imported.

## Lenny skills by Refound AI — 2 skills

- Repository: https://github.com/RefoundAI/lenny-skills
- Branch: `main`
- Pinned commit: `13598cc54e09399bc1bc1398b0fca284110efb2f`
- Skills: `defining-product-strategy`, `product-taste`
- License: MIT

## Cross-platform compatibility adjustments

Matt Pocock's `grilling` skill and Codex metadata match the pinned upstream
snapshot exactly. The redundant `grill-me` alias is intentionally omitted.
Matt Pocock's tracker-aware skills reuse Cogine's portable adaptations;
`to-spec` and `to-tickets` are explicit-only in both Claude Code and Codex.
The four Anthropic workflows and GitHub PRD workflow were condensed and made
connector-independent. `prototype` gained four concise design gates and a
standalone HTML fallback. `ui-ux-pro-max` resolves its own skill directory
instead of relying on `CLAUDE_PLUGIN_ROOT`, and both hosts treat it as explicit-only.
The two Lenny skills retain their full evidence references as on-demand
material. The current `to-tickets` snapshot omits its former final `/implement`
handoff sentence.

On 2026-09-08, `backlog-ready-spec` selectively adopted issue-data trust and
failed-query handling from
[GStack spec](https://github.com/garrytan/gstack/blob/0530392821c277b95e5cd65aa9d9fda4248718b2/spec/SKILL.md.tmpl).
It remains byte-identical to the Coding Engineer copy and retains Preserve,
required sequencing, conditional rollback, and local-spec output. No GStack
runtime or automatic issue creation is imported.
