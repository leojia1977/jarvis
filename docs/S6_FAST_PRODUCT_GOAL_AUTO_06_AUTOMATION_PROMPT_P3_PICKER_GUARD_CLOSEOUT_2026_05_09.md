# S6 Fast Product Goal AUTO-06 Automation Prompt P3 Picker Guard Closeout

Date: 2026-05-09

Goal: GOAL-AUTO-06_AUTOMATION_PROMPT_P3_PICKER_GUARD

## Outcome

PASS

## Why This Exists

GOAL-AUTO-04 fixed the picker so low-priority backlog work cannot monopolize automation while product-route candidates are open. The active automation prompt still had a broad instruction allowing direct consumption of any open reviewer backlog item before picker execution. That created a small bypass risk: a future automation run could behave diligently but keep producing low-value backlog fragments again.

## Policy Synchronized Into Automation Prompt

- Run `scripts/pick_next_mvp_goal.py` before consuming reviewer backlog unless a newly recorded RC review decision needs export.
- P0/P1 backlog may preempt the product queue.
- P2 backlog may receive at most one implementation attempt plus one closeout attempt for the same backlog item.
- P3 backlog must not preempt an open product queue.
- P3 backlog may receive only one bounded closeout attempt after queue exhaustion, then automation must return to the product-route picker or HOLD for a new product goal.

## Boundary

This Goal only synchronizes the active automation prompt with the already-implemented picker policy. It does not change picker code, tests, schedule, model, cwd, active status, or hard product safety boundaries. It does not authorize real data, masked-real data, live Qwen/API/connectors, production write-back, customer-visible output, deploy, external pilot, production launch, or autonomous security action.

## Verification

Commands:

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-AUTO-06_AUTOMATION_PROMPT_P3_PICKER_GUARD.md
Select-String -Path C:\Users\Administrator\.codex\automations\secupilot-fast-mvp-5-day-queue\automation.toml -Pattern "P3 backlog must not preempt an open product queue","Run scripts/pick_next_mvp_goal.py before consuming reviewer_backlog","P2 backlog may receive at most one implementation attempt plus one closeout attempt" -SimpleMatch
git -c core.quotepath=false diff --check
```

Results:

- Goal-card validation: PASS after tightening the validator-required Goal type, merge rule, next unlock, and commit posture wording
- Automation prompt guard search: PASS
- Diff whitespace check: PASS, with line-ending warnings only on pre-existing dirty picker candidate files

## Manual Closeout Posture

- stage=false
- commit=false
- push=false

## Next Route

Continue A/B review:

1. A: lightweight scheduling review of picker policy plus automation prompt guard.
2. B: RC-018 customer-readable product path review before sending the reviewer package.
