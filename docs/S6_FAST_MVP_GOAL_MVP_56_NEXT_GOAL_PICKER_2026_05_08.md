# S6 Fast MVP GOAL-MVP-56 Next Goal Picker

Date: 2026-05-08

Goal: GOAL-MVP-56_NEXT_GOAL_PICKER

Decision: PASS_WITH_NOTES

## Scope

Implemented a deterministic local/offline goal picker script that reads the latest reviewer backlog and returns one executable next-goal candidate with exact files, acceptance commands, and HOLD conditions.

## Outputs

```text
Goal card: docs/goals/GOAL-MVP-56_NEXT_GOAL_PICKER.md
Script: scripts/pick_next_mvp_goal.py
Unit tests: backend/tests/test_pick_next_mvp_goal.py
Run artifact json: artifacts/product_acceleration/next_goal_candidate.json
Run artifact md: artifacts/product_acceleration/next_goal_candidate.md
Automated review: artifacts/reviews/claude_code/mvp-56-current-diff-review-20260508.txt
Closeout: docs/S6_FAST_MVP_GOAL_MVP_56_NEXT_GOAL_PICKER_2026_05_08.md
```

## What Changed

- Added `scripts/pick_next_mvp_goal.py`.
- Implemented selection flow:
  - choose highest-priority OPEN/BACKLOG_OPEN item from latest `reviewer_backlog.json`
  - otherwise choose first incomplete queue fallback item
  - otherwise emit concrete blocker `QUEUE_EXHAUSTED_REQUIRE_NEW_PRODUCT_GOAL`
- Added `backend/tests/test_pick_next_mvp_goal.py` for:
  - open-backlog selection
  - queue fallback when no OPEN items
  - HOLD on invalid backlog item structure
- Ran script once to produce durable run artifact under `artifacts/product_acceleration/`.

## Non-Authorization

This Goal does not authorize real data, masked-real data, live Qwen/API calls, live connectors, production write-back, customer-visible publish/deploy/output, external pilot, production launch, or push.

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-56_NEXT_GOAL_PICKER.md
```

Result: PASS.

```text
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
```

Result: PASS (3 tests).

```text
py -3 scripts/pick_next_mvp_goal.py --repo-root . --output-json artifacts/product_acceleration/next_goal_candidate.json --output-md artifacts/product_acceleration/next_goal_candidate.md
```

Result: PASS. Current output is `selection_mode=CONCRETE_BLOCKER` with `queue_key=QUEUE_EXHAUSTED_REQUIRE_NEW_PRODUCT_GOAL` and candidate `GOAL-MVP-57_QUEUE_EXHAUSTED`.

```text
git -c core.quotepath=false diff --check
```

Result: PASS.

## Automated Review Status

```text
Tool: claude --print (current diff review)
Artifact: artifacts/reviews/claude_code/mvp-56-current-diff-review-20260508.txt
Decision: PASS_WITH_NOTES
```

Non-blocking notes:

- P2: add tests for "no backlog file" and "top-level backlog not dict" paths.
- P3: optional path traversal guard for explicit absolute output paths.

## HOLD Review

- Backlog parsing failure: NO.
- Missing `exact_files` or `acceptance_commands` in output: NO.
- Scope expansion beyond allowed local/offline boundary: NO.
- Unit test failures: NO.

## Next Unlock

Current queue fallback set is exhausted after MVP-56, so next run should execute a bounded blocker-closeout goal definition (`GOAL-MVP-57_QUEUE_EXHAUSTED`) or receive one new explicit product-acceleration queue item.
