# Approved skill updates — 2026-09-08

Base: `2d977e9a1a4dcb22f12825a4b33dc8c2b6269120`. The approved scope is
17 existing entries across five plugins. The marketplace remains six plugins
and 99 entries; no proposed new skill is added.

## Upstream methods adopted

| Proposal | Existing entries | Source | Change |
| --- | --- | --- | --- |
| U01 | [product-manager-skills/ui-ux-pro-max](../plugins/product-manager-skills/skills/ui-ux-pro-max/SKILL.md) | [nextlevelbuilder/ui-ux-pro-max-skill@4aad058](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/4aad0584d92131626b16d4ff4d77f0455385013c/.claude/skills/ui-ux-pro-max/SKILL.md) | Smallest query mode, one bounded retry, exact product/stack matching, protected persistence, coherent runtime/data/reference update. |
| U02 | [growth-and-gtm-skills/search-visibility](../plugins/growth-and-gtm-skills/skills/search-visibility/SKILL.md) | [coreyhaines31/marketingskills@5b2c000](https://github.com/coreyhaines31/marketingskills/blob/5b2c0007766c6a1cf1d53fd8fc73e979e0821022/skills/seo-audit/SKILL.md) | Untrusted fetched content, repeated platform-specific sampling, format volatility, agent access, and video text layers. |
| U03 | [coding-engineer-skills/backlog-ready-spec](../plugins/coding-engineer-skills/skills/backlog-ready-spec/SKILL.md), [product-manager-skills/backlog-ready-spec](../plugins/product-manager-skills/skills/backlog-ready-spec/SKILL.md) | [garrytan/gstack@0530392](https://github.com/garrytan/gstack/blob/0530392821c277b95e5cd65aa9d9fda4248718b2/spec/SKILL.md.tmpl) | Issue data is not authorization; failed lookups cannot establish zero duplicates or unqualified readiness. |
| U04 | [growth-and-gtm-skills/customer-research](../plugins/growth-and-gtm-skills/skills/customer-research/SKILL.md) | [coreyhaines31/marketingskills@5b2c000](https://github.com/coreyhaines31/marketingskills/blob/5b2c0007766c6a1cf1d53fd8fc73e979e0821022/skills/customer-research/SKILL.md) | Primary interviews/surveys mode with disconfirming questions, recruiting drafts, and evidence-aware synthesis. |
| U05 | [growth-and-gtm-skills/content-strategy](../plugins/growth-and-gtm-skills/skills/content-strategy/SKILL.md) | [coreyhaines31/marketingskills@5b2c000](https://github.com/coreyhaines31/marketingskills/blob/5b2c0007766c6a1cf1d53fd8fc73e979e0821022/skills/content-strategy/SKILL.md) | Production formats, distribution, reuse, and maintenance planned with content. |
| U06 | [growth-and-gtm-skills/onboarding](../plugins/growth-and-gtm-skills/skills/onboarding/SKILL.md) | [coreyhaines31/marketingskills@5b2c000](https://github.com/coreyhaines31/marketingskills/blob/5b2c0007766c6a1cf1d53fd8fc73e979e0821022/skills/onboarding/SKILL.md) | Activation-model choice and inventory/remove/reconstruct minimum path to value. |
| U07 | [growth-and-gtm-skills/pricing](../plugins/growth-and-gtm-skills/skills/pricing/SKILL.md) | [coreyhaines31/marketingskills@5b2c000](https://github.com/coreyhaines31/marketingskills/blob/5b2c0007766c6a1cf1d53fd8fc73e979e0821022/skills/pricing/SKILL.md) | First-price hypothesis, eight charging models, and staged rollout preserving existing commitments. |
| U08 | [coding-engineer-skills/frontend-design](../plugins/coding-engineer-skills/skills/frontend-design/SKILL.md) | [anthropics/claude-plugins-official@85cce03](https://github.com/anthropics/claude-plugins-official/blob/85cce0381e7860082641b59d961a2b8c368b8b79/plugins/frontend-design/skills/frontend-design/SKILL.md) | Typography roles, reading measure, alignment, meaningful grouping, and action-responsive motion. |
| U09 | [growth-and-gtm-skills/copywriting](../plugins/growth-and-gtm-skills/skills/copywriting/SKILL.md) | [coreyhaines31/marketingskills@5b2c000](https://github.com/coreyhaines31/marketingskills/blob/5b2c0007766c6a1cf1d53fd8fc73e979e0821022/skills/copywriting/SKILL.md) | Small hero-copy checks for ability, problem-to-action logic, and audience interpretation. |
| U10 | [growth-and-gtm-skills/free-tools](../plugins/growth-and-gtm-skills/skills/free-tools/SKILL.md) | [coreyhaines31/marketingskills@5b2c000](https://github.com/coreyhaines31/marketingskills/blob/5b2c0007766c6a1cf1d53fd8fc73e979e0821022/skills/free-tools/SKILL.md) | Input/API maintenance risk and useful product continuation within the existing scorecard. |
| U11 | [growth-and-gtm-skills/launch](../plugins/growth-and-gtm-skills/skills/launch/SKILL.md) | [coreyhaines31/marketingskills@5b2c000](https://github.com/coreyhaines31/marketingskills/blob/5b2c0007766c6a1cf1d53fd8fc73e979e0821022/skills/launch/SKILL.md) | Simple, Lovable, Complete check within the accepted launch scope. |

## Confirmed local corrections

| Proposal | Existing entries | Correction |
| --- | --- | --- |
| F01 | Coding `shadcn` | Run the project-context command explicitly; distinguish lookup failure from a project requiring initialization. |
| F02 | Design `pick-ui-library`, Design `prototype`, PM `ui-ux-pro-max` | Make Claude Code and existing Codex explicit-only invocation policies agree. |
| F03 | Coding `local-ultra-review` | Every target defaults to local output. Posting requires explicit user-authorized mode; independent verification remains required. |
| F04 | Sales `pipeline-review` | Review reads and drafts by default; authorized writes require record/task readback. |

U01 and F02 touch the same UI UX Pro Max entry. U03 touches two copies of
the same skill. Deduplicating all targets gives exactly 17 entries.

## Packaging and retained adaptations

| Plugin | Prepared version |
| --- | --- |
| `coding-engineer-skills` | `0.2.1` |
| `design-engineer-skills` | `0.1.2` |
| `product-manager-skills` | `0.2.1` |
| `growth-and-gtm-skills` | `0.1.3` |
| `sales-skills` | `0.1.1` |

The Founder/CEO plugin remains `0.1.1`. Both host manifests and the Claude
catalog agree. These are source-package versions; preparing them does not
publish the marketplace or change installed caches.

- UI UX Pro Max runtime/data/references match its fixed source snapshot except 46 added blank-line trailing spaces removed from `design_system.py` for diff validation; its executable AST is unchanged and only docstring whitespace differs. The entry keeps absolute skill-root resolution and an explicit project output directory. Ten portable upstream test modules are copied; the script-path test is adapted to the installed layout. Catalog-refresh, catalog-generation line-ending, and relevance-evaluator tests depend on unshipped upstream repository tools and are excluded.
- Growth references selectively adapt the approved methods. New vendor percentages, mandatory sample sizes/incentives, universal trial windows, default price bands, and automatic revocation of customer commitments are not imported.
- Customer Research evals 12 and 13 are adapted from the fixed upstream snapshot to those local constraints. They are prompt-evaluation cases, not an automated runtime test suite.
- The 33-file Matt upstream lock remains unchanged. The two `backlog-ready-spec` files remain identical. `cogine-power-gates` remains in Coding Engineer Skills.
- New-skill candidates remain proposals only: `animate`, `contract-first`, `docs-sync-audit`, `test-gap-audit`, `events`, and `mcp-release-qa`.

## Validation

Run from the marketplace root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s plugins/coding-engineer-skills/tests
PYTHONDONTWRITEBYTECODE=1 python3 plugins/coding-engineer-skills/scripts/validate_bundle.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s plugins/coding-engineer-skills/skills/local-ultra-review/tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s plugins/product-manager-skills/skills/ui-ux-pro-max/scripts/tests
PYTHONDONTWRITEBYTECODE=1 python3 plugins/product-manager-skills/skills/ui-ux-pro-max/scripts/validate_data.py
git diff --check
```

The Coding bundle checks require PyYAML. The review and UI runtime tests use
the Python standard library. Prompt evaluations and real host-trigger/CRM/
GitHub publication flows are separate from these local checks.
