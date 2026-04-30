# S6 Fast MVP Implementation Plan 2026-04-30

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | Fast MVP implementation plan |
| Date | 2026-04-30 |
| Scope | Discussion-ready implementation plan and command map |
| Status | `FAST_MVP_EXECUTION_ACTIVE` |
| Current blocker | `NONE_FOR_MVP_03_FRONTEND_ARTIFACT_VIEWER` |
| Primary goal | Make SecuPilot runnable, testable, reviewable, and deployable for fast MVP iteration |

## 2. Direction Change

Decision principle:

```text
NO_MORE_AUTHORIZATION_ONLY_WORK_UNLESS_IT_UNLOCKS_AN_EXECUTABLE
```

From this point, every new task should produce at least one of:

```text
script
command
API endpoint
frontend surface
test
artifact
deployable package
reviewable run output
```

Docs remain useful only when they define an exact implementation slice, review command, rollback command, or customer-facing delivery boundary.

## 3. Fast MVP Target

The MVP should run without waiting for full enterprise backend integration.

Target flow:

```text
approved input package or synthetic fixture
-> scripts/s1_closed_shadow_run.py
-> artifacts/s1_closed_shadow_runs/<run-id>/
-> frontend artifact viewer
-> reviewer/customer demo discussion
```

Qwen should be a pluggable provider, not a blocker for the product shell:

```text
--provider fixture
--provider external-output
--provider qwen-api
```

Initial MVP can ship with `fixture` and `external-output`. `qwen-api` is added after the local product loop is running.

## 4. Minimal Implementation Slices

| Slice | Deliverable | Owner mode | Result |
| --- | --- | --- | --- |
| MVP-01 | `scripts/s1_closed_shadow_run.py` plus `backend/tests/test_s1_closed_shadow_run.py` | Codex / VS Code implementation | S1 run command exists |
| MVP-02 | Standard S1 artifact schema | Codex implementation | `run_record.json`, `artifact_manifest.json`, `safety_scan.json`, `case_summary.json`, `final_status.json` |
| MVP-03 | Frontend artifact viewer | Codex / VS Code implementation | Product can show S1 status and case summary |
| MVP-04 | One-shot local automation commands | Codex / VS Code tasks | Fast test loop, no recurring empty automation |
| MVP-05 | Claude Code focused review | Review-only | Catch implementation bugs |
| MVP-06 | Claude Web product review | Manual external review | Catch product/demo gaps |
| MVP-07 | Optional SWE acceleration | Exact bounded slice only | Parallel work without scope drift |
| MVP-08 | Qwen provider | Later slice | Real model integration without blocking MVP |

## 5. MVP-01 Exact Target

Create:

```text
scripts/s1_closed_shadow_run.py
backend/tests/test_s1_closed_shadow_run.py
```

Required command shape:

```powershell
py -3 scripts\s1_closed_shadow_run.py `
  --run-id S1-CLOSED-SHADOW-2026-04-30-001 `
  --input mock_data\s0_synthetic\qwen_fact_bundle `
  --output artifacts\s1_closed_shadow_runs\2026-04-30-001 `
  --provider fixture `
  --no-writeback `
  --no-customer-visible
```

Required outputs:

```text
artifacts/s1_closed_shadow_runs/2026-04-30-001/run_record.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/artifact_manifest.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/safety_scan.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/case_summary.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/final_status.json
```

Minimum behavior:

| Case | Expected result |
| --- | --- |
| Valid synthetic input folder | `PASS_FOR_MVP_FIXTURE` or `PASS_WITH_NOTES_FOR_MVP_FIXTURE` |
| Missing input folder | `HOLD_INPUT_NOT_FOUND` |
| Empty input folder | `HOLD_NO_INPUT_FILES` |
| Secret/token/auth marker found | `HOLD_SECRET_OR_AUTH_FINDING` |
| Customer-visible flag requested | `HOLD_CUSTOMER_VISIBLE_NOT_ALLOWED` |
| Write-back flag requested | `HOLD_WRITEBACK_NOT_ALLOWED` |
| Provider unknown | `HOLD_UNSUPPORTED_PROVIDER` |

Non-goals for MVP-01:

```text
no live connector
no production write-back
no customer-visible output
no secrets
no backend API
no database migration
no deploy
no Qwen call
```

## 6. MVP-02 Artifact Contract

`run_record.json` should include:

```json
{
  "run_id": "S1-CLOSED-SHADOW-2026-04-30-001",
  "provider": "fixture",
  "status": "PASS_FOR_MVP_FIXTURE",
  "input_root": "mock_data/s0_synthetic/qwen_fact_bundle",
  "output_root": "artifacts/s1_closed_shadow_runs/2026-04-30-001",
  "customer_visible_output": false,
  "production_writeback": false,
  "qwen_autonomous_action": false
}
```

