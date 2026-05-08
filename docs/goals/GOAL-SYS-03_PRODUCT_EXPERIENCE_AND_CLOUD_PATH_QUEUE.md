# GOAL-SYS-03_PRODUCT_EXPERIENCE_AND_CLOUD_PATH_QUEUE

## Goal ID

```text
GOAL-SYS-03_PRODUCT_EXPERIENCE_AND_CLOUD_PATH_QUEUE
```

## Goal type

```text
script
```

## Goal statement

```text
Extend the SecuPilot product-acceleration queue beyond RC maintenance into product experience closure and cloud-model dry integration path work for MVP-67 through MVP-75.
```

## Primary executable object

```text
script=scripts/pick_next_mvp_goal.py
test=backend/tests/test_pick_next_mvp_goal.py
artifact=artifacts/product_acceleration/next_goal_candidate.json
artifact=artifacts/product_acceleration/next_goal_candidate.md
closeout=docs/S6_FAST_MVP_GOAL_SYS_03_PRODUCT_EXPERIENCE_AND_CLOUD_PATH_QUEUE_2026_05_08.md
```

## Inputs

```text
scripts/pick_next_mvp_goal.py
backend/tests/test_pick_next_mvp_goal.py
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
```

## Output paths

```text
docs/goals/GOAL-SYS-03_PRODUCT_EXPERIENCE_AND_CLOUD_PATH_QUEUE.md
scripts/pick_next_mvp_goal.py
backend/tests/test_pick_next_mvp_goal.py
artifacts/product_acceleration/next_goal_candidate.json
artifacts/product_acceleration/next_goal_candidate.md
docs/S6_FAST_MVP_GOAL_SYS_03_PRODUCT_EXPERIENCE_AND_CLOUD_PATH_QUEUE_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-SYS-03_PRODUCT_EXPERIENCE_AND_CLOUD_PATH_QUEUE.md
scripts/pick_next_mvp_goal.py
backend/tests/test_pick_next_mvp_goal.py
artifacts/product_acceleration/next_goal_candidate.json
artifacts/product_acceleration/next_goal_candidate.md
docs/S6_FAST_MVP_GOAL_SYS_03_PRODUCT_EXPERIENCE_AND_CLOUD_PATH_QUEUE_2026_05_08.md
```

## Allowed scope

```text
local/offline only
Goal picker queue definitions
Goal picker tests
next-goal candidate artifact refresh
automation prompt update
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
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-SYS-03_PRODUCT_EXPERIENCE_AND_CLOUD_PATH_QUEUE.md
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts/pick_next_mvp_goal.py --repo-root . --output-json artifacts/product_acceleration/next_goal_candidate.json --output-md artifacts/product_acceleration/next_goal_candidate.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
MVP-67 does not become the next queue fallback after MVP-61 through MVP-66 cards exist
MVP-75 does not become the next queue fallback after MVP-67 through MVP-74 cards exist
candidate Goal lacks exact_files, acceptance_commands, or hold_conditions
script output grants deploy, customer-visible output, live Qwen/API, connector, or write-back authority
unit test fails twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
restore prior next_goal_candidate artifacts only if this Goal is reverted
preserve failure evidence in closeout
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
next_goal_candidate.json
next_goal_candidate.md
closeout note with exact commands
```

## Safety sentinels

```text
no customer_visible_output=true
no production_writeback=true
no live_qwen_api=true
no connector execution
no Authorization: / Bearer / refresh_token in artifacts
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, keep MVP-61 as the immediate next executable Goal and unlock MVP-67 through MVP-75 after MVP-61 through MVP-66 complete.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit for this queue extension Goal
commit message: chore(secupilot): extend product experience goal queue
do not push unless separately authorized
```
