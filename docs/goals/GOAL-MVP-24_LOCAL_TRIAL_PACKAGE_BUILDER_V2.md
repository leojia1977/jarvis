# GOAL-MVP-24_LOCAL_TRIAL_PACKAGE_BUILDER_V2

## Goal ID

```text
GOAL-MVP-24_LOCAL_TRIAL_PACKAGE_BUILDER_V2
```

## Goal type

```text
package
```

## Goal statement

```text
Build a self-contained RC-009 Chinese local/offline reviewer package from the accepted RC-008 evidence and the MVP-22 productized screenshots.
```

## Primary executable object

```text
script=scripts/build_local_offline_trial_rc.py
package=artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review
artifact=artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review-package-20260507.zip
test=backend/tests/test_build_local_offline_trial_rc.py
closeout=docs/S6_FAST_MVP_MVP_24_LOCAL_TRIAL_PACKAGE_BUILDER_V2_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-008-cn-review/
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
```

## Output paths

```text
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review-package-20260507.zip
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/**
docs/S6_FAST_MVP_MVP_24_LOCAL_TRIAL_PACKAGE_BUILDER_V2_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review/**
artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review-package-20260507.zip
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/**
docs/S6_FAST_MVP_MVP_24_LOCAL_TRIAL_PACKAGE_BUILDER_V2_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
local package generation
local screenshot capture
local tests
local reviewer handoff artifacts
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
production write-back
customer-visible publish/deploy/output
secrets/tokens/auth headers/raw customer logs
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-24_LOCAL_TRIAL_PACKAGE_BUILDER_V2.md
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
npm run test -- src/App.test.tsx
npm run build
npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_009_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_008_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-008-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review-package-20260507.zip --source-commit 0c2a119
```

## HOLD conditions

```text
package manifest missing SHA256
candidate/source_candidate inconsistent
screenshot path missing or cannot open
screenshot exposes P1/P2/P3, Mock Fixture, Expert Mode, or debug controls
safety_scan finding_count > 0
customer_visible_output != false
production_writeback != false
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
delete generated RC-009 package directory and zip only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
package manifest with SHA256
SCREENSHOT_INDEX.json
RC-009 zip artifact
closeout note with exact commands
```

## Safety sentinels

```text
no P1/P2/P3 in reviewer-clean screenshots
no Mock Fixture in reviewer-clean screenshots
no Expert Mode in reviewer-clean screenshots
no Authorization: / Bearer / refresh_token in artifacts
no writeback_enabled=true
no customer_visible_output=true
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-23_REVIEWER_FEEDBACK_EXPORT.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-24 local offline trial package builder
do not push unless separately authorized
```