`final_status.json` should include:

```json
{
  "final_status": "PASS_FOR_MVP_FIXTURE",
  "can_show_in_local_demo": true,
  "can_deploy_to_customer_production": false,
  "next_step": "FRONTEND_ARTIFACT_VIEW"
}
```

## 7. MVP-03 Frontend Viewer

Create or update the minimum surface needed to inspect a completed artifact:

```text
frontend/src/secupilot/s1/
frontend/src/secupilot/s1/S1RunSummaryPanel.tsx
frontend/src/secupilot/s1/s1ArtifactTypes.ts
frontend/src/secupilot/s1/s1ArtifactFixtures.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
```

The viewer should show:

```text
run status
run id
provider
case count
safety scan state
HOLD/PASS reason
artifact manifest count
customer visibility = NO
write-back = NO
Qwen autonomy = NO
```

Do not build enterprise RBAC, real connector setup, production deployment UI, or customer-visible publish controls in this slice.

## 8. Tooling Roles

### Codex

Use Codex for:

```text
implementing exact file slices
running local tests
updating artifacts
preparing concise closeout
```

Codex must not:

```text
invent run outputs
hide HOLDs
silently broaden scope
start recurring automations that have no executable work
```

### VS Code

Use VS Code as the human-supervised implementation workspace:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
code.cmd .
code.cmd scripts\s1_closed_shadow_run.py backend\tests\test_s1_closed_shadow_run.py
```

Recommended later `.vscode/tasks.json` tasks:

```text
S1 Runner Fixture
Backend Targeted Test
Frontend Test
Frontend Build
Fast Gate
```

### Full Automation

Use one-shot commands only. No recurring empty loops.

Baseline:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder'
git -c core.quotepath=false status --short --branch
py -3 scripts\git_preflight.py --mode fast
```

Targeted backend loop:

```powershell
py -3 -m unittest -q backend.tests.test_s1_closed_shadow_run
py -3 scripts\s1_closed_shadow_run.py --run-id S1-CLOSED-SHADOW-2026-04-30-001 --input mock_data\s0_synthetic\qwen_fact_bundle --output artifacts\s1_closed_shadow_runs\2026-04-30-001 --provider fixture --no-writeback --no-customer-visible
```

Frontend loop:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder\frontend'
npm run test -- --run
npm run build
npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts
```

Local inspection:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder\frontend'
npm run dev -- --port 5173
```

### Claude Code

Local `claude.exe` / `claude.cmd` is visible, but the governed `cc switch` path is not verified. Use Claude Code as focused review only, not as an autonomous implementation owner.

Suggested focused review command:

```powershell
claude --print "Review only the current diff for the S1 Fast MVP runner. Check correctness, unsafe data handling, secret retention, production write-back, customer-visible output, test gaps, and overengineering. Return findings ordered by severity. Do not edit files."
```

If Claude Code is unavailable or returns tool/path errors, route review through Claude Web or human review.

### Claude Web

Use Claude Web for product and customer demo review after a runnable artifact exists.

Manual prompt:

```text
Review SecuPilot Fast MVP after S1 runner artifact output exists. Focus on whether the current product loop is demoable, understandable, safe for local/customer trial, and not pretending to be production-integrated. Identify blocking product gaps and highest-leverage next iteration.
```

Claude Web output is review evidence, not automatic approval.

### SWE

Use SWE only after an exact slice is named with disjoint file ownership.

Allowed SWE usage examples:

```text
Worker A: frontend S1RunSummaryPanel only
Worker B: backend tests for s1_closed_shadow_run only
Worker C: artifact schema validation only
```

Do not use SWE for:

```text
route selection
permission decisions
production deployment
broad refactors
multi-area changes without exact file ownership
```

## 9. Qwen Integration Position

Qwen is needed for AI-value proof, but it should not block product MVP.

Implementation order:

```text
1. fixture provider
2. external-output provider
3. qwen-api provider
```

Future Qwen command shape:

```powershell
$env:SECUPILOT_QWEN_BASE_URL='http://<approved-host>:8000/v1'
$env:SECUPILOT_QWEN_MODEL='qwen-72b'
py -3 scripts\s1_closed_shadow_run.py --run-id S1-CLOSED-SHADOW-2026-04-30-002 --input <approved-input-root> --output artifacts\s1_closed_shadow_runs\2026-04-30-002 --provider qwen-api --no-writeback --no-customer-visible
```

Do not put tokens, SSH keys, API keys, auth headers, or credential-bearing URLs in commands, docs, or artifacts.

## 10. Client Trial Path

Client trial can start before full backend integration if it is scoped as:

```text
local/offline trial
synthetic or approved package input
no production write-back
no customer-visible publish path
no live SIEM/EDR connector
manual artifact import/export
```

Full production integration is a later lane:

