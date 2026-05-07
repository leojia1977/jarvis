# S6 Fast MVP MVP-28 RC Diff Checker Closeout

Date: 2026-05-07

Goal ID: GOAL-MVP-28_RC_DIFF_CHECKER

Decision: PASS

## Scope

MVP-28 adds a local/offline RC consistency validator so RC package drift is caught before reviewer handoff.

The validator checks:

- `candidate` and `source_candidate` consistency across `package_manifest.json`, `PACKAGE_INDEX_中文.json`, and `SCREENSHOT_INDEX.json`
- `package_dir` and `zip_name` consistency across manifest/index/zip path
- required reviewer docs, evidence files, screenshots, and manifest entries
- manifest SHA256 values
- screenshot PNG validity
- unexpected stale candidate tokens
- unexpected stale package slugs
- local/offline boundary fields remaining `false`

This closeout does not authorize real data, masked-real data, live Qwen/API calls, live connectors, customer-visible publish/deploy, production write-back, backend API/schema migration, or autonomous Qwen action.

## Executable Objects

- Goal card: `docs/goals/GOAL-MVP-28_RC_DIFF_CHECKER.md`
- Validator: `scripts/validate_local_trial_rc_consistency.py`
- Unit tests: `backend/tests/test_validate_local_trial_rc_consistency.py`
- Scan artifact: `artifacts/local_trial_rc_consistency/local-offline-trial-rc-009-cn-review/rc_consistency_check.json`

## Verification

Command:

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-MVP-28_RC_DIFF_CHECKER.md
```

Result: PASS

Command:

```powershell
py -3 -m unittest backend.tests.test_validate_local_trial_rc_consistency
```

Result: PASS, 4 tests

Command:

```powershell
py -3 scripts\validate_local_trial_rc_consistency.py --package-dir artifacts\local_demo_packages\local-offline-trial-rc-009-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_009_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_008_CN --zip-name local-offline-trial-rc-009-cn-review-package-20260507.zip --zip-path artifacts\local_demo_packages\local-offline-trial-rc-009-cn-review-package-20260507.zip --output-json artifacts\local_trial_rc_consistency\local-offline-trial-rc-009-cn-review\rc_consistency_check.json
```

Result: PASS

## Scan Result

Package: `artifacts/local_demo_packages/local-offline-trial-rc-009-cn-review`

Zip: `local-offline-trial-rc-009-cn-review-package-20260507.zip`

Checked JSON files:

- `PACKAGE_INDEX_中文.json`
- `SCREENSHOT_INDEX.json`
- `package_manifest.json`

Blocking finding count: 0

## HOLD Behavior

The validator returns HOLD if:

- candidate/source_candidate drift appears
- package_dir/zip_name drift appears
- a required reviewer, evidence, screenshot, or manifest entry is missing
- a manifest SHA256 does not match the actual file
- an unexpected stale RC candidate token appears
- an unexpected stale package slug appears
- a required boundary field is not `false`

## Next Unlock

MVP-28 unlocks adding this consistency check to the next RC package builder or local/offline reviewer handoff flow.

Recommended next item:

- Select the next exact GOAL-* by product route.

