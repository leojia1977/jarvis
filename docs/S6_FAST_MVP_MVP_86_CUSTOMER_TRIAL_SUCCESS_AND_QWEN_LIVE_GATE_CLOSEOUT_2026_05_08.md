# S6 Fast MVP MVP-86 Customer Trial Success And Qwen Live Gate Closeout

Date: 2026-05-08

Goal: `GOAL-MVP-86_CUSTOMER_TRIAL_SUCCESS_AND_QWEN_LIVE_GATE`

## Decision

```text
CUSTOMER_TRIAL_SUCCESS_CRITERIA_PASS_FOR_LOCAL_PRIVATE_TRIAL
QWEN_LIVE_GATE_HOLD_PENDING_EXPLICIT_SYNTHETIC_ONLY_GO
```

## What Changed

- Added a local validator for customer trial success criteria and the Qwen live integration gate.
- Added unit tests for the validator, including success, threshold failure, boundary failure, forbidden literal, and missing Qwen spec cases.
- Generated a product readiness report under `artifacts/product_readiness/customer_trial_success_qwen_live_gate/`.
- Captured the Goal as an executable contract.

## Customer Trial Success Criteria

The current local/private trial package passes the local customer-trial readiness gate:

- local trial entry status is ready
- role coverage includes security engineer, security manager, and CTO
- understanding rate is at or above 80 percent
- usefulness rate is at or above 60 percent
- KPI report has no blockers
- private deployment precheck passes
- sizing report remains a draft and does not claim production benchmark or customer pilot readiness
- real data, masked-real data, live Qwen/API, live connectors, network request, production write-back, customer-visible output, and deploy execution remain false

## Qwen Live Gate

Qwen live integration is intentionally not opened by this Goal.

Current status:

```text
HOLD_PENDING_EXPLICIT_QWEN_LIVE_SYNTHETIC_ONLY_GO
```

The first allowed future live scope is:

```text
QWEN_LIVE_SYNTHETIC_ONLY_SANDBOX
```

That future GO must separately name:

- run ID
- operator
- artifact root
- data mode as `SYNTHETIC_ONLY`
- provider flag default as `false`
- secret source outside repo
- timeout
- max retries
- cost or token budget
- stop conditions
- rollback plan

## Generated Evidence

```text
artifacts/product_readiness/customer_trial_success_qwen_live_gate/customer_trial_success_qwen_live_gate_report.json
artifacts/product_readiness/customer_trial_success_qwen_live_gate/customer_trial_success_qwen_live_gate_report_中文.md
```

The report outcome is:

```text
READY_FOR_LOCAL_PRIVATE_TRIAL_AND_HOLD_FOR_QWEN_LIVE
```

## Acceptance Commands

```powershell
py -3 scripts/validate_customer_trial_success_and_qwen_live_gate.py --package-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1 --qwen-spec docs/S6_FAST_MVP_QWEN_CLOUD_ADAPTER_SPEC_2026_05_06.md --output-dir artifacts/product_readiness/customer_trial_success_qwen_live_gate --repo-root .
py -3 -m unittest -q backend.tests.test_validate_customer_trial_success_and_qwen_live_gate
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-86_CUSTOMER_TRIAL_SUCCESS_AND_QWEN_LIVE_GATE.md
git -c core.quotepath=false diff --check
```

## Non-Authorization

This closeout does not authorize:

- real data
- masked-real data
- live Qwen/API calls
- API keys, secrets, tokens, auth headers, or raw customer logs
- live connectors
- production write-back
- customer-visible publish, deploy, or output
- external pilot
- production launch

## Next Unlock

Proceed with dry-run model-provider setup and UI/product flow work. For actual Qwen live execution, create a separate synthetic-only live GO record first.
