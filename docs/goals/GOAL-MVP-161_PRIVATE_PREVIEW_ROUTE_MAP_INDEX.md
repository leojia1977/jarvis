# GOAL-MVP-161 Private Preview Route Map Index

## Goal ID

```text
GOAL-MVP-161_PRIVATE_PREVIEW_ROUTE_MAP_INDEX
```

## Goal type

```text
test-report
```

## Goal statement

```text
Generate a product route-map index from the latest private preview package so reviewers see journeys and pages instead of evidence-package internals.
```

## Primary executable object

```text
script=scripts/build_private_preview_route_map_index.py
test=backend/tests/test_build_private_preview_route_map_index.py
artifact_md=artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.md
artifact_json=artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json
closeout=docs/S6_FAST_MVP_GOAL_MVP_161_PRIVATE_PREVIEW_ROUTE_MAP_INDEX_2026_05_09.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review/PACKAGE_INDEX_中文.json
artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review/SCREENSHOT_INDEX.json
artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review/package_manifest.json
```

## Output paths

```text
docs/goals/GOAL-MVP-161_PRIVATE_PREVIEW_ROUTE_MAP_INDEX.md
scripts/build_private_preview_route_map_index.py
backend/tests/test_build_private_preview_route_map_index.py
artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.md
artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json
docs/S6_FAST_MVP_GOAL_MVP_161_PRIVATE_PREVIEW_ROUTE_MAP_INDEX_2026_05_09.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-161_PRIVATE_PREVIEW_ROUTE_MAP_INDEX.md
scripts/build_private_preview_route_map_index.py
backend/tests/test_build_private_preview_route_map_index.py
artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.md
artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json
docs/S6_FAST_MVP_GOAL_MVP_161_PRIVATE_PREVIEW_ROUTE_MAP_INDEX_2026_05_09.md
```

## Allowed scope

```text
private-preview route-map index generation from existing local/offline package metadata
product-journey-first markdown/json output with engineer/manager/CTO route coverage
focused unittest and command invocation for deterministic local report generation
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-161_PRIVATE_PREVIEW_ROUTE_MAP_INDEX.md
py -3 -m unittest backend.tests.test_build_private_preview_route_map_index
py -3 scripts/build_private_preview_route_map_index.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review --output-md artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.md --output-json artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json --repo-root .
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
route map index is dominated by artifact file tables instead of product journeys
route map grants customer-visible deploy, live Qwen/API, connector, or production write-back authority
report omits engineer, manager, or CTO route coverage
unit test or report command fails twice in the same way
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
unittest PASS output
route_map_index.md and route_map_index.json regenerated from RC-019 package
diff --check PASS output
closeout record with exact command outcomes
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
PASS unlock: rerun picker and continue the next selected product-acceleration goal.
HOLD behavior: report exact failing check and stop this run.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-161 private preview route map index
stage only Goal files
do not push
```
