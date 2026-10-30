---
name: tasks
description: 在 CogineX 中查找、创建、编辑和推进任务，设置负责人、状态、优先级、截止时间及父子关系，并回写任务讨论。
---

# CogineX 任务

使用当前加载的 CogineX 工具和实时 schema。用户给定的目标、可见性及已有授权可以直接接续；只澄清会影响执行的缺失信息。需要当前账户或 Team 时调用 `GetXConnectionContext`。连接问题仅在宿主当前已启用、可发现 `coginex:setup` 时转交该技能；否则按当前工具返回和宿主原生连接状态处理，不读取已关闭或未发现的 setup 文件。

## 找到任务并接续工作

用 `ListEntities`、`NameSearch` 或 `ContentSearch` 定位任务，从实际结果取得 ID。用 `ReadMetadata`、`ReadContent`、`GetEntityProperties` 补齐正文和字段；需要讨论背景时读取 `ListTaskChannelThreads` / `ReadTaskChannelThread`。同名任务仍不明确时再询问目标。

“我的任务”的负责人从当前身份取得，不把创建者或最近查看者当作负责人。保留列表的分页、截断或范围提示；只查到一页时不宣称覆盖全部任务。

## 创建与编辑

- `CreateXTask`：一次逻辑创建生成一个 UUID `operationId`。`visibility` 使用 `selfOnly` 或带实际 `expectedTeamId` 的 `teamVisible`；不要自行把个人任务扩大为 Team 可见。遇到不确定结果时，保留原 `operationId` 及相同创建参数恢复，避免重复新建。
- `EditDocument` 修改任务正文，`RenameDocument` 修改标题。按照实际返回区分完成修改和仍需补充的信息。
- `GetEntityProperties` 发现属性定义、选项和当前值，再用 `SetEntityProperty` 设置负责人、优先级、截止时间、父任务、子任务、Story Points 等。人员与关联任务 ID 从查询结果接力。
- 标签用 `ListTags` 查定义与选项；增减标签优先用原子的 `add_option_ids` / `remove_option_ids`。只有用户要把多选值设为明确列表时，才使用整体替换字段。

先取得创建结果中的任务 ID，再填写正文和属性。某一步失败时，报告已经完成的部分并从失败处继续，不用重新创建任务来补后续字段。

## 状态与任务更新

`GetXTaskStatus` 返回规范状态和版本；`SetXTaskStatus` 当前专用于带版本比较的 `inProgress → inReview`。其他受支持的状态编辑使用 `SetEntityProperty` 的当前 schema。出现版本冲突时先读取现状，重新判断用户的目标，不覆盖并发变更。

`PostXTaskThreadMessage` 可在任务自身发表评论；只有回复已关联的频道线程时才传 `sourceRef`，从 `ListTaskChannelThreads` 结果取得该值。一次逻辑消息使用稳定的 `operationId`；提交结果不确定时，用同一任务、来源、内容和 ID 配合 `readbackOnly` 查询，不换 ID 重发同一条消息。报告时保留返回的消息 ID 或链接。

## 删除及结果恢复

`DeleteXTask` 是服务端 Owner 权限下的软删除。其 `operationId` 只关联结果，不是持久化去重键；不能仅凭复用 ID 就断言重试安全。`incomplete` 后按服务描述读取或恢复，之后的拒绝也不能证明前一次没有删除成功。

操作沿用用户的任务请求和授权直接执行，不增加插件专有审批步骤。用实际响应区分成功、冲突、未完成和不可用；传输错误不等于业务未发生。
