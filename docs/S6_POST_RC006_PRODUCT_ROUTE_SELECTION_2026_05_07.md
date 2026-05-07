# S6 Post-RC006 Product Route Selection 2026-05-07

## 1. Entry

This route follows:

```text
docs/S6_FAST_MVP_RC_006_S1_LOCAL_OFFLINE_GO_NOGO_READINESS_CLOSEOUT_2026_05_06.md
```

RC-006 closed S1 local/offline readiness for internal review only.

## 2. Decision

```text
POST_RC006_PRODUCT_ROUTE_SELECTION_CREATED
SELECTED_ROUTE = FAST_INTERNAL_LOCAL_OFFLINE_TRIAL_PRODUCTIZATION
START_NEXT_ITEMS = MVP_14_LOCAL_OFFLINE_TRIAL_LAUNCHER_AND_MVP_15_REVIEWER_USER_WALKTHROUGH
CUSTOMER_VISIBLE_OR_DEPLOY_GO = NOT_AUTHORIZED
```

This route moves SecuPilot from repeated local RC review into a usable internal local/offline trial surface.

## 3. Selected Work

| Item | Outcome |
| --- | --- |
| MVP-14 | Add a local/offline trial launcher command that verifies the reviewed S1 package and can start a local browser preview |
| MVP-15 | Add a reviewer/user walkthrough page in the existing frontend workbench for the S1 local/offline package |

## 4. Why This Route

The RC-002 through RC-006 chain already proves that the current package is reviewable and boundary-safe for local/offline internal review.

The next product value is making that package easy to open, inspect, and walk through without asking reviewers to reconstruct paths from docs.

## 5. Routes Not Selected

| Route | Reason |
| --- | --- |
| More RC-only review loops | RC-006 already closes the current local/offline readiness chain |
| Live Qwen integration | Still requires a separate explicit GO and must not be hidden inside local trial work |
| Customer-visible trial or deploy | Not authorized by RC-006 |
| Real or masked-real data trial | Not authorized by RC-006 |

## 6. Exact Files

Planned implementation files:

```text
scripts/launch_s1_local_offline_trial.ps1
.vscode/tasks.json
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
docs/S6_FAST_MVP_MVP_14_15_LOCAL_OFFLINE_TRIAL_LAUNCHER_AND_WALKTHROUGH_2026_05_07.md
```

## 7. Exact Commands

Verification commands:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\launch_s1_local_offline_trial.ps1 -CheckOnly -SkipBuild
cd frontend
npm run test -- src/App.test.tsx
npm run build
npx playwright test tests/e2e/s1-artifact-viewer.spec.ts
```

Trial launch command:

```text
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\launch_s1_local_offline_trial.ps1
```

## 8. Non-Authorization

This route does not authorize:

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
