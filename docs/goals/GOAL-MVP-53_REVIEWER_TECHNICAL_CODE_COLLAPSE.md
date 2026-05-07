# GOAL-MVP-53_REVIEWER_TECHNICAL_CODE_COLLAPSE

## Goal ID

```text
GOAL-MVP-53_REVIEWER_TECHNICAL_CODE_COLLAPSE
```

## Goal type

```text
page
```

## Goal statement

```text
Close RC-014 reviewer backlog item RFB-RC014-003 by keeping final_outcome technical code out of the /s1-run collapsed first-screen surface and showing it only inside the expanded technical reconciliation details.
```

## Primary executable object

```text
page=/s1-run
source=frontend/src/secupilot/s1/S1ArtifactView.tsx
unit_test=frontend/src/App.test.tsx
playwright=frontend/tests/e2e/s1-artifact-viewer.spec.ts
playwright=frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
closeout=docs/S6_FAST_MVP_MVP_53_REVIEWER_TECHNICAL_CODE_COLLAPSE_2026_05_08.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
```

## Output paths

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
docs/goals/GOAL-MVP-53_REVIEWER_TECHNICAL_CODE_COLLAPSE.md
docs/S6_FAST_MVP_MVP_53_REVIEWER_TECHNICAL_CODE_COLLAPSE_2026_05_08.md
artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review/screenshot_safety_scan_mvp53.json
artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review/rc_consistency_check_mvp53.json
artifacts/reviews/claude_code/mvp-53-current-diff-review-20260508.txt
```

## Allowed files

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
docs/goals/GOAL-MVP-53_REVIEWER_TECHNICAL_CODE_COLLAPSE.md
docs/S6_FAST_MVP_MVP_53_REVIEWER_TECHNICAL_CODE_COLLAPSE_2026_05_08.md
artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review/screenshot_safety_scan_mvp53.json
artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review/rc_consistency_check_mvp53.json
artifacts/reviews/claude_code/mvp-53-current-diff-review-20260508.txt
```

## Allowed scope

```text
local/offline only
reviewer-facing copy and technical code exposure scope on /s1-run
test updates coupled to the UI change
local validators and automated review artifacts
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
API keys
secrets/tokens/auth headers/raw customer logs
live connectors
external tracker writes
production write-back
customer-visible publish/deploy/output
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-53_REVIEWER_TECHNICAL_CODE_COLLAPSE.md
Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review/screenshot_safety_scan_mvp53.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --zip-name local-offline-trial-rc-015-cn-review-package-20260507.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-package-20260507.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review/rc_consistency_check_mvp53.json
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
RFB-RC014-003 is no longer BACKLOG_OPEN at execution start
final_outcome code is still visible in collapsed /s1-run first-screen elements
/s1-run route, local/offline boundary attributes, or reviewer package references regress
screenshot safety validator reports blocking findings
RC consistency validator reports blocking findings
automated review reports blocking P1/P2 issue
any acceptance command fails twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files only
preserve validator/test/review artifacts for audit
do not remove failure evidence
```

## Evidence contract

```text
goal card validation output
App unit test output
frontend build output
Playwright smoke output and refreshed screenshot artifacts
screenshot safety validator json with blocking_finding_count=0
RC consistency validator json with blocking_finding_count=0
automated review artifact or REVIEW_TOOL_UNAVAILABLE_NON_BLOCKING note
closeout note with exact command results
```

## Safety sentinels

```text
no external tracker write
no Authorization: / Bearer / refresh_token in generated artifacts
no raw_payload in generated artifacts
no customer_visible_output=true
no customer_visible_or_deploy_go=true
no production_writeback=true
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock a dedicated backlog closeout Goal for RFB-RC014-003 with commit evidence.
If PASS_WITH_NOTES, capture non-blocking follow-up without changing scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-53 collapse technical code exposure
do not push unless separately authorized
```
