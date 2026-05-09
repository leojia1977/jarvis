# GOAL-MVP-162 Private Preview Customer Task Flow

## Goal ID

```text
GOAL-MVP-162_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW
```

## Goal type

```text
page
```

## Goal statement

```text
Add a customer-readable private preview task flow that guides engineer, manager, and CTO users through the product without exposing debug fixtures.
```

## Primary executable object

```text
page=frontend/src/secupilot/s1/S1LocalTrialView.tsx
fixture=frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
tests=frontend/src/App.test.tsx + frontend/tests/e2e/s1-artifact-viewer.spec.ts + frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
closeout=docs/S6_FAST_MVP_GOAL_MVP_162_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW_2026_05_09.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review/**
docs/goals/GOAL-MVP-161_PRIVATE_PREVIEW_ROUTE_MAP_INDEX.md
```

## Output paths

```text
docs/goals/GOAL-MVP-162_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW.md
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
docs/S6_FAST_MVP_GOAL_MVP_162_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW_2026_05_09.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-162_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW.md
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
docs/S6_FAST_MVP_GOAL_MVP_162_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW_2026_05_09.md
```

## Allowed scope

```text
customer task flow copy and route guidance in /s1-trial private preview view
engineer/manager/CTO route visibility and stale RC wording cleanup
frontend unit/build/playwright assertion updates aligned to new task flow wording
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
production write-back
customer-visible publish/deploy/output
external pilot
production launch
secrets/tokens/auth headers/raw customer logs
autonomous remediation/action-mode choice
backend API/schema migration
push
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-162_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW.md
Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
customer task flow exposes P1/P2/P3, Mock Fixture, Expert Mode, or stale RC wording
first screen is dominated by evidence paths instead of product tasks and next actions
engineer, manager, or CTO path is missing
frontend unit/build/playwright fails twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
leave unrelated dirty/untracked residue untouched
```

## Evidence contract

```text
goal card validator PASS output
frontend unit test PASS output for src/App.test.tsx
frontend build PASS output
playwright smoke+visual PASS output for targeted specs
diff --check PASS output
closeout with exact assertion evidence and hold checks
```

## Safety sentinels

```text
real_data=false
masked_real_data=false
live_qwen_api=false
live_connectors=false
production_writeback=false
customer_visible_output=false
push=false
```

## Merge rule

```text
Stage and commit only allowed files after all acceptance commands PASS and no HOLD condition triggers.
Reject unrelated changes; do not stage unrelated files.
Do not push.
```

## Next unlock

```text
PASS unlock: rerun picker and continue next selected goal.
HOLD behavior: report exact failing check and stop this run.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-162 private preview customer task flow
stage only Goal files
do not push
```
