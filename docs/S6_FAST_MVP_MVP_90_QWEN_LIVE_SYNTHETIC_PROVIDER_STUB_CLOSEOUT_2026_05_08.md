# S6 Fast MVP MVP-90 Qwen Live Synthetic Provider Stub Closeout

Date: 2026-05-08

Goal: `GOAL-MVP-90_QWEN_LIVE_SYNTHETIC_PROVIDER_STUB`

## Decision

```text
QWEN_SYNTHETIC_PROVIDER_STUB_READY_NO_NETWORK
```

## What Changed

- Added a deterministic no-network Qwen synthetic provider stub.
- Generated metadata-only provider output from 20 local synthetic fact bundles.
- Kept the output compatible with `secupilot.qwen_provider_dry_response.v1`.
- Added tests for pass, non-ready runtime config, non-synthetic input, forbidden action text, and full 20-case repo bundle generation.

## Generated Evidence

```text
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_output.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report_中文.md
```

## Acceptance Commands

```powershell
py -3 scripts/qwen_live_synthetic_provider_stub.py --bundle-dir mock_data/s0_synthetic/qwen_fact_bundle --runtime-config-report artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json --output-dir artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001 --repo-root .
py -3 scripts/validate_qwen_provider_contract.py artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_output.json
py -3 -m unittest -q backend.tests.test_qwen_live_synthetic_provider_stub
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-90_QWEN_LIVE_SYNTHETIC_PROVIDER_STUB.md
git -c core.quotepath=false diff --check
```

## Non-Execution Statement

This Goal did not:

- call Qwen
- call any live API
- make a network request
- read, store, print, or validate secret values
- use real data or masked-real data
- call connectors
- write back to production
- create customer-visible output
- authorize external pilot or production launch

## Next Unlock

Proceed to `GOAL-MVP-91_MODEL_PROVIDER_SWITCH_UI`, using this provider stub as a product-facing model readiness source.
