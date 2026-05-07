# GOAL-MVP-60_QUEUE_EXHAUSTED

## Goal ID

```text
GOAL-MVP-60_QUEUE_EXHAUSTED
```

## Goal type

```text
script
```

## Goal statement

```text
When reviewer backlog has no OPEN items and predefined queue items remain exhausted, deliver a concrete blocker closeout artifact that requests one explicit new product-acceleration Goal input for the next run.
```

## Primary executable object

```text
script=scripts/pick_next_mvp_goal.py
test=backend/tests/test_pick_next_mvp_goal.py
artifact=artifacts/product_acceleration/next_goal_candidate.json
artifact=artifacts/product_acceleration/next_goal_candidate.md
closeout=docs/S6_FAST_MVP_GOAL_MVP_60_QUEUE_EXHAUSTED_2026_05_08.md
```

## Inputs

```text
scripts/pick_next_mvp_goal.py
backend/tests/test_pick_next_mvp_goal.py
artifacts/product_backlog/**/reviewer_backlog.json
docs/goals/GOAL-MVP-*.md
```

## Output paths

```text
docs/goals/GOAL-MVP-60_QUEUE_EXHAUSTED.md
artifacts/product_acceleration/next_goal_candidate.json
artifacts/product_acceleration/next_goal_candidate.md
artifacts/reviews/claude_code/mvp-60-current-diff-review-20260508.txt
docs/S6_FAST_MVP_GOAL_MVP_60_QUEUE_EXHAUSTED_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-60_QUEUE_EXHAUSTED.md
artifacts/product_acceleration/next_goal_candidate.json
artifacts/product_acceleration/next_goal_candidate.md
artifacts/reviews/claude_code/mvp-60-current-diff-review-20260508.txt
docs/S6_FAST_MVP_GOAL_MVP_60_QUEUE_EXHAUSTED_2026_05_08.md
```

## Allowed scope

```text
local/offline only
deterministic queue exhaustion blocker reporting
focused script test execution
single real script invocation to refresh next-goal artifact
automated current-diff review capture
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-60_QUEUE_EXHAUSTED.md
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts/pick_next_mvp_goal.py --repo-root . --output-json artifacts/product_acceleration/next_goal_candidate.json --output-md artifacts/product_acceleration/next_goal_candidate.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
latest reviewer_backlog.json cannot be parsed
generated candidate does not report CONCRETE_BLOCKER after queue exhaustion
script output misses candidate_goal.exact_files or acceptance_commands
scope expands beyond listed files
unit test fails twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files only
preserve failure evidence and command output
do not hide failed evidence
```

## Evidence contract

```text
goal card validator output
unit test output
real picker invocation output
next_goal_candidate.json and next_goal_candidate.md updates
automated review artifact or REVIEW_TOOL_UNAVAILABLE_NON_BLOCKING record
closeout note with exact commands and results
```

## Safety sentinels

```text
no external network dependency required for acceptance
no Authorization: / Bearer / refresh_token markers in new artifacts
no raw_payload markers in generated outputs
customer_visible_output remains false
production_writeback remains false
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not stage unrelated historical RC zip files or unrelated changes.
```

## Next unlock

```text
If PASS, unlock an explicit new product-acceleration queue item request for the next run.
If HOLD, stop and report exact blocker plus artifact paths.
```

## Commit posture

```text
one commit per passing Goal
commit message: docs(secupilot): GOAL-MVP-60 queue exhausted closeout
do not push unless separately authorized
```
