# Changelog

## 0.6.0 - 2026-07-19

- Add the cross-platform `founder-ceo-skills` plugin with 16 focused
  workflows for founder judgment, PMF, strategy, planning, organization,
  finance, fundraising, and board communication.
- Add `measuring-pmf`, `seven-powers`, and a compact, tool-neutral
  `startup-finance` skill for burn, runway, scenarios, and unit economics.
- Keep `planmode-ceo` unchanged and reserve the broad `ceo-advisor` skill
  for explicit requests for comprehensive CEO advice.
- Route `ceo-advisor` financial analysis to the smaller
  `startup-finance` skill instead of bundling a duplicate upstream model.

## 0.5.0 - 2026-07-19

- Add the cross-platform `sales-skills` plugin with 12 focused workflows for
  founder-led sales, first customers, prospecting, outreach, calls, enablement,
  enterprise execution, pipeline review, and PLG sales assist.
- Replace a basic post-call summary with a compact `call-review` workflow that
  preserves follow-up output and adds evidence-based coaching on request.
- Add `enterprise-account-planning` for stakeholder maps, MEDDPICC, stage
  gates, and mutual action plans without importing the long upstream narrative.
- Expand `growth-and-gtm-skills` from 17 to 18 skills by intentionally sharing
  `plg-sales-integration` across the Growth and Sales role bundles.

## 0.4.1 - 2026-07-19

- Expand `product-manager-skills` from 14 to 16 skills with Lenny's
  `defining-product-strategy` and `product-taste`.
- Keep both skills' sourced insight and framework references available on
  demand without adding more overlapping PRD or roadmap workflows.

## 0.4.0 - 2026-07-19

- Add the cross-platform `growth-and-gtm-skills` plugin with 17 focused
  strategy, channel, acquisition, conversion, retention, measurement, and
  recurring-execution skills.
- Add Lenny's `growth-model` and `acquisition-channels` skills with their
  full on-demand evidence references.
- Consolidate traditional SEO, AI discovery, and programmatic search behind
  `search-visibility`, and harden `growth-experiments` with sample-size,
  SRM, pre-registration, and suspicious-result safeguards.

## 0.3.0 - 2026-07-19

- Add the cross-platform `product-manager-skills` plugin with 14 focused
  product discovery, research, PRD, prototype, roadmap, metrics, design, spec,
  and ticketing skills.
- Add current `interface-design` and `ui-ux-pro-max` snapshots, keeping the
  larger design database explicit-only to limit routine prompt overhead.
- Condense product-management workflows into portable, connector-independent
  skills for Codex and Claude Code.

## 0.2.3 - 2026-07-18

- Let `tdd` apply to suitable feature work without an explicit test-first request.
- Add three concise red/green safeguards without importing Superpowers.

## 0.2.2 - 2026-07-18

- Remove Matt Pocock's `code-review` skill from `coding-engineer-skills`.
- Make `implement` perform a focused final self-review without depending on a
  separate review skill.

## 0.2.1 - 2026-07-18

- Remove `setup-matt-pocock-skills` from `coding-engineer-skills`.
- Make `to-spec`, `to-tickets`, and `code-review` discover repository tracker
  conventions without a separate setup step.

## 0.2.0 - 2026-07-18

- Add the cross-platform `coding-engineer-skills` plugin with 26 skills.
- Prioritize Cogine workflows and Matt Pocock's lightweight engineering chain.
- Include frontend design, React, shadcn, review, security, CI, and Auto Agents
  orchestration skills while explicitly excluding `superpowers`.

## 0.1.0 - 2026-07-18

- Add the cross-platform `design-engineer-skills` plugin.
- Add native marketplace and plugin manifests for Codex and Claude Code.
- Bundle all six skills from `emilkowalski/skills` at commit `6bf24434`.
