# SecuPilot 客户试用成功标准与 Qwen Live 接入 Gate

Report ID: `secupilot-customer-trial-success-qwen-live-gate`

Overall: `READY_FOR_LOCAL_PRIVATE_TRIAL_AND_HOLD_FOR_QWEN_LIVE`

## 一句话结论

客户试用成功标准在当前本地/私有化包证据上通过；Qwen live 接入仍保持 HOLD，必须等待单独的 synthetic-only live GO 和运行时 secret 方案。

## 客户试用成功标准

- CTS-01: local trial entry ready = PASS (observed: LOCAL_TRIAL_ENTRY_READY)
- CTS-02: role coverage includes engineer manager CTO = PASS (observed: ['cto', 'security_engineer', 'security_manager'])
- CTS-03: understanding rate threshold = PASS (observed: 100.0)
- CTS-04: usefulness rate threshold = PASS (observed: 66.67)
- CTS-05: no KPI blockers = PASS (observed: 0)
- CTS-06: private deployment precheck pass = PASS (observed: PRIVATE_DEPLOYMENT_PRECHECK_PASS)
- CTS-07: sizing report remains draft not benchmarked = PASS (observed: SIZING_DRAFT_READY_NOT_BENCHMARKED)
- CTS-08: no production or customer pilot sizing claims = PASS (observed: all sizing profile claims false)
- CTS-TRIAL-real_data: real_data remains false = PASS (observed: False)
- CTS-TRIAL-masked_real_data: masked_real_data remains false = PASS (observed: False)
- CTS-TRIAL-live_qwen_api: live_qwen_api remains false = PASS (observed: False)
- CTS-TRIAL-live_connectors: live_connectors remains false = PASS (observed: False)
- CTS-TRIAL-network_request: network_request remains false = PASS (observed: False)
- CTS-TRIAL-production_writeback: production_writeback remains false = PASS (observed: False)
- CTS-TRIAL-customer_visible_output: customer_visible_output remains false = PASS (observed: False)
- CTS-TRIAL-deploy_executed: deploy_executed remains false = PASS (observed: False)
- CTS-PRECHECK-real_data: real_data remains false = PASS (observed: False)
- CTS-PRECHECK-masked_real_data: masked_real_data remains false = PASS (observed: False)
- CTS-PRECHECK-live_qwen_api: live_qwen_api remains false = PASS (observed: False)
- CTS-PRECHECK-live_connectors: live_connectors remains false = PASS (observed: False)
- CTS-PRECHECK-network_request: network_request remains false = PASS (observed: False)
- CTS-PRECHECK-production_writeback: production_writeback remains false = PASS (observed: False)
- CTS-PRECHECK-customer_visible_output: customer_visible_output remains false = PASS (observed: False)
- CTS-PRECHECK-deploy_executed: deploy_executed remains false = PASS (observed: False)

## Qwen Live 接入 Gate

当前状态：`HOLD_PENDING_EXPLICIT_QWEN_LIVE_SYNTHETIC_ONLY_GO`

- QWEN-GATE-01: synthetic-only live sandbox scope = DEFINED
- QWEN-GATE-02: explicit GO required = DEFINED
- QWEN-GATE-03: live Qwen not currently authorized = DEFINED
- QWEN-GATE-04: request/response forbidden fields = DEFINED
- QWEN-GATE-05: timeout and retry guard = DEFINED
- QWEN-GATE-06: secret runtime provisioning outside repo = REQUIRES_SEPARATE_OPERATOR_CONFIRMATION
- QWEN-GATE-07: run id, operator, artifact root, rollback and stop plan = REQUIRES_SEPARATE_GO_RECORD

## Qwen Live GO 必须包含

- run_id
- operator
- artifact_root
- data_mode=SYNTHETIC_ONLY
- provider_flag_default=false
- secret_source=human_runtime_or_secret_manager_only
- timeout_seconds
- max_retries
- cost_or_token_budget
- stop_conditions
- rollback_plan

## 当前允许推进

- 可以继续本地/离线/私有化试用包打磨。
- 可以继续 Qwen dry-run setup flow、config contract、validator、UI preview。
- 可以准备 synthetic-only live sandbox GO 记录。

## 当前不允许

- 不允许真实数据或脱敏真实数据。
- 不允许 live Qwen/API 实际调用。
- 不允许 API key、token、auth header 或 secret 写入 repo、命令、日志、artifact 或聊天。
- 不允许 live connector、生产写回、客户可见发布、外部试点或生产上线。
