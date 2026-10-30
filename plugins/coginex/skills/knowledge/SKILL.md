---
name: knowledge
description: 搜索和读写 CogineX 文档，结合任务历史、讨论和来源回答问题，或整理并上传用户选定的历史证据。
---

# CogineX 文档与知识

根据问题选择当前加载的 CogineX 搜索与读取工具。查资料不需要先创建任务。连接问题仅在宿主当前已启用、可发现 `coginex:setup` 时转交该技能；否则按当前工具返回和宿主原生连接状态处理，不读取已关闭或未发现的 setup 文件。

## 搜索与读取

`NameSearch` 定位标题、人员已知引用或对象名称，`ContentSearch` 检索正文，`ListEntities` 按类型、属性、项目等当前 schema 支持的条件浏览。需要时组合名称与内容搜索，按实际 ID 合并结果。项目可用于发现和组织上下文，不能据此假定存在项目创建、移动或删除工具。

用 `ReadMetadata`、`ReadContent` 读取文档和任务，按内容需要调用 `ReadDesign`、`ReadPhotoshopDocument`、`ReadIllustratorDocument`。讨论背景使用 `ReadDocumentDiscussion` / `ReadDocumentDiscussionThread`，频道背景使用当前的频道读取工具。不要把搜索摘要当作已经读过全文。

保留结果的分页、截断和访问范围。需要进一步内容时按工具当前支持的读取方式继续；没有搜到证据只能说明本次检索未命中，不能据此断言资料从未存在。

## 创建与维护文档

`CreateDocument` 创建文档，`EditDocument` 修改正文，`RenameDocument` 改标题；属性与标签使用 `GetEntityProperties`、`SetEntityProperty`、`ListTags`。先沿用用户明确的文档、项目和可见性，调用时按实时 schema 填参数。写入后报告实际文档 ID、链接和完成范围，不把修改请求已受理当成正文已经变更。

普通修改沿用用户已有请求直接完成。上传二进制文件、通用文档删除或其他操作若未在当前服务暴露，明确指出对应缺口，不以创建空文档等近似操作冒充完成。

## 任务历史与来源

`SearchXTaskHistory` 查找历史证据，`ReadXTaskHistory` 读取任务历史修订。使用返回的任务、revision、内容与来源链接回答；区分原文事实与自己的推断。分页不是完整时间线快照，不把一页结果或排序候选说成所有历史。

`UploadXTaskHistorySelection` 接收显式选定、已经做过凭据过滤的源记录修订。用户要求保存本地历史时，先明确所选内容，依实时 schema 准备 selection，并保留源记录标识、修订号和选区标识用于恢复；遇到冲突先核对源记录和内容，不把冲突回包当作上传成功。

插件尚未实现 Codex / Claude Code 原生聊天记录的自动采集与同步。能调用上传工具，不代表已取得本地转录或已建立持续录制；缺少可用源记录时说明所缺输入。不要读取或上传登录凭据。

需要了解 CogineX 本身时可用 `SelfKnowledge`，但其链接的上游参考或历史说明不自动定义当前产品能力。引用实际读取到的来源，遇到 Macro 等旧品牌词时指出具体位置和语境，不静默改写原始证据。
