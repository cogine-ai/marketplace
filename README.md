# Cogine AI Marketplace

A curated marketplace of role-based skills and agent tools, maintained by Cogine AI.

## Install the Marketplace

### Codex (recommended)

```bash
codex plugin marketplace add cogine-ai/marketplace
```

Then open the Codex App's **Plugins** page, choose **Cogine AI**, and install
only the plugins you want. If the Marketplace does not appear immediately,
restart Codex once.

![Cogine AI Marketplace in Codex](docs/images/cogine-ai-marketplace.png)

### Claude Code

```bash
claude plugin marketplace add cogine-ai/marketplace
```

Adding the Marketplace registers its catalog; it does not install every plugin.

## Available plugins

| Plugin | Skills | Focus |
| --- | ---: | --- |
| `design-engineer-skills` | 9 | UI prototyping, supplementary marketing-page candidates, frontend library selection, polish, animation review, and motion design. |
| `coding-engineer-skills` | 30 | Specs, implementation, domain and architecture design, isolated worktrees, frontend and React work, debugging, testing, independent review, security, Git/CI, and multi-repository orchestration. |
| `product-manager-skills` | 15 | Strategy, product judgment, discovery, research, PRDs, prototypes, roadmaps, metrics, design, specs, and tickets. |
| `growth-and-gtm-skills` | 18 | Product marketing, growth models, channels, acquisition, conversion, retention, measurement, PLG sales assist, and recurring execution. |
| `sales-skills` | 12 | Founder-led selling, first customers, prospecting, outreach, calls, enablement, enterprise accounts, pipeline review, and PLG sales integration. |
| `founder-ceo-skills` | 16 | Founder judgment, product-market fit, strategy, decisions, planning, organization, finance, fundraising, and board communication. |
| [`cursourcing`](https://github.com/cogine-ai/cursourcing) | 1 | **Your Codex just hired Cursor.** Codex plans, hands suitable subtasks to Cursor, and reviews results. Codex only. |

The Codex catalog contains seven plugins. The six role-based skill plugins are
also available in Claude Code; Cursourcing targets Codex and requires Node.js 22+
and an authenticated Cursor CLI.

Install any plugin from the table with its ID:

```bash
# Codex
codex plugin add coding-engineer-skills@cogine-ai

# Claude Code
claude plugin install coding-engineer-skills@cogine-ai
```

In an existing Claude Code session, run `/reload-plugins` after installation.

To use Cursourcing in Codex:

```bash
codex plugin add cursourcing@cogine-ai
```

Start a new task and invoke `$cursourcing:cursourcing`. Codex plans normally and
uses Cursor when a well-defined subtask would benefit from delegation.

## Compatibility

Codex is the primary target. The six role-based plugins also ship native Claude
Code manifests while sharing the same skill folders:

- Codex catalog: `.agents/plugins/marketplace.json`
- Codex manifests: `plugins/*/.codex-plugin/plugin.json`
- Claude Code catalog: `.claude-plugin/marketplace.json`
- Claude Code manifests: `plugins/*/.claude-plugin/plugin.json`

## Update

### Codex

```bash
codex plugin marketplace upgrade cogine-ai
codex plugin list --json
```

Confirm that `coding-engineer-skills@cogine-ai` reports the expected version.
Start a new task after upgrading so its skill index is rebuilt.

### Claude Code

```bash
claude plugin marketplace update cogine-ai
claude plugin update coding-engineer-skills@cogine-ai
claude plugin list --json
```

Restart Claude Code after the plugin update so the new version is loaded.

## Repository layout

```text
.agents/plugins/marketplace.json       # Codex catalog
.claude-plugin/marketplace.json        # Claude Code catalog
docs/images/                           # Marketplace screenshots
plugins/design-engineer-skills/
  .codex-plugin/plugin.json            # Codex manifest
  .claude-plugin/plugin.json           # Claude Code manifest
  skills/                              # 9 shared skills
plugins/coding-engineer-skills/
  .codex-plugin/plugin.json            # Codex manifest
  .claude-plugin/plugin.json           # Claude Code manifest
  skills/                              # 30 shared skills
plugins/product-manager-skills/
  .codex-plugin/plugin.json            # Codex manifest
  .claude-plugin/plugin.json           # Claude Code manifest
  skills/                              # 15 shared skills
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
plugins/cursourcing/
  .codex-plugin/plugin.json            # Codex manifest
  .mcp.json                           # Cursor execution bridge
  dist/                                # Bundled runtime and dependency notices
  skills/                              # 1 Codex collaboration skill
```

Cursourcing is maintained in [cogine-ai/cursourcing](https://github.com/cogine-ai/cursourcing).
This repository carries its installable release snapshot; see the plugin's
`UPSTREAM.md` for the pinned source commit.
