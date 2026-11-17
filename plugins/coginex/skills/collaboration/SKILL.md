---
name: collaboration
description: 使用 CogineX 处理频道和同事沟通、日历、提醒、定时工作、Agent 会话、通知、邮件、通话记录、Bot 和 CRM 工作。
---

# CogineX 协作

按用户本次工作组合当前 CogineX 工具，沿用目标与已有授权；工具权限和参数以实时服务描述为准。连接或账户问题仅在宿主当前已启用、可发现 `coginex:setup` 时转交该技能；否则按当前工具返回和宿主原生连接状态处理，不读取已关闭或未发现的 setup 文件。

## 沟通与工作上下文

- 用 `ListEntities` 查频道、讨论、邮件或其他对象；需要团队成员时用 `ListTeamMembers`。不要把频道 ID、线程 ID、消息 ID 混用。
- `ReadChannelMessages`、`ReadChannelThread`、`ReadChannelMessageContext` 读取频道背景，`ReadChat` 读取已有 AI 对话。发送或回复使用 `SendChannelMessage`，按实际结果中的频道与线程 ID 定位；用户只要求阅读或起草时不发送。
- 服务提供 `ListColleagueMessages` / `SendColleagueMessage` 时，可读取 ask 协议同事消息或发送同事私信；列表不是完整 DM 历史，按 `nextCursor` 续读并按消息 ID 去重。发送工具当前要求 UUIDv7 `operationId`，同一条消息恢复时保留原 ID 和参数；不能套用频道发送的无去重假设。
- 邮件可用 `ListInboxes`、`ListLabels`、`GetThread`、`UpdateThreadLabels` 读取和整理。历史公开 MCP 清单不含 `SendEmail`；以当前发现为准，只有服务实际提供发送工具时才能据其 schema 发送，不能把标签更新说成邮件已发出。
- `ListCallRecords` / `ReadCallRecord` 查通话记录；引用实际返回的记录与内容，不把列表条目当作已读逐字稿。

## 日历、提醒与通知

先用 `ListCalendars` / `ListCalendarEvents` 取得需要操作的日历或事件。通过 `CreateCalendarEvent`、`UpdateCalendarEvent`、`DeleteCalendarEvent` 完成用户的日程请求，沿用用户时区与明确的参会人，避免把自然语言时间直接当成 UTC。

按 `nextCursor` 继续个人或团队日程查询，保留 `syncStatus` 等不完整提示。服务提供 `ListTeamCalendarEvents` / `GetTeamAvailability` 时，团队忙闲投影不等于完整事件详情，其不透明 ID 不能用于修改个人事件。修改团队共享设置前，先用已发现的 `GetCalendarTeamSettings` 取得现状，并按当前 schema 和用户要求修改。

本地 MCP 调用日历创建后会立即写入，参会人可能立即收到邀请；不要套用 CogineX 站内“先打开编辑卡片”的流程或把成功创建称为待确认草稿。用户已经明确要求安排并邀请时接续执行，只有缺少会影响对象或时间的信息时再澄清。

提醒使用 `ListReminders`、`CreateReminder`、`UpdateReminder`、`DeleteReminder`。创建时间按当前 schema 转换；提醒交付到当前用户的 CogineX inbox，当前只支持一次性提醒，不能宣称已设置循环提醒或替别人设置。将频道线程关联为提醒时，使用其父频道 ID，不把 thread ID 当 channel ID。

`ReadActivity`、`ListNotifications` 读取动态和通知；按用户要求用 `MarkNotificationsSeen` / `MarkNotificationsDone` 标记。读取通知不自动等于用户要求清空或完成它们。

## 定时工作与 Agent 会话

提醒用于通知用户；用户要求在 CogineX 定时执行工作时，使用当前服务提供的 Routine 工具，按实际 schema 区分单次与 Cron，保留用户时区和执行目标。创建前按需查已有 Routine，已有定时工作的一次执行不应再新建相同 Routine。用返回的 Routine ID 和下一次触发时间说明实际配置。

用户要委派或跟进 CogineX 托管 Agent 时，按当前发现使用 `ListCodingAgents`、`DispatchCodingAgent`、`ReadAgentSession`、`ListAgentUpdates` 等工具；返回的会话 ID 用于后续读取或管理。托管执行不代表当前本机工作区已经改变，读取会话也不自动授权发送新指令或改变运行状态。

## Bot 与 CRM

`ListBots` 找到 Bot，按请求使用 `CreateBot`、`ConfigureBot`、`ManageBotChannelAccess`、`GetBotWebhooks`、`DeleteBot`。更新配置只传本次需要变化的字段；Bot 的稳定 handle 可能被集成和提及引用，按工具描述处理改名影响。

`IssueBotCredential` 当前仅准备创建凭据的请求，不直接生成或返回 secret。本地宿主没有 CogineX 的凭据卡片时，引导用户在 CogineX 中打开该 Bot 的设置创建 token；此工具不返回设置页链接，不自行拼接 URL，不能报告 token 已签发，也不要把现有 OAuth token 当 Bot 凭据搬用。

`ListCompanies`、`GetCompany` 读取 CRM 公司。服务提供 `CreateCompany` / `CreateContact` 时，先定位已有公司，再按用户要求新增公司或联系人。编辑公司自身属性时使用 `GetEntityProperties` / `SetEntityProperty`。

用户提到 deal、Pipeline、阶段或移动公司 / 联系人时，先用 `ListPipelines` 获取实际 Pipeline、字段名和阶段选项，再用 `FindPipelineEntries` 定位条目，按请求使用 `AddToPipeline` / `UpdatePipelineEntries`。阶段、负责人、收入属于 Pipeline 条目的字段时，不改公司自身属性；多个 Pipeline 都可能匹配时再澄清目标。CSV 导入使用当前发现的专用工具，按实际结果报告导入及部分失败范围。

## 操作结果

完成后用返回的对象、事件或消息 ID / 链接说明实际变化。不同写入工具的去重能力不同；按当前 schema 使用其操作 ID，结果不确定时先读取目标现状，避免重复发送或重复安排。插件不增加固定确认轮次或工具白名单，也不越过用户原本的工作请求扩大发送和变更范围。
