# Changelog

## Design Engineer Skills 0.1.4 - 2026-09-16

- Release Design Engineer Skills 0.1.4 with `marketing-page-design-candidate`
  (候选营销页面设计), for supplementary candidates after a main design exists.
  Preserve the full pinned Taste Skill body, adapting only its name and
  description and adding matching UI metadata and upstream license.

## 0.7.1 - 2026-08-26

- Prepare `product-manager-skills` version `0.2.0` with 15 focused skills.
- Refresh `grilling` and its Codex metadata exactly from Matt Pocock's current
  pinned snapshot, replacing one-question-at-a-time interviews with numbered
  design-tree frontier rounds.
- Make `to-spec` and `to-tickets` explicit-only in both Claude Code and Codex.
- Remove the redundant explicit-only `grill-me` alias; `grilling` remains the
  single interview skill.

## 0.7.0 - 2026-08-25

- Expand `coding-engineer-skills` from 25 to 30 skills and prepare plugin
  version `0.2.0`.
- Restore Matt Pocock's current implementation and architecture stack:
  `code-review`, `setup-matt-pocock-skills`, `domain-modeling`,
  `improve-codebase-architecture`, and `grilling`;
  refresh `diagnosing-bugs`, `tdd`, `codebase-design`, and `implement`;
  and align `fix-merge-conflicts` with upstream
  `resolving-merge-conflicts`.
- Keep `grill-with-docs` out of the bundle because it only aliases the
  separately available `grilling` and `domain-modeling` skills, and retain the
  local `implement` pre-commit review instead of chaining fixed-point review.
- Make 12 workflow commands explicit-only in both Claude Code and Codex while
  keeping 18 focused skills model-invokable, and namespace operational
  cross-skill calls to the local plugin.
- Make Local Ultra Review fail closed: reviewer and verifier contexts emit
  explicit completion receipts, candidate ids are scoped to their originating
  reviewer, light mode retains a dedicated security/privacy pass, all worktree
  phases retain one absolute session artifact root, reports expose incomplete
  execution, and GitHub output refuses to render or post an incomplete review.
- Apply narrow reviewed corrections to the pinned Matt workflows for
  multi-context routing, recoverable conflict handling, executable issue
  tracker commands, and secure architecture report generation.
- Add deterministic inventory, invocation-policy, runtime-placeholder,
  execution, verifier, manifest, and upstream-hash contracts.

## 0.6.3 - 2026-07-29

- Update `design-engineer-skills` to the latest Emil Kowalski snapshot, add
  explicit-only `prototype` and `pick-ui-library`, and release version `0.1.1`.
- Update Growth `pricing` to 2.1.0 with human-buyer and AI-agent pricing-page
  review, the paste test, and `Product`/`Offer` structured-data guidance;
  release `growth-and-gtm-skills` version `0.1.2`.
- Refresh `to-tickets` in Coding Engineer and Product Manager by removing the
  obsolete final `/implement` handoff; release versions `0.1.6` and `0.1.2`.
- Clarify that `to-spec` comes from Matt Pocock while `backlog-ready-spec` is a
  Cogine adaptation informed by GStack's `spec` workflow.
- Selectively strengthen GStack-derived workflows: behavioral demand evidence
  in `founder-office-hours`, preserve/sequence/rollback contracts in
  `backlog-ready-spec`, and a complete evidence-based journey in
  `devex-review`; release `founder-ceo-skills` version `0.1.1`.

## 0.6.2 - 2026-07-22

- Refresh `fix-ci`, `loop-on-ci`, and `review-and-ship` from their newer local
  Cogine snapshots.
- Update `vercel-react-best-practices` from 58 to 70 rules.
- Release `coding-engineer-skills` version `0.1.5`.

## 0.6.1 - 2026-07-22

- Add `worktree-management` to `coding-engineer-skills` as a narrowly triggered
  adaptation of Superpowers' worktree isolation workflow.
- Preserve existing-worktree detection and native-tool preference, make setup
  proportional, and add confirmation-gated cleanup for manual worktrees.

## 0.6.0 - 2026-07-19

- Add the cross-platform `founder-ceo-skills` plugin with 16 focused
  workflows for founder judgment, PMF, strategy, planning, organization,
  finance, fundraising, and board communication.
- Add `measuring-pmf`, `seven-powers`, and a compact, tool-neutral
  `startup-finance` skill for burn, runway, scenarios, and unit economics.
- Keep `planmode-ceo` unchanged and reserve the broad `ceo-advisor` skill
  for explicit requests for comprehensive CEO advice.
- Route `ceo-advisor` analysis to focused strategy, planning, and finance
  skills instead of bundling duplicate upstream Python models, and replace
  fixed capital-allocation recipes with runway-aware guardrails.

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
