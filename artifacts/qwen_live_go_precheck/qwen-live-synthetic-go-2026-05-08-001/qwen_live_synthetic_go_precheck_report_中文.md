# SecuPilot Qwen Live Synthetic-Only GO Precheck

Report ID: `secupilot-qwen-live-synthetic-go-precheck`

Overall: `READY_FOR_QWEN_LIVE_SYNTHETIC_GO_REVIEW_NOT_EXECUTION`

Execution status: `NOT_EXECUTED`

## 一句话结论

Qwen live synthetic-only GO 参数已具备可审核形态；当前仅完成前置检查，没有发起 live call，真正执行仍需要单独人工 GO。

## Precheck Checks

- QWEN-GO-01: schema version = PASS (observed: secupilot.qwen_live_synthetic_go_request.v1)
- QWEN-GO-02: request status is prepared not executed = PASS (observed: PREPARED_NOT_EXECUTED)
- QWEN-GO-03: live call remains not authorized in precheck = PASS (observed: False)
- QWEN-GO-04: separate human GO remains required = PASS (observed: True)
- QWEN-GO-05: data mode is synthetic only = PASS (observed: SYNTHETIC_ONLY)
- QWEN-GO-06: run id present = PASS (observed: QWEN-LIVE-SYNTHETIC-2026-05-08-001)
- QWEN-GO-07: operator alias present and human confirmation required = PASS (observed: {'type': 'human_runtime_operator', 'alias': 'SecuPilot-QWEN-RUNNER-01', 'confirmation_required': True})
- QWEN-GO-08: artifact root is governed relative path = PASS (observed: artifacts/qwen_live_synthetic_runs/2026-05-08-001)
- QWEN-GO-09: provider disabled by default = PASS (observed: False)
- QWEN-GO-10: secret source is runtime or secret manager only = PASS (observed: human_runtime_or_secret_manager_only)
- QWEN-GO-11: secret value absent from repo package = PASS (observed: False)
- QWEN-GO-12: timeout is bounded = PASS (observed: 30)
- QWEN-GO-13: retry count is bounded = PASS (observed: 1)
- QWEN-GO-14: cost and token budget present = PASS (observed: {'max_requests': 20, 'max_tokens_per_case': 1200, 'stop_on_budget_exceeded': True})
- QWEN-BOUNDARY-real_data: real_data remains false = PASS (observed: False)
- QWEN-BOUNDARY-masked_real_data: masked_real_data remains false = PASS (observed: False)
- QWEN-BOUNDARY-raw_payload_allowed: raw_payload_allowed remains false = PASS (observed: False)
- QWEN-BOUNDARY-raw_log_allowed: raw_log_allowed remains false = PASS (observed: False)
- QWEN-BOUNDARY-customer_visible_output: customer_visible_output remains false = PASS (observed: False)
- QWEN-BOUNDARY-production_writeback: production_writeback remains false = PASS (observed: False)
- QWEN-BOUNDARY-live_connectors: live_connectors remains false = PASS (observed: False)
- QWEN-BOUNDARY-autonomous_qwen_action: autonomous_qwen_action remains false = PASS (observed: False)
- QWEN-GO-15: stop conditions are explicit = PASS (observed: 8)
- QWEN-GO-16: rollback plan is explicit = PASS (observed: 4)

## 真正执行前还需要人工确认

- human confirms this exact run_id
- human supplies runtime secret outside repo and outside chat
- operator confirms artifact root is empty or dedicated to this run
- operator starts provider flag manually for this run only
- operator confirms cost/token budget and timeout/retry values
- operator confirms stop conditions and rollback plan

## Stop Conditions

- runtime secret appears in repo, command, log, artifact, or chat
- input package is not synthetic-only
- provider flag is enabled by default
- timeout, retry, or budget guard is missing
- response contains forbidden fields
- adapter attempts connector action or write-back
- network target or model name differs from the human-confirmed runtime values
- operator cannot write to the dedicated artifact root

## Rollback Plan

- disable provider flag
- delete incomplete run artifact directory
- preserve precheck report and failure reason
- record HOLD without retrying automatically

## 当前不授权

- 不发起 live Qwen/API call。
- 不使用真实数据或脱敏真实数据。
- 不读取、不保存、不打印 API key、token、auth header 或 secret 值。
- 不调用 connector，不生产写回，不发布客户可见输出。
