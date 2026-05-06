# S6 Fast MVP Local Trial Runbook 2026-05-06

## 1. Purpose

This runbook gives an operator a short local/offline path to review the current SecuPilot Fast MVP candidate.

Target:

```text
LOCAL_OFFLINE_TRIAL_RC_001
```

This runbook does not authorize customer-visible publishing, external pilot execution, production deployment, real data, masked-real data, live Qwen/API calls, live connectors, write-back, credential handling, or push.

## 2. Operator Assumptions

The operator has:

```text
local repo access
Windows PowerShell
Python launcher available as py -3
frontend dependencies already installed or installable locally
no production credentials in the terminal
```

The operator must not paste secrets, tokens, auth headers, real customer records, raw logs, or production connector output into commands, docs, artifacts, or feedback.

## 3. Preflight

Run:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
git -c core.quotepath=false status --short --branch
py -3 scripts\git_preflight.py --mode fast
```

Expected:

```text
no unrelated dirty files outside the current docs/artifact scope
fast preflight passes
```

If automation is actively editing MVP-10 through MVP-13 files, wait until that run commits or stops before running RC packaging commands.

## 4. Generate Or Refresh Synthetic Artifact

Run:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
py -3 scripts\s1_closed_shadow_run.py --run-id S1-CLOSED-SHADOW-2026-04-30-001 --input mock_data\s0_synthetic\qwen_fact_bundle --output artifacts\s1_closed_shadow_runs\2026-04-30-001 --provider fixture --no-writeback --no-customer-visible
```

Expected artifact root:

```text
artifacts/s1_closed_shadow_runs/2026-04-30-001
```

## 5. Validate Artifact

Run:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
py -3 scripts\s1_artifact_validate.py --artifact-dir artifacts\s1_closed_shadow_runs\2026-04-30-001
```

Expected:

```text
artifact validation passes
manifest paths exist
safety scan passes
no raw payloads, secrets, tokens, auth headers, customer-visible output, or write-back artifacts
```

## 6. Review Workbench Locally

Run:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder\frontend'
npm run test -- --run App.test.tsx
npm run build
```

If a local dev server is needed for manual review, start it only for local machine access:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder\frontend'
npm run dev
```

Open the local `/s1-run` route in the browser. Confirm:

```text
run status is visible
case summary is visible
evidence list is visible
PASS/HOLD reason is visible
reviewer action is visible
no raw payload or secret-like content is visible
```

## 7. Build Local Demo Package

Run:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
py -3 scripts\package_s1_local_demo.py --artifact-dir artifacts\s1_closed_shadow_runs\2026-04-30-001 --output-dir artifacts\local_demo_packages\s1-closed-shadow-2026-04-30-001
```

Expected package root:

```text
artifacts/local_demo_packages/s1-closed-shadow-2026-04-30-001
```

Confirm that the package manifest uses portable paths and does not include forbidden material.

## 8. Capture Feedback

Use:

```text
docs/S6_FAST_MVP_CUSTOMER_TRIAL_FEEDBACK_FORM_2026_05_06.md
```

Feedback should describe product usefulness, confusing screens, missing fields, and blocker severity. It must not include raw customer data, credentials, tokens, raw logs, or production output.

## 9. Stop Conditions

Stop and report if any condition appears:

```text
git status shows unexpected dirty files in automation-owned code paths
fast preflight fails
artifact validator fails
package builder fails
frontend tests or build fail
local workbench shows raw payload, secret-like content, customer-visible output, or write-back implication
any step requires real data, masked-real data, live Qwen/API, live connector, production write-back, deploy, push, or customer-visible publish
```

## 10. Exit Result

If every step passes, the runbook result is:

```text
LOCAL_OFFLINE_TRIAL_RC_001_READY_FOR_REVIEW_DECISION
```

This result means internal local/offline review can be considered. It does not authorize sending the package to a customer, publishing, deploying, or using real data.
