# S6 Fast MVP MVP-93 Customer Trial Entry Cleanup Closeout

Date: 2026-05-08

Goal: GOAL-MVP-93_CUSTOMER_TRIAL_ENTRY_CLEANUP

Status: PASS

## What Changed

- Cleaned up `/s1-trial` so the first screen now explains:
  - who SecuPilot is: `企业安全分析助理`
  - what it helps judge: `这起事件该怎么处理`
  - what to do next: `先看结论，再核依据，最后反馈`
- Replaced the role entry language with customer/product roles:
  - 工程师视角
  - 分析负责人视角
  - 安全负责人视角
  - CTO / 部署视角
- Reduced first-screen package/evidence feel by replacing raw path-forward actions with product actions.
- Moved the one-click local launch command behind an expandable `一键启动脚本` control.
- Advanced reviewer-facing package wording to `LOCAL_OFFLINE_TRIAL_RC_018_CN`.
- Built a fresh RC-018 local/offline package with updated screenshots and Qwen readiness validation evidence.

## Package Evidence

```text
candidate = LOCAL_OFFLINE_TRIAL_RC_018_CN
source_candidate = LOCAL_OFFLINE_TRIAL_RC_017_CN
package_dir = artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review
zip_path = artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip
zip_sha256 = c62d1bfb9efddb8502ad7c11492543844a457e79752770489782d443db797db8
manifest_self_sha256 = 5ffd96264b07470bac70ed7f8f29c7c76241c83859e236d4d92895beb7ef4fbc
outer_zip_manifest_sha256 = 5f13f24092e73846fcbe52e26ab5e874669d3db4dd1008d843a091dc13b6d65e
file_count = 19
```

## Verification

```text
Set-Location -LiteralPath frontend
npm run test -- --run src/App.test.tsx
Result: PASS, 63 passed
```

```text
Set-Location -LiteralPath frontend
npm run build
Result: PASS
```

```text
Set-Location -LiteralPath frontend
npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts
Result: PASS, 4 passed
```

```text
Set-Location -LiteralPath frontend
npm run test:e2e -- tests/e2e/s1-artifact-viewer.visual.spec.ts
Result: PASS, 4 passed
```

```text
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
Result: PASS, blocking_finding_count = 0, warning_count = 0
```

```text
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip --source-commit 888df44 --repo-root . --screenshot-safety-scan artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report_中文.md --outer-zip-manifest artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip.outer_zip_manifest.json
Result: PASS
```

```text
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --zip-name local-offline-trial-rc-018-cn-review-package-20260508.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260508.zip --output-json artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json
Result: PASS, blocking_finding_count = 0
```

## Boundary

This closeout does not authorize real data, masked-real data, live Qwen/API calls, secrets/tokens/auth headers/raw customer logs, live connectors, production write-back, customer-visible publish/deploy/output, external pilot, production launch, backend API/schema migration, or push.

## Next Unlock

Next product acceleration Goal can be selected from the product acceleration pool. Recommended next direction: turn the customer trial entry into a deployable private preview shell with one product-facing route map and a clearer internal/customer boundary.
