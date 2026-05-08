# GOAL-MVP-116 Backlog Item RFB-RC016-003

## Goal ID

```text
GOAL-MVP-116_BACKLOG_ITEM_RFB_RC016_003
```

## Goal type

```text
package
```

## Goal statement

```text
Include one first-load no-interaction folded-state screenshot for AI advice source in the next RC package.
```

## Primary executable object

```text
script=scripts/build_local_offline_trial_rc.py
test=backend/tests/test_build_local_offline_trial_rc.py
closeout=docs/S6_FAST_MVP_GOAL_MVP_116_BACKLOG_ITEM_RFB_RC016_003_2026_05_08.md
```

## Inputs

```text
artifacts/product_acceleration/next_goal_candidate.json
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
```

## Output paths

```text
docs/goals/GOAL-MVP-116_BACKLOG_ITEM_RFB_RC016_003.md
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
docs/S6_FAST_MVP_GOAL_MVP_116_BACKLOG_ITEM_RFB_RC016_003_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-116_BACKLOG_ITEM_RFB_RC016_003.md
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
docs/S6_FAST_MVP_GOAL_MVP_116_BACKLOG_ITEM_RFB_RC016_003_2026_05_08.md
```

## Allowed scope

```text
bounded package-builder enhancement for optional folded-state screenshot inclusion
unit-test coverage for the optional screenshot behavior
no unrelated package pipeline changes
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
API keys
secrets/tokens/auth headers/raw customer logs
live connectors
production write-back
customer-visible publish/deploy/output
external pilot
production launch
backend API/schema migration
push
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-116_BACKLOG_ITEM_RFB_RC016_003.md
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
py -3 scripts/build_local_offline_trial_rc.py --help
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
package builder behavior changes outside selected backlog scope
unit test fails twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
keep historical residue untouched
```

## Evidence contract

```text
goal card validator PASS output
unit test PASS output for build_local_offline_trial_rc
build_local_offline_trial_rc --help output available
diff --check PASS output
closeout report with bounded change summary
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no production_writeback=true
no customer_visible_output=true
no Authorization header
no Bearer token
no raw_payload
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock one follow-up backlog closeout Goal for this exact item or next picker-selected candidate.
If HOLD, stop and report exact failing command and artifact.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-116 backlog folded screenshot support
stage and commit only Goal files
do not push
```
