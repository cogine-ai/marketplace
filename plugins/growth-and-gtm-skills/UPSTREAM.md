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

### Selective update — 2026-09-08

The base snapshot above remains the source for unchanged material. Eight
existing entries selectively absorb methods from commit
[`5b2c0007766c6a1cf1d53fd8fc73e979e0821022`](https://github.com/coreyhaines31/marketingskills/tree/5b2c0007766c6a1cf1d53fd8fc73e979e0821022/skills):

| Packaged skill | Source method adopted |
| --- | --- |
| `search-visibility` | `seo-audit` fetched-content trust; `ai-seo` repeated sampling, format volatility, access/discovery/parseability, and video text layers |
| `customer-research` | Primary interviews/surveys mode and a scoped playbook; adapted upstream evals 12 and 13 |
| `content-strategy` | Production format, distribution, reuse, and maintenance planning |
| `onboarding` | Activation-model selection and inventory/remove/reconstruct minimum path to value |
| `pricing` | First-price learning hypothesis, eight charging models, and staged rollout |
| `copywriting` | “Now you can”, Human Action Model, and audience perception checks |
| `free-tools` | Input/API/security maintenance risk and product continuation checks |
| `launch` | Simple, Lovable, Complete readiness within the accepted scope |

The added references are adaptations of methods, not complete upstream copies.
Fixed uplift figures, platform format rankings, mandatory incentive/sample
sizes, universal activation windows, default price bands, and automatic changes
to existing customer commitments are not imported. `programmatic-seo` and the
other entries retain their reviewed snapshot. No new skills are added.

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

## Complete upstream refresh with retained local adaptations — 2026-09-15

Eight entries now include the applicable complete upstream support files and evaluation cases from `5b2c0007766c6a1cf1d53fd8fc73e979e0821022`: search-visibility, customer-research, content-strategy, onboarding, pricing, copywriting, free-tools, and launch. The merged search router, concise method references documented on September 8, bundled skill/tool alternatives, contextual research samples/incentives, truthful progress, product-specific observation windows, and customer commitments are preserved. Fixed vendor uplift/format rankings and generic price bands remain excluded. Source-specific search evals use separate directories. Existing customer-research cases 12/13 remain; new cases conflicting with these established constraints are adapted. The other entries retain their earlier source snapshot.

See `UPSTREAM_SYNC_2026-09-15.json` for the per-entry overlay ledger. The refresh ships as version 0.1.4 in both Codex and Claude Code manifests and the Claude marketplace catalog.
