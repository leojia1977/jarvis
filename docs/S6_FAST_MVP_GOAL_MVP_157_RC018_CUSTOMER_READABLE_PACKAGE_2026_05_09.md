# S6 Fast MVP GOAL-MVP-157 RC018 Customer Readable Package

Date: 2026-05-09

Goal: GOAL-MVP-157_RC018_CUSTOMER_READABLE_PACKAGE

Decision: PASS

## Scope

Rebuild RC018 local/offline review package as customer-readable product-path material, with refreshed screenshot index, ECI/VFE summaries, manifest, safety evidence, and zip artifacts.

## Executable Object Delivered

```text
scripts/build_rc018_customer_review_package.py
backend/tests/test_build_rc018_customer_review_package.py
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/REVIEWER_START_HERE_中文.md
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/01_REVIEW_PROMPT.md
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/02_PRODUCT_ROUTE_MAP_中文.md
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/03_REVIEWER_CHECKLIST_中文.md
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/04_FEEDBACK_TEMPLATE_中文.md
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/package_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/SCREENSHOT_INDEX_中文.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/safety_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/eci_vfe/output_guard_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/eci_vfe/chain_assessment_summary.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/eci_vfe/forecast_candidate_summary.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip.outer_zip_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json
```

## Files Changed

```text
docs/goals/GOAL-MVP-157_RC018_CUSTOMER_READABLE_PACKAGE.md
scripts/build_rc018_customer_review_package.py
backend/tests/test_build_rc018_customer_review_package.py
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/REVIEWER_START_HERE_中文.md
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/01_REVIEW_PROMPT.md
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/02_PRODUCT_ROUTE_MAP_中文.md
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/03_REVIEWER_CHECKLIST_中文.md
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/04_FEEDBACK_TEMPLATE_中文.md
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/package_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/SCREENSHOT_INDEX_中文.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/safety_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/eci_vfe/output_guard_scan.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/eci_vfe/chain_assessment_summary.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/eci_vfe/forecast_candidate_summary.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip.outer_zip_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json
docs/S6_FAST_MVP_GOAL_MVP_157_RC018_CUSTOMER_READABLE_PACKAGE_2026_05_09.md
```

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-157_RC018_CUSTOMER_READABLE_PACKAGE.md
```

Result: PASS.

```text
py -3 -m unittest backend.tests.test_build_rc018_customer_review_package
```

Result: PASS, 2 tests passed.

```text
py -3 scripts/build_rc018_customer_review_package.py --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --output-dir artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip --repo-root .
```

Result: PASS, zip_sha256=`b50e81f7044df1b33c4484078bb84b7829de1f97cab204e921eb821b2791a47c`.

```text
py -3 -c "import json, pathlib; s=json.loads(pathlib.Path(r'artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json').read_text(encoding='utf-8')); c=json.loads(pathlib.Path(r'artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json').read_text(encoding='utf-8')); assert s['status']=='PASS' and s['blocking_finding_count']==0; assert c['status']=='PASS'"
```

Result: PASS.

```text
git -c core.quotepath=false diff --check
```

Result: PASS (line-ending warnings only on pre-existing picker files and refreshed rc018 artifacts).

## HOLD Condition Check

- `package starts from artifact tables`: PASS (新增 `02_PRODUCT_ROUTE_MAP_中文.md` + reviewer start path-first instructions).
- `required screenshots missing`: PASS (screenshot index contains 4 required entries).
- `ECI/VFE appears standalone technical route`: PASS (customer docs frame it as product explanation with summary files).
- `forbidden debug/secret/attacker-readable content`: PASS (safety scan json reports 0 blocking).
- `output_guard missing or not PASS`: PASS (`eci_vfe/output_guard_scan.json` copied from PASS source).
- `manifest/scan/consistency/outer-zip blocking`: PASS (consistency and screenshot-safety outputs are PASS; outer zip manifest written).
- `scope expands beyond listed files`: PASS.

## Automated Review Status

```text
Tool: not executed in this Goal run
Status: NOT_RUN
Reason: deterministic package + tests + scan artifacts already produced
```

## Safety and Boundaries

- real_data=false
- masked_real_data=false
- live_qwen_api=false
- live_connectors=false
- production_writeback=false
- customer_visible_output=false
- push=false

## Next Suggested Goal

GOAL-RC018_REVIEW_DECISION_EXPORT.
