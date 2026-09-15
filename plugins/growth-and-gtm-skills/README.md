# Growth & GTM Skills

Growth & GTM Skills is a focused, cross-platform toolkit for Codex and Claude
Code. It covers the path from product and customer context to channel choice,
launch, acquisition, conversion, retention, measurement, recurring execution,
and the handoff from product-qualified usage to sales assist.

## Included skills

### Foundation and growth strategy — 5

- product-marketing
- customer-research
- competitors
- growth-model
- acquisition-channels

### GTM planning and acquisition — 6

- pricing
- launch
- content-strategy
- copywriting
- search-visibility
- free-tools

### Conversion, retention, and operations — 6

- cro
- onboarding
- churn-prevention
- analytics
- growth-experiments
- marketing-loops

### Product-led revenue handoff — 1

- plg-sales-integration

## Optional marketing-page design

For an additional visual candidate after the main page direction is established,
pair the marketing brief, copy, and conversion goal with
`marketing-page-design-candidate` (候选营销页面设计) from the separately installed
[Design Engineer Skills](https://github.com/cogine-ai/marketplace/tree/main/plugins/design-engineer-skills)
plugin. It is supplementary and is not used independently.

Design owns the complete upstream implementation and its updates. This GTM
bundle keeps one optional pairing note and does not ship a second skill copy.

## Design choices

- The bundle keeps only broadly useful growth and GTM workflows from the larger
  marketing-skills catalog.
- Lenny's growth-model replaces the planned custom growth-loops skill with a
  stronger evidence-backed model; acquisition-channels fills the channel
  selection gap.
- search-visibility is a lightweight router. Traditional SEO, AI discovery,
  and programmatic-search details load only when needed.
- growth-experiments combines practical A/B testing with pre-registration,
  sample-size, sample-ratio-mismatch, and suspicious-result safeguards.
- marketing-loops remains separate from growth-model: one models business
  mechanics, while the other schedules bounded recurring execution.
- plg-sales-integration is intentionally shared with Sales Skills because PQL
  design and sales-assisted expansion sit at the boundary of both roles.
- Tool-specific integrations are optional. The skills work without assuming a
  particular connector, analytics vendor, or scheduler.

See [UPSTREAM.md](./UPSTREAM.md) and
[THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) for provenance.
