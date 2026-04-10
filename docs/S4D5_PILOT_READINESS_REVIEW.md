# S4-D-5 Pilot Readiness Review

## Goal
Create one governed readiness-review record for Sprint 4 pilot entry so operator-facing readiness can be judged against the existing `S4-D-1` through `S4-D-4` baseline before any external pilot begins.

## Scope
- review the governed pilot baseline already frozen under `S4-D-1`, `S4-D-2`, `S4-D-3`, and `S4-D-4`
- judge whether the current governed evidence is coherent enough for an operator-focused pilot-readiness decision
- make PASS versus HOLD criteria explicit before any final readiness closeout is written

## Review Baseline
- current governed snapshot: `S4-D-2026-04-10-006`
- governed stage at review start: `Sprint 4 pilot validation gate baseline`
- baseline intent:
  - `S4-D-1` freezes the pilot environment and secret contract
  - `S4-D-2` freezes the governed `POST /api/v1/pilot-smoke` round trip
  - `S4-D-3` freezes operator runbooks and failure triage
  - `S4-D-4` freezes the pilot validation gate and its deterministic entry

## Review Inputs
- [docs/HANDOFF.md](./HANDOFF.md)
- [docs/SPRINT4_JIRA_BACKLOG.md](./SPRINT4_JIRA_BACKLOG.md)
- [docs/S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md](./S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md)
- [docs/S4C5_PRODUCT_REVIEW_PASS.md](./S4C5_PRODUCT_REVIEW_PASS.md)
- [docs/S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md](./S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md)
- [docs/S4D2_PILOT_SMOKE_PATH.md](./S4D2_PILOT_SMOKE_PATH.md)
- [docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md)
- [docs/S4D4_PILOT_VALIDATION_GATE.md](./S4D4_PILOT_VALIDATION_GATE.md)
- [docs/RELEASE_PROCESS.md](./RELEASE_PROCESS.md)
- [releases/release_manifest.json](../releases/release_manifest.json)
- [releases/verify_report.json](../releases/verify_report.json)

## Review Dimensions

### 1. 环境与 profile 准入
- Governed evidence:
  - [docs/S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md](./S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md)
  - [docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md)
  - [docs/HANDOFF.md](./HANDOFF.md)
- Pass condition:
  - operator 能从 governed 文档直接确认 `pilot_local` 的必填环境项、必需 secret 名称、远程访问边界，以及 `environment_profile / profile_contract_ready / profile_contract_missing` 的判读方式
  - `pilot_local` 前提不依赖聊天历史、隐含脚本参数或本地经验补全
- Hold condition:
  - 必填字段、secret 名称或 `server_host` 远程访问边界存在不一致
  - operator 不能仅凭 governed 文档判断配置是否满足 pilot 准入

### 2. `/health` 与 `/ready` 判读语义
- Governed evidence:
  - [docs/S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md](./S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md)
  - [docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md)
- Pass condition:
  - operator 能明确确认 `environment_profile=pilot_local`，而不是只凭 `ready=true`、`state_class=READY`、`failure_category=none` 推定已满足 pilot 准入
  - operator 能稳定基于 `state_class`、`failure_category`、`reasons`、`operator_message` 判断当前是否允许进入 `POST /api/v1/pilot-smoke`
  - `READY`、`MISCONFIGURED`、`BOOTSTRAP_FAILED` 与保留态 `DEGRADED / runtime` 的解释互不混淆
- Hold condition:
  - `/health` 与 `/ready` 的语义存在冲突，或粗粒度 `status` 足以误导 operator 做出错误判断
  - 文档暗示当前 bootstrap-only code path 会产生并非现状支持的状态组合

### 3. `POST /api/v1/pilot-smoke` 成功证据
- Governed evidence:
  - [docs/S4D2_PILOT_SMOKE_PATH.md](./S4D2_PILOT_SMOKE_PATH.md)
  - [docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md)
- Pass condition:
  - 成功标准明确覆盖外层 `200 OK`、`smoke_path.path_id`、`failed_step=null`、阶段顺序、`create_case` 的 `http_status=201`、`case_id` 对齐、`persistent_case.lifecycle_status=open`
  - operator 能明确知道哪些响应摘录构成最小成功证据集
