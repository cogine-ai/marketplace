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

### Requirements and product design — 4

- `write-prd`
- `prototype`
- `interface-design`
- `ui-ux-pro-max`

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
- `ui-ux-pro-max` retains its full local design database and scripts but is
  explicit-only, avoiding unnecessary prompt overhead on unrelated work.
- Product-management workflows adapted from Anthropic were reduced to portable,
  connector-independent essentials.
- Lenny's full evidence references stay on demand; unrelated work only sees the
  concise skill names and trigger summaries.

See [UPSTREAM.md](./UPSTREAM.md) and
[THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) for provenance.
