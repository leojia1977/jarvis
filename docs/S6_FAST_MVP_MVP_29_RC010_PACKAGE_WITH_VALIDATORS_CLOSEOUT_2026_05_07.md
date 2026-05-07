# S6 Fast MVP MVP-29 RC010 Package With Validators Closeout

Date: 2026-05-07

Goal ID: GOAL-MVP-29_RC010_PACKAGE_WITH_VALIDATORS

Decision: PASS

## Scope

MVP-29 builds RC-010 as a Chinese local/offline reviewer package and wires the MVP-27/MVP-28 validators into the package handoff flow.

This closeout does not authorize real data, masked-real data, live Qwen/API calls, live connectors, customer-visible publish/deploy, production write-back, backend API/schema migration, push, or autonomous Qwen action.

## Executable Objects

- Package: `artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review`
- Zip: `artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review-package-20260507.zip`
- Builder: `scripts/build_local_offline_trial_rc.py`
- Screenshot safety scan: `artifacts/review_screenshot_safety/local-offline-trial-rc-010-cn-review/screenshot_safety_scan.json`
- Package consistency scan: `artifacts/local_trial_rc_consistency/local-offline-trial-rc-010-cn-review/rc_consistency_check.json`
- Goal card: `docs/goals/GOAL-MVP-29_RC010_PACKAGE_WITH_VALIDATORS.md`

## Verification

Command:

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-MVP-29_RC010_PACKAGE_WITH_VALIDATORS.md
```

Result: PASS

Command:

```powershell
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
```

Result: PASS, 3 tests

Command:

```powershell
npm run test -- src/App.test.tsx
```

Workdir: `frontend`

Result: PASS, 62 tests

Command:

```powershell
npm run build
```

Workdir: `frontend`

Result: PASS

Command:

```powershell
npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
```

Workdir: `frontend`

Result: PASS, 7 tests

Command:

```powershell
py -3 scripts\validate_review_screenshots.py --screenshot-dir artifacts\s1_closed_shadow_runs\2026-04-30-001\playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_010_CN --output-json artifacts\review_screenshot_safety\local-offline-trial-rc-010-cn-review\screenshot_safety_scan.json
```

Result: PASS

Command:

```powershell
py -3 scripts\build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_010_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_009_CN --source-package artifacts\local_demo_packages\local-offline-trial-rc-009-cn-review --screenshot-dir artifacts\s1_closed_shadow_runs\2026-04-30-001\playwright --output-dir artifacts\local_demo_packages\local-offline-trial-rc-010-cn-review --zip-path artifacts\local_demo_packages\local-offline-trial-rc-010-cn-review-package-20260507.zip --source-commit 069afd0 --screenshot-safety-scan artifacts\review_screenshot_safety\local-offline-trial-rc-010-cn-review\screenshot_safety_scan.json
```

Result: PASS

Zip SHA256: `52dc5f47916632a8c71866669648f83345d59e9ff5a55464549655b8b7fa7352`

Command:

```powershell
py -3 scripts\validate_local_trial_rc_consistency.py --package-dir artifacts\local_demo_packages\local-offline-trial-rc-010-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_010_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_009_CN --zip-name local-offline-trial-rc-010-cn-review-package-20260507.zip --zip-path artifacts\local_demo_packages\local-offline-trial-rc-010-cn-review-package-20260507.zip --output-json artifacts\local_trial_rc_consistency\local-offline-trial-rc-010-cn-review\rc_consistency_check.json
```

Result: PASS

## Validator Results

Screenshot safety:

- status: PASS
- checked screenshots: 4
- blocking findings: 0
- warnings: 0

RC consistency:

- status: PASS
- checked JSON files: `PACKAGE_INDEX_中文.json`, `SCREENSHOT_INDEX.json`, `package_manifest.json`
- blocking findings: 0

## Package Notes

The RC-010 package includes `validation/screenshot_safety_scan.json` in `PACKAGE_INDEX_中文.json` and `package_manifest.json`.

The builder now derives reviewer-facing RC labels from the candidate instead of hardcoding RC-009.

The `/s1-trial` source-candidate phrase that previously displayed `RC-008 中文评审包` has been removed from the reviewer-clean UI.

## Next Unlock

MVP-29 unlocks:

- GOAL-MVP-30_REVIEWER_FEEDBACK_TO_PRODUCT_BACKLOG
- GOAL-MVP-31_QWEN_DRY_PROVIDER_UI_PREVIEW

