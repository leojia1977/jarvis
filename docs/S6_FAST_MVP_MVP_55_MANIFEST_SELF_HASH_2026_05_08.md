# S6 Fast MVP MVP-55 Manifest Self Hash

Date: 2026-05-08

Goal: GOAL-MVP-55_MANIFEST_SELF_HASH

Decision: PASS_WITH_NOTES

## Scope

MVP-55 adds deterministic `manifest_self_sha256` support in the local/offline RC package builder to strengthen package-manifest integrity attestations without changing any product UI or route behavior.

## Outputs

```text
Goal card: docs/goals/GOAL-MVP-55_MANIFEST_SELF_HASH.md
Builder script: scripts/build_local_offline_trial_rc.py
Unit tests: backend/tests/test_build_local_offline_trial_rc.py
RC consistency artifact: artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review-mvp55/rc_consistency_check_mvp55.json
Screenshot safety artifact: artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review-mvp55/screenshot_safety_scan_mvp55.json
Automated review artifact: artifacts/reviews/claude_code/mvp-55-current-diff-review-20260508.txt
Closeout: docs/S6_FAST_MVP_MVP_55_MANIFEST_SELF_HASH_2026_05_08.md
```

## What Changed

- Added `json_payload_sha256(payload)` helper for stable JSON hashing using sorted keys and compact separators.
- Added `manifest_self_sha256(manifest)` helper that computes hash from the manifest payload with `manifest_self_sha256` field normalized to `null`.
- Added `manifest_self_sha256` field into generated `package_manifest.json`.
- Exposed `manifest_self_sha256` in builder stdout result payload for machine pipeline consumption.
- Extended `backend/tests/test_build_local_offline_trial_rc.py` to verify:
  - the field format is `^[0-9a-f]{64}$`
  - recomputation by `builder.manifest_self_sha256(manifest)` equals stored value.

## Non-Authorization

This Goal does not authorize real data, masked-real data, live Qwen/API calls, live connectors, production write-back, customer-visible publish/deploy/output, external pilot, production launch, or push.

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-55_MANIFEST_SELF_HASH.md
```

Result: PASS.

```text
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
```

Result: PASS, 3 tests passed.

```text
py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review --screenshot-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review/screenshots --output-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp55 --zip-path artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp55-package-20260508.zip --source-commit 137da34 --screenshot-safety-scan artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review/screenshot_safety_scan.json
```

Result: PASS, returned `manifest_self_sha256=4bd270c6e3dd5865fdc663036d1f7e69138c1075f65e6431bfec4252dca2f31e`.

```text
py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp55 --candidate LOCAL_OFFLINE_TRIAL_RC_015_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --zip-name local-offline-trial-rc-015-cn-review-mvp55-package-20260508.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-015-cn-review-mvp55-package-20260508.zip --output-json artifacts/local_trial_rc_consistency/local-offline-trial-rc-015-cn-review-mvp55/rc_consistency_check_mvp55.json
```

Result: PASS, blocking_finding_count = 0.

```text
py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_014_CN --output-json artifacts/review_screenshot_safety/local-offline-trial-rc-015-cn-review-mvp55/screenshot_safety_scan_mvp55.json
```

Result: PASS, blocking_finding_count = 0.

```text
git -c core.quotepath=false diff --check
```

Result: PASS.

## Automated Review Status

```text
Tool: claude --print (current diff review)
Artifact: artifacts/reviews/claude_code/mvp-55-current-diff-review-20260508.txt
Decision: PASS_WITH_NOTES
```

Key notes (non-blocking):

- P2: no explicit zip-level manifest integrity assertion in tests.
- P3: no negative tamper test for `manifest_self_sha256`.

## HOLD Review

- `manifest_self_sha256` field missing: NO.
- `manifest_self_sha256` malformed: NO.
- Boundary flags changed from local/offline false posture: NO.
- Test/validator failures: NO.

## Execution Notes

The temporary package directory and zip produced during acceptance command execution were cleaned after validation to avoid committing large transient artifacts. Lightweight validation artifacts and automated review artifact are retained.

## Next Unlock

Preferred next Goal: add one focused integrity hardening follow-up (zip-level manifest presence check + tamper negative test) or run GOAL-MVP-NEXT_GOAL_PICKER to auto-select the next executable queue item.