```text
SIEM/EDR connector
customer auth/RBAC
secret management
case database
audit log
monitoring
deployment hardening
rollback
tenant/environment isolation
```

## 11. Proposed 3-Day Execution Plan

Day 1:

```text
Implement MVP-01 S1 runner and backend tests.
Run targeted backend tests and fast gate.
Produce first local artifact from synthetic input.
```

Day 2:

```text
Implement MVP-03 frontend artifact viewer.
Run frontend unit/build/e2e.
Open local dev server for inspection.
```

Day 3:

```text
Claude Code focused review.
Claude Web product review.
Package local MVP demo.
Decide whether next iteration is Qwen provider or customer local trial packaging.
```

## 12. Discussion Points Before Execution

Decide these before the first code patch:

| Topic | Recommended answer |
| --- | --- |
| First provider | `fixture` |
| First input | `mock_data/s0_synthetic/qwen_fact_bundle` |
| First output root | `artifacts/s1_closed_shadow_runs/2026-04-30-001` |
| Frontend route | Reuse current workbench first, add S1 panel without new router |
| Qwen in first slice | No |
| Customer trial mode | Local/offline first |
| Automation style | One-shot commands, no recurring loop |
| Commit style | Small commits per executable slice |

## 13. Ready-To-Execute Gate

Execution may begin after discussion if the user confirms:

```text
GO_FAST_MVP_MVP_01_S1_RUNNER
```

That GO authorizes only:

```text
scripts/s1_closed_shadow_run.py
backend/tests/test_s1_closed_shadow_run.py
artifact output under artifacts/s1_closed_shadow_runs/2026-04-30-001/
targeted tests and fast gate
```

It does not authorize Qwen live calls, live connectors, backend API/schema changes, deploy, customer-visible publish, production write-back, or production launch.

## 14. Update 2026-04-30: v1.1 External Runner Package Intake

The following external files were read before implementation:

```text
D:\产品设计\secupilot0421\SecuPilot_S1_Fast_MVP_Closed_Shadow_Run_Package_v1.1_2026-04-30.md
D:\产品设计\secupilot0421\SecuPilot_S1_Fast_MVP_Closed_Shadow_Run_Package_v1.1_2026-04-30.zip
```

Intake hashes:

```text
md  = EA253A0B3936FC6E4A2F36EE0CBD90242F36AA49D89CB769C644B0FFD63A05C1
zip = 51AD3BECD36485E42631B799FA4B22E6163E8367C5616C44B9DF275A58690A25
```

Decision:

```text
S1_FAST_MVP_RUN_PACKAGE_V1_1_ACCEPTED_AS_IMPLEMENTATION_INPUT
ADOPT_ARTIFACT_CONTRACT = YES
ADOPT_SAFETY_RULES = YES
ADOPT_PROVIDER_SHAPE = YES
COPY_VERBATIM = NO
```

Required adaptation:

```text
support the user-selected input folder mock_data/s0_synthetic/qwen_fact_bundle
map QwenFactBundle files into metadata-only S1 cases
keep qwen-api provider as approved-output import only, no live API calls in MVP-01
add repo-native backend tests because the package does not include tests
defer frontend artifact reader to MVP-03
```

## 15. Update 2026-04-30: MVP-01 / MVP-02 Executed

MVP-01 and MVP-02 are implemented and committed in:

```text
dd0d3d2 feat: add S1 closed shadow fixture runner
```

The executed local command was:

```powershell
py -3 scripts\s1_closed_shadow_run.py --run-id S1-CLOSED-SHADOW-2026-04-30-001 --input mock_data\s0_synthetic\qwen_fact_bundle --output artifacts\s1_closed_shadow_runs\2026-04-30-001 --provider fixture --no-writeback --no-customer-visible
```

Result:

```text
final_outcome = S1_CLOSED_SHADOW_PASS_WITH_NOTES
case_count = 20
provider = fixture
qwen_used = false
customer_visible_output = false
production_writeback = false
safety_scan_findings = 0
```

## 16. Update 2026-04-30: MVP-03 Frontend Artifact Viewer

MVP-03 adds the S1 artifact viewer to the existing workbench:

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

Frontend route:

```text
/s1-run
```

Viewer scope:

```text
show S1 run status
show run id / GO record / provider / case count
show safety scan finding count
show artifact manifest rows
show all 20 synthetic case summaries
show boundary facts: customer-visible output = NO, production write-back = NO, Qwen autonomy = NO
```

Non-goals preserved:

```text
no backend API
no schema change
no live file-system reader
no live Qwen call
no live connector
no deploy
no customer-visible publish control
no approve/deploy/publish action button
```

Verification:

```powershell
Set-Location -LiteralPath 'D:\产品设计\New folder\frontend'
npm run test -- --run App.test.tsx
npm run build
```
