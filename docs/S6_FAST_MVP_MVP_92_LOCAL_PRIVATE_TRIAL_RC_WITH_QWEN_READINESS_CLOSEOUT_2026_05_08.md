# S6 Fast MVP MVP-92 Local Private Trial RC With Qwen Readiness Closeout

Date: 2026-05-08

Goal: GOAL-MVP-92_LOCAL_PRIVATE_TRIAL_RC_WITH_QWEN_READINESS

Status: PASS

## What Changed

- Advanced the local/offline reviewer-facing RC package from `LOCAL_OFFLINE_TRIAL_RC_016_CN` to `LOCAL_OFFLINE_TRIAL_RC_017_CN`.
- Updated `/s1-run` and `/s1-trial` fixture references so the UI, screenshots, package path, source candidate, and ZIP name all point to RC-017.
- Kept the Qwen provider readiness wording reviewer-safe by using `运行时密钥值` instead of visible `API key` text.
- Extended `scripts/build_local_offline_trial_rc.py` with repeatable `--validation-artifact` support so Qwen go-precheck, runtime config, and provider stub reports can ship inside the local package validation folder.
- Built the self-contained package:
  - `artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review/`
  - `artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip`
  - `artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip.outer_zip_manifest.json`

## Package Evidence

```text
candidate = LOCAL_OFFLINE_TRIAL_RC_017_CN
source_candidate = LOCAL_OFFLINE_TRIAL_RC_016_CN
package_dir = artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review
zip_path = artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip
zip_sha256 = b41aa2c313e2011a375860fd5fb630bb4fd7e0971cbcf85a36dfc977a6acfd76
manifest_self_sha256 = 45a8a7af69eee18ad1536b3a8cacb45ad79303dd7a3744e0c6e61dc0aa2c90f4
outer_zip_manifest_sha256 = e2bf948243e26b1b1d6d2429a704c5c1f07367b66fccf64fd69994d4999b79b2
file_count = 19
```

## Included Validation Artifacts

```text
validation/screenshot_safety_scan.json
validation/qwen_live_synthetic_go_precheck_report.json
validation/qwen_live_synthetic_runtime_config_report.json
validation/qwen_live_synthetic_provider_stub_report.json
validation/qwen_live_synthetic_provider_stub_report_中文.md
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
npm run test:e2e -- tests/e2e/s1-artifact-viewer.visual.spec.ts
Result: PASS, 4 passed
```

```text
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
Result: PASS, blocking_finding_count = 0, warning_count = 0
```

```text
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_016_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip --source-commit 7d4b4d5 --repo-root . --screenshot-safety-scan artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_go_precheck_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report.json --validation-artifact artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report_中文.md --outer-zip-manifest artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip.outer_zip_manifest.json
Result: PASS
```

```text
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_016_CN --zip-name local-offline-trial-rc-017-cn-review-package-20260508.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-package-20260508.zip --output-json artifacts/local_demo_packages/local-offline-trial-rc-017-cn-review-consistency-check.json
Result: PASS, blocking_finding_count = 0
```

```text
py -3 -m unittest -q backend.tests.test_build_local_offline_trial_rc
Result: PASS, 5 tests
```

## Boundary

This closeout does not authorize real data, masked-real data, live Qwen/API calls, secrets/tokens/auth headers/raw customer logs, live connectors, production write-back, customer-visible publish/deploy/output, external pilot, production launch, backend API/schema migration, or push.

## Next Unlock

`GOAL-MVP-93_CUSTOMER_TRIAL_ENTRY_CLEANUP` is unlocked after this Goal is committed.
