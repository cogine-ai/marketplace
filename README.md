# Cogine AI Marketplace

Cogine AI's INTERNAL plugin marketplace for Codex and Claude Code.

## Install in Codex

```bash
codex plugin marketplace add cogine-ai/marketplace
codex plugin add design-engineer-skills@cogine-ai
```

## Install in Claude Code

```bash
claude plugin marketplace add cogine-ai/marketplace
claude plugin install design-engineer-skills@cogine-ai
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
```
