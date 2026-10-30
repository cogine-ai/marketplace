---
name: setup
description: 设置或排查 CogineX 插件账户连接，处理登录、当前账户查询、重连、切换账户与退出。
---

# CogineX 账户与连接

区分插件已安装、账户已连接、当前对象有权限这三件事。需要确认当前 CogineX 账户或 Team 时调用 `GetXConnectionContext`，按实际返回报告身份与 Team；插件的启用状态本身不能证明登录成功。

## Codex

绑定应用连接器的安装包，在 Codex App 中打开 **Plugins → CogineX → Manage**，使用当前界面的连接管理入口完成登录、重连或断开。切换账户时优先使用账户列表或账户选择器；需要新增账户时，使用 **Connect another account**（若界面提供），在浏览器中由用户登录目标 CogineX 账户。只有当前宿主不支持保留多个账户连接，或用户明确要求退出时，才先断开已有连接。

重新连接时选择需要恢复的具体账户，不影响其他已有连接。切换或新增账户后，用 `GetXConnectionContext` 核对当前操作实际使用的身份与 Team；账户已添加不等于它已经成为当前操作账户。

只有当前环境实际使用名为 `coginex` 的直接 MCP 配置时，才使用该配置的 CLI 流程：

```bash
codex mcp login coginex
codex mcp logout coginex
```

App 中管理的插件连接可能采用不同的注册方式；不要为了让上述命令可用再添加一个同名 MCP。以当前宿主识别的入口为准。


若当前安装只有直接 MCP，先通过原生 MCP 登录即可使用工具。用户需要原生账户列表时，在 ChatGPT 的 Plugins 中添加自己的 CogineX 自定义 MCP，URL 为 `https://mcp.x.cogine.ai/mcp`，使用 OAuth 自动发现；或使用所在工作区已提供的集成。只采用实际注册结果中的 App ID，不猜 ID 或复用别人的个人连接器。

通过插件自带 [打包脚本](../../scripts/prepare_package.py) 的 `--app-id <真实ID> --output <新目录> --with-marketplace` 生成绑定包，然后按原生 Marketplace 流程安装。脚本创建新包而不编辑安装缓存或凭据。已有同名插件时，验证新包版本、App 与技能后才停用旧的精确条目，并保留原来源和共享目录。Claude 已有直接 MCP 安装不必跟随迁移。

## Claude Code

在 `/mcp` 中选择插件服务 `plugin:coginex:coginex` 查看状态并认证。CLI 的对应命令为：

```bash
claude mcp login plugin:coginex:coginex
claude mcp logout plugin:coginex:coginex
```

普通重连优先在 `/mcp` 使用当前服务的重连或重新认证入口，也可重新运行 `claude mcp login`。只有用户明确要求换账户、退出，或宿主原生认证流程需要清除旧凭据时，才执行 `logout`。插件或连接更新后，在新会话中确认工具已加载。退出命令清除该宿主保存的 OAuth 凭据，不代表已退出 CogineX 网站或其他宿主。

## 判断连接问题

- 未安装或未发现入口：按插件 [README](../../README.md) 处理安装，不从旧会话猜配置或重建用户的其他 MCP 条目。
- 需要认证或返回 401：使用对应宿主的连接入口重新登录；完成后用 `GetXConnectionContext` 验证实际账户。
- 返回 403 或对象不可访问：核对当前账户、Team 和目标对象；这不等于登录失效。
- 超时或服务暂不可用：报告当前失败，不把它说成用户已退出，也不自动删除连接配置。

每个宿主通过自己的 OAuth 流程管理凭据。不要读取、复制或展示现有 token，也不要把 Codex、Claude Code 或 CogineWork 的凭据互相搬用。连接恢复后继续用户原本的工作；仅请求查看连接状态时不启动新的登录或退出操作。
