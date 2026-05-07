# S6 Fast MVP MVP-58 Outer Zip Manifest

Date: 2026-05-08

Goal: GOAL-MVP-58_OUTER_ZIP_MANIFEST

Decision: PASS_WITH_NOTES

## Scope

MVP-58 adds `outer_zip_manifest` support to the local/offline RC package builder, creating a machine-verifiable integrity file for each generated zip while preserving existing local/offline product boundaries and reviewer-facing behavior.

## Outputs

```text
Goal card: docs/goals/GOAL-MVP-58_OUTER_ZIP_MANIFEST.md
Builder script: scripts/build_local_offline_trial_rc.py
Unit tests: backend/tests/test_build_local_offline_trial_rc.py
Outer zip manifest artifact: artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp58-package-20260508.zip.outer_zip_manifest.json
RC consistency artifact: artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review-mvp58/rc_consistency_check_mvp58.json
Screenshot safety artifact: artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review-mvp58/screenshot_safety_scan_mvp58.json
Automated review artifact: artifacts/reviews/claude_code/mvp-58-current-diff-review-20260508.txt
Closeout: docs/S6_FAST_MVP_MVP_58_OUTER_ZIP_MANIFEST_2026_05_08.md
```

## What Changed

- Added `build_outer_zip_manifest_payload(...)` to produce deterministic outer integrity metadata including `zip_sha256`, `package_manifest_sha256`, and cross-linked `manifest_self_sha256`.
- Added `resolve_outer_zip_manifest_path(...)` with repo-boundary enforcement via `assert_inside_repo` for both default and explicit output path modes.
- Extended builder CLI with `--outer-zip-manifest` (optional); default output path is `<zip-path>.outer_zip_manifest.json`.
- Extended builder PASS payload with `outer_zip_manifest_path` and `outer_zip_manifest_sha256` for downstream automation pipelines.
- Expanded unit coverage:
  - validates default-path outer manifest hashes and cross-link invariants
  - validates explicit-path mode hash fields and cross-link invariants
  - validates HOLD when explicit manifest path escapes repo root
  - validates HOLD path does not leave outer manifest residue

## Non-Authorization

This Goal does not authorize real data, masked-real data, live Qwen/API calls, live connectors, production write-back, customer-visible publish/deploy/output, external pilot, production launch, or push.

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-58_OUTER_ZIP_MANIFEST.md
```

Result: PASS.

```text
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
```

Result: PASS, 5 tests passed.

```text
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review --screenshot-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review/screenshots --output-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp58 --zip-path artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp58-package-20260508.zip --source-commit f9c561a --screenshot-safety-scan artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review/screenshot_safety_scan.json
```

Result: PASS.

- zip_sha256: `9f840c4a4dd54db589b71b25556b9b5f2472c95b9d8f1e66c079c69d4ad6f7ed`
- manifest_self_sha256: `5f7b30828cd7d6750b0dea9f45789f00c681acc7b55a84a3b8fe9a2862cfcdf6`
- outer_zip_manifest_sha256: `a8d8cac81d1224cbea0ff77445d106dc15c92b8133a4618db4955b0b43e0e775`

```text
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp58 --candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --zip-name local-offline-trial-rc-015-cn-review-mvp58-package-20260508.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp58-package-20260508.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review-mvp58/rc_consistency_check_mvp58.json
```

Result: PASS, blocking_finding_count = 0.

```text
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review-mvp58/screenshot_safety_scan_mvp58.json
```

Result: PASS, blocking_finding_count = 0.

```text
git -c core.quotepath=false diff --check
```

Result: PASS (line-ending warnings only, no blocking diff issues).

## Automated Review Status

```text
Tool: claude --print (current diff review)
Artifact: artifacts/reviews/claude_code/mvp-58-current-diff-review-20260508.txt
Decision: PASS_WITH_NOTES
```

Interpretation:

- Review confirms boundary and integrity logic are correct and local/offline safety constraints are preserved.
- One evidence-alignment note was raised during review and resolved in this closeout: hashes now match the committed outer manifest artifact from the final builder invocation.

## HOLD Review

- outer_zip_manifest missing: NO.
- hash format invalid: NO.
- manifest_self_sha256 mismatch: NO.
- local/offline boundary regression: NO.
- consistency validator blocking findings: NO.
- screenshot safety validator blocking findings: NO.

## Execution Notes

- Temporary package directory/zip was regenerated for final evidence consistency during this run.
- Historical RC zip files already present in workspace were preserved and not staged.

## Next Unlock

Preferred next Goal: define one new explicit product-acceleration queue item beyond the exhausted predefined list, or execute a reviewer-driven item if a new OPEN backlog entry appears.
