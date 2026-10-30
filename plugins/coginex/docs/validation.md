# 0.2.0 候选版验收 — 2026-10-30

宿主：Codex CLI `0.165.0`、Claude Code `2.1.311`。2026-10-30 已获用户授权完成账户连接、线上读取及一个 `selfOnly` 临时任务的创建 / 读取 / 修改 / 软删除。
Codex 原生连接与该任务流程通过；Claude 的 CogineX MCP OAuth 已通过，模型驱动的工具调用因本机没有可用的 Claude Code 模型账户而尚未执行，不能据此宣称双端完整端到端通过。

| 检查 | 实际结果 |
| --- | --- |
| 双端隔离安装 | 从独立 `coginex-development` Marketplace 安装 `0.2.0`，Claude 组件盘点为 5 个 Skill、1 个 MCP。 |
| Codex Skill 开关 | 通过原生 `skills/config/write` 将 5 个 Skill 各自关闭、用 `skills/list` 读回关闭状态，确认另外 4 个状态不变，再逐个恢复；全部通过。 |
| Skill 路由行为 | 路由入口只使用宿主当前启用且可发现的技能，不自动读取已关闭 Skill 文件；技能文本与相对链接已校验。 |
| 用户本地开发安装 | 两端均通过原生 CLI 安装 `coginex@coginex-development`，版本 `0.2.0`。新增独立开发 Marketplace，没有替换原 `cogine-ai` 远程来源。 |
| Codex 原生插件读取 | `plugin/read` 读回 `installed: true`、`enabled: true`、`localVersion: 0.2.0`，5 个 Skill，以及真实 App ID；`mcpServers: []`，符合 ChatGPT 账户模式隐藏同名直接 MCP 的路由规则。 |
| Claude 原生组件读取 | `plugin details` 显示 5 个 Skill，直接 HTTP MCP 已发现。安装时的 `Needs authentication` 已由下述独立 MCP OAuth 登录完成，不再作为当前连接结论。 |
| 注册连接器与 Codex OAuth | 个人 CogineX 连接器 ID 为 `asdk_app_6ae3a09207788191a7081d25634ff509`；用户授权后的 ChatGPT/Codex OAuth 回调成功。OAuth 发现选择 DCR、canonical resource 与 `mcp` scope。 |
| Codex 线上工具发现 | 原生 `codex_apps` 发现 60 个 CogineX 工具。11 个连接 / 任务 / 历史专有工具全部存在，`Subagent` 也在其中；与源码最大集合的差异见能力清单。发现不等于每个工具均已调用。 |
| Codex 当前账户与 Team | 原生调用 `GetXConnectionContext` 成功，实际返回 schemaVersion 2，并核对账户 principal、account 与 Team；落盘证据中的身份字段仅保留哈希，不提交原值。 |
| Codex 私有任务流程 | 一个临时任务以 `selfOnly` 创建，`ReadMetadata` 读回原题，`RenameDocument` 改题后再次 `ReadMetadata` 核对，最后 `DeleteXTask` 返回 `deleted`；任务与清理 operation ID 均匹配。没有发送消息或修改其他业务对象。正文 `ReadContent` 未在本次流程执行。 |
| 原生账户管理界面 | 官方网页实际显示已连接账户、Primary 标识和“连接另一个账户”；账户菜单有重命名、重新连接和断开入口。当前使用宿主默认账户标签，Profile 邮箱标签尚未上线；没有把菜单存在当作实际双账户 / revoke 通过。 |
| Claude MCP 连接健康 | OAuth 后 `claude mcp get plugin:coginex:coginex` 返回 `Connected`。该健康检查不依赖 Claude 模型账户，也不等同于业务工具调用。 |
| Claude MCP OAuth | `claude mcp login plugin:coginex:coginex --no-browser` 经本地回调显示认证成功。第一次尝试因浏览器控制延迟超时，清理后第二次完整尝试成功；第一次超时不计为通过。 |
| Claude 模型与工具调用边界 | `claude -p` 在调用任何 MCP 工具前返回宿主认证错误；`claude auth status` 为 `loggedIn: false`、first-party 路线且没有 API key。用户随后确认没有 Claude Code 账号，因此不能将报错文本解释成用户已有账号只是过期。已取消等待登录，不要求用户注册；业务调用为 `NOT_RUN`，需未来有可用 Claude Code 模型账户的测试者补验。CogineX MCP OAuth 已独立通过。 |
| Profile 源码 | [CogineX PR #879](https://github.com/cogine-ai/CogineX-mono/pull/879) 最终提交 `a647d5250761831f13454aa5375af9ae150fb8d4` 基于 `8d993421f48ec80b373c7af7b7749fa7176dd569`；6 个专项与完整 MCP 服务 125 个测试（含 9 个本地 PostgreSQL 夹具）及 `just check` 通过。PR 已可评审，当前必要 CI（含 Affected Rust、Repository result、Changed-code gate）及 CodeRabbit 已全部通过，未合并或部署。补丁不改 SQL，但目标基线含 15 个新增迁移，不能视为已发布或已应用。 |
| 可移植打包 | `prepare_package.py` 的 15 个标准库测试通过，验证 App / 直接模式、源码不变、来源回执、目录与覆盖行为。生成目录的双端原生隔离安装和严格校验通过，两个目录型 Marketplace 都使用相对 `./` 来源。 |
| 严格包校验 | Claude 原生严格 manifest 校验通过。目录级图标 / 隐私 URL 建议仍为非阻断建议。 |
| Claude Skill 开关边界 | 官方文档与本机实现确认 `skillOverrides` 不覆盖插件内 Skill；支持插件整体启停和技能独立调用，不宣称逐项开关与 Codex 等同。 |

实际本地分发快照位于 `~/.local/share/coginex-plugin/development-marketplace`；内容来自本仓库 `plugins/coginex`，通过显式 App 绑定生成，保留来源回执；源码默认不包含个人 App ID。两端原生安装缓存仍是消费者，没有手工改缓存，也没有读取、输出或搬用现有 token。

本机验收证据位于 `/tmp/coginex-native-acceptance/`：`codex-read-status.json` 记录原生工具发现，`codex-context-redacted.json` 记录去标识后的身份结果，`task-roundtrip.json` 记录任务步骤与清理断言。这些临时证据没有加入仓库；提交文档不包含原始邮箱、principal 或临时任务 ID。


## 待完成

- Claude 模型驱动的工具发现及账户查询需由拥有可用 Claude Code 模型账户的测试者补验；当前用户没有该账号，不将注册或登录列为用户待办。一个私有临时任务的写入与清理已由 Codex 完成，无需重复创建。Claude MCP OAuth 成功不等同于业务调用成功。
- 核实线上缺少三个非可选设计读取工具的原因，并确认需要发布的服务版本；当前不能归因为旧部署或缓存。
- 合入并定向发布 Profile 服务变更，刷新连接器，再验证账户标签及重新连接的稳定 ID。
- 刷新与断开 / revoke、多真实账户切换，以及同事所处工作区的连接器可见性。
- 远程 Marketplace 的发布与安装 readback。

原生应用自动化访问受宿主限制，连接器注册和授权使用官方网页登录入口。2026-10-30 用户授权后已完成连接与上述限定验收；未代填用户凭据。token refresh、撤销和两个真实账户切换均未验收。

以下保留最初 `0.1.0` 的历史验证，不将其成功项冒充为本版本登录验收。

---

# 0.1.0 历史验收记录

日期：2026-10-29（Asia/Taipei）。版本：`0.1.0`。
宿主：Codex CLI `0.165.0`、Claude Code `2.1.311`。

## 已通过

| 检查 | 实际结果 |
| --- | --- |
| Claude 原生严格校验 | 插件与 Marketplace 均 `success: true`，manifest 无错误或警告。内部首版未填写图标和隐私页，校验器另给出非阻断的 directory 发布建议。 |
| Codex 隔离安装 | 在临时配置根中从本地 Marketplace 安装 `coginex@cogine-ai`，读回名称和版本 `0.1.0`。 |
| Codex MCP 配置加载 | `codex mcp get coginex --json` 返回 `streamable_http`、正确 URL、`enabled: true`；`enabled_tools` / `disabled_tools` 均为空，没有插件工具过滤。 |
| Codex 原生技能发现 | 使用隔离配置的 app-server `skills/list`，读回 `coginex:coginex`、`enabled: true` 和安装缓存中的实际 `SKILL.md` 路径。未启动模型任务。 |
| Claude 隔离安装 | 在独立临时配置根安装同一插件，`plugin list --json` 读回 `0.1.0`、启用状态和相同 MCP 地址。 |
| Claude 组件与 MCP 加载 | `plugin details` 识别 1 个 skill、1 个 MCP server；`mcp get plugin:coginex:coginex` 识别 HTTP 与正确 URL，状态为 `Needs authentication`。 |
| 安装内容 | 对两端安装文件与源文件逐文件比较 SHA-256，内容一致。 |
| 线上公开发现 | protected-resource 与 authorization-server metadata 均 HTTP 200；资源为 `https://mcp.x.cogine.ai/mcp`，资源 scope 为 `mcp`，发现 DCR、token 和 revocation 入口。 |
| 未认证 MCP 入口 | `POST /mcp` 的 initialize 返回 HTTP 401，并提供 `resource_metadata` challenge；没有使用或读取现有账户凭据。 |
| 源码盘点 | 固定 CogineX 版本的 67 个工具名称无重复；完整名称见能力文档。`git diff --check` 通过。 |

隔离安装仅向临时子进程传入配置目录；没有安装到用户日常配置，没有替换现有
Marketplace、MCP 条目、技能缓存或任何共享宿主目录。

## 尚未验收

以下为 2026-10-29 的历史状态，2026-10-30 的新增验收以上文为准。

- 两个宿主的真实浏览器 OAuth 登录、token refresh / 撤销。
- 登录后的生产 `tools/list`、账户 / Team 读取，以及真实任务和其他业务工具调用。
- 本地历史采集、自动上传或同步：首版没有实现对应运行时。
- 远程 Marketplace 发布：当前本地源码和安装验证不代表远程版本已经可安装。

## OAuth scope 的兼容依据

线上资源 metadata 只发布 `mcp`；issuer metadata 还列出 auto-review 和 enterprise
等其他资源的 scope，因此不能把整个 issuer scope 清单当成本插件权限集合。
Codex 当前源码的 [`discover_supported_scopes`][codex-scopes] 采用资源相关 scope，
Claude 的 [OAuth 说明][claude-oauth] 也支持从资源发现权限。共享 `.mcp.json`
因此保留 `type` 和 `url`，让宿主处理 OAuth，不写两端语法不同的 scope 扩展。

这部分是源码和公开 metadata 证据，未冒充安装版本的真实登录结果。

[codex-scopes]: https://github.com/openai/codex/blob/b26b0a7a777bd9c153da2e1e86f00ee1600476bd/codex-rs/rmcp-client/src/auth_status.rs
[claude-oauth]: https://code.claude.com/docs/en/mcp#authenticate-with-remote-mcp-servers
