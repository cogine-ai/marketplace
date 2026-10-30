---
name: collaboration
description: 使用 CogineX 处理频道沟通、日历、提醒、通知、邮件、通话记录、Bot 和 CRM 工作。
---

# CogineX 协作

按用户本次工作组合当前 CogineX 工具，沿用目标与已有授权；工具权限和参数以实时服务描述为准。连接或账户问题仅在宿主当前已启用、可发现 `coginex:setup` 时转交该技能；否则按当前工具返回和宿主原生连接状态处理，不读取已关闭或未发现的 setup 文件。

## 沟通与工作上下文

- 用 `ListEntities` 查频道、讨论、邮件或其他对象；需要团队成员时用 `ListTeamMembers`。不要把频道 ID、线程 ID、消息 ID 混用。
- `ReadChannelMessages`、`ReadChannelThread`、`ReadChannelMessageContext` 读取频道背景，`ReadChat` 读取已有 AI 对话。发送或回复使用 `SendChannelMessage`，按实际结果中的频道与线程 ID 定位；用户只要求阅读或起草时不发送。
- 邮件可用 `ListInboxes`、`ListLabels`、`GetThread`、`UpdateThreadLabels` 读取和整理。当前源码未向入站 MCP 开放 `SendEmail`；只有当前服务实际提供发送工具时才能据其 schema 发送，不能把标签更新说成邮件已发出。
- `ListCallRecords` / `ReadCallRecord` 查通话记录；引用实际返回的记录与内容，不把列表条目当作已读逐字稿。

## 日历、提醒与通知

先用 `ListCalendars` / `ListCalendarEvents` 取得需要操作的日历或事件。通过 `CreateCalendarEvent`、`UpdateCalendarEvent`、`DeleteCalendarEvent` 完成用户的日程请求，沿用用户时区与明确的参会人，避免把自然语言时间直接当成 UTC。

本地 MCP 调用日历创建后会立即写入，参会人可能立即收到邀请；不要套用 CogineX 站内“先打开编辑卡片”的流程或把成功创建称为待确认草稿。用户已经明确要求安排并邀请时接续执行，只有缺少会影响对象或时间的信息时再澄清。

提醒使用 `ListReminders`、`CreateReminder`、`UpdateReminder`、`DeleteReminder`。创建时间按当前 schema 转换；提醒交付到当前用户的 CogineX inbox，当前只支持一次性提醒，不能宣称已设置循环提醒或替别人设置。将频道线程关联为提醒时，使用其父频道 ID，不把 thread ID 当 channel ID。

`ReadActivity`、`ListNotifications` 读取动态和通知；按用户要求用 `MarkNotificationsSeen` / `MarkNotificationsDone` 标记。读取通知不自动等于用户要求清空或完成它们。

## Bot 与 CRM

`ListBots` 找到 Bot，按请求使用 `CreateBot`、`ConfigureBot`、`ManageBotChannelAccess`、`GetBotWebhooks`、`DeleteBot`。更新配置只传本次需要变化的字段；Bot 的稳定 handle 可能被集成和提及引用，按工具描述处理改名影响。

`IssueBotCredential` 当前仅准备创建凭据的请求，不直接生成或返回 secret。本地宿主没有 CogineX 的凭据卡片时，引导用户在 CogineX Bot settings 中完成，不能报告 token 已签发，也不要把现有 OAuth token 当 Bot 凭据搬用。

`ListCompanies`、`GetCompany` 读取 CRM 公司。阶段、负责人、收入等通过 `GetEntityProperties` / `SetEntityProperty` 编辑；团队可以定制阶段，因此从实际结果取得选项 ID，不照搬历史枚举或假设另有公司创建接口。

## 操作结果

完成后用返回的对象、事件或消息 ID / 链接说明实际变化。发送消息、日历写入等没有统一的 `operationId` 去重能力；结果不确定时先读取目标现状，避免重复发送或重复安排。插件不增加固定确认轮次或工具白名单，也不越过用户原本的工作请求扩大发送和变更范围。
