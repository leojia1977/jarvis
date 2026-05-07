# GOAL-MVP-51_REVIEWER_EVIDENCE_LABEL_CLEANUP

## Goal ID

```text
GOAL-MVP-51_REVIEWER_EVIDENCE_LABEL_CLEANUP
```

## Goal type

```text
page
```

## Goal statement

```text
Address RC-014 backlog item RFB-RC014-004 by renaming the /s1-run navigation label from "S1 证据" to "S1 证据清单" so reviewer wording aligns with artifact manifest semantics, without changing route behavior or safety boundaries.
```

## Primary executable object

```text
page=/s1-run
test=frontend/src/App.test.tsx
test=frontend/tests/e2e/s1-artifact-viewer.spec.ts
test=frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
validator=scripts/validate_review_screenshots.py
validator=scripts/validate_local_trial_rc_consistency.py
closeout=docs/S6_FAST_MVP_MVP_51_REVIEWER_EVIDENCE_LABEL_CLEANUP_2026_05_07.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
```

## Output paths

```text
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
docs/goals/GOAL-MVP-51_REVIEWER_EVIDENCE_LABEL_CLEANUP.md
docs/S6_FAST_MVP_MVP_51_REVIEWER_EVIDENCE_LABEL_CLEANUP_2026_05_07.md
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-mobile.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.text.json
artifacts/review_screenshot_safety/local-offline-trial-rc-014-cn-review/screenshot_safety_scan_mvp51.json
artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review/rc_consistency_check_mvp51.json
artifacts/reviews/claude_code/mvp-51-current-diff-review-20260507.txt
```

## Allowed files

```text
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
docs/goals/GOAL-MVP-51_REVIEWER_EVIDENCE_LABEL_CLEANUP.md
docs/S6_FAST_MVP_MVP_51_REVIEWER_EVIDENCE_LABEL_CLEANUP_2026_05_07.md
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-mobile.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.text.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.png
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.text.json
artifacts/review_screenshot_safety/local-offline-trial-rc-014-cn-review/screenshot_safety_scan_mvp51.json
artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review/rc_consistency_check_mvp51.json
artifacts/reviews/claude_code/mvp-51-current-diff-review-20260507.txt
```

## Allowed scope

```text
local/offline only
single-label copy cleanup for /s1-run nav entry
matching unit/e2e test updates
local screenshot safety and RC consistency validation
automated engineering review capture
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
API keys
secrets/tokens/auth headers/raw customer logs
live connectors
production write-back
customer-visible publish/deploy/output
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-51_REVIEWER_EVIDENCE_LABEL_CLEANUP.md
Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-014-cn-review/screenshot_safety_scan_mvp51.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --zip-name local-offline-trial-rc-015-cn-review-package-20260507.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-package-20260507.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review/rc_consistency_check_mvp51.json
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
S1 nav still renders "S1 证据" instead of "S1 证据清单"
/s1-run route is no longer reachable from nav
UI tests/build/Playwright fail twice in the same way
screenshot safety validator reports blocking findings
RC consistency validator reports blocking findings
any boundary flips to true
```

## Rollback

```text
revert changed files listed in Allowed files only
preserve failure evidence
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
updated Playwright screenshots and text evidence
screenshot_safety_scan_mvp51.json
rc_consistency_check_mvp51.json
automated review artifact or REVIEW_TOOL_UNAVAILABLE_NON_BLOCKING record
closeout note with exact commands
```

## Safety sentinels

```text
no customer_visible_output=true
no production_writeback=true
no live_qwen_api=true
no live_connectors=true
no Authorization: / Bearer / refresh_token in artifacts
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock a follow-up backlog closeout Goal to mark RFB-RC014-004 BACKLOG_CLOSED with this commit evidence.
If PASS_WITH_NOTES, capture notes without expanding scope.
If HOLD, stop and report blocker.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-51 reviewer evidence label cleanup
do not push unless separately authorized
```
