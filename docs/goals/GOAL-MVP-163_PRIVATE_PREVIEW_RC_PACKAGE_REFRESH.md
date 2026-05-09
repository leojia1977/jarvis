# GOAL-MVP-163 Private Preview RC Package Refresh

## Goal ID

```text
GOAL-MVP-163_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH
```

## Goal type

```text
package
```

## Goal statement

```text
Refresh the local/private preview RC package after product route-map changes, including validators, screenshots, consistency checks, and zip manifest.
```

## Primary executable object

```text
package_dir=artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review
zip=artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip
outer_zip_manifest=artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip.outer_zip_manifest.json
consistency=artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-consistency-check.json
screenshot_scan=artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
closeout=docs/S6_FAST_MVP_GOAL_MVP_163_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH_2026_05_09.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review/**
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/*
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
```

## Output paths

```text
docs/goals/GOAL-MVP-163_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH.md
artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review
artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip
artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip.outer_zip_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-consistency-check.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
docs/S6_FAST_MVP_GOAL_MVP_163_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH_2026_05_09.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-163_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH.md
artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review
artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip
artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip.outer_zip_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-consistency-check.json
artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
docs/S6_FAST_MVP_GOAL_MVP_163_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH_2026_05_09.md
```

## Allowed scope

```text
RC-020 local/offline package regeneration and consistency validation
screenshot safety scan refresh from Playwright capture outputs
zip and outer zip manifest refresh for RC-020 review handoff
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-163_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH.md
Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_019_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip --source-commit 07acfaa --repo-root . --screenshot-safety-scan artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json --outer-zip-manifest artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip.outer_zip_manifest.json
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_019_CN --zip-name local-offline-trial-rc-020-cn-review-package-20260508.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip --output-json artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-consistency-check.json
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
package or screenshots contain stale RC-019-as-current after RC-020 refresh
manifest, screenshot safety, RC consistency, or outer zip manifest reports blocking findings
package grants customer-visible deploy, live Qwen/API, connector, or production write-back authority
frontend/package command fails twice in the same way
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
frontend unit/build/playwright PASS outputs
screenshot safety scan JSON for expected candidate RC-020
package build output + zip + outer zip manifest
RC consistency JSON PASS result
diff --check PASS output
closeout with exact command evidence and hold checks
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
commit message: feat(secupilot): GOAL-MVP-163 private preview rc package refresh
stage only Goal files
do not push
```
