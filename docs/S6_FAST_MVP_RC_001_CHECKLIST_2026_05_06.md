# S6 Fast MVP RC-001 Checklist 2026-05-06

## 1. Purpose

This checklist defines the minimum evidence needed before treating the current Fast MVP as a local/offline trial candidate.

Target candidate:

```text
LOCAL_OFFLINE_TRIAL_RC_001
```

This checklist does not authorize production deployment, customer-visible publication, external pilot execution, real data, masked-real data, live Qwen/API calls, live connectors, write-back, credential handling, or push.

## 2. Entry Conditions

| Gate | Required result | Evidence |
| --- | --- | --- |
| Worktree | No unrelated dirty files | `git -c core.quotepath=false status --short --branch` |
| Fast MVP queue | MVP-09 closed and automation resumed to MVP-10+ or stopped cleanly | `docs/S6_FAST_MVP_AUTOMATION_RETROSPECTIVE_2026_05_06.md`; automation status artifact |
| Data boundary | Synthetic or approved metadata-only external-output only | runner args and artifact manifest |
| Write-back boundary | No write-back flags enabled | runner args and safety scan |
| Customer visibility | No customer-visible publish/deploy | local-only commands and package manifest |

## 3. Required Commands

Run from the repo root unless a command says otherwise.

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
git -c core.quotepath=false status --short --branch
py -3 scripts\git_preflight.py --mode fast
py -3 scripts\s1_artifact_validate.py --artifact-dir artifacts\s1_closed_shadow_runs\2026-04-30-001
py -3 scripts\package_s1_local_demo.py --artifact-dir artifacts\s1_closed_shadow_runs\2026-04-30-001 --output-dir artifacts\local_demo_packages\s1-closed-shadow-2026-04-30-001
```

Frontend verification:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder\frontend'
npm run test -- --run App.test.tsx
npm run build
```

Visual smoke, after MVP-11 exists:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\s1_fast_mvp_loop.ps1 -Mode mvp-11 -WriteStatus
```

## 4. Pass Criteria

| Area | PASS condition |
| --- | --- |
| Artifact validation | Required S1 files exist, SHA256 checks pass, retention classes are known, safety scan passes |
| Workbench | `/s1-run` renders S1 status, case summary, evidence list, reason, and reviewer action |
| Demo package | Package manifest uses portable paths and includes only allowed local/offline artifacts |
| Feedback path | Feedback form exists and tells reviewers not to paste raw data, secrets, tokens, or customer logs |
| Scope | No command uses real data, masked-real data, live Qwen/API, live connectors, write-back, deploy, push, or customer-visible publishing |

## 5. HOLD Conditions

Stop and report instead of forcing RC readiness if any condition is true:

```text
artifact validator fails
manifest has unknown retention_class
package contains absolute local workspace paths
package contains raw payload, secret, token, auth header, cookie, private key, or credential-like text
workbench smoke fails to render required S1 fields
any command attempts real data, masked-real data, live Qwen/API, live connector, write-back, deploy, push, or customer-visible output
automation has unrelated dirty files in code/artifact paths
MVP-10 through MVP-13 changes are in progress and not yet committed
```

## 6. RC-001 Decision Record Stub

Fill this only after the commands above pass:

| Field | Value |
| --- | --- |
| Candidate | `LOCAL_OFFLINE_TRIAL_RC_001` |
| Decision | `PENDING` |
| Artifact run | `artifacts/s1_closed_shadow_runs/2026-04-30-001` |
| Local demo package | `artifacts/local_demo_packages/s1-closed-shadow-2026-04-30-001` |
| Trial audience | `PENDING_HUMAN_DECISION` |
| Delivery channel | `PENDING_HUMAN_DECISION` |
| Customer-visible authorization | `NOT_AUTHORIZED` |
| Real or masked-real data authorization | `NOT_AUTHORIZED` |
| Live Qwen/API/connectors authorization | `NOT_AUTHORIZED` |
| Production write-back authorization | `NOT_AUTHORIZED` |

## 7. Exit Result

If every required check passes, the allowed result is:

```text
READY_FOR_LOCAL_OFFLINE_TRIAL_RC_001_REVIEW
```

This status means the local/offline candidate is ready for internal review. It does not authorize sending, publishing, deploying, or running against customer data.
