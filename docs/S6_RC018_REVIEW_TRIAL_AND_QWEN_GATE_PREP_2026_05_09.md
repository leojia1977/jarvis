# S6 RC-018 Review, Customer Trial, And Qwen Gate Prep

Date: 2026-05-09

Status: PREPARED_WAITING_FOR_RC018_PACKAGE

This document prepares the non-implementation work around RC-018 while automation continues on:

1. `GOAL-ECIVFE-32_FORECAST_CARD_UI`
2. `GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE`
3. `GOAL-RC018_CUSTOMER_READABLE_PACKAGE`

It does not authorize live Qwen/API calls, real data, masked-real data, production write-back, customer-visible deploy/publish/output, external pilot, production launch, or autonomous security action.

## 1. RC-018 Reviewer Handoff Message

Use after `LOCAL_OFFLINE_TRIAL_RC_018_CN` package and zip exist.

```text
请按 RC-018 本地/离线产品评审范围审阅这个包：

Candidate:
  LOCAL_OFFLINE_TRIAL_RC_018_CN

Package:
  artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review

ZIP:
  <attach RC-018 review package zip here>

Review entry:
  REVIEWER_START_HERE_中文.md

评审范围：
  - 只评审本地/离线包
  - 只使用 synthetic fixture metadata
  - 不涉及真实数据/脱敏真实数据
  - 不涉及 live Qwen/API/connectors
  - 不涉及生产写回
  - 不涉及客户可见发布/部署/输出
  - 不涉及外部试点或生产上线
  - 不允许自动隔离、阻断、处置、审批或拒绝

请不要先逐文件审 artifact。请按产品路径先看：
  1. 产品首页 / 本地试用入口
  2. 事件工作台 /incident/CASE-2847
  3. 首屏结论、建议动作、可信边界
  4. AI 建议来源
  5. 攻击链判断 / VFE 预警摘要
  6. 缺失证据和补证窗口
  7. 本地反馈预览

重点判断：
  1. 客户第一眼能不能理解 SecuPilot 是什么
  2. 工程师能不能知道下一步该做什么
  3. 经理能不能理解风险、紧急度、可信度和人工边界
  4. CTO 能不能理解本地/离线、无写回、无 live connector、无部署边界
  5. ECI/VFE 是否像产品解释，而不是工程输出
  6. 攻击链和预警内容是否保持防御性、不可被攻击者直接利用
  7. 是否仍出现 debug/fixture/旧 RC/敏感信息/live 系统/生产授权等越界内容

请返回以下之一：
  PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL
  PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL
  HOLD_FOR_UI_OR_PACKAGE_FIXES
  NO_GO_SECURITY_BOUNDARY

请先列 blocking findings，再列 non-blocking notes，最后给出下一轮建议目标。
```

## 2. RC-018 Review Decision Template

Use this as the repo decision doc source after external/local review returns.

```text
# RC-018 CN Review Decision

Candidate:
  LOCAL_OFFLINE_TRIAL_RC_018_CN

Package:
  artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review

Reviewer:
  <name / role>

Timestamp:
  <YYYY-MM-DD HH:mm Asia/Shanghai>

Decision:
  PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL
  | PASS_WITH_NOTES_TO_NEXT_INTERNAL_LOCAL_TRIAL
  | HOLD_FOR_UI_OR_PACKAGE_FIXES
  | NO_GO_SECURITY_BOUNDARY

Scope Confirmed:
  local_offline_only = true
  synthetic_fixture_metadata_only = true
  real_data = false
  masked_real_data = false
  live_qwen_api = false
  live_connectors = false
  production_writeback = false
  customer_visible_publish_deploy_output = false
  autonomous_security_action = false

Product Path Checks:
  product_home_first_impression = PASS | NOTE | HOLD
  incident_workbench_first_screen = PASS | NOTE | HOLD
  ai_advice_source = PASS | NOTE | HOLD
  eci_vfe_product_explanation = PASS | NOTE | HOLD
  missing_evidence_and_collection_window = PASS | NOTE | HOLD
  local_feedback_preview = PASS | NOTE | HOLD

Safety / Boundary Checks:
  debug_controls_hidden = PASS | HOLD
  stale_rc_wording_absent = PASS | HOLD
  secrets_tokens_auth_absent = PASS | HOLD
  raw_payload_raw_logs_absent = PASS | HOLD
  attacker_readable_path_absent = PASS | HOLD
  no_live_system_language = PASS | HOLD
  output_guard_pass_before_eci_vfe_render = PASS | HOLD

Blocking Findings:
  - <none or list>

Non-blocking Notes:
  - <none or list>

Next Recommended Product Goal:
  - <goal id / short statement>

Final One-line Judgment:
  <one sentence>
```

## 3. Customer Trial Success Criteria

RC-018 is still internal/local/offline, but the success standard should already match a future customer trial.

### Minimum Product Scope

The trial is successful only if the user can complete this path:

```text
Open product entry
  -> understand what SecuPilot does
  -> open one high-risk incident
  -> understand SecuPilot's judgment
  -> understand recommended next action
  -> understand why it is conservative
  -> inspect missing evidence / collection window
  -> understand no automatic action is taken
  -> leave local feedback
```

### Role-Based Success

Engineer:

- Can identify the incident.
- Can understand the recommended next operational step.
- Can understand what evidence is missing.
- Can understand what to collect next and within what window.

Manager:

- Can understand risk and urgency.
- Can understand confidence and uncertainty.
- Can see that SecuPilot does not auto-approve or auto-remediate.
- Can decide whether the case is ready for human review.

CTO:

- Can understand deployment boundary.
- Can verify no live connector, no real data, no write-back, no customer-visible publish.
- Can evaluate whether this is suitable for internal/local trial continuation.

