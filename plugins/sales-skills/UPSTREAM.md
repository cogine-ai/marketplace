# Upstream sources

Packaged on 2026-07-19. Skill directories are copied or adapted into this
plugin so Codex and Claude Code can discover the same bundle.

## Lenny skills by Refound AI — 4 skills

- Repository: https://github.com/RefoundAI/lenny-skills
- Branch: main
- Pinned commit: 13598cc54e09399bc1bc1398b0fca284110efb2f
- Skills: founder-sales, first-b2b-customers, enterprise-sales-motion,
  plg-sales-integration
- License: MIT

## Corey Haines marketing skills — 3 adapted skills

- Repository: https://github.com/coreyhaines31/marketingskills
- Branch: main
- Pinned commit: 67264763cb107d61749f418d081c56e5bcbc0209
- Skills: prospecting, cold-email, sales-enablement
- License: MIT

The prospecting demand-signal reference retains Corey's attribution to
https://github.com/Kappaemme-git/codex-first-customer-finder-skill under MIT.

## Anthropic Knowledge Work Plugins — 4 workflows

- Repository: https://github.com/anthropics/knowledge-work-plugins
- Branch: main
- Pinned commit: 74d516ad8d4026b314bb1c0ee47f4516104c32cc
- Copied skills: account-research, call-prep, pipeline-review
- Adapted source: call-summary, packaged as call-review
- License: Apache-2.0

## GitHub Awesome Copilot — 1 adapted skill

- Repository: https://github.com/github/awesome-copilot
- Branch: main
- Pinned commit: 26fe2d126bf79aafb38f43344d450b69632200f8
- Source skill: gtm-enterprise-account-planning
- Packaged as: enterprise-account-planning
- License: MIT

## Cross-platform compatibility adjustments

Nonstandard frontmatter and Claude-only command syntax were removed.
References to unbundled tool registries were replaced with portable guidance,
and all external integrations remain optional. call-review keeps the concise
summary and customer follow-up while adding an evidence-based, stage-aware
coaching mode. enterprise-account-planning retains the stakeholder, MEDDPICC,
mutual-action-plan, and stage-gate core without the upstream's long narrative.
