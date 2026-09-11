# Memova 公司知识助手（公开分发）

本公开仓库只分发公司知识助手 Plugin 和 Codex Marketplace 元数据，不包含后端代码、
生产凭证或公司知识数据。

## 最简单的员工安装方式

员工把 [`INSTALL_PROMPT.md`](INSTALL_PROMPT.md) 中整段文字复制给自己的 Codex，
让 Codex 完成安装和验证。仓库可以匿名只读访问，不要求员工登录 GitHub，也不需要理解
`git clone`。

所有员工现在都可按统一流程参加安装和真实使用测试。第一次使用、日常查询、本人委托知识发布、
跨员工验证、更正和常见故障处理，请直接阅读
[`EMPLOYEE_GUIDE_ZH.md`](EMPLOYEE_GUIDE_ZH.md)。该指南面向完全不了解 GitHub、Plugin、MCP
或 OAuth 的员工。

安装／升级话术会先刷新公开 Marketplace 和 Plugin，然后运行 `codex mcp list`。如果专用 MCP
显示 `Not logged in`，Codex 会执行明确的 `codex mcp login company_knowledge_assistant` 命令；
员工本人在 Microsoft 页面完成登录和 MFA。Codex 不会代为操作身份页面，也不会要求员工把密码、
验证码、Token、Cookie 或 OAuth 回调内容发到对话中。

首次登录成功后需要完全退出并重新打开 Codex，再新建一个任务并发送：

> 开始公司知识助手入职自检

受保护的 MCP 工具可能在登录前完全不出现在任务工具面，因此 `0.4.1` 不再依赖首次查询自动弹出
登录。它会先完成显式登录，再在重启后的新任务中验证七个工具。

`0.5.0` 增加“大任务完成后的知识沉淀检查”。当 Codex 真正完成一项有稳定证据、可复用且适合
公司内部公开的重大结果时，Plugin 会安静地去重和检查敏感性；符合条件时可自动创建一次临时
预览，但仍必须由员工核对完整服务器预览并确认一次，才会正式发布。Plugin 还包含一个
`SessionEnd` 本地兜底 Hook：它只在本机私有目录记录已结束任务的指针，不上传对话、不调用 MCP、
不创建预览也不发布。安装或升级时，如 Codex 要求审阅 Plugin Hook，请核对后信任这条本地命令。

`0.4.2` 为发布预览增加完整的机器可读候选契约。Plugin 与后端 MCP 使用同一份字段、枚举和证据
结构；不完整候选会返回安全字段路径，而不会要求员工或 Codex 猜测服务端字段。

`0.4.3` 为当前 Codex 任务中的 `business_status` 增加服务端确定性收集。员工只选择状态事实；
来源定位、版本、证据锚点和知识所有者由后端生成，不需要为了当前任务证据额外提供 HTTPS 链接。

`0.4.4` 修复发布确认的幂等身份绑定：最终提交必须原样复用服务器预览返回的
`client_request_id`、`preview_id` 和 `preview_payload_sha256`，不能在确认发布时生成新的请求 ID。
后端幂等保护保持不变。

`0.4.5` 移除创建临时预览前的重复确认。员工明确要求提交确定内容，或从评估结果中明确选择一个
候选后，系统直接创建一次30分钟预览；员工只需在看到完整服务器预览后确认一次正式发布。预览
哈希、请求身份、审计、本人委托身份和禁止自动发布等保护保持不变。

`0.4.7` 修复入职自检：查询探针改为固定的前平台空快照，并核验 MCP 返回的实际策略版本；合成
预览取消和当前任务 `general_knowledge` 改由服务端生成来源定位、版本、证据锚点、哈希和知识
所有者，不再要求员工或 Codex 猜测 HTTPS 来源。

`0.4.8` 将普通员工入职自检改为只读短流程；预览和负向检查只在明确要求的管理员/QA 深度模式中
串行运行，且不发布合成知识。服务端生成演练输入、从本人所有的预览绑定提交请求身份、拒绝五个
保留敏感标识，并为新发布返回 SharePoint Author 安全读回。因此普通入职不再制造测试知识，也不
需要反复批准或让 Codex 拼装机器字段。

`0.4.9` 移除入职自检中的重复身份确认。Microsoft 委托登录令牌和服务端在职员工目录解析共同决定
当前身份；安全 UPN/姓名只用于透明展示，员工无需再回复“这是我本人”。服务端发现错误租户、无效
员工映射或身份不匹配时仍然关闭失败。

## 管理员/高级用户手动安装

```bash
codex plugin marketplace add gxyfred/memova-company-knowledge-plugin --ref main
codex plugin add memova-company-knowledge@memova-company-knowledge-pilot
codex mcp login company_knowledge_assistant
```

如果 Marketplace 已经存在，先用
`codex plugin marketplace upgrade memova-company-knowledge-pilot` 刷新快照。登录后完全重启 Codex。
