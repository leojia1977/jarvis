# S6 Fast Product Goal RC018 Customer Path Screenshot And Copy Fix

Date: 2026-05-09

Goal: GOAL-MVP-159_RC018_CUSTOMER_PATH_SCREENSHOT_AND_COPY_FIX

## Outcome

PASS

## Scope

Repair RC-018 customer-readable review readiness by adding the missing customer-path screenshots and replacing reviewer-facing fixture/package/provider language with product-path language.

## Expected Deliverables

- 7 customer-path screenshots:
  - product home desktop/mobile
  - incident first load desktop/mobile
  - AI advice source expanded
  - ECI/VFE summary expanded
  - local feedback preview
- RC-018 package screenshot index updated to 7 screenshots.
- Incident workbench includes customer-readable ECI/VFE explanation.
- RC-018 package text starts from product path, not artifact tables.
- Safety and output guard evidence remains PASS.

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

- `py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-MVP-159_RC018_CUSTOMER_PATH_SCREENSHOT_AND_COPY_FIX.md`
- `npm run test -- --run App.test.tsx`
- `py -3 -m unittest backend.tests.test_build_rc018_customer_review_package`
- `npm run test:e2e -- tests/e2e/rc018-customer-path.spec.ts`
- `py -3 scripts\build_rc018_customer_review_package.py --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --output-dir artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip`
- `npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts`
- `npm run build`

Package output:

- zip: `artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip`
- zip_sha256: `30b64a031cc7014868ad692c8778c9581854cedbaea46452d7971abc6a7c5bbe`
- package_manifest_sha256: `e90a601382485b9b2eb3be85961820d7667f6748ac0d4a10ad6820da58f6604b`
- screenshot_count: `7`

Manual product-path spot check:

- `01_product_home_desktop.png`: starts from product home and RC-018 status, not evidence artifact tables.
- `03_incident_first_load_desktop.png`: starts from incident workbench conclusion, recommendation, evidence gap, and human review boundary.
- `05_ai_advice_source_expanded_desktop.png`: explains local/offline AI advice source without provider/stub/dry-run language in visible reviewer copy.
- `06_eci_vfe_summary_expanded_desktop.png`: presents ECI/VFE as attack-chain judgment, risk summary, missing evidence, evidence-collection window, and conservative boundary.
- `07_feedback_preview_desktop.png`: keeps feedback local-only and non-writeback.

## External Reviewer Rule

Do not send RC-018 to an external reviewer until this Goal is PASS, the package is rebuilt, 7 screenshots are present, safety/guard/consistency checks are PASS, and a final manual product-path review accepts the package.
