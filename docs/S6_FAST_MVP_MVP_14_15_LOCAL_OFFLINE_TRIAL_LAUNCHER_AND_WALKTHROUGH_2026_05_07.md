# S6 Fast MVP MVP-14/15 Local Offline Trial Launcher And Walkthrough 2026-05-07

## 1. Entry

This implementation follows:

```text
docs/S6_POST_RC006_PRODUCT_ROUTE_SELECTION_2026_05_07.md
```

## 2. Decision

```text
MVP_14_LOCAL_OFFLINE_TRIAL_LAUNCHER_IMPLEMENTED
MVP_15_REVIEWER_USER_WALKTHROUGH_IMPLEMENTED
SCOPE = LOCAL_OFFLINE_INTERNAL_TRIAL_ONLY
CUSTOMER_VISIBLE_OR_DEPLOY_GO = NOT_AUTHORIZED
```

## 3. Implementation

| Item | Files |
| --- | --- |
| MVP-14 launcher | `scripts/launch_s1_local_offline_trial.ps1`, `.vscode/tasks.json` |
| MVP-15 walkthrough | `frontend/src/secupilot/s1/S1LocalTrialView.tsx`, `frontend/src/App.tsx`, `frontend/src/App.css`, `frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts` |
| Tests | `frontend/src/App.test.tsx`, `frontend/tests/e2e/s1-artifact-viewer.spec.ts`, `frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts` |

## 4. Local Trial Entry

```text
Route: /s1-trial
Launcher: scripts/launch_s1_local_offline_trial.ps1
Package: artifacts/local_demo_packages/s1-closed-shadow-local-offline-trial-rc-004
```

The launcher validates required package files, confirms boundary fields remain false, confirms safety findings are zero, and can start a local Vite preview on `127.0.0.1`.

## 5. Verification Commands

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\launch_s1_local_offline_trial.ps1 -CheckOnly -SkipBuild
cd frontend
npm run test -- src/App.test.tsx
npm run build
npx playwright test tests/e2e/s1-artifact-viewer.spec.ts
```

## 6. Non-Authorization

This MVP-14/15 implementation does not authorize:

```text
real data
masked-real data
live Qwen/API calls
live connectors
production connectors
production write-back
customer-visible publish/deploy/output
external pilot execution
production launch
credential handling
secrets/tokens/auth headers in repo, docs, artifacts, commands, or chat
push
```
