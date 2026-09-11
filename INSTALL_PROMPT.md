# 发给员工 Codex 的固定安装／升级话术（0.5.0）

请帮我安装或升级 Memova“公司知识助手”Plugin，并完成首次登录前置检查。我的这条请求明确
授权你执行下面列出的 Marketplace、Plugin 和专用 MCP 登录命令；Microsoft 登录页面必须由我
本人操作：

1. 先只读运行 `codex plugin marketplace list`。
   - 如果尚未配置 `memova-company-knowledge-pilot`，运行：
     `codex plugin marketplace add gxyfred/memova-company-knowledge-plugin --ref main`
   - 如果已经配置，运行：
     `codex plugin marketplace upgrade memova-company-knowledge-pilot`
   这个公开仓库可匿名读取，不检查或要求 GitHub 登录。
2. 安装或刷新 Plugin：
   `codex plugin add memova-company-knowledge@memova-company-knowledge-pilot`
3. 只读验证 Plugin 已安装、已启用且版本至少为 `0.5.0`，并确认专用 MCP 名称为
   `company_knowledge_assistant`。不要修改或删除其他 Plugin、Marketplace 或 Codex 设置。
   如果 Codex 显示 Plugin Hook 审阅或信任提示，只审阅并信任这个 Plugin 自带的
   `SessionEnd` 本地命令；它只记录本机私有任务指针，不上传对话、不调用 MCP、不创建预览、
   不正式发布。不要替我信任其他 Plugin 的 Hook。
4. 运行 `codex mcp list` 并只检查 `company_knowledge_assistant`：
   - 如果是 `Not logged in`，运行
     `codex mcp login company_knowledge_assistant`，浏览器打开后立即停下，让我本人使用自己的
     Memova Microsoft 工作账号完成登录和 MFA。
   - 不要索取、读取、显示或保存我的密码、MFA 验证码、OAuth code、Token、Cookie 或回调内容。
   - 我确认浏览器登录完成后，再运行一次 `codex mcp list`。如果仍是 `Not logged in`，停止并报告
     `oauth_login_incomplete`；不要循环登录、反复重装或改用 SharePoint 连接器。
5. 登录状态正常后，告诉我完全退出并重新打开 Codex。重启后新建任务，再发送：
   “开始公司知识助手入职自检”。不要在登录前创建的旧任务里宣称七工具自检通过。

如果任一步失败，请停在只读诊断并告诉我确切失败步骤和状态；不要删除配置、绕过认证或使用他人账号。
如需撤销本机专用 MCP 登录，只在我明确要求时运行：
`codex mcp logout company_knowledge_assistant`。

安装和入职自检完成后，员工可按照
[`EMPLOYEE_GUIDE_ZH.md`](EMPLOYEE_GUIDE_ZH.md) 学习日常查询、提交、预览确认、更正和故障处理。
