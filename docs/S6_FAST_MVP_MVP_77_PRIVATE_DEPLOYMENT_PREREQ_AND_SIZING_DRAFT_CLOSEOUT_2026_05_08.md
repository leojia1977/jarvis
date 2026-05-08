# S6 Fast MVP-77 Private Deployment Prereq And Sizing Draft Closeout

Date: 2026-05-08

Goal: `GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT`

Status: PASS

## Scope

MVP-77 turns MVP-76 feedback into a local/offline private deployment prerequisite and sizing draft. It covers Windows prerequisites, resource sizing profiles, and the dry-run model provider path.

This is a draft report only. It does not deploy, benchmark production, call live Qwen/API, connect live systems, read secrets, use real data, publish customer-visible output, or write back to production.

## Product Changes

- Added `scripts/generate_private_deployment_prereq_sizing_draft.py`.
- Added tests for draft generation and HOLD paths.
- Generated draft artifacts:
  - `artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft.json`
  - `artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft_中文.md`
- Added Goal card:
  - `docs/goals/GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT.md`

## Draft Result

Current generated draft status:

```text
DRAFT_READY_FOR_INTERNAL_PRODUCT_REVIEW
```

Source feedback:

```text
FB-SAMPLE-002: Windows prerequisite checks requested.
FB-SAMPLE-003: private deployment resource sizing and model provider path requested.
```

Generated sections:

```text
windows_prerequisites = 4 checks
resource_sizing_profiles = 3 profiles
model_provider_path = 4 dry-run stages
blockers = 0
next_unlock = GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT
```

Draft sizing remains non-benchmark and non-production:

```text
SIZE-LOCAL-TRIAL = 2 vCPU / 4 GB RAM / 2 GB disk draft
SIZE-LAB-PILOT-DRAFT = 4 vCPU / 8 GB RAM / 10 GB disk draft
SIZE-PRODUCTION-TBD = TBD, not authorized and not benchmarked
```

## Files Changed

- `scripts/generate_private_deployment_prereq_sizing_draft.py`
- `backend/tests/test_generate_private_deployment_prereq_sizing_draft.py`
- `docs/goals/GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT.md`
- `docs/S6_FAST_MVP_MVP_77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT_CLOSEOUT_2026_05_08.md`
- `artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft.json`
- `artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft_中文.md`

## Verification

Commands run:

```powershell
py -3 scripts\generate_private_deployment_prereq_sizing_draft.py --package-dir artifacts\private_deployment_packages\secupilot-private-deployment-windows-local-v0_1 --feedback-json artifacts\private_deployment_packages\secupilot-private-deployment-windows-local-v0_1\trial_output\customer_trial_feedback.sample.json --output-dir artifacts\private_deployment_packages\secupilot-private-deployment-windows-local-v0_1\trial_output --repo-root .
py -3 -m unittest -q backend.tests.test_generate_private_deployment_prereq_sizing_draft
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT.md
git -c core.quotepath=false diff --check
```

Results:

- Prereq/sizing draft generation: PASS
- Unit test `backend.tests.test_generate_private_deployment_prereq_sizing_draft`: 6 passed
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
GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT
```

Purpose:

```text
Turn the MVP-77 Windows prerequisite draft into a local PowerShell/Python precheck script that verifies OS, PowerShell, Python launcher, and package write permissions without deploying or calling live services.
```
