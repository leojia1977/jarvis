# GOAL-SYS-02_PRODUCT_ACCELERATION_QUEUE_SEED

## Goal ID

```text
GOAL-SYS-02_PRODUCT_ACCELERATION_QUEUE_SEED
```

## Goal type

```text
script
```

## Goal statement

```text
Seed the product-acceleration Goal picker with MVP-61 through MVP-66 executable candidates so the overnight automation can continue product work after reviewer backlog exhaustion.
```

## Primary executable object

```text
script=scripts/pick_next_mvp_goal.py
test=backend/tests/test_pick_next_mvp_goal.py
artifact=artifacts/product_acceleration/next_goal_candidate.json
artifact=artifacts/product_acceleration/next_goal_candidate.md
closeout=docs/S6_FAST_MVP_GOAL_SYS_02_PRODUCT_ACCELERATION_QUEUE_SEED_2026_05_08.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-014-cn-review/reviewer_backlog.json
scripts/pick_next_mvp_goal.py
backend/tests/test_pick_next_mvp_goal.py
```

## Output paths

```text
docs/goals/GOAL-SYS-02_PRODUCT_ACCELERATION_QUEUE_SEED.md
scripts/pick_next_mvp_goal.py
backend/tests/test_pick_next_mvp_goal.py
artifacts/product_acceleration/next_goal_candidate.json
artifacts/product_acceleration/next_goal_candidate.md
docs/S6_FAST_MVP_GOAL_SYS_02_PRODUCT_ACCELERATION_QUEUE_SEED_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-SYS-02_PRODUCT_ACCELERATION_QUEUE_SEED.md
scripts/pick_next_mvp_goal.py
backend/tests/test_pick_next_mvp_goal.py
artifacts/product_acceleration/next_goal_candidate.json
artifacts/product_acceleration/next_goal_candidate.md
docs/S6_FAST_MVP_GOAL_SYS_02_PRODUCT_ACCELERATION_QUEUE_SEED_2026_05_08.md
```

## Allowed scope

```text
local/offline only
Goal picker queue definitions
Goal picker tests
next-goal candidate artifact generation
automation prompt update
local tests
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-SYS-02_PRODUCT_ACCELERATION_QUEUE_SEED.md
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts/pick_next_mvp_goal.py --repo-root . --output-json artifacts/product_acceleration/next_goal_candidate.json --output-md artifacts/product_acceleration/next_goal_candidate.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
picker still returns QUEUE_EXHAUSTED_REQUIRE_NEW_PRODUCT_GOAL while MVP-61 has no goal card
candidate Goal lacks exact_files, acceptance_commands, or hold_conditions
unit test fails twice in the same way
script output grants deploy, customer-visible output, live Qwen/API, connector, or write-back authority
scope expands beyond listed files
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
If PASS, unlock GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE for the next automation run.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit for this queue seed Goal
commit message: chore(secupilot): seed product acceleration goal queue
do not push unless separately authorized
```
