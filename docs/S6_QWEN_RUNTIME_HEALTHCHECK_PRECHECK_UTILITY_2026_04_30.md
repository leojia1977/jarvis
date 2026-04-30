# S6 Qwen Runtime Healthcheck Precheck Utility 2026-04-30

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Utility/checklist record |
| Date | 2026-04-30 |
| Utility | `scripts/s0_qwen_readiness.py` |

## 2. Decision

```text
QWEN_RUNTIME_HEALTHCHECK_PRECHECK_UTILITY_CREATED
LOCAL_PREFLIGHT_PASS
CLOUD_HEALTHCHECK_NOT_RUN_BY_THIS_RECORD
S0_002_RERUN_REMAINS_CONDITIONAL
```

## 3. Utility Modes

| Mode | Network? | Purpose |
| --- | --- | --- |
| `preflight` | No | Validate 20 synthetic QwenFactBundle files, synthetic boundary, and prompt budget |
| `artifact-validate` | No | Validate S0 run-folder shape and scan artifacts for hard-stop secret patterns |
| `healthcheck` | Yes, explicit only | Check `/v1/models` and optionally one minimal synthetic chat completion |

## 4. Exact Commands

Local-only S0-002 preflight:

```powershell
py -3 scripts\s0_qwen_readiness.py preflight
```

Local-only artifact validation:

```powershell
py -3 scripts\s0_qwen_readiness.py artifact-validate --run-dir artifacts\s0_qwen_runs\2026-04-30-001 --output-json artifacts\s0_qwen_runs\2026-04-30-001\artifact_completeness.json
```

Cloud healthcheck, only after cloud team confirms qwen-72b is expected alive:

```powershell
py -3 scripts\s0_qwen_readiness.py healthcheck --endpoint http://192.168.10.139:8000/v1 --model qwen-72b --run-chat-check
```

## 5. HOLD Rules

HOLD S0-002 rerun if:

- EngineCore is not confirmed alive.
- `/v1/models` is unavailable.
- Minimal synthetic chat completion fails.
- Prompt budget preflight fails.
- Any synthetic QwenFactBundle fails synthetic boundary validation.
- Any hard-stop secret pattern appears in artifacts.

## 6. Non-Authorization

The healthcheck utility does not authorize S0 run execution by itself and does not authorize real data, masked real data, customer-visible output, backend/runtime/API/schema, connector changes, secrets, deploy, external pilot, launch, or autonomous action.
