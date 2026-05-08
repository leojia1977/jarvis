# GOAL-MVP-92_LOCAL_PRIVATE_TRIAL_RC_WITH_QWEN_READINESS

## Goal ID

```text
GOAL-MVP-92_LOCAL_PRIVATE_TRIAL_RC_WITH_QWEN_READINESS
```

## Goal type

```text
package
run-artifact
test-report
```

## Goal statement

```text
Build the next local/offline private trial RC package with Qwen synthetic provider readiness evidence included, while keeping the package no-network, no-live-call, no-real-data, and reviewer-clean.
```

## Primary executable object

```text
package=artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip
script=scripts/build_local_offline_trial_rc.py
test=frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
validator=scripts/validate_review_screenshots.py
closeout=docs/S6_FAST_MVP_MVP_92_LOCAL_PRIVATE_TRIAL_RC_WITH_QWEN_READINESS_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report.json
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/secupilot/s1/s1QwenProviderReadiness.ts
```

## Output paths

```text
docs/goals/GOAL-MVP-92_LOCAL_PRIVATE_TRIAL_RC_WITH_QWEN_READINESS.md
docs/S6_FAST_MVP_MVP_92_LOCAL_PRIVATE_TRIAL_RC_WITH_QWEN_READINESS_CLOSEOUT_2026_05_08.md
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/secupilot/s1/s1QwenProviderContract.ts
frontend/src/secupilot/s1/s1QwenProviderReadiness.ts
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/
artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip
artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip.outer_zip_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-consistency-check.json
```

## Allowed files

```text
docs/goals/GOAL-MVP-92_LOCAL_PRIVATE_TRIAL_RC_WITH_QWEN_READINESS.md
docs/S6_FAST_MVP_MVP_92_LOCAL_PRIVATE_TRIAL_RC_WITH_QWEN_READINESS_CLOSEOUT_2026_05_08.md
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/secupilot/s1/s1QwenProviderContract.ts
frontend/src/secupilot/s1/s1QwenProviderReadiness.ts
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/
artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip
artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip.outer_zip_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-consistency-check.json
```

## Allowed scope

```text
local/offline RC package generation
reviewer-clean frontend candidate/source/package wording
local package builder support for multiple validation artifacts
local screenshot capture and validator output
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
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_016_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip --source-commit <current-head> --repo-root . --screenshot-safety-scan artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report_中文.md --outer-zip-manifest artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip.outer_zip_manifest.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_016_CN --zip-name local-offline-trial-rc-017-cn-review-package-20260508.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip --output-json artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-consistency-check.json
py -3 -m unittest -q backend.tests.test_build_local_offline_trial_rc
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-92_LOCAL_PRIVATE_TRIAL_RC_WITH_QWEN_READINESS.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
screenshot validator reports any blocking finding
RC-017 screenshots expose P1/P2/P3, Mock Fixture, Expert Mode, or stale RC-001..RC-007 wording
package candidate/source_candidate/package_dir/zip_name are inconsistent
package manifest missing SHA256 or validation artifacts
Qwen readiness evidence implies live Qwen/API call, network call, secret read, or connector usage
tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert listed frontend/script/test/doc files
delete generated RC-017 package directory, ZIP, outer manifest, and consistency check
preserve failed validator output if failure occurred
```

## Evidence contract

```text
frontend unit test output
frontend build output
Playwright screenshot output
screenshot_safety_scan.json
RC-017 package_manifest.json and outer zip manifest
RC consistency check output
package builder unit test output
goal card validator output
closeout report with exact commands
```

## Safety sentinels

```text
no live_qwen_api=true
no data-network-request=true
no secret value read
no real_data=true
no masked_real_data=true
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
If PASS, unlock GOAL-MVP-93_CUSTOMER_TRIAL_ENTRY_CLEANUP.
If HOLD, stop and report the exact package, screenshot, or validator failure.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-92 local private trial rc with qwen readiness
stage and commit only Goal files
do not push
```
