# SecuPilot Qwen Live Synthetic Runtime Config Validator

Report ID: `secupilot-qwen-live-synthetic-runtime-config-validator`

Mode: `policy`

Overall: `RUNTIME_CONFIG_POLICY_READY_PROCESS_ENV_NOT_CHECKED`

Execution status: `NOT_EXECUTED`

## 一句话结论

Runtime config policy is ready; process env values were intentionally not checked in repo artifact mode.

## Required Local Runtime Env Names

- SECUPILOT_QWEN_API_BASE
- SECUPILOT_QWEN_MAX_RETRIES
- SECUPILOT_QWEN_MODEL
- SECUPILOT_QWEN_PROVIDER_ENABLED
- SECUPILOT_QWEN_SYNTHETIC_ONLY
- SECUPILOT_QWEN_TIMEOUT_SECONDS

## Secret Env Names

- SECUPILOT_QWEN_API_KEY

Secret values are not read into this report.

## Checks

- RUNTIME-REQ-01: request is prepared not executed = PASS (observed: PREPARED_NOT_EXECUTED)
- RUNTIME-REQ-02: request does not authorize live call = PASS (observed: False)
- RUNTIME-REQ-03: request still requires separate human GO = PASS (observed: True)
- RUNTIME-REQ-04: request data mode is synthetic only = PASS (observed: SYNTHETIC_ONLY)
- RUNTIME-REQ-05: provider disabled by default in request = PASS (observed: False)
- RUNTIME-REQ-06: secret source remains local runtime or secret manager only = PASS (observed: human_runtime_or_secret_manager_only)
- RUNTIME-REQ-07: secret value absent from request package = PASS (observed: False)
- RUNTIME-POLICY-01: non-secret env names are declared without values = PASS (observed: ['SECUPILOT_QWEN_API_BASE', 'SECUPILOT_QWEN_MAX_RETRIES', 'SECUPILOT_QWEN_MODEL', 'SECUPILOT_QWEN_PROVIDER_ENABLED', 'SECUPILOT_QWEN_SYNTHETIC_ONLY', 'SECUPILOT_QWEN_TIMEOUT_SECONDS'])
- RUNTIME-POLICY-02: secret env names are declared as names only = PASS (observed: ['SECUPILOT_QWEN_API_KEY'])
- RUNTIME-POLICY-03: request timeout/retry bounds are usable = PASS (observed: {'timeout_seconds': 30, 'max_retries': 1})

## 当前不授权

- 不发起 live Qwen/API call。
- 不发起 network request。
- 不读取、不保存、不打印 secret 值。
- 不使用真实数据或脱敏真实数据。
- 不调用 connector，不生产写回，不发布客户可见输出。
