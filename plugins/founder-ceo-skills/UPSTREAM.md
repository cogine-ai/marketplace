# Upstream sources

Packaged on 2026-07-19. Skill directories are copied or adapted into this
plugin so Codex and Claude Code can discover the same bundle.

## Cogine Dev Skillset — 2 skills

- Repository: https://github.com/cogine-ai/cogine-dev-skillset
- Branch: main
- Pinned commit: a823bcaef7e932a06ecd86e57d0354c4814539b2
- Skills: founder-office-hours, planmode-ceo
- License: Apache-2.0

## Lenny skills by Refound AI — 8 skills

- Repository: https://github.com/RefoundAI/lenny-skills
- Branch: main
- Pinned commit: 13598cc54e09399bc1bc1398b0fca284110efb2f
- Skills: high-stakes-decisions, competitive-strategy, planning-cadence,
  org-design, founding-exec-team, leading-org-change, fundraising,
  measuring-pmf
- License: MIT

## Anthropic Knowledge Work Plugins — 1 skill

- Repository: https://github.com/anthropics/knowledge-work-plugins
- Branch: main
- Pinned commit: 74d516ad8d4026b314bb1c0ee47f4516104c32cc
- Skill: risk-assessment
- License: Apache-2.0

## GitHub Awesome Copilot — 1 skill

- Repository: https://github.com/github/awesome-copilot
- Branch: main
- Pinned commit: 26fe2d126bf79aafb38f43344d450b69632200f8
- Skill: gtm-board-and-investor-communication
- License: MIT

## Everything Claude Code — 1 skill

- Repository: https://github.com/affaan-m/ECC
- Branch: main
- Reference commit: 754b8dd76ca885b764ec22f476664377aa46b6cd
- Skill: investor-materials
- License: MIT

The installed snapshot was normalized to the current supported placement of
its `origin` metadata; the skill body matches this reference commit.

## Claude Code Templates — 1 adapted skill

- Repository: https://github.com/davila7/claude-code-templates
- Branch: main
- Pinned commit: e4efa5367903f06d8be0320b88a95c1224b87f7e
- Skill: ceo-advisor
- License: MIT

Only the activation description was narrowed so this large generalist skill
loads after an explicit request for comprehensive CEO advice.

## David Turner Product Skills — 1 skill

- Repository: https://github.com/wdavidturner/product-skills
- Branch: main
- Pinned commit: 103d6540d3c71610a3132917897746070a03bb0c
- Skill: seven-powers
- License: MIT

## Cogine-authored — 1 skill

- Skill: startup-finance
- License: Apache-2.0

This compact, tool-neutral workflow was added for burn, runway, financial
scenarios, unit economics, hiring, and fundraising tradeoffs.

## Cross-platform compatibility adjustments

`planmode-ceo` remains byte-for-byte identical to its source.
`investor-materials` only moves its origin marker into supported metadata,
and `ceo-advisor` only narrows its activation description. Other imported
content is preserved with line endings and trailing whitespace normalized.
