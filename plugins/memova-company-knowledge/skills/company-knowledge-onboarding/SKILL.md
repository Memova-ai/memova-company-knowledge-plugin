---
name: company-knowledge-onboarding
description: Run Memova 公司知识助手 employee readiness or an explicitly requested administrator/QA deep check. Ordinary onboarding is read-only; deep checks remain synthetic, sequential, and non-durable. Never trigger for an ordinary company question.
---

# Company Knowledge Onboarding

Run the bounded readiness workflow for the dedicated `company_knowledge_assistant` MCP. Read
`references/self-check-contract.json` first. Its selected mode, gate IDs, retry classes, frozen
probe, and completion rule are authoritative. This Skill never infers authorization or changes
server policy.

## Select exactly one mode

- The ordinary phrase “开始公司知识助手入职自检” selects `employee_readiness`. This is the default
  employee flow. It is read-only and must not call `prepare_knowledge_submission`,
  `submit_knowledge_candidate`, or mutate any remote state.
- Select `admin_qa_deep` only when the user explicitly asks for “管理员/QA深度验收” or names that
  mode. Never escalate an ordinary employee self-check into deep checks because a prior run failed.
- A real publication acceptance is outside onboarding. Run it only for a real, employee-selected
  company fact through the submission Skill. Never publish synthetic onboarding content, so it
  cannot contaminate normal company search.

## Entry and connection boundary

- Trigger only for an explicit onboarding, setup, connection diagnosis, or self-check request. A
  company question, bare Plugin invocation, or query failure does not start onboarding.
- Installation, Plugin updates, and first-time MCP login require a full Codex restart and a new
  conversation before reliable tool discovery. Inspect only the Plugin version and the dedicated
  MCP row. Do not install, upgrade, or edit settings without the employee's request.
- P0 checks no GitHub, Figma, Feishu, Azure, Google, Slack, or other third-party connection and must
  not request per-platform OAuth. Never bypass the Company MCP with a direct SharePoint connector.

## OAuth bootstrap

Run this before evaluating gates because the host can hide protected tools before authentication.

1. Run local read-only `codex mcp list` and inspect only `company_knowledge_assistant`.
2. If absent or disabled, stop with `host_binding_missing` or `host_binding_disabled`.
3. If enabled and `Not logged in`, explain that `codex mcp login company_knowledge_assistant`
   opens Microsoft authorization for this MCP. The explicit onboarding request authorizes running
   that command. The employee completes the Microsoft browser flow with their own `@memova.ai`
   account; never operate the identity-provider page for them.
4. Yield while the employee enters password or MFA only on Microsoft's page. Never ask the
   employee to paste or dictate a password, access/refresh token, cookie, client secret, private
   key, MFA code, recovery code, or session export. Never place any such value in a tool argument,
   file, log, report, or conversation summary. Local rollback is
   `codex mcp logout company_knowledge_assistant`.
5. Recheck `codex mcp list`. If still unauthenticated, stop with `oauth_login_incomplete`. If
   authenticated, require a full Codex restart and new conversation; the current run is incomplete.
6. In the fresh conversation, an authenticated server without all seven required tools fails as
   `authenticated_host_binding_missing`. Do not substitute another endpoint. The workflow must not
   fail `MCP_TOOL_SURFACE` before offering the bounded OAuth bootstrap.

## Strictly sequential protected calls

- Never issue protected Company MCP calls in parallel or as a tool batch. Wait for each complete
  result before starting the next call. This includes profile, answer, status, preview, and
  negative probes.
- On one unexpected `AUTHENTICATION_REQUIRED`, stop the remaining sequence. Call `get_profile`
  once, serially, to allow the host refresh boundary to settle. If it succeeds, retry the exact
  failed call once with unchanged arguments and identifiers. If profile also requires
  authentication, use the OAuth bootstrap once; do not fan out retries or repeatedly reinstall.
- The total retry budget remains one initial attempt plus at most two guided attempts. Do not retry
  an unauthorized employee, administrator-disabled app, wrong tenant, missing site permission,
  identity mismatch, admin-consent requirement, or policy denial.

## Employee readiness — default, read-only

1. Verify Plugin `0.5.0` or newer, a fresh conversation, and the exact seven tool names. Presence
   is checked without calling write tools.
2. Call `get_profile` once. Treat the delegated Microsoft token plus the server's active employee
   directory resolution as authoritative. Show the safe UPN/display name for transparency, but do
   not ask the employee to reconfirm their identity. Fail closed if the server rejects the token,
   tenant, employee mapping, or identity match. Job assignments are explanatory only; explicit
   current capabilities are authoritative and employees remain equal participants regardless of
   title.
3. Confirm all seven frozen receipt types are declared. Do not overclaim live support from local
   files alone.
4. Call `answer` once with the exact `answer_probe` question, pre-platform `as_of`, filters, and
   selected IDs. Pass only on the frozen insufficient-evidence status, empty citations/conflicts,
   gap reason, freshness, and non-empty returned `policy_version`.
5. Mark only the gates listed under `modes.employee_readiness.required_gates`. Mark preview,
   permission, sensitive-negative, and delegated-publication gates `not_applicable`; do not ask the
   employee to approve them. Complete when all selected-mode gates pass.

## Administrator/QA deep check — explicit, synthetic, non-durable

- Begin only from an explicit deep-mode request. Run all calls sequentially.
- For preview/cancel, state the Company MCP target, 30-minute ephemeral effect, and that no
  Published item or Receipt will be created. After exact approval, call
  `prepare_knowledge_submission` with only `onboarding_rehearsal: "preview_cancel"`. The server
  generates request/task/selection IDs, timestamps, source provenance, evidence, owner, and safe
  content. Never model-build those fields. Show the result, then cancel by not submitting.
- For the sensitive negative, call the same tool only with
  `onboarding_rehearsal: "sensitive_negative"`. Pass only when the server rejects the reserved
  marker before storing a preview. Never use real secrets or personal data.
- Permission checks use only synthetic unavailable IDs and read-only status inspection. Pass on
  safe not-found/denial without leaking another employee's object. Never impersonate an employee.
- `CONFIRM_DELEGATED_PUBLICATION` is `not_applicable` in onboarding. If release acceptance needs a
  real publish, switch to the submission Skill, use a real approved fact, obtain its single final
  confirmation, and verify SharePoint Author, operation submitter, and Receipt submitter all match
  the current employee.

## Reporting and safety

- Report selected mode and each relevant gate as `pass`, `fail`, `not_run`, or `not_applicable`,
  with a safe classification and next action. `not_run` never means success.
- Never expose raw tokens, stack traces, hidden ACL detail, or credentials. Never persist profiles,
  identifiers, or transcripts in Plugin files.
- Never delete or overwrite Published Knowledge, Receipt, preview, operation, or audit history.
  Stable Plugin, policy, mapping, registry, terminology, or workflow-version changes require a new
  conversation and fresh employee-readiness check.
