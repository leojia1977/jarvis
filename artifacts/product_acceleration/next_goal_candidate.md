# SecuPilot Next MVP Goal Candidate

Generated at: 2026-05-08T07:50:05

Selection mode: CONCRETE_BLOCKER

## Candidate Goal

- queue_key: QUEUE_EXHAUSTED_REQUIRE_NEW_PRODUCT_GOAL
- goal_id: GOAL-MVP-61_QUEUE_EXHAUSTED
- goal_type: script
- statement: All predefined queue goals appear completed; require one new explicit product-acceleration goal definition.

## Exact Files

- docs/goals/GOAL-MVP-61_QUEUE_EXHAUSTED.md
- scripts/close_reviewer_backlog_items.py
- docs/S6_FAST_MVP_GOAL-MVP-61_QUEUE_EXHAUSTED_2026_05_08.md

## Acceptance Commands

- py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-61_QUEUE_EXHAUSTED.md
- py -3 scripts/close_reviewer_backlog_items.py --help
- git -c core.quotepath=false diff --check

## HOLD Conditions

- backlog item cannot map to a bounded execution profile
- script command fails
- scope expands beyond listed files
