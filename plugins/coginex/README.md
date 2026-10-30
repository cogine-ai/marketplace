# CogineX for Codex / Claude Code

内部自用插件，当前候选版本 `0.2.0`。通过完整的 CogineX MCP 工具集，在本地处理任务、文档、搜索、讨论、日历、提醒、Bot 和 CRM 工作。

## 账户连接与管理

默认分发包通过原生 HTTP MCP OAuth 接入，两端均可使用。为 Codex 绑定真实的个人或工作区 CogineX 应用连接器后，可在原生插件管理页连接账户、查看已连接账户、连接另一个账户，以及使用宿主提供的选择和断开操作。本机验收使用的就是已绑定版本。

| 环境 | 连接入口 |
| --- | --- |
| Codex + ChatGPT 账户，已绑定 App | **Plugins → CogineX → Manage** 的应用连接器。 |
| Codex 直接 MCP 模式 | 当前配置确实有 `coginex` 时，使用 `codex mcp login coginex`。 |
| Claude Code | `/mcp` 中的 `plugin:coginex:coginex`，或 `claude mcp login plugin:coginex:coginex`。 |

源码的 `.app.json` 为空，不固定某个人私有的连接器 ID。绑定包中的 Codex App 和直接 MCP 使用同名别名 `coginex`：支持 App 路由时隐藏同名直接 MCP，没有 App 路由时保留直接 MCP。Claude manifest 只引用直接 MCP。服务地址为 `https://mcp.x.cogine.ai/mcp`，无需本地代理、手填 token 或自己的账号数据库。

账户连接与 OAuth 凭据由宿主管理，不存进插件包。两种宿主分别授权。原生账户界面、注册记录、团队可见范围和注销边界见 [账户说明](docs/accounts.md)。当前候选版的实际通过与待验收项见 [验收记录](docs/validation.md)。

## 安装

从本仓库安装到独立测试配置，或确认 Marketplace 指向本次源码后安装：

```bash
# Codex
codex plugin marketplace add .
codex plugin add coginex@cogine-ai

# Claude Code
claude plugin marketplace add .
claude plugin install coginex@cogine-ai
```

已有同名远程 Marketplace 时，本地候选版使用独立开发 Marketplace，保留原来源。远程发布后可刷新原 Marketplace 再升级；本地文件和安装测试不代表远程已发布。Claude Code 也可运行 `claude --plugin-dir ./plugins/coginex`。安装或更新后在新会话中使用。

## 生成账户管理版安装包

先在 ChatGPT 的 **Plugins → 添加 → 添加自定义 MCP 服务器** 注册 CogineX，使用上面的 MCP URL 和 OAuth 自动发现。可以使用自己创建的个人连接器，或管理员已提供给团队的工作区连接器。取得真实的 `asdk_app_...` / `connector_...` ID 后生成新包：

```bash
python3 -B plugins/coginex/scripts/prepare_package.py \
  --app-id asdk_app_实际注册ID \
  --output /新的目录/coginex-account \
  --with-marketplace
```

脚本只创建新目录，不覆盖源码、安装缓存或旧包，不读取账号和 token。安装生成的 `coginex-local` Marketplace：

```bash
codex plugin marketplace add /新的目录/coginex-account
codex plugin add coginex@coginex-local
```

先验证替代包版本和 App / Skill 配置，再停用旧的同名插件条目，保留其原 Marketplace 来源。Claude 原有直接 MCP 安装无需为了 Codex 的绑定而更换来源。

没有注册 App 时可用 `--direct-mcp` 生成直接 MCP 包。两种包都不设置插件层工具过滤，具体工具列表取决于服务及当前连接信息；直接包的账户授权从 MCP 设置进入。注册、团队可见性与包来源回执见 [账户说明](docs/accounts.md)。

## 五个 Skill

| Skill | 内容 |
| --- | --- |
| `coginex` | 跨任务、知识与协作的入口，按宿主当前启用的技能路由。 |
| `setup` | 账户连接、当前身份与 Team、重连、切换账户和退出。 |
| `tasks` | 任务发现、创建、正文、属性、状态、讨论与结果回写。 |
| `knowledge` | 文档读写、搜索、讨论和任务历史证据。 |
| `collaboration` | 频道、邮件读取、日历、提醒、通知、Bot、CRM 与通话记录。 |

Codex 使用 `$coginex:tasks` 等命名空间；Claude Code 使用 `/coginex:tasks`。也可直接描述工作，由当前启用的技能提供指导。

Codex 支持独立 Skill 开关，关闭后路由器不会自动读其文件绕过开关。Claude Code 当前原生设置管理插件整体启停，插件内技能可独立调用，但没有同样的逐项开关。Skill 开关控制工作指导，不是 MCP 工具权限开关。

## 工具覆盖与维护

插件接入实时工具集，不设置插件白名单、只读模式或额外审批器。原源码盘点为 67 项；Profile 适配器部署后会增加一项，实际以登录后的发现和调用结果为准。

完整分组和缺口见 [能力清单](docs/capabilities.md)，来源与 Macro 遗留见 [源码审查](docs/source-review.md)。任务负责人、状态、优先级、截止日期及父子任务已有通用属性工具支持。邮件发送、部分项目 / 文件操作、本地历史采集和 Bot 凭据的本地签发交接仍属上游能力边界。

维护 `plugins/coginex` 源码，保留双端 manifest，共用五个 Skill 和直接 MCP 配置。Codex `.app.json` 只记录真实注册的连接器 ID，不自动向其他用户授予连接器访问权。安装缓存是消费者，不直接编辑。

```bash
claude plugin validate ./plugins/coginex --strict
claude plugin validate ./.claude-plugin/marketplace.json --strict
```
