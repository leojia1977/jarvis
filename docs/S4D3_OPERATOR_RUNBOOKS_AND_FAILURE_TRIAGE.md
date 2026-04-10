# S4-D-3 Operator Runbooks and Failure Triage

## Goal
为 Sprint 4 pilot runtime 提供一份最小 operator runbook 入口，用现有合同字段定位常见 readiness、misconfiguration、bootstrap 和 pilot smoke failure，不把本阶段扩写成完整运维手册。

## Scope
- 覆盖 `pilot_local` 运行前预检。
- 覆盖 `GET /health` 与 `GET /ready` 的最小判读规则。
- 覆盖 `MISCONFIGURED / adapter_config`、`MISCONFIGURED / static_data`、`BOOTSTRAP_FAILED / bootstrap`。
- 覆盖 `POST /api/v1/pilot-smoke` 的成功校验与分阶段失败 triage。
- 覆盖 case store 相关失败与升级材料要求。
- 为保留态 `DEGRADED / runtime` 留出明确占位处理。

## Non-Goals
- 不新增 runtime state、`failure_category` 或环境契约字段。
- 不把本文件扩写成完整值班、监控、告警或恢复手册。
- 不改写 `AdapterResult`、case 语义或 pilot smoke 合同。

## Lookup Keys
- 运行态 triage 的主键是 `state_class`。
- 故障分类的主键是 `failure_category`。
- 详细定位优先看 `reasons`，再看 `operator_message`。
- `pilot_smoke` 的阶段定位优先看 `smoke_path.failed_step` 与 `smoke_path.steps`。
- `/health.status` 只是粗粒度活性信号；需要精确判断时以 `state_class` 为准。

## Secret Safety
- 所有排障材料都必须脱敏。
- 允许记录缺失的 secret 名称，例如 `required_secret_names` 或 `profile_contract_missing` 中的名称。
- 不允许记录或上传任何 `*_auth_token`、`llm_api_key`、Cookie、Authorization header、原始连接串或其他 secret 值。

## Preflight
- 确认运行 profile 目标是 `pilot_local`，且 `runtime_mode=production`。
- 确认 `static_data_path` 已显式设置，且本次 pilot 不依赖 `mock_data_path` 兜底。
- 确认 `siem_vendor` 仅为 `splunk_like` 或 `elastic_like`，不能使用 `generic_http`。
- 确认 `siem_base_url` 已配置，且 `siem_auth_token` 已按 secret 注入，但不要输出 token 值。
- 确认 `edr_source_mode` 已显式设置；只有当 `edr_source_mode=api` 时才要求 `edr_auth_token`。
- 确认 `case_store_backend=sqlite_local`，且 `case_store_path` 可写。
- 如需远程 analyst 或 manager 访问，确认 `server_host` 不是默认 `127.0.0.1`。
- 先执行 `GET /ready`，再决定是否进入 `POST /api/v1/pilot-smoke`。

## Health And Readiness
- 先看 `GET /health`，确认进程仍可响应。
- 再看 `GET /ready`，这是是否允许进入 smoke path 的准入判断。
- 当 `ready=true`、`state_class=READY`、`failure_category=none` 时，才进入 `POST /api/v1/pilot-smoke`。
- 当 `/health.status=degraded` 但 `state_class=READY` 以外时，不要继续依赖粗粒度 `status`，应直接转到对应 runbook。
- 当 `ready=false` 时，用 `state_class + failure_category + reasons + operator_message` 进行分类，不要靠本地经验猜测。

## Misconfigured Adapter Config
- 触发条件：`state_class=MISCONFIGURED` 且 `failure_category=adapter_config`。
- 常见信号：
  - `reasons` 包含 `production_adapter_not_configured`
  - `pilot_local` 缺少生产 SIEM 必需配置
  - `siem_vendor` 非 `splunk_like` 或 `elastic_like`
  - `edr_source_mode=api` 但未注入 `edr_auth_token`
- 操作步骤：
  1. 对照 `docs/S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md` 逐项核对 `pilot_local` 契约。
  2. 只核对字段名称、是否存在、值是否合法，不输出任何 secret 值。
  3. 修正配置后重新执行 `GET /ready`。
  4. 只有在 `/ready` 回到 `READY / none` 后，才重新执行 `pilot_smoke`。

## Misconfigured Static Data
- 触发条件：`state_class=MISCONFIGURED` 且 `failure_category=static_data`。
- 常见信号：
  - `reasons` 指向 `static_data_path` 缺失或不可用
  - `reasons` 指向不受支持的静态数据 source mode
  - 生产模式下本地 governed 静态数据不存在
- 操作步骤：
  1. 确认 `static_data_path` 已显式配置且指向本次运行应使用的数据根。
  2. 确认静态数据相关 source mode 使用受治理的现有取值。
  3. 重新执行 `GET /ready`，确认 `state_class` 不再是 `MISCONFIGURED / static_data`。
  4. 不要用 `mock_data_path` 临时替代 `pilot_local` 的显式 `static_data_path` 契约。

