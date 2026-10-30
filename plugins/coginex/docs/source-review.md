# CogineX 本地插件：来源与能力缺口

调研日期：2026-10-29。首版面向内部使用，把 CogineX 已有 MCP 能力提供给
Codex / Claude Code；采用宿主原生远程 MCP 连接和 OAuth。插件不另建任务服务，
也不把 CogineWork 的产品界面范围当成 CogineX 的完整能力范围。

这里记录的是源码证据。工具清单和部署状态可能变化，当前尚未完成带认证的线上
`tools/list`、实际工具调用及两种宿主的登录验收。

## CogineX 运行时清单

CogineX 参考版本固定为
[`cogine-ai/CogineX-mono@cf473c41cf6b432c3d7a0c50790a3322c0564906`](https://github.com/cogine-ai/CogineX-mono/tree/cf473c41cf6b432c3d7a0c50790a3322c0564906)。
[共享注册表](https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/crates/ai_tools/src/lib.rs#L130)
有 56 个工具，入站 MCP 的 [服务注册](https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/services/mcp_service/src/tool_service.rs#L130)
再加入 11 个身份 / 任务适配器，源码最大注册量为 67；四个 Anthropic 工具和
Subagent 由配置决定，未启用时为 62。线上数量仍需带认证发现确认。

只采用共享注册表生成的文档会漏掉这 11 个 MCP 专属工具，因此插件以运行时
发现为准。任务负责人、截止时间、优先级、父任务、子任务及 story points 已可
通过属性工具读写；任务改名可走 `RenameDocument`，无需另造重复接口。
`SetXTaskStatus` 本身限定 `inProgress → inReview` 并带 CAS 版本检查，其他
状态走服务现有的 `SetEntityProperty`，不能靠插件绕过服务契约。

## CogineWork 集成证据

参考版本固定为
[`cogine-ai/CogineWork@f06181cbc864bdc3938d45920a86a5724fdd1c48`](https://github.com/cogine-ai/CogineWork/tree/f06181cbc864bdc3938d45920a86a5724fdd1c48)。
本次只读分析，没有修改该仓库或读取现有登录凭据。

| 来源 | 对插件实现的含义 |
| --- | --- |
| [生产端点说明](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/website/service-gateway/README.md#L90) | 标准端点为 `https://mcp.x.cogine.ai/mcp`。 |
| [OAuth 适配器](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/src/coginework/app/x_connection/remote.py) | 已有 protected-resource discovery、authorization-server discovery、公开客户端动态注册、PKCE S256、`scope=mcp`、resource binding、refresh rotation 和撤销协议，可由宿主原生 MCP OAuth 接入。 |
| [身份模型](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/src/coginework/app/x_connection/models.py) | `GetXConnectionContext` 的 schemaVersion 2 区分 resource、accountIssuer、accountSubject、principal、organizationId 和 teamContext；principal 使用 `coginex\|…`。 |
| [Task MCP 适配器](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/src/coginework/app/x_tasks/remote.py) | Work 使用 Streamable HTTP 和 Bearer token，初始化后调用上游工具；任务搜索、详情和属性是多个工具的组合。 |
| [复用会话](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/src/coginework/app/x_tasks/sessions.py) | `tools/list` 需要处理分页；凭据轮换时会话身份随之失效。发生传输错误不自动重放业务写入。 |

Work 代码已调用的工具包括：

- 任务写入：`CreateXTask`、`DeleteXTask`、`EditDocument`、
  `PostXTaskThreadMessage`、`GetXTaskStatus`、`SetXTaskStatus`。
- 发现与详情：`ListEntities`、`NameSearch`、`ContentSearch`、`ReadMetadata`、
  `ReadContent`、`GetEntityProperties`、`SetEntityProperty`。
- 来源与历史：`ListTaskChannelThreads`、`ReadTaskChannelThread`、
  `SearchXTaskHistory`、`ReadXTaskHistory`、`UploadXTaskHistorySelection`。

这张清单用于证明已有集成路径，不是插件允许调用的工具白名单。宿主应从当前
上游 MCP 发现全部可用工具，保留原始参数 schema、结果和错误语义。

## 为什么直接开放上游能力

Work 的 [Task 契约投影](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/src/coginework/app/x_tasks/contract.py)
有意锁定特定产品流程，只选取上游接口的一部分来构造产品操作。
[当前任务工具](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/src/coginework/app/x_tasks/run.py)、
[Chat Link](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/src/coginework/app/x_tasks/link_tools.py)
及 [审批包装器](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/src/coginework/app/x_tasks/mutation_approval.py)
还依赖 Work 的会话、当前任务关联和审批协调器。直接复制会引入本地插件没有的
运行环境，并缩小内部同事能用到的能力。

首版因此只增加安装入口与使用指导。身份、对象权限及工具本身的业务约束继续由
CogineX 执行，宿主沿用自身的工具授权方式；插件不额外增加确认轮次、只读模式、
固定任务状态路线或工具白名单。稳定 operationId、版本冲突和不确定写入结果的
恢复仍须遵循上游返回，不把超时当作操作未发生。

## 仍需补齐或验收

| 项目 | 当前边界与后续工作 |
| --- | --- |
| 线上工具覆盖 | 源码清单不能证明生产部署具备全部工具；登录后读取完整 `tools/list`，核对数量、名称和 schema。 |
| 宿主登录和安装 | 两端隔离安装、技能与 MCP 配置加载已通过，见 [验收记录](validation.md)。仍需真实 OAuth、刷新或重登、登录后的工具发现，以及只读任务查询和实际工作中的写入验证。 |
| 上游尚未开放的操作 | 项目创建 / 移动 / 删除、通用文档删除 / 上传未作为入站 MCP 工具提供。`SendEmail` 被上游 [显式排除](https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/crates/email/src/inbound/toolset/mod.rs#L162)，Feishu `FindDocuments` / `ReadDocument` 属于 DCS 内部工具。这些需要 CogineX 服务实现或开放，插件配置不能补出不存在的接口。 |
| 本地聊天历史 | 暴露 `UploadXTaskHistorySelection` 仅提供上传接口，不等于自动取得 Codex / Claude Code 聊天记录。宿主记录定位、选择、格式转换和导出需要单独实现。 |
| 历史上传可靠性 | Work 的 [历史客户端](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/src/coginework/app/x_tasks/history_client.py) 和 [上传流程](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/src/coginework/task_history/mcp.py) 提供身份绑定、已选内容与持久 outbox 的参考。若后续做宿主历史导出，应保留凭据过滤及幂等 revision 恢复；首版不宣称已具备该采集流程。 |

## Macro 关键词需要区分处理

- Work 的任务、身份连接和历史 MCP 路径未发现 Macro 品牌字串。
- CogineX 的工具 schema 和 `SelfKnowledge` 当前正文已使用 CogineX；其链接的
  [变更记录](https://github.com/cogine-ai/CogineX-mono/tree/cf473c41cf6b432c3d7a0c50790a3322c0564906/apps/docs/changelog)
  仍有 Macro 标题 / 描述与 `macro-inc/macro` 来源链接，可能经阅读文档进入输出。
  [上游参考页](https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/apps/docs/coginex/upstream-reference.mdx)
  则有意保留 Macro 的工程来源说明；
  [品牌检查脚本](https://github.com/cogine-ai/CogineX-mono/blob/cf473c41cf6b432c3d7a0c50790a3322c0564906/apps/web/scripts/check-visible-brand.ts)
  还留有已不匹配当前 SelfKnowledge 的 `docs.macro.com` 例外，需要清理例外或重新说明用途。
- [主题登记表](https://github.com/cogine-ai/CogineWork/blob/f06181cbc864bdc3938d45920a86a5724fdd1c48/console/src/styles/cogineXThemeRegistry.generated.ts#L67)
  保留 `Macro Light → CogineX Light`、`Macro Dark → CogineX Dark` 兼容别名，
  相应测试也保留旧名。这属于品牌迁移兼容，不宜为了新插件直接删除。
- Office 文档工具中的 `LibreOffice macro` 以及 OOXML `macro` 属性表示“宏”
  技术能力，不是产品品牌；不应机械替换为 CogineX。
- Rust 的 `macro_rules!` 与 Cargo 宏依赖也属于语言和构建术语，保留原名。

新插件对外名称、提示和安装入口统一使用 CogineX。上游工具返回或来源字段若仍含
旧品牌，保留协议原值并报告具体位置，再按字段的兼容要求调整。

## 2026-10-30 账户体验补齐

- Marketplace 候选版升级为 0.2.0，增加 5 个独立技能和原生 Codex App 映射。
- 对应 [Profile 服务 PR #879](https://github.com/cogine-ai/CogineX-mono/pull/879) 最终提交 `a647d5250761831f13454aa5375af9ae150fb8d4` 已基于 `8d993421f48ec80b373c7af7b7749fa7176dd569` 更新；复用既有 active-account 查询，不增加 SQL 或依赖。
- Profile 部署后的最大源码注册集合增加为 68；不能把未部署改动当作当前线上工具。
- 新发现的 Macro 工具配置耦合：该 fork 的 GitHub CLI 默认仓库解析为 `macro-inc/macro`。本次 PR 命令显式使用 `--repo cogine-ai/CogineX-mono`；没有向上游创建 PR。
- 账户与 Skill 控制的宿主差异见 [账户说明](accounts.md)，实际验收状态见 [验收记录](validation.md)。

账户分发补充：默认源码 App 映射为空；本机已验收绑定包的个人 App ID 仅保留在本地分发回执。其他个人 / 工作区按实际连接器生成各自包，不将个人连接器可见性误认为团队共享。
