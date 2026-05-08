# S6 Fast MVP-74 Customer Trial README And One-Click Start Script Closeout

Date: 2026-05-08

Goal: `GOAL-MVP-74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT`

Status: PASS

## Scope

MVP-74 adds a customer/internal reviewer local-offline trial entry layer on top of the MVP-73 private deployment package structure.

This is still local/offline dry-run only. It does not deploy, start production services, connect live systems, call Qwen/API, read secrets, use real data, or write back to production.

## Product Changes

- Updated `scripts/build_private_deployment_package.py` to generate customer trial entry files.
- Added root start-here document:
  - `CUSTOMER_TRIAL_START_HERE_中文.md`
- Added root one-click Windows entry:
  - `START_SECUPILOT_LOCAL_TRIAL.cmd`
- Added PowerShell dry-run entry:
  - `scripts/START_CUSTOMER_TRIAL.ps1`
- Added trial output slot:
  - `trial_output/README_TRIAL_OUTPUT_中文.md`
  - `trial_output/customer_trial_status.json`
- Updated `package_manifest.json` with `entry_points`.
- Regenerated local zip:
  - `artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1.zip`
- Extended unit tests to verify:
  - customer trial entry files exist
  - manifest entry points are present
  - the PowerShell entry script writes `customer_trial_status.json`
  - dry-run boundaries remain false

## Files Changed

- `scripts/build_private_deployment_package.py`
- `backend/tests/test_build_private_deployment_package.py`
- `docs/goals/GOAL-MVP-74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT.md`
- `docs/S6_FAST_MVP_MVP_74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT_CLOSEOUT_2026_05_08.md`
- `artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/`
- `artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1.zip`

## Verification

Commands run:

```powershell
py -3 scripts\build_private_deployment_package.py --package-id secupilot-private-deployment-windows-local-v0_1 --output-dir artifacts\private_deployment_packages\secupilot-private-deployment-windows-local-v0_1 --zip-path artifacts\private_deployment_packages\secupilot-private-deployment-windows-local-v0_1.zip --repo-root .
powershell.exe -NoProfile -ExecutionPolicy Bypass -File artifacts\private_deployment_packages\secupilot-private-deployment-windows-local-v0_1\scripts\START_CUSTOMER_TRIAL.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File artifacts\private_deployment_packages\secupilot-private-deployment-windows-local-v0_1\scripts\VERIFY_BOUNDARIES.ps1
py -3 -m unittest -q backend.tests.test_build_private_deployment_package
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-MVP-74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT.md
git -c core.quotepath=false diff --check
```

Results:

- Private deployment package generation: PASS
- Customer trial one-click PowerShell entry: `LOCAL_TRIAL_ENTRY_READY`
- Customer trial status artifact: `trial_output/customer_trial_status.json`
- Boundary verification script: `BOUNDARY_CHECK_PASS`
- Unit test `backend.tests.test_build_private_deployment_package`: 5 passed
- Goal card validator: PASS
- `git diff --check`: PASS
- Generated manifest status: `STRUCTURE_ONLY_NOT_DEPLOYED`
- Generated manifest entry points:
  - `CUSTOMER_TRIAL_START_HERE_中文.md`
  - `START_SECUPILOT_LOCAL_TRIAL.cmd`
  - `scripts/START_CUSTOMER_TRIAL.ps1`
  - `trial_output/customer_trial_status.json`

## Boundary

This closeout does not authorize:

- real data
- masked-real data
- live Qwen/API/connectors
- production write-back
- customer-visible publish/deploy
- external pilot
- production launch
- secrets, tokens, auth headers, or raw customer logs
- backend/runtime/API/schema changes
- autonomous Qwen approval or action

## Next Unlock

Recommended next product Goal:

```text
GOAL-MVP-75_INTERNAL_TRIAL_KPI_REPORT
```

Purpose:

```text
Generate a local/offline internal trial KPI report from the private deployment package and trial status artifact, covering understanding rate, completion status, feedback count, and blockers without requiring live services or real data.
```
