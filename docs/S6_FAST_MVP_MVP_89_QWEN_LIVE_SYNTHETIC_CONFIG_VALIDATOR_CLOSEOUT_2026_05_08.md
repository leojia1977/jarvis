# S6 Fast MVP MVP-89 Qwen Live Synthetic Config Validator Closeout

Date: 2026-05-08

Goal: `GOAL-MVP-89_QWEN_LIVE_SYNTHETIC_CONFIG_VALIDATOR`

## Decision

```text
RUNTIME_CONFIG_POLICY_READY_PROCESS_ENV_NOT_CHECKED
```

## What Changed

- Added a local validator for future Qwen live synthetic-only runtime configuration.
- Added policy mode for repo artifacts. Policy mode records required env names and bounds only.
- Added process mode for future operator checks. Process mode validates local env presence and shape without retaining values.
- Added unit tests proving process mode does not retain API base, model name, or secret value.
- Generated a runtime config policy report.

## Required Local Runtime Env Names

Non-secret env names:

```text
SECUPILOT_QWEN_PROVIDER_ENABLED
SECUPILOT_QWEN_SYNTHETIC_ONLY
SECUPILOT_QWEN_API_BASE
SECUPILOT_QWEN_MODEL
SECUPILOT_QWEN_TIMEOUT_SECONDS
SECUPILOT_QWEN_MAX_RETRIES
```

Secret env names:

```text
SECUPILOT_QWEN_API_KEY
```

The generated reports retain names only. They do not retain env values.

## Generated Evidence

```text
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report_中文.md
```

## Process Mode Intended Use

Before any future synthetic-only live run, the operator can run:

```powershell
py -3 scripts/validate_qwen_live_synthetic_runtime_config.py --request artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_request.json --output-dir artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001 --repo-root . --mode process
```

This command checks local env values but still does not call Qwen/API. It does not write API base, model, or secret values into the report.

## Acceptance Commands

```powershell
py -3 scripts/validate_qwen_live_synthetic_runtime_config.py --request artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_request.json --output-dir artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001 --repo-root . --mode policy
py -3 -m unittest -q backend.tests.test_validate_qwen_live_synthetic_runtime_config
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-89_QWEN_LIVE_SYNTHETIC_CONFIG_VALIDATOR.md
git -c core.quotepath=false diff --check
```

## Non-Execution Statement

This Goal did not:

- call Qwen
- call any live API
- make a network request
- read, store, print, or validate secret values in repo artifact mode
- retain local env values in process mode tests
- use real data or masked-real data
- call connectors
- write back to production
- create customer-visible output
- authorize external pilot or production launch

## Next Unlock

The next useful model-provider step is a provider stub or adapter skeleton that can consume this config contract, still behind dry/no-network behavior until a separate synthetic-only live GO exists.
