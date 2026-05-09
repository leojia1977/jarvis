# S6 Fast Product GOAL-RC018-01 Customer Route Package Hygiene Fix

Date: 2026-05-09

Goal: GOAL-RC018-01_CUSTOMER_ROUTE_PACKAGE_HYGIENE_FIX

## Outcome

PASS

## Scope

Fix RC-018 reviewer package hygiene after review found stale root indexes, stale screenshot safety evidence, and engineering validation annex files in the customer-facing zip.

## Reviewer Finding Synthesis

- Team 1: product UI path PASS_WITH_NOTES.
- Team 2: package hygiene HOLD_FOR_UI_OR_PACKAGE_FIXES.
- Aggregate decision before this fix: HOLD_FOR_UI_OR_PACKAGE_FIXES.

## Expected Deliverables

- stale root `PACKAGE_INDEX_中文.json`, `SCREENSHOT_INDEX.json`, `REVIEWER_CHECKLIST_中文.md`, and `FEEDBACK_TEMPLATE_中文.md` removed from package and zip
- package-level `validation/screenshot_safety_scan.json` regenerated for exactly 7 current RC-018 customer-path screenshots
- stale provider/stub/live-Qwen validation annex removed from customer-facing zip
- package manifest, consistency check, screenshot safety summary, outer zip manifest, and zip rebuilt

## Boundary

- real_data=false
- masked_real_data=false
- live_qwen_api=false
- live_connectors=false
- production_writeback=false
- customer_visible_output=false
- push=false

## Verification

PASS:

- `py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-RC018-01_CUSTOMER_ROUTE_PACKAGE_HYGIENE_FIX.md`
- `py -3 -m unittest backend.tests.test_build_rc018_customer_review_package`
- `py -3 scripts\build_rc018_customer_review_package.py --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --output-dir artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip --repo-root .`
- zip hygiene assertion command: PASS, `checked=7`, `zip_entry_count=23`
- `git -c core.quotepath=false diff --check`

Package output:

- zip: `artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip`
- zip_sha256: `d623f83657a0cf54cca99a2cedec30c59734ceed8d7b234455fedf88d96a9456`
- package_manifest_sha256: `863807e814f1515d22a8e30b72b027f40f761a72d8b7ab61a8b8a05fec5647c8`
- package-level screenshot safety scan: `artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/validation/screenshot_safety_scan.json`
- screenshot_safety_scan.checked: `7`
- screenshot_safety_scan.blocking_finding_count: `0`

Reviewer blocker disposition:

- B1 old root package index/template residue: FIXED.
- B2 old 4-screenshot safety scan: FIXED; package-level scan now covers exactly the current 7 customer-path screenshots.
- B3 provider/stub/live-Qwen engineering validation annex in customer-facing zip: FIXED; only `validation/screenshot_safety_scan.json` remains in the package validation directory.

Current zip entry set excludes:

- `PACKAGE_INDEX_中文.json`
- `SCREENSHOT_INDEX.json`
- root `REVIEWER_CHECKLIST_中文.md`
- root `FEEDBACK_TEMPLATE_中文.md`
- `validation/qwen_live_synthetic_provider_stub_report.json`
- `validation/qwen_live_synthetic_provider_stub_report_中文.md`
- old `screenshots/s1-run-*.png`
- old `screenshots/s1-trial-*.png`

## External Reviewer Rule

Do not send RC-018 to an external reviewer until this Goal is PASS, the zip is rebuilt, package hygiene assertions pass, and the new zip hash is used in the handoff message.