## Bootstrap Failed
- 触发条件：`state_class=BOOTSTRAP_FAILED` 且 `failure_category=bootstrap`。
- 常见信号：
  - `reasons` 包含 `bootstrap_failed:*`
  - `operator_message` 明确指向运行时构建 investigation pipeline 失败
- 操作步骤：
  1. 先确认这不是 `adapter_config` 或 `static_data` 的伪装问题。
  2. 收集脱敏后的 `/health` 与 `/ready` 响应。
  3. 收集 `secupilot.runtime` 相关日志片段，保留 `event`、`service`、`mode`、`failure_category`、`reasons` 或 `reason`。
  4. 将其视为代码、依赖或运行时构建异常升级，不要在未定位根因前反复重试。

## Pilot Smoke Success
- 执行前提：`GET /ready` 已返回 `ready=true`、`state_class=READY`、`failure_category=none`。
- 发送 governed `POST /api/v1/pilot-smoke` 请求体。
- 成功校验至少包括：
  - 外层响应 `200 OK`
  - `smoke_path.path_id=pilot_local_production_case_round_trip`
  - `smoke_path.failed_step=null`
  - `smoke_path.steps` 顺序为 `readiness -> investigate -> create_case -> get_case`
  - `smoke_path.steps[2].http_status=201`
  - 返回 `case_id`
  - `persistent_case.case_id` 与顶层 `case_id` 一致
  - `persistent_case.lifecycle_status=open`

## Pilot Smoke Failure Triage
- 先看 `smoke_path.failed_step`，再看对应 `smoke_path.steps[*].http_status`。
- 当 `failed_step=readiness` 时：
  - 回到 `Health And Readiness`，并根据 `state_class / failure_category` 转到 `Misconfigured Adapter Config`、`Misconfigured Static Data` 或 `Bootstrap Failed`。
- 当 `failed_step=investigate` 时：
  - 若对应 `http_status=400`，按请求校验失败处理，优先检查请求体是否仍符合 governed `intent / user_input / time_range` 约束。
  - 若对应 `http_status=503` 或 payload 继承 not-ready 语义，回到 readiness 分类，不要把它误判为 case store 故障。
- 当 `failed_step=create_case` 时：
  - 说明 readiness 与 investigation 已完成，故障点在持久化构建或写入。
  - 优先转到 `Case Store Failures`。
- 当 `failed_step=get_case` 时：
  - 说明持久化已被尝试，检索阶段失败。
  - 同样转到 `Case Store Failures`，并重点比对 `create_case` 步骤是否已返回 `201`。
- 不要只看外层 HTTP code；只要 `failed_step` 非空，就不能把本次 smoke 判为成功。

## Case Store Failures
- 主要覆盖 `pilot_smoke` 中的 `create_case` 与 `get_case` 阶段失败。
- 先确认 `case_store_backend=sqlite_local` 与 `case_store_path` 契约未漂移。
- 当 `create_case` 失败时：
  - 记录 `smoke_path.steps[2]` 的 `http_status`
  - 记录顶层错误码或错误文本的脱敏版本
  - 确认这是持久化失败，不要回退去怀疑 investigation 已失败
- 当 `get_case` 失败时：
  - 先确认 `smoke_path.steps[2].http_status=201`
  - 再记录 `smoke_path.steps[3]` 的 `http_status`
  - 重点说明这是“创建后检索失败”，而不是“创建未发生”
- 如果 `reasons` 或 `operator_message` 明确指出 case store 不可用，应按持久化依赖故障升级。

## Escalation Artifacts
- 升级时至少附带以下脱敏材料：
  - 当前 snapshot ID、分支名、commit hash
  - `GET /health` 响应摘录
  - `GET /ready` 响应摘录
  - `POST /api/v1/pilot-smoke` 的脱敏请求体与响应摘录
  - `smoke_path.failed_step`
  - `smoke_path.steps` 摘录
  - `state_class`
  - `failure_category`
  - `reasons`
  - `operator_message`
  - `secupilot.runtime` 相关日志片段
- 只记录缺失的 secret 名称，不记录 secret 值。
- 如需说明环境问题，只记录字段名、是否缺失、是否合法，不记录敏感内容。

## Degraded Runtime Placeholder
- 触发条件：`state_class=DEGRADED` 且 `failure_category=runtime`。
- 当前 Sprint 4 bootstrap-only readiness 路径通常不应把启动问题落到这个组合。
- 若在 pilot readiness 或 smoke path 中出现该组合，应将其视为保留态被意外触发。
- 处理方式：
  1. 收集 `state_class / failure_category / reasons / operator_message`。
  2. 收集脱敏日志与 smoke 证据。
  3. 直接升级，不自行发明新的本地 workaround，也不要把它重新解释成 `READY`、`MISCONFIGURED` 或 `BOOTSTRAP_FAILED`。

## Acceptance Intent
- operator message 分类可以映射到明确 runbook 章节。
- runbook 不依赖隐藏本地知识。
- 所有排障材料要求都遵循 secret 脱敏规则。
