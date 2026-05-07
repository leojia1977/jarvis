# S6 Fast MVP MVP-47 Result Page Field Downshift Closeout

Date: 2026-05-07

Goal: GOAL-MVP-47_RESULT_PAGE_FIELD_DOWNSHIFT

Decision: PASS_WITH_NOTES

## Scope

MVP-47 closes RC-014 backlog item `RFB-RC014-002` by moving candidate/run-id/data-mode/provider from the `/s1-run` first-screen emphasis into technical reconciliation while preserving local/offline reviewer traceability.

## Outputs

```text
Goal card: docs/goals/GOAL-MVP-47_RESULT_PAGE_FIELD_DOWNSHIFT.md
Page: frontend/src/secupilot/s1/S1ArtifactView.tsx
Unit test: frontend/src/App.test.tsx
Playwright smoke: frontend/tests/e2e/s1-artifact-viewer.spec.ts
Visual evidence: artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-desktop.png
Visual evidence: artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-run-mobile.png
Visual evidence: artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-desktop.png
Visual evidence: artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/s1-trial-mobile.png
Screenshot safety scan: artifacts/review_screenshot_safety/local-offline-trial-rc-014-cn-review/screenshot_safety_scan.json
RC consistency scan: artifacts/local_trial_rc_consistency/local-offline-trial-rc-014-cn-review/rc_consistency_check.json
Automated review artifact: artifacts/reviews/claude_code/mvp-47-current-diff-review-20260507.txt
```

## What Changed

- Removed first-screen summary facts block from `/s1-run` hero so candidate/run id/data mode are no longer front-loaded.
- Removed first-screen KPI card for `离线 provider`.
- Added a dedicated `运行对账字段` section under the existing technical reconciliation `<details>`.
- Kept reviewer traceability using existing/new test ids:
  - `s1-run-id`
  - `s1-provider`
  - `s1-reconciliation-candidate`
  - `s1-reconciliation-data-mode`
- Updated test flow to assert `技术对账信息` is closed by default, then expand and assert the downshifted fields.

## Non-Authorization

This closeout does not authorize real data, masked-real data, live Qwen/API calls, live connectors, production write-back, customer-visible publish/deploy/output, external pilot, production launch, or push.

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-47_RESULT_PAGE_FIELD_DOWNSHIFT.md
```

Result: PASS.

```text
Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
```

Result: PASS, 62 tests passed.

```text
Set-Location -LiteralPath frontend; npm run build
```

Result: PASS.

```text
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
```

Result: PASS, 7 tests passed.

```text
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-014-cn-review/screenshot_safety_scan.json
```

Result: PASS, checked 4 screenshots, blocking_finding_count = 0.

```text
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_013_CN --zip-name local-offline-trial-rc-014-cn-review-package-20260507.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review-package-20260507.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-014-cn-review/rc_consistency_check.json
```

Result: PASS, blocking_finding_count = 0.

```text
git -c core.quotepath=false diff --check
```

Result: PASS (line-ending warnings only).

## Automated Review Status

```text
Tool: claude --print (current diff review)
Artifact: artifacts/reviews/claude_code/mvp-47-current-diff-review-20260507.txt
Decision: PASS_WITH_FINDINGS
```

Disposition:

- F1 (closeout missing): resolved in this document.
- F2 (visual spec maybe needs updates): verified non-issue; visual spec already aligned and passing.
- F3 (accordion assertion risk): mitigated by test updates to expand details before asserting downshifted fields.

No blocking finding remained after mitigation.

## HOLD Review

- Downshift objective completed: PASS.
- Technical reconciliation remains closed by default: PASS.
- `customer_visible_output` remains false: PASS.
- `production_writeback` remains false: PASS.
- Screenshot safety blocking findings: 0.
- RC consistency blocking findings: 0.

## Next Unlock

Create one focused backlog-closeout Goal to mark `RFB-RC014-002` as `BACKLOG_CLOSED` with this goal and commit hash as evidence.
