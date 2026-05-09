# GOAL-MVP-157 RC018 Customer Readable Package

## Goal ID

```text
GOAL-MVP-157_RC018_CUSTOMER_READABLE_PACKAGE
```

## Goal type

```text
package
```

## Goal statement

```text
Build LOCAL_OFFLINE_TRIAL_RC_018_CN as a customer-readable local/offline review package that starts from the product path, not raw artifact tables.
```

## Primary executable object

```text
script=scripts/build_rc018_customer_review_package.py
test=backend/tests/test_build_rc018_customer_review_package.py
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/REVIEWER_START_HERE_中文.md
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/01_REVIEW_PROMPT.md
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/02_PRODUCT_ROUTE_MAP_中文.md
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/03_REVIEWER_CHECKLIST_中文.md
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/04_FEEDBACK_TEMPLATE_中文.md
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/package_manifest.json
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/SCREENSHOT_INDEX_中文.json
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/safety_scan.json
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/eci_vfe/output_guard_scan.json
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/eci_vfe/chain_assessment_summary.json
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/eci_vfe/forecast_candidate_summary.json
zip=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip.outer_zip_manifest.json
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
artifact=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json
closeout=docs/S6_FAST_MVP_GOAL_MVP_157_RC018_CUSTOMER_READABLE_PACKAGE_2026_05_09.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/screenshots/*.png
artifacts/eci_vfe_fixture_runs/rc001/output_guard_scan.json
artifacts/eci_vfe_fixture_runs/rc001/chain_assessment.json
artifacts/eci_vfe_fixture_runs/rc001/forecast_candidates.json
```

## Output paths

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

## Allowed files

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

## Allowed scope

```text
customer-readable local/offline package copywriting and manifest refresh only
RC018 screenshot index and ECI/VFE summary linkage
zip and consistency evidence generation
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
secrets/tokens/auth headers/raw payloads
attacker-readable attack path/topology
autonomous action authority
push
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-157_RC018_CUSTOMER_READABLE_PACKAGE.md
py -3 -m unittest backend.tests.test_build_rc018_customer_review_package
py -3 scripts/build_rc018_customer_review_package.py --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --output-dir artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip --repo-root .
py -3 -c "import json, pathlib; s=json.loads(pathlib.Path(r'artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json').read_text(encoding='utf-8')); c=json.loads(pathlib.Path(r'artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json').read_text(encoding='utf-8')); assert s['status']=='PASS' and s['blocking_finding_count']==0; assert c['status']=='PASS'"
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
package starts from artifact tables instead of product route map
required customer-path screenshots are missing
ECI/VFE appears as standalone technical route instead of product explanation
package exposes P1/P2/P3, Mock Fixture, Expert Mode, provider/stub/dry-run wording, stale RC wording, raw payloads, secrets, auth headers, PoC, exploit steps, or attacker-readable topology
output_guard_scan missing or not PASS
manifest or screenshot/consistency evidence reports blocking findings
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
leave unrelated historical residue untouched
```

## Evidence contract

```text
goal card validator PASS json
unittest output for rc018 package builder
rc018 package build command output
screenshot safety + consistency evidence json PASS
zip + outer zip manifest with sha256
closeout report with exact command outcomes and safety assertions
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
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock RC018 review decision export.
If HOLD, stop and report exact failing artifact.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-157 rc018 customer readable package
stage and commit only Goal files
do not push
```
