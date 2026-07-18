# Cogine AI Marketplace

A cross-platform plugin marketplace for Codex and Claude Code.

## Available plugins

### Design Engineer Skills

Six design-engineering skills covering UI polish, animation review, motion
audits, animation opportunities, motion vocabulary, and Apple-inspired web
interaction design.

The original skill content is by [Emil Kowalski](https://github.com/emilkowalski)
and comes from [emilkowalski/skills](https://github.com/emilkowalski/skills).
Cogine AI maintains the cross-platform plugin packaging.

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

This repository is private. Installers need GitHub access to the `cogine-ai`
organization and working Git credentials on their machine.

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
