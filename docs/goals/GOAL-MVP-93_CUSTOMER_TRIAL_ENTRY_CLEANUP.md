# GOAL-MVP-93_CUSTOMER_TRIAL_ENTRY_CLEANUP

## Goal ID

```text
GOAL-MVP-93_CUSTOMER_TRIAL_ENTRY_CLEANUP
```

## Goal type

```text
page
package
test-report
```

## Goal statement

```text
Clean up the /s1-trial product entry so the first screen explains SecuPilot as a customer-facing trial experience for engineers through CTOs, while keeping technical reconciliation and package evidence available but visually lower priority.
```

## Primary executable object

```text
page=frontend/src/secupilot/s1/S1LocalTrialView.tsx
package=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip
test=frontend/src/App.test.tsx
validator=scripts/validate_review_screenshots.py
closeout=docs/S6_FAST_MVP_MVP_93_CUSTOMER_TRIAL_ENTRY_CLEANUP_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review/
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/
```

## Output paths

```text
docs/goals/GOAL-MVP-93_CUSTOMER_TRIAL_ENTRY_CLEANUP.md
docs/S6_FAST_MVP_MVP_93_CUSTOMER_TRIAL_ENTRY_CLEANUP_CLOSEOUT_2026_05_08.md
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip.outer_zip_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
```

## Allowed files

```text
docs/goals/GOAL-MVP-93_CUSTOMER_TRIAL_ENTRY_CLEANUP.md
docs/S6_FAST_MVP_MVP_93_CUSTOMER_TRIAL_ENTRY_CLEANUP_CLOSEOUT_2026_05_08.md
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip.outer_zip_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
```

## Allowed scope

```text
/s1-trial customer trial entry UI copy and layout cleanup
RC-018 candidate/source/package wording updates
local screenshot capture and screenshot safety scan
local/offline RC package generation
docs-only Goal and closeout records
stage and commit this Goal if all acceptance commands pass
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
secrets/tokens/auth headers/raw customer logs
live connectors
production write-back
customer-visible publish/deploy/output
external pilot
production launch
backend API/schema migration
push
```

## Acceptance commands

```text
Set-Location -LiteralPath frontend; npm run test -- --run src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip --source-commit <current-head> --repo-root . --screenshot-safety-scan artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report_中文.md --outer-zip-manifest artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip.outer_zip_manifest.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --zip-name local-offline-trial-rc-018-cn-review-package-20260508.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip --output-json artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-93_CUSTOMER_TRIAL_ENTRY_CLEANUP.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
/s1-trial first screen still reads mainly as a package evidence table
role entry does not cover engineer, analyst lead, security owner, and CTO/deployment perspectives
screenshot validator reports any blocking finding
RC-018 candidate/source/package/zip wording is inconsistent
package manifest missing SHA256 or validation artifacts
UI claims customer deployment, production write-back, real data, live Qwen/API, or connector usage is enabled
tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert listed frontend/doc files
delete generated RC-018 package directory, ZIP, outer manifest, and consistency check
preserve failed screenshot validator output if failure occurred
```

## Evidence contract

```text
frontend unit test output
frontend build output
Playwright smoke output
Playwright screenshot output
screenshot_safety_scan.json
RC-018 package_manifest.json and outer zip manifest
RC consistency check output
goal card validator output
closeout report with exact commands
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no production_writeback=true
no customer_visible_output=true
no reviewer-facing P1/P2/P3, Mock Fixture, Expert Mode, or stale RC wording
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock the next product acceleration Goal selected from the product acceleration pool.
If HOLD, stop and report the UI, screenshot, or package inconsistency.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-93 customer trial entry cleanup
stage and commit only Goal files
do not push
```
