# GOAL-MVP-164 Private Preview Healthcheck

## Goal ID

```text
GOAL-MVP-164_PRIVATE_PREVIEW_HEALTHCHECK
```

## Goal type

```text
validator
```

## Goal statement

```text
Add a private-preview healthcheck that verifies the local package, launch metadata, route map, and local-only boundaries before reviewers open the trial.
```

## Primary executable object

```text
validator=scripts/check_private_preview_health.py
tests=backend/tests/test_check_private_preview_health.py
artifact=artifacts/private_preview/healthcheck/local-offline-trial-rc-020-healthcheck.json
closeout=docs/S6_FAST_MVP_GOAL_MVP_164_PRIVATE_PREVIEW_HEALTHCHECK_2026_05_09.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review/**
artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json
artifacts/local_trial_launches/local-offline-trial-rc-020/launch_info.json
```

## Output paths

```text
docs/goals/GOAL-MVP-164_PRIVATE_PREVIEW_HEALTHCHECK.md
scripts/check_private_preview_health.py
backend/tests/test_check_private_preview_health.py
artifacts/private_preview/healthcheck/local-offline-trial-rc-020-healthcheck.json
docs/S6_FAST_MVP_GOAL_MVP_164_PRIVATE_PREVIEW_HEALTHCHECK_2026_05_09.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-164_PRIVATE_PREVIEW_HEALTHCHECK.md
scripts/check_private_preview_health.py
backend/tests/test_check_private_preview_health.py
artifacts/private_preview/healthcheck/local-offline-trial-rc-020-healthcheck.json
docs/S6_FAST_MVP_GOAL_MVP_164_PRIVATE_PREVIEW_HEALTHCHECK_2026_05_09.md
```

## Allowed scope

```text
private-preview readiness validator for package + launch metadata + route map
fixture-based unittest coverage for PASS/HOLD behavior
healthcheck artifact emission for review gate evidence
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
production write-back
customer-visible publish/deploy/output
external pilot
production launch
secrets/tokens/auth headers/raw customer logs
autonomous remediation/action-mode choice
backend API/schema migration
push
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-164_PRIVATE_PREVIEW_HEALTHCHECK.md
py -3 -m unittest backend.tests.test_check_private_preview_health
py -3 scripts/check_private_preview_health.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review --route-map artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json --output-json artifacts/private_preview/healthcheck/local-offline-trial-rc-020-healthcheck.json --repo-root .
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
healthcheck cannot find package, route map, launch metadata, or local-only boundary text
healthcheck reports live Qwen/API, connector, production write-back, customer-visible deploy, or secret exposure
unit test or healthcheck command fails twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
leave unrelated dirty/untracked residue untouched
```

## Evidence contract

```text
goal card validator PASS output
unittest PASS output for backend.tests.test_check_private_preview_health
healthcheck command output JSON with PASS or HOLD details
diff --check PASS output
closeout with exact command evidence and hold checks
```

## Safety sentinels

```text
real_data=false
masked_real_data=false
live_qwen_api=false
live_connectors=false
production_writeback=false
customer_visible_output=false
push=false
```

## Merge rule

```text
Stage and commit only allowed files after all acceptance commands PASS and no HOLD condition triggers.
Reject unrelated changes; do not stage unrelated files.
Do not push.
```

## Next unlock

```text
PASS unlock: rerun picker and continue next selected goal.
HOLD behavior: report exact failing check and stop this run.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-164 private preview healthcheck
stage only Goal files
do not push
```
