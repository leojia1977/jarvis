# S6 Fast MVP-79 Private Deployment Sizing Report Closeout

Date: 2026-05-08

Goal: `GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT`

Status: PASS

## Scope

MVP-79 turns the MVP-77 sizing draft and MVP-78 precheck result into a local/offline private deployment sizing report. It separates observed local precheck evidence from draft sizing assumptions.

This is not a production benchmark, customer pilot sizing claim, deployment authorization, or live model readiness statement.

## Product Changes

- Added `scripts/generate_private_deployment_sizing_report.py`.
- Added tests for sizing report generation and HOLD paths.
- Generated sizing report artifacts:
  - `artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_sizing_report.json`
  - `artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_sizing_report_中文.md`
- Added Goal card:
  - `docs/goals/GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT.md`

## Report Result

Current generated report status:

```text
SIZING_DRAFT_READY_NOT_BENCHMARKED
```

Observed precheck:

```text
PRIVATE_DEPLOYMENT_PRECHECK_PASS
passed_count = 4 / 4
```

Sizing profiles:

```text
SIZE-LOCAL-TRIAL = 2 vCPU draft / 4 GB RAM draft / 2 GB disk draft
SIZE-LAB-PILOT-DRAFT = 4 vCPU draft / 8 GB RAM draft / 10 GB disk draft
SIZE-PRODUCTION-TBD = TBD / not authorized / not benchmarked
```

All profiles include:

```text
measurement_status = NOT_BENCHMARKED_DRAFT_ONLY
production_claim = false
customer_pilot_claim = false
```

## Files Changed

- `scripts/generate_private_deployment_sizing_report.py`
- `backend/tests/test_generate_private_deployment_sizing_report.py`
- `docs/goals/GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT.md`
- `docs/S6_FAST_MVP_MVP_79_PRIVATE_DEPLOYMENT_SIZING_REPORT_CLOSEOUT_2026_05_08.md`
- `artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_sizing_report.json`
- `artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_sizing_report_中文.md`

## Verification

Commands run:

```powershell
py -3 scripts\generate_private_deployment_sizing_report.py --package-dir artifacts\private_deployment_packages\secupilot-private-deployment-windows-local-v0_1 --draft-json artifacts\private_deployment_packages\secupilot-private-deployment-windows-local-v0_1\trial_output\private_deployment_prereq_sizing_draft.json --precheck-json artifacts\private_deployment_packages\secupilot-private-deployment-windows-local-v0_1\trial_output\private_deployment_precheck_result.json --output-dir artifacts\private_deployment_packages\secupilot-private-deployment-windows-local-v0_1\trial_output --repo-root .
py -3 -m unittest -q backend.tests.test_generate_private_deployment_sizing_report
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT.md
git -c core.quotepath=false diff --check
```

Results:

- Sizing report generation: PASS
- Unit test `backend.tests.test_generate_private_deployment_sizing_report`: 8 passed
- Goal card validator: PASS
- `git diff --check`: PASS

## Boundary

This closeout does not authorize:

- real data
- masked-real data
- live Qwen/API/connectors
- production write-back
- customer-visible publish/deploy
- external pilot
- production launch
- production benchmark or sizing claim
- secrets, tokens, auth headers, or raw customer logs
- backend/runtime/API/schema changes
- autonomous Qwen approval or action

## Next Unlock

Recommended next product Goal:

```text
GOAL-MVP-80_MODEL_PROVIDER_SETUP_FLOW_DRY_RUN
```

Purpose:

```text
Turn the dry-run model provider path into a customer-understandable setup flow without live calls, API keys, network access, or real data.
```
