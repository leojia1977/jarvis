# GOAL-RC018-02 Customer Copy And Annex Polish

## Goal ID

GOAL-RC018-02_CUSTOMER_COPY_AND_ANNEX_POLISH

## Goal Type

package

## Goal Statement

Polish the RC-018 customer path after PASS_WITH_NOTES by making deployment/action copy more conservative, moving or rewriting engineering annex language, adding a mobile incident scrolled-state screenshot, and preserving accepted AI-source and ECI/VFE regression guards.

## Primary Executable Object

ui=frontend/src/App.tsx
test=frontend/src/App.test.tsx
e2e=frontend/tests/e2e/rc018-customer-path.spec.ts
script=scripts/build_rc018_customer_review_package.py
test=backend/tests/test_build_rc018_customer_review_package.py
package=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review
zip=artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
closeout=docs/S6_FAST_PRODUCT_GOAL_RC018_02_CUSTOMER_COPY_AND_ANNEX_POLISH_2026_05_09.md

## Inputs

- docs/S6_RC018_CUSTOMER_PATH_REVIEW_DECISION_2026_05_09.md
- artifacts/product_backlog/local-offline-trial-rc-018-cn-review/reviewer_backlog.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review
- frontend routes `/s1-trial` and `/incident/CASE-2847`

## Output Paths

- docs/goals/GOAL-RC018-02_CUSTOMER_COPY_AND_ANNEX_POLISH.md
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- frontend/tests/e2e/rc018-customer-path.spec.ts
- scripts/build_rc018_customer_review_package.py
- backend/tests/test_build_rc018_customer_review_package.py
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/SCREENSHOT_INDEX_中文.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/validation/screenshot_safety_scan.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/internal_validation/**
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/package_manifest.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip.outer_zip_manifest.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json
- docs/S6_FAST_PRODUCT_GOAL_RC018_02_CUSTOMER_COPY_AND_ANNEX_POLISH_2026_05_09.md

## Allowed Files

- docs/goals/GOAL-RC018-02_CUSTOMER_COPY_AND_ANNEX_POLISH.md
- frontend/src/App.tsx
- frontend/src/App.test.tsx
- frontend/tests/e2e/rc018-customer-path.spec.ts
- scripts/build_rc018_customer_review_package.py
- backend/tests/test_build_rc018_customer_review_package.py
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review/**
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip.outer_zip_manifest.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
- artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json
- docs/S6_FAST_PRODUCT_GOAL_RC018_02_CUSTOMER_COPY_AND_ANNEX_POLISH_2026_05_09.md

## Allowed Scope

- Change `查看部署准备` to `查看本地接入准备`.
- Change `隔离 finance-042 并锁定凭据` to `待复核：finance-042 隔离与凭据锁定建议`.
- Move or rewrite engineering annex language as `internal_validation/` or customer-readable local/offline synthetic metadata validation.
- Add one mobile incident scrolled-state screenshot covering conclusion, trusted boundary, and recommended action.
- Preserve AI advice source default folded behavior and ECI/VFE defensive product framing as regression checks.

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
- changing automation schedule, picker policy, GOAL-MVP-163 files, RC-020 package scope, or private-preview healthcheck scope
- push

## Acceptance Commands

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-RC018-02_CUSTOMER_COPY_AND_ANNEX_POLISH.md
Set-Location -LiteralPath frontend; npm run test -- --run App.test.tsx
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/rc018-customer-path.spec.ts
py -3 -m unittest backend.tests.test_build_rc018_customer_review_package
py -3 scripts\build_rc018_customer_review_package.py --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --output-dir artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip --repo-root .
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- UI still says `查看部署准备` or `隔离 finance-042 并锁定凭据` in the customer path
- customer-facing annex foregrounds `qwen_fact_bundle`, `source_payload`, `provider_decision_hint`, `provider = fixture`, `provider_output_scan`, or `qwen_fact_bundle_directory`
- mobile incident scrolled-state screenshot is missing or not included in the screenshot safety scan
- AI advice source is expanded by default in first-load screenshots
- ECI/VFE exposes reusable attack path, payload, PoC, exploit steps, or topology reachability
- package grants real data, live Qwen/API/connectors, production write-back, customer-visible deploy/publish/output, external pilot, production launch, or autonomous action authority
- scope touches GOAL-MVP-163, RC-020, picker policy, automation schedule, live systems, or unrelated files

## Rollback

- Revert only files listed in Allowed Files.
- Preserve generated screenshots and package artifacts for audit if a HOLD condition is observed.
- Leave unrelated dirty picker files, GOAL-MVP-163/164 HOLD files, and historical residue untouched.

## Evidence Contract

- goal-card validation PASS
- focused frontend unit test PASS
- RC-018 customer-path Playwright screenshot spec PASS, including mobile scrolled-state evidence
- RC-018 package builder unittest PASS
- rebuilt package, screenshot index, screenshot safety scan, consistency check, and zip manifest
- command transcript showing no customer-visible publish/deploy/output, no production write-back, and no live Qwen/API/connectors
- diff whitespace check PASS

## Safety Sentinels

- real_data=false
- masked_real_data=false
- live_qwen_api=false
- live_connectors=false
- production_writeback=false
- customer_visible_output=false
- external_pilot=false
- production_launch=false
- push=false
- no Authorization
- no Bearer
- no token
- no raw_payload
- no action_command
- no attacker-readable attack_path

## Merge Rule

Acceptance commands must PASS before this Goal is considered complete. Reject unrelated changes. Do not push. Stage and commit only this Goal's allowed files when explicitly authorized.

## Next Unlock

PASS unlock: RC-018 notes N1-N3 are closed and N4-N5 remain protected as regression evidence for the next internal/local trial package. HOLD behavior: report the exact copy, annex, screenshot, or safety-boundary failure and do not treat the polish Goal as complete.

## Commit Posture

Prepare or execute this as a small standalone Goal. Commit only after explicit human authorization and passing acceptance commands. Do not push.