### Quantitative Targets For Internal Trial

For a small internal review group:

- first-screen comprehension: at least 80% can explain SecuPilot in one sentence
- task completion: at least 80% can follow product home to incident workbench
- next-action clarity: at least 80% can identify the recommended next step
- boundary clarity: 100% can identify that no automatic production action occurs
- safety finding tolerance: 0 blocking findings
- feedback capture: at least one structured feedback item per reviewer

### PASS / HOLD Rule

PASS if:

- product path is understandable without verbal explanation
- no blocking safety or boundary issue appears
- ECI/VFE reads as product explanation
- local feedback path works or is clearly previewed

HOLD if:

- reviewer cannot tell whether this is a product page or evidence harness
- ECI/VFE appears as engineering output or attacker-usable detail
- product path depends on artifact filenames
- debug/internal labels appear in first-screen customer path
- any forbidden boundary is violated

## 4. Qwen Live Synthetic-Only Gate

This gate is not execution authorization. It defines what must be true before a future one-time live Qwen synthetic-only call can be considered.

### Gate Name

`QWEN_LIVE_SYNTHETIC_ONLY_GATE_RC_PREVIEW`

### Purpose

Allow a future controlled test where Qwen is called only with synthetic metadata, only for HITL summary support, and only after local/offline product path is stable.

### Required Before GO

- RC package has PASS or PASS_WITH_NOTES without safety blockers.
- No real or masked-real input is present.
- Runtime secret is supplied only through local environment at execution time.
- Secret is never committed, logged, printed, zipped, or copied into artifacts.
- Provider config declares:
  - `provider_mode=live_synthetic_only`
  - `input_class=synthetic_metadata_only`
  - `qwen_action_mode=HITL_SUMMARY_ONLY`
  - `autonomous_action=false`
  - `writeback_enabled=false`
  - `customer_visible_output=false`
- Timeout and retry are bounded.
- Every output passes output guard before UI display.
- Prompt-injection and forbidden-content sentinels are enabled.
- Stop/rollback command exists and has been dry-run locally.

### Forbidden In Live Synthetic Gate

- real data
- masked-real data
- customer logs
- raw payloads
- secrets/tokens/auth headers
- connector output
- production write-back
- customer-visible publish/deploy/output
- autonomous approval/rejection/blocking/isolation/remediation
- action command generation
- attacker-readable attack path, exploit steps, PoC, payload, or topology reachability

### Required Operator Inputs

```text
run_id:
operator:
artifact_root:
model_name:
base_url:
timeout_seconds:
retry_count:
secret_source:
stop_command:
rollback_command:
```

### Dry Command Shape

This is a dry shape only, not execution authorization:

```powershell
py -3 scripts\qwen_live_synthetic_precheck.py `
  --run-id <RUN_ID> `
  --artifact-root artifacts\qwen_live_synthetic\<RUN_ID> `
  --provider-mode live_synthetic_only `
  --input-class synthetic_metadata_only `
  --qwen-action-mode HITL_SUMMARY_ONLY `
  --no-writeback `
  --no-customer-visible-output `
  --no-autonomous-action
```

### GO / NO-GO

GO only if:

- precheck PASS
- runtime secret source confirmed
- synthetic-only input package confirmed
- output guard and safety sentinels confirmed
- human operator explicitly starts the one-time run

NO-GO if:

- any input is real or masked-real
- any secret appears in repo/artifact/log
- any live connector/write-back/deploy path is required
- output guard is unavailable
- model output can directly authorize an action

## 5. Product Home And Incident Workbench Customer Polish Targets

These targets should guide post-RC018 work. They are not implementation scope for this document.

### Product Home

Goal:

Make the first screen answer:

- SecuPilot 是谁
- 它帮我判断什么
- 现在建议我做什么
- 为什么可信
- 不会自动做什么

Targets:

- Reduce artifact/package vocabulary.
- Make engineer/manager/CTO paths visible but not fragmented into separate products.
- Show one current high-risk incident entry.
- Show local/offline boundary in plain Chinese.
- Keep route to incident workbench obvious.

### Incident Workbench

Goal:

Make the incident page feel like a security judgment assistant, not a report viewer.

Targets:

- First screen: conclusion, recommended action, confidence, uncertainty, no-auto-action boundary.
- Evidence: folded, explanatory, not raw.
- Timeline: explains meaning, not log rows.
- AI advice source: folded by default or clearly secondary.
- ECI/VFE: integrated as `攻击链判断` and `风险预警摘要`.
- Feedback: asks accuracy, usefulness, missing info, and action clarity.

### ECI/VFE Integration

Goal:

Use ECI/VFE to improve judgment clarity, not to expose model internals.

Targets:

- Replace fixture IDs as primary display labels.
- Translate stage/status/confidence into Chinese operator language.
- Show missing evidence and collection windows.
- Keep all guard/output details in technical reconciliation.
- Never show attacker-readable paths.

### RC-018 Review Package

Goal:

Package should open like a product review, not a file audit.

Targets:

- `REVIEWER_START_HERE_中文.md` starts with product path.
- screenshots are ordered by customer journey.
- artifact manifest remains available but secondary.
- reviewer checklist uses product questions first, file integrity second.

## Immediate Next Step

Do not manually edit ECIVFE-32 or ECIVFE-35 implementation files while automation owns them.

Manual work may continue on:

- reviewer handoff language refinement
- trial success criteria
- Qwen live synthetic-only gate
- product polish target definitions
- post-review decision capture

Automation should continue on:

```text
GOAL-ECIVFE-32_FORECAST_CARD_UI
GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE
GOAL-RC018_CUSTOMER_READABLE_PACKAGE
```
