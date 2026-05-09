# GOAL-RC018 Customer Path Screenshot And Copy Fix

## Goal ID

GOAL-MVP-159_RC018_CUSTOMER_PATH_SCREENSHOT_AND_COPY_FIX

## Goal Type

package

## Goal Statement

Repair the RC-018 customer-readable review package so reviewers can follow the product path through product home, incident workbench, AI advice source, ECI/VFE explanation, missing evidence, collection window, and local feedback without starting from evidence-package or fixture-harness language.

## Primary Executable Object

script=scripts/build_rc018_customer_review_package.py
test=backend/tests/test_build_rc018_customer_review_package.py
ui=frontend/src/secupilot/s1/S1LocalTrialView.tsx
ui=frontend/src/App.tsx
e2e=frontend/tests/e2e/rc018-customer-path.spec.ts
package=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review
zip=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
closeout=docs/S6_FAST_PRODUCT_GOAL_RC018_CUSTOMER_PATH_SCREENSHOT_AND_COPY_FIX_2026_05_09.md

## Inputs

- docs/S6_RC018_CUSTOMER_READABLE_REVIEW_PACKAGE_DESIGN_2026_05_09.md
- docs/S6_RC018_REVIEW_TRIAL_AND_QWEN_GATE_PREP_2026_05_09.md
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review
- artifacts/eci_vfe_fixture_runs/rc001/output_guard_scan.json
- frontend product routes `/s1-trial` and `/incident/CASE-2847`

## Output Paths

- docs/goals/GOAL-MVP-159_RC018_CUSTOMER_PATH_SCREENSHOT_AND_COPY_FIX.md
- frontend/src/secupilot/s1/S1LocalTrialView.tsx
- frontend/src/secupilot/s1/s1QwenProviderReadiness.ts
- frontend/src/secupilot/s1/s1QwenProviderContract.ts
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx
- frontend/tests/e2e/rc018-customer-path.spec.ts
- frontend/tests/e2e/s1-artifact-viewer.spec.ts
- scripts/build_rc018_customer_review_package.py
- backend/tests/test_build_rc018_customer_review_package.py
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/REVIEWER_START_HERE_中文.md
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/01_REVIEW_PROMPT.md
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/02_PRODUCT_ROUTE_MAP_中文.md
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/03_REVIEWER_CHECKLIST_中文.md
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/04_FEEDBACK_TEMPLATE_中文.md
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/SCREENSHOT_INDEX_中文.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/package_manifest.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/safety_scan.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/eci_vfe/chain_assessment_summary.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/eci_vfe/forecast_candidate_summary.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/screenshots/01_product_home_desktop.png
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/screenshots/02_product_home_mobile.png
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/screenshots/03_incident_first_load_desktop.png
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/screenshots/04_incident_first_load_mobile.png
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/screenshots/05_ai_advice_source_expanded_desktop.png
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/screenshots/06_eci_vfe_summary_expanded_desktop.png
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/screenshots/07_feedback_preview_desktop.png
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip.outer_zip_manifest.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json
- docs/S6_FAST_PRODUCT_GOAL_RC018_CUSTOMER_PATH_SCREENSHOT_AND_COPY_FIX_2026_05_09.md

## Allowed Files

- docs/goals/GOAL-MVP-159_RC018_CUSTOMER_PATH_SCREENSHOT_AND_COPY_FIX.md
- frontend/src/secupilot/s1/S1LocalTrialView.tsx
- frontend/src/secupilot/s1/s1QwenProviderReadiness.ts
- frontend/src/secupilot/s1/s1QwenProviderContract.ts
- frontend/src/App.tsx
- frontend/src/App.css
- frontend/src/App.test.tsx
- frontend/tests/e2e/rc018-customer-path.spec.ts
- frontend/tests/e2e/s1-artifact-viewer.spec.ts
- scripts/build_rc018_customer_review_package.py
- backend/tests/test_build_rc018_customer_review_package.py
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/**
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip.outer_zip_manifest.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json
- docs/S6_FAST_PRODUCT_GOAL_RC018_CUSTOMER_PATH_SCREENSHOT_AND_COPY_FIX_2026_05_09.md

## Allowed Scope

- Add the missing customer-path screenshot states for RC-018.
- Reframe visible product-home and incident-workbench copy away from fixture/package/provider language.
- Add customer-readable ECI/VFE explanation inside the incident workbench route.
- Rebuild the RC-018 package and zip from local/offline synthetic-only artifacts.

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
- changing automation schedule or picker policy
- push

## Acceptance Commands

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-MVP-159_RC018_CUSTOMER_PATH_SCREENSHOT_AND_COPY_FIX.md
Set-Location -LiteralPath frontend; npm run test -- --run App.test.tsx
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/rc018-customer-path.spec.ts
py -3 -m unittest backend.tests.test_build_rc018_customer_review_package
py -3 scripts\build_rc018_customer_review_package.py --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --output-dir artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip --repo-root .
py -3 -c "import json, pathlib; s=json.loads(pathlib.Path(r'artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json').read_text(encoding='utf-8')); c=json.loads(pathlib.Path(r'artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json').read_text(encoding='utf-8')); i=json.loads(pathlib.Path(r'artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/SCREENSHOT_INDEX_中文.json').read_text(encoding='utf-8')); assert s['status']=='PASS' and s['blocking_finding_count']==0; assert c['status']=='PASS'; assert len(i['screenshots'])==7"
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- fewer than 7 customer-path screenshots exist in the RC-018 package
- package starts from `/s1-run` or artifact tables instead of product home and incident workbench
- customer-path screenshots expose P1/P2/P3, Mock Fixture, Expert Mode, provider/stub/dry-run, mock_data, package manifest, output_guard_scan, stale RC wording, raw payloads, secrets, auth headers, PoC, exploit steps, or attacker-readable topology
- ECI/VFE is missing from the incident workbench customer path
- ECI/VFE appears as engineering output instead of attack-chain judgment, risk warning, missing evidence, collection window, and conservative boundary
- output guard is missing or not PASS
- package grants real data, live Qwen/API/connectors, production write-back, customer-visible deploy/publish/output, external pilot, production launch, or autonomous action authority
- scope expands beyond listed files

## Rollback

- Revert only files listed in Allowed Files.
- Keep failing screenshots and package artifacts for audit if a HOLD condition is observed.
- Preserve unrelated dirty picker candidate files and historical residue.

## Evidence Contract

- goal-card validation PASS
- focused frontend unit test PASS
- RC-018 customer-path Playwright screenshot spec PASS
- RC-018 package builder unittest PASS
- rebuilt package, screenshot index, safety scan, consistency check, and zip manifest
- diff whitespace check PASS

## Safety Sentinels

- no real_data=true
- no masked_real_data=true
- no live_qwen_api=true
- no production_writeback=true
- no customer_visible_output=true
- no Authorization
- no Bearer
- no token
- no raw_payload
- no action_command
- no attacker-readable attack_path

## Merge Rule

Acceptance commands must pass before this Goal is considered complete. Do not push. Reject unrelated changes. Do not stage or commit unless the human explicitly authorizes commit for this Goal.

## Next Unlock

If PASS, unlock a manual RC-018 reviewer send decision using the prepared reviewer handoff message. If HOLD, stop and report the exact UI, screenshot, package, or safety failure.

## Commit Posture

Manual run prepares a commit-ready patch only. Do not push.
