# Product Manager Skills

Product Manager Skills is a focused, cross-platform product-management toolkit
for Codex and Claude Code. It keeps the bundle small enough to use every day
while covering the path from idea and evidence to PRD, prototype, roadmap, and
implementation handoff, with explicit support for product strategy and taste.

## Included skills

### Strategy and product judgment — 2

- `defining-product-strategy`
- `product-taste`

### Discovery and evidence — 4

- `founder-office-hours`
- `grilling`
- `synthesize-research`
- `competitive-brief`

### Requirements and product design — 5

- `write-prd`
- `prototype`
- `interface-design`
- `ui-ux-pro-max`
- `ux-audit` — 产品 UX 巡检: walk an existing product against a design principle,
  then show its 3–5 strongest violations with screenshots or source-grounded
  schematics and concrete redesigns.

### Roadmap and delivery handoff — 5

- `roadmap-update`
- `metrics-review`
- `backlog-ready-spec`
- `to-spec`
- `to-tickets`

## Design choices

- `defining-product-strategy` turns ambitions into explicit choices, while
  `product-taste` supplies a quality bar before execution starts.
- Product discovery and requirements stay separate: validate the decision before
  writing the PRD, then verify implementation readiness before ticketing.
- `grilling` follows Matt Pocock's current design-tree workflow, asking each
  dependency-ready frontier as a numbered round. The redundant `grill-me` alias
  is intentionally omitted.
- `to-spec` and `to-tickets` are explicit-only in both Codex and Claude Code
  because they publish artifacts to a tracker or the local workspace.
- `prototype` supports logic and UI exploration and includes a standalone HTML
  fallback when no host application exists.
- `interface-design` supplies the everyday craft discipline for product UI.
- `ux-audit` supplies a repeatable product walkthrough. Its default principle
  favors intuitive structure over explanatory paragraphs while retaining
  necessary labels, feedback and operation consequences. Users can supply
  another principle; coverage and evidence limits remain visible.
- `ui-ux-pro-max` retains its full local design database and scripts but is
  explicit-only, avoiding unnecessary prompt overhead on unrelated work.
- Product-management workflows adapted from Anthropic were reduced to portable,
  connector-independent essentials.
- Lenny's full evidence references stay on demand; unrelated work only sees the
  concise skill names and trigger summaries.

See [UPSTREAM.md](./UPSTREAM.md) and
[THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) for provenance.

## Product UX audit

After installing the version containing this skill, invoke
`$product-manager-skills:ux-audit` in Codex or
`/product-manager-skills:ux-audit` in Claude Code, for example:

> 全面走查本项目，按“界面应靠直觉理解，减少解释性文案”的原则，找到最违背原则的 3–5 处，每处展示截图或有依据的示意图，并给出具体改法。

The skill first maps the product's modules and core tasks, then ranks and
deduplicates findings. An audit request produces a report; a request that also
authorizes fixes can continue through implementation and verification.
