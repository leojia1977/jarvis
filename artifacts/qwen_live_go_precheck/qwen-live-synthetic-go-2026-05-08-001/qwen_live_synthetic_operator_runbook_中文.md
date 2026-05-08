# SecuPilot Qwen Live Synthetic-Only Operator Runbook

Run ID: `QWEN-LIVE-SYNTHETIC-2026-05-08-001`

Request ID: `QWEN-LIVE-SYNTHETIC-GO-2026-05-08-001`

Status: `OPERATOR_RUNBOOK_READY_DRY_COMMAND_ONLY`

## 一句话结论

这份手册说明操作员未来如何在本机准备一次 Qwen live synthetic-only run。当前产物只提供 dry command，不发起 live call，不读取 secret 值，不调用 Qwen/API。

## 操作员

- alias: `SecuPilot-QWEN-RUNNER-01`
- type: `human_runtime_operator`
- confirmation required: `True`

## 输入与输出

- input package: `mock_data/s0_synthetic/qwen_fact_bundle`
- artifact root: `artifacts/qwen_live_synthetic_runs/2026-05-08-001`
- precheck status: `READY_FOR_QWEN_LIVE_SYNTHETIC_GO_REVIEW_NOT_EXECUTION`
- dry command: `artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_dry_command.ps1`

## Runtime Secret 提供方式

1. 打开一个新的本机 PowerShell session。
2. 从人工控制的 secret manager 或本机安全输入渠道取得 Qwen runtime secret。
3. 只在这个本机 session 里设置 `SECUPILOT_QWEN_API_KEY`。
4. 不要把 secret 写入 repo、脚本、Markdown、JSON、命令历史、日志、artifact 或聊天。
5. dry command 不会读取、保存、打印或校验 secret 值。

## 未来真实 synthetic-only run 前必须人工确认

- exact run ID: `QWEN-LIVE-SYNTHETIC-2026-05-08-001`
- data mode: `SYNTHETIC_ONLY`
- provider flag default: `False`
- secret source: `human_runtime_or_secret_manager_only`
- timeout seconds: `30`
- max retries: `1`
- max requests: `20`
- max tokens per case: `1200`
- stop on budget exceeded: `True`

## Dry Command 使用方式

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_dry_command.ps1
```

该命令只打印运行计划和人工确认项；它不会执行 live runner。

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

- 不授权 live Qwen/API call。
- 不授权真实数据或脱敏真实数据。
- 不授权 live connector。
- 不授权生产写回。
- 不授权客户可见输出。
- 不授权 autonomous Qwen action。
