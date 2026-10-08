# Platforms for Pages at Scale

Load after choosing the page playbook and data model. Start with the current
site's CMS and actual plan. Verify current vendor limits and operational cost
before proposing a migration; a partner relationship is not suitability proof.

| Requirement | What to verify |
|---|---|
| Page capacity | Actual item/row limits and headroom for the expected set |
| Data refresh | Imports/API/webhooks, validation, and how edited rows reach pages |
| Retrieval | Useful initial HTML or verified target-agent rendering capability |
| Unique utility | Conditional sections and real data per page rather than name swaps |
| Index controls | Per-page noindex/canonical, sitemaps, and exclusion of thin variants |
| Discovery | Hubs, related pages, and links queryable from the data model |
| Operations | Partial/full build times, preview, rollback, export, and ownership |

## Compare options

- Existing hosted CMS: low migration cost; check actual plan limits and template
  branching before assuming it cannot support the requested volume.
- WordPress/custom content types: editorial familiarity; verify hosting, plugins,
  import reliability, and bulk-edit performance.
- Static/hybrid generation: control over templates and unique data; engineers
  own build times, incremental regeneration, and operational maintenance.
- Headless CMS plus framework: structured editorial workflow with engineering
  ownership of templates and schema migrations.
- Other hosted or AI site builders: inspect real data, rendering, export, and
  rollback capabilities. Name alternatives and disclose a known commercial
  relationship if recommending a tool; do not default to an upstream partner.

## Decide and prove

1. Use the existing CMS when it meets the evidence-backed requirements.
2. Compare a subpath, reverse proxy, or subdomain on architecture, operations,
   ownership, and linking. Do not assert a universal ranking advantage.
3. Prove a representative first batch sized for the risk and available traffic.
   Check content correctness, crawlability, actual index observations, build and
   rollback behavior, and qualified use before scaling. Publication requires
   existing or explicit user authorization.

Use [programmatic-seo.md](programmatic-seo.md) for quality and
[seo-audit.md](seo-audit.md) for crawl/index diagnosis. No unbundled
site-architecture skill or platform-specific CLI is required.
