# GOAL-ECIVFE-35 Local Review Package

## Goal ID

```text
GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE
```

## Goal type

```text
package
```

## Goal statement

```text
Build a self-contained local/offline ECI/VFE review package with guard scan, UI screenshot index, manifest, and reviewer handoff while remaining fixture-only and metadata-only.
```

## Primary executable object

```text
script=scripts/package_eci_vfe_local_review.py
test=backend/tests/test_package_eci_vfe_local_review.py
artifact=artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/REVIEWER_START_HERE_中文.md
artifact=artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/package_manifest.json
artifact=artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/output_guard_scan.json
artifact=artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/chain_assessment.json
artifact=artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/forecast_candidates.json
artifact=artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/correlation_result.json
artifact=artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/SCREENSHOT_INDEX_中文.json
zip=artifacts/local_demo_packages/eci-vfe-local-offline-rc-001-review-package.zip
closeout=docs/S6_FAST_MVP_GOAL_ECIVFE_35_LOCAL_REVIEW_PACKAGE_2026_05_09.md
```

## Inputs

```text
artifacts/eci_vfe_fixture_runs/rc001/output_guard_scan.json
artifacts/eci_vfe_fixture_runs/rc001/chain_assessment.json
artifacts/eci_vfe_fixture_runs/rc001/forecast_candidates.json
artifacts/eci_vfe_fixture_runs/rc001/correlation_result.json
artifacts/eci_vfe_fixture_runs/rc001/screenshots/*.png
```

## Output paths

```text
docs/goals/GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE.md
scripts/package_eci_vfe_local_review.py
backend/tests/test_package_eci_vfe_local_review.py
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/REVIEWER_START_HERE_中文.md
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/package_manifest.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/output_guard_scan.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/chain_assessment.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/forecast_candidates.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/correlation_result.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/SCREENSHOT_INDEX_中文.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001-review-package.zip
docs/S6_FAST_MVP_GOAL_ECIVFE_35_LOCAL_REVIEW_PACKAGE_2026_05_09.md
```

## Allowed files

```text
docs/goals/GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE.md
scripts/package_eci_vfe_local_review.py
backend/tests/test_package_eci_vfe_local_review.py
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/REVIEWER_START_HERE_中文.md
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/package_manifest.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/output_guard_scan.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/chain_assessment.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/forecast_candidates.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/correlation_result.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/SCREENSHOT_INDEX_中文.json
artifacts/local_demo_packages/eci-vfe-local-offline-rc-001-review-package.zip
docs/S6_FAST_MVP_GOAL_ECIVFE_35_LOCAL_REVIEW_PACKAGE_2026_05_09.md
```

## Allowed scope

```text
local/offline fixture package generation only
guard-passed ECI/VFE json copy with manifest and screenshot index
zip generation with hash evidence
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
external pilot
production launch
autonomous containment/remediation/action-mode choice
backend API/schema migration
push
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE.md
py -3 -m pytest backend\tests\test_package_eci_vfe_local_review.py
py -3 scripts/package_eci_vfe_local_review.py --run-dir artifacts\eci_vfe_fixture_runs\rc001 --output-dir artifacts/local_demo_packages/eci-vfe-local-offline-rc-001 --zip-output artifacts/local_demo_packages/eci-vfe-local-offline-rc-001-review-package.zip
py -3 -c "import json, pathlib; p=pathlib.Path(r'artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/package_manifest.json'); m=json.loads(p.read_text(encoding='utf-8')); assert all('sha256' in x and 'bytes' in x and 'safety_class' in x for x in m['package_files']); s=json.loads(pathlib.Path(r'artifacts/local_demo_packages/eci-vfe-local-offline-rc-001/SCREENSHOT_INDEX_中文.json').read_text(encoding='utf-8')); assert len(s['screenshots'])==4"
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
package includes raw evidence, raw logs, PoC, exploit steps, payload, credentials, token, auth header, action command, or attacker-readable topology
package includes ECI/VFE output that did not pass output guard
package implies real data, live Qwen/API/connectors, production write-back, customer-visible deploy, or autonomous remediation
package manifest omits SHA256, bytes, or safety_class
screenshot index omits route, viewport, sha256, or safety_class
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
pytest output for package builder tests
package builder command output with zip_sha256
manifest and screenshot index consistency check PASS
zip artifact under artifacts/local_demo_packages
closeout report with exact command outcomes and safety assertions
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no production_writeback=true
no customer_visible_output=true
no Authorization header
no Bearer token
no raw_payload
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-RC018_CUSTOMER_READABLE_PACKAGE.
If HOLD, stop and report exact failing package evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-ECIVFE-35 local review package
stage and commit only Goal files
do not push
```
