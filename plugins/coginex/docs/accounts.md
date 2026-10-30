# 账户、连接与 Skill 开关

插件声明能力及连接入口，宿主管理每个用户的授权状态。安装插件、连接账户、启用 Skill，以及拥有某个实体的访问权限，应分别验证。

## Codex

源码中的 `.app.json` 使用空映射，避免把某个人私有的连接器固定给全体同事。使用 ChatGPT 账户的 Codex 可以通过已绑定包里的 `coginex` 应用连接器进入原生账户管理；真实 ID 来自官方注册结果，是集成标识，不是账号或凭据。本机验收包已记录其个人绑定，授权结果见验收文档。

宿主提供账户列表、连接另一个账户、选择及断开等操作。每次工具调用使用被选连接的凭据，服务端继续执行当前账户的 Team / 实体权限。Codex 当前路由会在 App 路径生效时隐藏同名直接 MCP；没有 App 路由时保留直接 MCP，避免重复加载。

直接 MCP 模式下，当前配置确实存在 `coginex` 服务时，可以运行 `codex mcp login coginex` 或 `codex mcp logout coginex`。不要为了让命令可用再添加一个同名服务。

个人连接器不自动对同事开放。团队分发前，需要将连接器定义提供给相应工作区；各人再连接自己的 CogineX 账户。`.app.json` 不替代工作区发布，也不包含可传给同事使用的个人授权。


包维护者或用户可运行 `scripts/prepare_package.py --app-id <真实ID> --output <新目录> --with-marketplace` 生成绑定版本；输入 ID 必须来自自己或所在工作区实际可访问的连接器。它只改新目录中的 Codex App 引用，Claude 的直接 MCP、版本与五个 Skill 保持一致。`--direct-mcp` 生成没有 App 引用的直接包。来源回执只含模式、连接器 ID 和源码树哈希，不包含账号、token 或个人路径。

已有同名插件时，先安装并读回新包的版本、App 映射与所需技能，再通过宿主停用旧的精确插件条目；不手工删除缓存、改写旧 Marketplace 来源或影响其他宿主目录。

## Claude Code

Claude Code 使用插件的直接 HTTP MCP 和自己的 OAuth 凭据。在 `/mcp` 中选择 `plugin:coginex:coginex`，或运行：

```bash
claude mcp login plugin:coginex:coginex
claude mcp logout plugin:coginex:coginex
```

终端的 MCP 管理界面不同于 Codex 的 App 账户页面。使用宿主实际提供的连接和重连入口；不复制 Codex、CogineWork 或浏览器保存的 token。

## 账户标签与凭据

配套 CogineX 服务变更新增只读 `GetProfile`，接受空参数并返回当前已验证账户的 `{id, email}`。`id` 是稳定的账户 UUID，邮箱只用于显示；工具用 `_meta["openai/profile"]: true` 标记，发布精确输出 schema。部署并刷新连接器前，不将其视为线上已有能力。

Profile 改善账户标签和重新连接识别，本身不创建账户管理界面，也不是多账户功能的启用开关。登录与凭据由宿主管理，不存入插件源码。两种宿主分别授权，插件不跨宿主复制 token。

断开一个连接、清除本地宿主凭据、退出 CogineX 网站，以及服务端撤销 refresh family，有不同作用。当前 `/revoke` 契约包含 resource 参数，不能仅凭本地 logout 成功就宣称服务端 revoke 已验收。

## Skill 开关

Codex 使用原生 Skill 配置。关闭某个 Skill 后，路由器不会自动加载其文件；再次启用后恢复发现。关闭 Skill 不等于禁用相关 MCP 工具，工具和服务仍由各自的宿主配置控制。

Claude Code 2.1.311 的 `skillOverrides` 不适用于插件内 Skill，原生入口管理的是插件整体启停。五个 Skill 均可按命名空间独立调用，但不能把它描述为支持与 Codex 一致的独立开关，也不通过权限 deny 规则或打包时禁用来伪装同样的界面。

## 标准与验收

- [OpenAI 插件打包](https://developers.openai.com/plugins/build/plugins)
- [注册应用 ID 格式](https://learn.chatgpt.com/docs/enterprise/plugin-management#reference-an-existing-app-with-app-json)
- [多账户与 Profile](https://developers.openai.com/plugins/build/auth#support-multiple-accounts)
- [Claude Code Skill 设置边界](https://code.claude.com/docs/en/skills#override-skill-visibility-from-settings)
- [实际验收记录](validation.md)