- Hold condition:
  - 成功标准缺项，或外层 HTTP code 与内部步骤成功条件之间仍有解释歧义
  - operator 无法判断哪一份证据足以证明 round trip 成立

### 4. 失败分流与 runbook 映射
- Governed evidence:
  - [docs/S4D2_PILOT_SMOKE_PATH.md](./S4D2_PILOT_SMOKE_PATH.md)
  - [docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md)
- Pass condition:
  - `readiness`、`investigate`、`create_case`、`get_case` 每个失败点都能映射到单一且明确的 triage 路径
  - `MISCONFIGURED / adapter_config`、`MISCONFIGURED / static_data`、`BOOTSTRAP_FAILED / bootstrap` 的入口没有重叠和混淆
- Hold condition:
  - 同一失败现象在多个 runbook 之间摇摆，或 operator 需要依赖开发口头解释才能完成分流
  - `smoke_path.failed_step` 与 runbook 章节之间的映射不完整

### 5. case persistence 一致性
- Governed evidence:
  - [docs/SPRINT4_JIRA_BACKLOG.md](./SPRINT4_JIRA_BACKLOG.md)
  - [docs/S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md](./S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md)
  - [docs/S4C5_PRODUCT_REVIEW_PASS.md](./S4C5_PRODUCT_REVIEW_PASS.md)
  - [docs/S4D2_PILOT_SMOKE_PATH.md](./S4D2_PILOT_SMOKE_PATH.md)
  - [docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md)
- Pass condition:
  - `create_case` 与 `get_case` 的成功和失败边界明确，`case_store_ready=true` 被视为进入 smoke path 的前提之一
  - operator 能区分“创建失败”和“创建成功但检索失败”，不会误判为 investigation 失败
- Hold condition:
  - 持久化与检索的边界不清，或 case store 故障与 readiness / investigation 故障发生混淆
  - backlog 所要求的 case persistence coherence 仍缺少受治理证据支撑

### 6. 升级材料与脱敏边界
- Governed evidence:
  - [docs/S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md](./S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md)
  - [docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md)
  - [docs/RELEASE_PROCESS.md](./RELEASE_PROCESS.md)
- Pass condition:
  - 升级材料明确要求最小红线内的 `/health`、`/ready`、`POST /api/v1/pilot-smoke` 证据、缺失字段名、缺失 secret 名称和相关日志片段
  - 脱敏边界明确禁止 token、header、cookie、connection string 与其他 secret 值泄露
- Hold condition:
  - 升级材料不足以支持 triage，或脱敏边界仍可能诱导 operator 上传敏感信息
  - 文档没有把“缺失名称可见、secret 值不可见”说明清楚

### 7. pilot validation gate 可重复性
- Governed evidence:
  - [docs/S4D4_PILOT_VALIDATION_GATE.md](./S4D4_PILOT_VALIDATION_GATE.md)
  - [docs/RELEASE_PROCESS.md](./RELEASE_PROCESS.md)
  - [releases/release_manifest.json](../releases/release_manifest.json)
  - [releases/verify_report.json](../releases/verify_report.json)
- Pass condition:
  - `py -3 scripts\\git_preflight.py --mode pilot` 作为 canonical deterministic entry 在 governed docs 中一致记录，且语义稳定
  - verification 明确证明 `S4D2`、`S4D3`、`S4D4` 已进入 manifest、review pack 和 release zip，且结果为 `PASS`
- Hold condition:
  - gate entry 存在多种不一致说法，或 `--mode release` 被误解为 pilot/full gate 的替代
  - pilot governed artifacts 未被 verification 显式证明

### 8. 治理锚点一致性
- Governed evidence:
  - [docs/HANDOFF.md](./HANDOFF.md)
  - [docs/SPRINT4_JIRA_BACKLOG.md](./SPRINT4_JIRA_BACKLOG.md)
  - [releases/release_manifest.json](../releases/release_manifest.json)
  - [releases/verify_report.json](../releases/verify_report.json)
- Pass condition:
  - snapshot、stage、`SP4-D-5` 目标、pilot validation 结果和下一步使用方式在 governed artifacts 中彼此一致
  - readiness review 可以明确建立在 `S4-D-2026-04-10-006` 这个统一 baseline 上
