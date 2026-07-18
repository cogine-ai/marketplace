# Product Manager Skills

Product Manager Skills is a focused, cross-platform product-management toolkit
for Codex and Claude Code. It keeps the bundle small enough to use every day
while covering the path from idea and evidence to PRD, prototype, roadmap, and
implementation handoff.

## Included skills

### Discovery and evidence — 5

- `founder-office-hours`
- `grilling`
- `grill-me`
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

- Product discovery and requirements stay separate: validate the decision before
  writing the PRD, then verify implementation readiness before ticketing.
- `prototype` supports logic and UI exploration and includes a standalone HTML
  fallback when no host application exists.
- `interface-design` supplies the everyday craft discipline for product UI.
- `ui-ux-pro-max` retains its full local design database and scripts but is
  explicit-only, avoiding unnecessary prompt overhead on unrelated work.
- Product-management workflows adapted from Anthropic were reduced to portable,
  connector-independent essentials.
- Claude Code's inspector estimates about 1,043 always-on tokens for the 14
  skill names and trigger summaries; full bodies load only when invoked.

See [UPSTREAM.md](./UPSTREAM.md) and
[THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) for provenance.
