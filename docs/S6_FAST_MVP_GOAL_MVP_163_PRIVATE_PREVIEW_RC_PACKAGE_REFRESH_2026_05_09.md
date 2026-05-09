# S6 Fast MVP GOAL-MVP-163 Private Preview RC Package Refresh

Date: 2026-05-09

Goal: GOAL-MVP-163_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH

Decision: PASS

## Scope

刷新 RC-020 本地/离线私有化预览评审包，解除上一轮 `expected_candidate_missing` HOLD，并补齐首载折叠态截图证据。

## Precondition Unlocks

- `fcdc677` 将 S1 本地评审 candidate 文案源从 RC-019 升级到 `LOCAL_OFFLINE_TRIAL_RC_020_CN`，source candidate 保留为 RC-019。
- `d032ce6` 让 Playwright 产出 `s1-run-first-load-folded-desktop.png`，并让截图安全扫描覆盖 5 张截图。
- `07acfaa` 移除 folded-state archive evidence 中旧 RC-016 candidate/path 令牌，避免 RC-020 包一致性校验误读为旧包引用。

## Commands Run

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-163_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH.md
```

Result: PASS.

```text
Set-Location -LiteralPath frontend; npm run test -- --run src/App.test.tsx
```

Result: PASS, 63 tests passed.

```text
Set-Location -LiteralPath frontend; npm run build
```

Result: PASS.

```text
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts
```

Result: PASS, 8 tests passed.

```text
py -3 -m unittest backend.tests.test_validate_review_screenshots backend.tests.test_validate_local_trial_rc_consistency backend.tests.test_build_local_offline_trial_rc
```

Result: PASS, 15 tests passed.

```text
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json
```

Result: PASS, checked=5, blocking_finding_count=0.

```text
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_019_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip --source-commit 07acfaa --repo-root . --screenshot-safety-scan artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json --outer-zip-manifest artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip.outer_zip_manifest.json
```

Result: PASS.

```text
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_019_CN --zip-name local-offline-trial-rc-020-cn-review-package-20260508.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip --output-json artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-consistency-check.json
```

Result: PASS, blocking_finding_count=0.

```text
git -c core.quotepath=false diff --check
```

Result: PASS with line-ending warnings only on existing Windows-touched files.

## Outputs

- Package dir: `artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review`
- Zip: `artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip`
- Zip SHA256: `bb6f1017a79217cd078c92813d9a08ccaf364e97d772a99e05e09500c9f2552d`
- Outer zip manifest: `artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip.outer_zip_manifest.json`
- Outer zip manifest SHA256: `774fa8b162d0c335122bb897b559b68e2b2935cd0204cc7eb555257e675b0413`
- Screenshot safety scan: `artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json`
- Consistency check: `artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-consistency-check.json`

## Boundary Result

- No real or masked-real data.
- No live Qwen/API/connectors.
- No secrets/tokens/auth headers/raw customer logs/raw payloads.
- No production write-back.
- No customer-visible publish/deploy/output.
- No autonomous containment/remediation/action/approval/rejection.
- No attacker-readable attack path, PoC, exploit steps, payload, or topology reachability.
- No push.

## Next Suggested Step

Run GOAL-MVP-164 private preview healthcheck against the RC-020 package and RC-019 route map. If it passes, automation can continue from the RC-020 private-preview mainline.
