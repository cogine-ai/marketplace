# 能力清单与服务端缺口

本清单来自 2026-10-29 的 CogineX 源码审查，固定版本为
[`cf473c41cf6b432c3d7a0c50790a3322c0564906`](https://github.com/cogine-ai/CogineX-mono/tree/cf473c41cf6b432c3d7a0c50790a3322c0564906)。
下表是该固定版本的源码注册清单；2026-10-30 的线上发现和实际调用另列，不能互相代替。

插件接入现有 `https://mcp.x.cogine.ai/mcp`，Codex 的 ChatGPT 账户模式使用注册 App，直接 MCP 路线供 Claude Code 及相应 CLI 环境使用，不另设工具白名单。
该版本的最大注册集合有 **67 个名称**：56 个共享工具和 11 个 MCP 专有连接、任务工具。
其中 4 个 Anthropic 工具及 `Subagent` 取决于服务端运行时配置；历史工具也依赖相应服务注入。
部署版本、配置与实际可用能力，以登录后 MCP `tools/list` 及调用结果为准。
服务端注册依据为 [共享工具组合][shared]、[MCP 专有工具注册][mcp-only] 和 [运行时装配][runtime]。

## 2026-10-30 线上发现与验收

用户授权后，Codex 原生 `codex_apps` 实际发现 **60 个 CogineX 工具**。11 个连接 / 任务 / 历史专有工具均存在，`Subagent` 也已发现；与 67 个名称的源码最大集合相比，未发现以下 7 个：

- 4 个可选 Anthropic 工具：`WebSearch`、`WebFetch`、`BashCodeExecution`、`TextEditorCodeExecution`。
- 3 个源码中非可选的设计读取工具：`ReadDesign`、`ReadPhotoshopDocument`、`ReadIllustratorDocument`。

上述三个设计工具的差异原因尚不明确；旧部署、缓存等都未获得验证，不能把它们归为提供商可选项或直接判定成插件过滤。

本次原生调用已验证 `GetXConnectionContext` 的 schemaVersion 2、当前账户和 Team，以及一个 `selfOnly` 临时任务的 `CreateXTask → ReadMetadata → RenameDocument → ReadMetadata → DeleteXTask` 流程；清理确认返回 `deleted`，未发送消息或修改其他业务对象。其余发现到的工具不因此自动计为调用通过，正文读取和历史上传等也未在该流程验收。

Claude 的 CogineX MCP OAuth 已通过本地回调认证；`claude -p` 在任何 MCP 调用前因 Claude Code 自身 Anthropic OAuth 登录失效停止。Claude 业务工具调用仍为 `NOT_RUN`，不能与 MCP 连接认证混为一项。完整证据和后续项见 [验收记录](validation.md)。

## 完整源码清单

| 类别 | 数量 | 工具名称 |
| --- | ---: | --- |
| 搜索、浏览与产品说明 | 4 | `ContentSearch`、`NameSearch`、`ListEntities`、`SelfKnowledge` |
| 文档与讨论 | 10 | `CreateDocument`、`EditDocument`、`RenameDocument`、`ReadContent`、`ReadMetadata`、`ReadDesign`、`ReadPhotoshopDocument`、`ReadIllustratorDocument`、`ReadDocumentDiscussion`、`ReadDocumentDiscussionThread` |
| 属性与标签 | 3 | `GetEntityProperties`、`SetEntityProperty`、`ListTags` |
| 频道与 AI Chat | 5 | `ReadChannelMessageContext`、`ReadChannelMessages`、`ReadChannelThread`、`SendChannelMessage`、`ReadChat` |
| Bot | 7 | `ListBots`、`CreateBot`、`IssueBotCredential`、`GetBotWebhooks`、`ManageBotChannelAccess`、`ConfigureBot`、`DeleteBot` |
| 团队与 CRM | 3 | `ListTeamMembers`、`ListCompanies`、`GetCompany` |
| 活动与通知 | 4 | `ReadActivity`、`ListNotifications`、`MarkNotificationsDone`、`MarkNotificationsSeen` |
| 提醒 | 4 | `ListReminders`、`CreateReminder`、`UpdateReminder`、`DeleteReminder` |
| 邮件 | 4 | `GetThread`、`ListLabels`、`ListInboxes`、`UpdateThreadLabels` |
| 日历 | 5 | `ListCalendars`、`ListCalendarEvents`、`CreateCalendarEvent`、`UpdateCalendarEvent`、`DeleteCalendarEvent` |
| 通话 | 2 | `ListCallRecords`、`ReadCallRecord` |
| 可选 Anthropic 能力 | 4 | `WebSearch`、`WebFetch`、`BashCodeExecution`、`TextEditorCodeExecution` |
| 可选模型运行时 | 1 | `Subagent` |
| MCP 专有连接与任务 | 11 | `GetXConnectionContext`、`CreateXTask`、`ListTaskChannelThreads`、`ReadTaskChannelThread`、`PostXTaskThreadMessage`、`GetXTaskStatus`、`SetXTaskStatus`、`DeleteXTask`、`UploadXTaskHistorySelection`、`ReadXTaskHistory`、`SearchXTaskHistory` |

可选项在服务端未配置时可能不出现在列表中。插件不会用本机命令补造同名工具；
`BashCodeExecution` 等调用的是服务器配置的提供商能力，不能据此推断它能操作当前本机工作区。

## 任务能力已经覆盖的内容

- **查找与读取**：搜索、`ListEntities`、正文、元数据、属性、任务讨论，以及关联频道线程。
- **创建**：`CreateXTask` 支持幂等 `operationId` 与明确的 `selfOnly` / `teamVisible` 可见范围；
  `CreateDocument` 也有任务创建字段，实际采用调用时的 schema。
- **标题、正文和字段**：`RenameDocument`、`EditDocument` 和 `SetEntityProperty`。
  [任务系统属性][properties] 已包含指派人、状态、优先级、截止时间、父任务、子任务与 Story Points，
  无需为这些字段再做一套本地任务实现。
- **评论与工作更新**：`PostXTaskThreadMessage` 支持任务自身评论和关联频道回复，带幂等提交与 `readbackOnly`。
- **状态**：`GetXTaskStatus` 读取状态及版本；[专有 `SetXTaskStatus`][status] 只处理
  `inProgress → inReview` 的版本比较更新。其他状态变更由已有属性工具提供。
- **删除**：`DeleteXTask` 提供 Owner 权限下的软删除；其 `operationId` 是结果关联字段，不是持久化去重键。
- **历史**：上传显式选定的源记录版本，读取精确版本，搜索当前有权访问的历史证据。
  上传需要客户端先完成凭证过滤；服务端工具本身不会采集本机聊天记录。

## 首版接入后仍需补的缺口

| 缺口 | 当前源码证据与处理方向 |
| --- | --- |
| 发送邮件 | [`email::mcp_toolset`][email] 明确排除 `SendEmail`，当前仅暴露读取、列表与标签更新。要开放发送，应在 CogineX 的现有邮件适配器上补 MCP 注册及调用契约。 |
| 飞书内容读取 | [`document_cognition_tools_with_anthropic_server_tools`][feishu] 添加的 `FindDocuments` / `ReadDocument` 属于 DCS 专有能力，未加入入站 MCP。插件不会因为其他仓库已有代码就宣称已经开放。 |
| 本地会话历史 | 已有历史上传接口，但尚无 Codex / Claude Code 原生聊天记录的采集、选择、凭证过滤与同步适配器。首版可调用显式 selection；自动同步需要另做本地接入。 |
| Bot 凭据签发 | [`IssueBotCredential`][bot-credential] 仅返回待签发提案，不创建或返回 secret；本地客户端没有 CogineX chat card，需要转到 Bot 设置完成签发。`CreateBot` 返回 credential proposal 时也有同样的后续步骤。若要在本地完整完成 Bot 接入，应补通用客户端的签发交接流程。 |
| 项目管理与文件 | 本次入站注册集合没有项目创建、移动、删除，通用文档删除或本地二进制文件上传工具。项目的搜索、列表及属性操作不等于完整项目 CRUD。 |
| 工具文档遗漏 | [MCP schema 导出][schema-export] 只覆盖共享工具集合，未包含 `mcp_service` 单独注册的 11 项连接及任务工具；文档生成链路应合并实际服务注册定义。 |
| 客户端专有措辞 | [`DeleteXTask` 描述][delete] 写有 “Work clients must obtain operation approval before calling”。通用 Codex / Claude Code 插件会直接收到这段描述，应在 CogineX 调整为通用客户端表述；Owner ACL 与调用结果语义继续由服务端执行。 |

以上是当前 MCP 边界，不代表底层业务服务完全没有这些实现。
后续补齐应继续复用 CogineX / CogineWork 的已有服务与适配点。

## Macro 等关键词：需要调衡的位置

本次扫描的入站 MCP 工具名称、共享 schema、工具描述及 `SelfKnowledge` 当前产品说明未发现 Macro 品牌残留。
但用户经工具提供的文档入口仍可能遇到以下内容：

| 位置 | 发现 | 建议调整 |
| --- | --- | --- |
| [`crates/ai_tools/src/self_knowledge.rs:87`][self-changelog] → [`apps/docs/changelog/introduction.mdx:4–7`][changelog] | `SelfKnowledge` 链接 CogineX changelog 路由，而对应源码正文仍写 Macro，并指向 `macro-inc/macro` Releases。 | 分清 CogineX 发布记录与上游参考记录，避免被理解为 CogineX 已发布的能力。这里只验证了源码链接关系，未验证该线上页面当前部署内容。 |
| [`apps/docs/coginex/upstream-reference.mdx`][upstream-doc] | 明确说明保留 Macro 文档作为工程参考，并规定其不自动定义 CogineX 产品范围。 | 保留真实来源说明，避免把引用页直接当作产品承诺。 |
| [`apps/web/scripts/check-visible-brand.ts:14–17`][brand-exception] | 仍为 `SelfKnowledge` 保留 `docs.macro.com` 例外，但当前该工具内容已使用 `x.cogine.ai/docs`。 | 清理失效例外与过时理由，防止以后重新引入旧域名却被放过。 |

Rust 的 `macro_rules!`、Cargo 的 `macros` 特性是语言术语，不是产品命名。
本插件接入配置使用 CogineX 名称和地址；工程来源记录中的 Macro 引用按上述语境保留。

[shared]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/crates/ai_tools/src/lib.rs#L130-L255
[mcp-only]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/services/mcp_service/src/tool_service.rs#L130-L151
[runtime]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/services/mcp_service/src/main.rs#L39-L81
[properties]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/crates/properties/src/inbound/toolset/set_entity_property.rs#L46-L53
[status]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/services/mcp_service/src/x_task_status/inbound.rs#L103-L125
[email]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/crates/email/src/inbound/toolset/mod.rs#L151-L173
[feishu]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/crates/ai_tools/src/lib.rs#L190-L198
[schema-export]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/crates/ai_tools/src/lib.rs#L221-L227
[delete]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/services/mcp_service/src/x_task_delete/inbound.rs#L22-L26
[self-changelog]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/crates/ai_tools/src/self_knowledge.rs#L87
[changelog]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/apps/docs/changelog/introduction.mdx#L4-L7
[upstream-doc]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/apps/docs/coginex/upstream-reference.mdx
[brand-exception]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/apps/web/scripts/check-visible-brand.ts#L14-L17
[bot-credential]: https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/crates/bots/src/inbound/toolset/issue_bot_credential.rs#L35-L39
