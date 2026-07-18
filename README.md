# Cogine AI Marketplace

Cogine AI's INTERNAL plugin marketplace for Codex and Claude Code.

## Available plugins

- `design-engineer-skills` — six design-engineering and UI motion skills.
- `coding-engineer-skills` — 24 skills for specs, implementation, frontend and
  React work, architecture, debugging, testing, review, security, Git/CI, and
  Cogine multi-repository orchestration.
- `product-manager-skills` — 16 skills for strategy, product judgment,
  discovery, research, PRDs, prototypes, roadmaps, metrics, design, specs, and
  tickets.
- `growth-and-gtm-skills` — 18 skills for product marketing, growth models,
  channels, acquisition, conversion, retention, measurement, PLG sales assist,
  and recurring execution.
- `sales-skills` — 12 skills for founder-led selling, first customers,
  prospecting, outreach, calls, enablement, enterprise accounts, pipeline
  review, and PLG sales integration.
- `founder-ceo-skills` — 16 skills for founder judgment, product-market fit,
  strategy, decisions, planning, organization, finance, fundraising, and board
  communication.

## Install in Codex

```bash
codex plugin marketplace add cogine-ai/marketplace
codex plugin add design-engineer-skills@cogine-ai
codex plugin add coding-engineer-skills@cogine-ai
codex plugin add product-manager-skills@cogine-ai
codex plugin add growth-and-gtm-skills@cogine-ai
codex plugin add sales-skills@cogine-ai
codex plugin add founder-ceo-skills@cogine-ai
```

## Install in Claude Code

```bash
claude plugin marketplace add cogine-ai/marketplace
claude plugin install design-engineer-skills@cogine-ai
claude plugin install coding-engineer-skills@cogine-ai
claude plugin install product-manager-skills@cogine-ai
claude plugin install growth-and-gtm-skills@cogine-ai
claude plugin install sales-skills@cogine-ai
claude plugin install founder-ceo-skills@cogine-ai
```

## Update

```bash
codex plugin marketplace upgrade cogine-ai
claude plugin marketplace update cogine-ai
```

## Repository layout

```text
.agents/plugins/marketplace.json       # Codex catalog
.claude-plugin/marketplace.json        # Claude Code catalog
plugins/design-engineer-skills/
  .codex-plugin/plugin.json            # Codex manifest
  .claude-plugin/plugin.json           # Claude Code manifest
  skills/                              # Shared skills
plugins/coding-engineer-skills/
  .codex-plugin/plugin.json            # Codex manifest
  .claude-plugin/plugin.json           # Claude Code manifest
  skills/                              # 24 shared skills
plugins/product-manager-skills/
  .codex-plugin/plugin.json            # Codex manifest
  .claude-plugin/plugin.json           # Claude Code manifest
  skills/                              # 16 shared skills
plugins/growth-and-gtm-skills/
  .codex-plugin/plugin.json            # Codex manifest
  .claude-plugin/plugin.json           # Claude Code manifest
  skills/                              # 18 shared skills
plugins/sales-skills/
  .codex-plugin/plugin.json            # Codex manifest
  .claude-plugin/plugin.json           # Claude Code manifest
  skills/                              # 12 shared skills
plugins/founder-ceo-skills/
  .codex-plugin/plugin.json            # Codex manifest
  .claude-plugin/plugin.json           # Claude Code manifest
  skills/                              # 16 shared skills
```
