# S6 Fast MVP MVP-20 Chinese Reviewer Package And UI Triage 2026-05-07

## 1. Decision

```text
MVP_20_RC_007_CHINESE_REVIEWER_PACKAGE_COMPLETED_THEN_HELD
MVP_20_RC_008_CHINESE_REVIEWER_PACKAGE_FIX_COMPLETED
CUSTOMER_VISIBLE_OR_DEPLOY_GO = NOT_AUTHORIZED
P1_P2_P3_WORKBENCH_UI_TRIAGE_REQUIRED_BEFORE_CUSTOMER_TRIAL
```

RC-007 reviewer decision:

```text
RC-007_CN = HOLD_FOR_UI_OR_PACKAGE_FIXES
```

Reason:

```text
Safety boundary passed.
Package/UI consistency held because screenshots and delivery docs still mixed old candidate/path/zip/source-candidate wording.
```

## 2. Reviewer Package Target

```text
artifacts/local_demo_packages/local-offline-trial-rc-007-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-007-cn-review-package-20260507.zip
artifacts/local_demo_packages/local-offline-trial-rc-008-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-008-cn-review-package-20260507.zip
```

The RC-008 package is intended for internal local/offline reviewer inspection of the Chinese-first S1 trial flow after RC-007 HOLD remediation.

RC-007 zip SHA256:

```text
4199a0a680d639278462ea1788af41b15c6135b4d4968f0509f080cd2bc42f38
```

RC-008 zip SHA256:

```text
cce04808aad73a641f2840d0392ae448c2cfe30c18d4494cc30f0158b1763ce5
```

## 3. Completed Package Contents

```text
REVIEWER_START_HERE_中文.md
REVIEWER_CHECKLIST_中文.md
FEEDBACK_TEMPLATE_中文.md
PACKAGE_INDEX_中文.json
SCREENSHOT_INDEX.json
package_manifest.json
screenshots/s1-trial-desktop.png
screenshots/s1-trial-mobile.png
screenshots/s1-run-desktop.png
screenshots/s1-run-mobile.png
evidence/final_status.json
evidence/case_summary.json
evidence/artifact_manifest.json
evidence/safety_scan.json
```

## 4. Verification

```text
frontend: npm run build = PASS
frontend: npm run test -- src/App.test.tsx = PASS, 62 passed
frontend: npx playwright test tests/e2e/s1-artifact-viewer.spec.ts = PASS, 3 passed
Playwright screenshot capture:
  /s1-trial desktop = PASS
  /s1-trial mobile = PASS
  /s1-run desktop = PASS
  /s1-run mobile = PASS
package_manifest SHA256 check = PASS, 13 files checked
forbidden text scan = PASS
old RC literal scan in RC-008 package = PASS
zip expand required-file check = PASS, 10 required files present
preview process stopped after capture = PASS
```

## 4.1 RC-008 Fixes

```text
candidate = LOCAL_OFFLINE_TRIAL_RC_008_CN
source_candidate = LOCAL_OFFLINE_TRIAL_RC_007_CN
package path = artifacts/local_demo_packages/local-offline-trial-rc-008-cn-review
zip name = local-offline-trial-rc-008-cn-review-package-20260507.zip
delivery_docs copied from RC-006 = removed from current package
P1/P2/P3 role switcher in S1 reviewer routes = hidden
Mock Fixture Phase / Mock Redline Fixture in S1 reviewer routes = hidden
Expert Mode diagnostics in S1 reviewer routes = hidden
```

## 5. UI Triage From User Screenshot

The attached screenshot shows the product surface is still mixing at least four layers in one viewport:

```text
role/debug shell: P1/P2/P3 selector, mock fixture phase, mock redline fixture
developer QA shell: Expert Mode, degraded lineage diagnostics
S1 local trial evidence surface: RC-006 cards, launcher, artifact paths
product navigation: Inbox, Search / History, S1 Evidence, Local Trial
```

This is not yet a clean product dimension for customer or broad internal trial. The next UI route should separate:

```text
Product trial mode: reviewer sees only the product workflow and bounded evidence
Developer fixture mode: mock phase, redline fixture, expert diagnostics stay hidden by default
Role preview mode: P1/P2/P3 remains a developer QA control, not primary product navigation
S1 reviewer package mode: local/offline review entry, screenshots, checklist, feedback
```

## 6. Non-Authorization

This MVP-20 package does not authorize:

```text
real data
masked-real data
live Qwen/API calls
live connectors
production connectors
production write-back
customer-visible publish/deploy/output
external pilot execution
production launch
credential handling
push
```
