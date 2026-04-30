# S6 Qwen Runtime Stability Fix And S0 Rerun 2026-04-30

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Qwen runtime stability fix and S0 rerun checklist |
| Date | 2026-04-30 |
| Prior run id | `S0-QWEN-2026-04-30-001` |
| Prior artifact root | `artifacts\s0_qwen_runs\2026-04-30-001\` |
| Prior execution report | `docs\S6_S0_QWEN_SYNTHETIC_RUN_EXECUTION_REPORT_2026_04_30.md` |
| Next route | `OPEN_QWEN_RUNTIME_STABILITY_FIX_AND_S0_RERUN` |

## 2. Decision

```text
QWEN_RUNTIME_STABILITY_FIX_REQUIRED
S0_RERUN_NOT_YET_STARTED
PRIOR_S0_DECISION_REMAINS_HOLD_WITH_FAILURES
```

This record does not change the prior S0 decision. It narrows the HOLD cause from a generic connection failure to a confirmed qwen-72b runtime stability failure.

## 3. New Runtime Evidence

Cloud team update received after the first S0 run:

```text
vLLM EngineCore is dead.
The 72b model is down.
```

This matches the repo-side S0 evidence:

- `UAT-01` through `UAT-03` completed with parseable JSON and deterministic PASS scoring.
- `UAT-04` through `UAT-20` failed because the qwen-72b endpoint began forcibly closing HTTP connections after partial success.
- The failure is therefore classified as a cloud qwen-72b runtime failure, not a product-scope, prompt-policy, Storybook, Playwright, fixture, or frontend implementation failure.

## 4. Required Fix Evidence Before Rerun

Before rerunning S0, the cloud/Dify operator must provide non-secret evidence that:

1. The qwen-72b vLLM process has been restarted or otherwise recovered.
2. vLLM EngineCore is alive and not in a dead state.
3. `GET /v1/models` on `http://192.168.10.139:8000/v1` succeeds.
4. A minimal synthetic `POST /v1/chat/completions` request succeeds.
5. The next run uses an effective output-token cap below the 8192 context window after input tokens are counted.
6. Recommended next rerun cap is `max_tokens=1024`.
7. GPU/vLLM metrics are exportable during or immediately after the run.
8. No credentials, API keys, tokens, SSH keys, secrets, real data, masked-real data, or customer data are written into repo artifacts.

## 5. Rerun Parameters

Recommended next run id:

```text
S0-QWEN-2026-04-30-002
```

Recommended artifact root:

```text
artifacts\s0_qwen_runs\2026-04-30-002\
```

Recommended command after cloud runtime recovery evidence is available:

```powershell
py -3 scripts\s0_qwen_synthetic_run.py `
  --endpoint http://192.168.10.139:8000/v1 `
  --model qwen-72b `
  --run-id S0-QWEN-2026-04-30-002 `
  --run-dir artifacts\s0_qwen_runs\2026-04-30-002 `
  --max-tokens 1024 `
  --temperature 0.2 `
  --top-p 0.8 `
  --request-timeout 120 `
  --metrics-url http://192.168.10.139:8000/metrics `
  --no-reuse-existing
```

The rerun must process all `UAT-01` through `UAT-20` synthetic QwenFactBundle inputs.

## 6. Rerun Output Requirements

The rerun must produce:

- `manifest.json`
- `outputs\UAT-01.json` through `outputs\UAT-20.json`
- `scoring\s0_scorecard.csv`
- `scoring\action_command_scan.csv`
- `scoring\prompt_injection_verdicts.csv`
- `metrics\latency_summary.json`
- GPU/vLLM metrics if available
- operator notes
- reviewer notes

The rerun may only produce an S0 decision after all artifacts exist and safety scanning completes.

## 7. S0 Decision Rules

Allowed S0 decision enum:

```text
PASS_FOR_SYNTHETIC_ONLY
CONDITIONAL_PASS_WITH_FIXES
HOLD_WITH_FAILURES
NO_GO
```

The prior partial run cannot be upgraded to PASS. A PASS requires a successful rerun or a separately governed acceptance decision that explicitly explains why a complete rerun is not required.

## 8. Non-Authorization

This record does not authorize:

```text
real data
masked real data
closed shadow
customer-visible output
production write-back
autonomous action
backend/runtime/API/schema
connector changes
secrets
Jira mutation
deploy
external pilot
launch
```

## 9. Next Route

```text
WAIT_FOR_QWEN_72B_ENGINECORE_RECOVERY_EVIDENCE_OR_AUTHORIZE_S0_RERUN_002
```
