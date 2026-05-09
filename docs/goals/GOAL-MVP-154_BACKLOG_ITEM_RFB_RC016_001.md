# GOAL-MVP-154 Backlog Item RFB-RC016-001

## Goal ID

```text
GOAL-MVP-154_BACKLOG_ITEM_RFB_RC016_001
```

## Goal type

```text
package
```

## Goal statement

```text
Add folded-state review source-owner metadata so archive evidence carries accountable ownership for the exact RC016 screenshot obligation.
```

## Primary executable object

```text
script=scripts/build_local_offline_trial_rc.py
validator=backend/tests/test_build_local_offline_trial_rc.py
goal_card=docs/goals/GOAL-MVP-154_BACKLOG_ITEM_RFB_RC016_001.md
closeout=docs/S6_FAST_MVP_GOAL_MVP_154_BACKLOG_ITEM_RFB_RC016_001_2026_05_09.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json
artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review/reviewer_feedback.json
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
GOAL-MVP-153 implementation commit 77ac7b4
```

## Output paths

```text
docs/goals/GOAL-MVP-154_BACKLOG_ITEM_RFB_RC016_001.md
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
docs/S6_FAST_MVP_GOAL_MVP_154_BACKLOG_ITEM_RFB_RC016_001_2026_05_09.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-154_BACKLOG_ITEM_RFB_RC016_001.md
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
docs/S6_FAST_MVP_GOAL_MVP_154_BACKLOG_ITEM_RFB_RC016_001_2026_05_09.md
```

## Allowed scope

```text
small package evidence-contract hardening for folded-state review source-owner traceability
matching unittest assertions only
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-154_BACKLOG_ITEM_RFB_RC016_001.md
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
preserve known residue and unrelated dirty/untracked artifacts
```

## Evidence contract

```text
goal card validator PASS output
unittest PASS output proving folded-state review source owner metadata exists in package manifest/package index/screenshot index pathways
builder help command PASS output
diff --check PASS output
closeout record mapping RFB-RC016-001 to source-owner traceability hardening
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
Do not stage unrelated residue.
```

## Next unlock

```text
If PASS, unlock a follow-up backlog closeout Goal for RFB-RC016-001.
If HOLD, stop and report failing command and exact boundary.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-154 folded screenshot source owner
stage and commit only Goal files
do not push
```
