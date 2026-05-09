# GOAL-RC018-01 Customer Route Package Hygiene Fix

## Goal ID

GOAL-RC018-01_CUSTOMER_ROUTE_PACKAGE_HYGIENE_FIX

## Goal Type

package

## Goal Statement

Repair the RC-018 customer-route review package so the zip contains only current customer-path indexes, current 7-screenshot safety evidence, and no stale RC-018 root templates or engineering validation annex that would mislead offline reviewers.

## Primary Executable Object

script=scripts/build_rc018_customer_review_package.py
test=backend/tests/test_build_rc018_customer_review_package.py
package=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review
zip=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
closeout=docs/S6_FAST_PRODUCT_GOAL_RC018_01_CUSTOMER_ROUTE_PACKAGE_HYGIENE_FIX_2026_05_09.md

## Inputs

- Reviewer findings from RC-018 package review on 2026-05-09.
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
- artifacts/eci_vfe_fixture_runs/rc001/output_guard_scan.json

## Output Paths

- docs/goals/GOAL-RC018-01_CUSTOMER_ROUTE_PACKAGE_HYGIENE_FIX.md
- scripts/build_rc018_customer_review_package.py
- backend/tests/test_build_rc018_customer_review_package.py
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/SCREENSHOT_INDEX_中文.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/validation/screenshot_safety_scan.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/package_manifest.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip.outer_zip_manifest.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json
- docs/S6_FAST_PRODUCT_GOAL_RC018_01_CUSTOMER_ROUTE_PACKAGE_HYGIENE_FIX_2026_05_09.md

## Allowed Files

- docs/goals/GOAL-RC018-01_CUSTOMER_ROUTE_PACKAGE_HYGIENE_FIX.md
- scripts/build_rc018_customer_review_package.py
- backend/tests/test_build_rc018_customer_review_package.py
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/**
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip.outer_zip_manifest.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json
- docs/S6_FAST_PRODUCT_GOAL_RC018_01_CUSTOMER_ROUTE_PACKAGE_HYGIENE_FIX_2026_05_09.md

## Allowed Scope

- Remove stale RC-018 package root files that point at `/s1-run`, old screenshot names, or the 20260508 zip.
- Regenerate package-level screenshot safety evidence from the current 7 RC-018 customer-path screenshots.
- Remove stale provider/stub/live-Qwen validation annex files from the customer-facing review zip.
- Rebuild package manifest, consistency output, screenshot safety output, and zip manifest.

## Forbidden Scope

- real data
- masked-real data
- live Qwen/API/connectors
- API keys, secrets, tokens, auth headers, raw customer logs, or raw payloads
- production write-back
- customer-visible publish, deploy, or output
- external pilot
- production launch
- PoC, exploit steps, payloads, credentials, or attacker-readable topology
- autonomous containment, remediation, isolation, blocking, approval, rejection, or action-mode choice
- changing automation schedule, picker policy, GOAL-MVP-163 files, or RC-020 package scope
- push

## Acceptance Commands

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-RC018-01_CUSTOMER_ROUTE_PACKAGE_HYGIENE_FIX.md
py -3 -m unittest backend.tests.test_build_rc018_customer_review_package
py -3 scripts\build_rc018_customer_review_package.py --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --output-dir artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip --repo-root .
py -3 -c "import json, pathlib, zipfile; root=pathlib.Path('artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review'); scan=json.loads((root/'validation/screenshot_safety_scan.json').read_text(encoding='utf-8')); assert scan['status']=='PASS' and scan['checked']==7 and scan['blocking_finding_count']==0; names={p.name for p in root.iterdir()}; assert 'PACKAGE_INDEX_中文.json' not in names and 'SCREENSHOT_INDEX.json' not in names and 'REVIEWER_CHECKLIST_中文.md' not in names and 'FEEDBACK_TEMPLATE_中文.md' not in names; z=zipfile.ZipFile('artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip'); zn=set(z.namelist()); assert 'validation/screenshot_safety_scan.json' in zn and 'PACKAGE_INDEX_中文.json' not in zn and 'SCREENSHOT_INDEX.json' not in zn and 'validation/qwen_live_synthetic_provider_stub_report.json' not in zn"
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- zip still contains `PACKAGE_INDEX_中文.json`, `SCREENSHOT_INDEX.json`, root `REVIEWER_CHECKLIST_中文.md`, root `FEEDBACK_TEMPLATE_中文.md`, or old `/s1-run` screenshot references
- package-level screenshot safety scan checks fewer or more than the current 7 RC-018 customer-path screenshots
- package-level screenshot safety scan references old `s1-run-*.png` or `s1-trial-*.png` files
- provider/stub/live-Qwen validation annex remains in the customer-facing review zip
- package manifest or outer zip manifest is not regenerated
- output guard is missing or not PASS
- scope touches GOAL-MVP-163, RC-020, picker policy, automation schedule, real data, live systems, or production write-back

## Rollback

- Revert only files listed in Allowed Files.
- Preserve the reviewer findings and regenerated artifacts for audit if a HOLD condition is observed.
- Leave unrelated dirty picker files, GOAL-MVP-163 HOLD files, and historical residue untouched.

## Evidence Contract

- goal-card validation PASS
- package builder unittest PASS
- real package rebuild command PASS
- zip hygiene assertion command transcript PASS
- regenerated `validation/screenshot_safety_scan.json` with exactly 7 current customer-path screenshots
- regenerated package manifest, screenshot safety summary, consistency check, and outer zip manifest
- diff whitespace check PASS

## Safety Sentinels

- real_data=false
- masked_real_data=false
- live_qwen_api=false
- live_connectors=false
- production_writeback=false
- customer_visible_output=false
- push=false
- no Authorization
- no Bearer
- no token
- no raw_payload
- no action_command
- no attacker-readable attack_path

## Merge Rule

Acceptance commands must PASS before this Goal is considered complete. Reject unrelated changes. Do not push. Do not stage or commit unless the human explicitly authorizes commit for this Goal.

## Next Unlock

PASS unlock: RC-018 can return to reviewer-send readiness with the hygiene-fixed zip and updated handoff hash. HOLD behavior: report the exact stale file, scan mismatch, or boundary issue and do not send the reviewer package.

## Commit Posture

Manual run prepares a commit-ready patch only. Do not push.
