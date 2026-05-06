# S6 Fast MVP Local Trial Launch Plan 2026-05-06

## 1. Purpose

This document defines the fastest launch-acceleration path from the current Fast MVP queue to a controlled local/offline trial candidate.

The first launch target is:

```text
LOCAL_OFFLINE_TRIAL_RC_001
```

This is a product trial candidate that can be reviewed from local artifacts and the existing workbench. It is not a production launch, external pilot, public demo, customer-visible deployment, live Qwen run, live connector run, or real-data run.

## 2. Current Product Direction

The operating goal is:

```text
ship a usable local/offline trial candidate quickly
verify the product loop with synthetic or approved external-output artifacts
collect actionable reviewer feedback
iterate toward customer trial only after RC gates pass
```

The current automation queue remains responsible for MVP-10 through MVP-13. This launch package should not compete with those write scopes.

## 3. Trial Boundary

Allowed for RC-001 preparation:

```text
local workbench review
local synthetic S1 artifact review
external-output metadata-only artifact review
local demo package generation
local screenshots and smoke-test evidence
docs-only reviewer instructions
local feedback capture
```

Not allowed without a later explicit GO:

```text
real data
masked-real data
live Qwen/API call
live connector
production connector
production write-back
customer-visible publish/deploy
public URL
credential handling
secrets/tokens/auth headers in repo, docs, artifacts, or chat
push
```

## 4. Minimum RC-001 Flow

The shortest useful trial flow is:

1. Generate or refresh a synthetic S1 run artifact.
2. Validate the S1 artifact manifest and safety scan.
3. Open the existing `/s1-run` workbench view.
4. Build a local demo package from the validated artifact.
5. Review the package README and feedback form.
6. Record feedback without pasting raw customer data, credentials, or live logs into the repo.

## 5. Candidate Commands

Use these commands after the active automation queue has either completed MVP-10 through MVP-13 or stopped cleanly with a non-safety HOLD.

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
py -3 scripts\s1_closed_shadow_run.py --run-id S1-CLOSED-SHADOW-2026-04-30-001 --input mock_data\s0_synthetic\qwen_fact_bundle --output artifacts\s1_closed_shadow_runs\2026-04-30-001 --provider fixture --no-writeback --no-customer-visible
py -3 scripts\s1_artifact_validate.py --artifact-dir artifacts\s1_closed_shadow_runs\2026-04-30-001
py -3 scripts\package_s1_local_demo.py --artifact-dir artifacts\s1_closed_shadow_runs\2026-04-30-001 --output-dir artifacts\local_demo_packages\s1-closed-shadow-2026-04-30-001
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode mvp-11 -WriteStatus
```

Frontend local review:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder\frontend'
npm run test -- --run App.test.tsx
npm run build
```

## 6. Human Decisions Needed Before Any Real Customer Trial

These decisions are intentionally not filled in by Codex:

| Decision | Needed from | Current status |
| --- | --- | --- |
| Trial audience | Product owner / human | `PENDING` |
| Delivery channel for local package | Product owner / human | `PENDING` |
| Target review date | Product owner / human | `PENDING` |
| Whether any customer-visible output is authorized | Product owner / human | `NOT_AUTHORIZED` |
| Whether real or masked-real data is authorized | Product owner / human | `NOT_AUTHORIZED` |
| Whether live Qwen/API/connectors are authorized | Product owner / human | `NOT_AUTHORIZED` |

## 7. Fast Launch Rule

RC-001 may be prepared locally when the checks in `S6_FAST_MVP_RC_001_CHECKLIST_2026_05_06.md` pass.

RC-001 may not be sent, published, deployed, or represented as customer-ready until a later explicit launch or trial GO names the exact package, audience, channel, and boundary.

## 8. Companion Docs

Use these files as the RC-001 launch-acceleration pack:

| File | Purpose |
| --- | --- |
| `docs/S6_FAST_MVP_RC_001_CHECKLIST_2026_05_06.md` | Minimum RC-001 gates, commands, pass criteria, and HOLD conditions |
| `docs/S6_FAST_MVP_LOCAL_TRIAL_RUNBOOK_2026_05_06.md` | Operator steps for a local/offline trial review |
| `docs/S6_FAST_MVP_CUSTOMER_TRIAL_FEEDBACK_FORM_2026_05_06.md` | Reviewer feedback capture without raw data or secrets |
| `docs/S6_FAST_MVP_TRIAL_SUCCESS_CRITERIA_2026_05_06.md` | Product success thresholds and next-iteration decision rules |
| `docs/S6_FAST_MVP_QWEN_CLOUD_ADAPTER_SPEC_2026_05_06.md` | Future Qwen cloud adapter design boundary; no live API authorization |