- Hold condition:
  - `HANDOFF`、backlog、manifest、verify report 对当前阶段和下一步目标的描述存在漂移
  - review 结论无法绑定到一个明确 snapshot

## PASS Criteria
- 没有未解决的 `P1 operator ambiguity`
- `S4-D-1` 到 `S4-D-4` 的 governed evidence 可共同支持 operator 在不依赖隐性知识的前提下完成 pilot readiness 判断
- source contracts、runtime state 语义、`POST /api/v1/pilot-smoke` 成功/失败证据、case persistence 边界、validation gate 与治理锚点彼此一致
- `releases/verify_report.json` 继续证明 pilot validation 为 `PASS`

## HOLD Criteria
- 存在任意未解决的 `P1 operator ambiguity`
- operator 仍无法仅凭 governed evidence 判断“可开始 pilot”或“必须 hold”
- `POST /api/v1/pilot-smoke` 的成功或失败证据仍需要依赖口头知识解释
- case persistence、failure triage、或 validation gate 入口存在治理漂移
- 任一 governed artifact 与 review 时的 governed snapshot 不一致

## P1 Operator Ambiguity Criteria
- operator 无法仅凭 governed 文档判断当前是否具备 pilot 启动条件
- operator 无法仅凭 `state_class`、`failure_category`、`reasons`、`operator_message`、`smoke_path.steps` 决定下一步动作
- 两份或以上 governed 文档对同一入口命令、前提条件、成功标准或失败归因给出冲突描述
- `POST /api/v1/pilot-smoke` 的成功证据仍需要依赖未写入 governed 文档的本地经验
- case store 创建与检索边界不清，足以让 operator 无法判定故障所在阶段
- governed evidence 未能让 operator 明确区分哪些升级材料可以附带、哪些 secret 值或认证材料必须排除
- governed evidence 把当前不会产出的 runtime 状态写成常规预期处理分支，导致 operator 无法区分保留态与当前受支持状态

## Review Findings
### Confirmed aligned evidence
- current governed baseline is aligned to snapshot `S4-D-2026-04-10-006`
- [releases/verify_report.json](../releases/verify_report.json) records `pilot_validation.ok=true`
- current governed evidence already defines:
  - the `pilot_local` profile contract
  - the governed `POST /api/v1/pilot-smoke` round trip
  - operator-facing failure triage and redaction boundaries
  - the canonical deterministic pilot validation entry
- current `S4-D-2` and `S4-D-3` both treat `environment_profile=pilot_local` as one of the governed prerequisites before `POST /api/v1/pilot-smoke`
- current `S4-D-3` `Pilot Smoke Success` explicitly requires `case_store_ready=true`
- current `S4-D-3` degraded placeholder wording is aligned with the current bootstrap-only runtime semantics and does not record `DEGRADED / runtime` as a normal produced state

### Open review questions / unresolved judgment points
- whether the combined `S4-D-1` through `S4-D-4` evidence is sufficient for an operator to make a pilot-readiness judgment without hidden local knowledge
- whether the current case-persistence evidence chain across `S4-C` and `S4-D` is explicit enough for pilot-use judgment, not just implementation history
- whether the current `S4-D-3` wording around smoke-path entry prerequisites is sufficiently uniform for operator use, especially around `case_store_ready=true`
- whether `S4-D-3`'s stricter `profile_contract_ready=true` prerequisite should be treated as the governing operator-facing reference when `S4-D-2` is less explicit
- whether any remaining wording ambiguity in readiness, failure triage, or escalation artifacts should still block a final PASS closeout
- this record does not yet declare final pilot readiness PASS
- explicit operator-focused review outcome remains pending against the dimensions and criteria listed above

## Preliminary Decision
- readiness review record created
- final PASS closeout pending explicit review outcome

## Next Step
- run one delta-focused `review only` pass against this review record plus the governed `S4-D-1` through `S4-D-4` inputs
- confirm whether any unresolved `P1 operator ambiguity` remains
- only after that review outcome is explicit should the project decide whether to create a governed `S4D5_PILOT_READINESS_REVIEW_PASS.md`
