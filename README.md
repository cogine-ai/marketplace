# Cogine AI Marketplace

Cogine AI's INTERNAL plugin marketplace for Codex and Claude Code.

## Available plugins

- `design-engineer-skills` — six design-engineering and UI motion skills.
- `coding-engineer-skills` — 26 skills for specs, implementation, frontend and
  React work, architecture, debugging, testing, review, security, Git/CI, and
  Cogine multi-repository orchestration.

## Install in Codex

```bash
codex plugin marketplace add cogine-ai/marketplace
codex plugin add design-engineer-skills@cogine-ai
codex plugin add coding-engineer-skills@cogine-ai
```

## Install in Claude Code

```bash
claude plugin marketplace add cogine-ai/marketplace
claude plugin install design-engineer-skills@cogine-ai
claude plugin install coding-engineer-skills@cogine-ai
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
  skills/                              # 26 shared skills
```
