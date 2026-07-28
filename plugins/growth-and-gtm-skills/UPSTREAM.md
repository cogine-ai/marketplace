# Upstream sources

Packaged on 2026-07-19. Skill directories are copied or adapted into this
plugin so Codex and Claude Code can discover the same bundle.

## Corey Haines marketing skills — 15 packaged skills

- Repository: https://github.com/coreyhaines31/marketingskills
- Branch: main
- Pinned commit: 7868cb9251fad80a73d26e488a5ad5f6c4a9f335
- Copied skills: product-marketing, customer-research, competitors, pricing,
  launch, content-strategy, copywriting, free-tools, cro, onboarding,
  churn-prevention, analytics, marketing-loops
- Adapted skills: search-visibility from seo-audit, ai-seo, and
  programmatic-seo; growth-experiments from ab-testing
- License: MIT

## Lenny skills by Refound AI — 3 skills

- Repository: https://github.com/RefoundAI/lenny-skills
- Branch: main
- Pinned commit: 13598cc54e09399bc1bc1398b0fca284110efb2f
- Skills: growth-model, acquisition-channels, plg-sales-integration
- License: MIT

## David Turner product skills — experiment safeguards

- Repository: https://github.com/wdavidturner/product-skills
- Branch: main
- Pinned commit: 103d6540d3c71610a3132917897746070a03bb0c
- Source skill: trustworthy-experiments
- Packaged into: growth-experiments references and deterministic sample-size
  and SRM scripts
- License: MIT

## Cross-platform compatibility adjustments

Version-only frontmatter was removed and trigger summaries were shortened.
References to unbundled skills were mapped to the focused plugin set.
Tool-registry links and hard connector assumptions were removed.
marketing-loops now describes both Codex and Claude Code scheduling.
search-visibility routes to on-demand source references, and
growth-experiments adds validity checks before outcome interpretation.
plg-sales-integration is deliberately shared with Sales Skills at the
cross-functional PQL and sales-assist boundary. `pricing` 2.1.0 is adapted to
route AI-readability checks through the bundled `search-visibility` skill and
direct `Product`/`Offer` JSON-LD guidance instead of unbundled skills.
