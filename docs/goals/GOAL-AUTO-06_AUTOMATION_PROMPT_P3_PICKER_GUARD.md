# GOAL-AUTO-06 Automation Prompt P3 Picker Guard

## Goal ID

GOAL-AUTO-06_AUTOMATION_PROMPT_P3_PICKER_GUARD

## Goal Type

script

## Goal Statement

Synchronize the active product-acceleration automation prompt with the picker policy from GOAL-AUTO-04 so automation cannot bypass the picker and directly consume P3 backlog micro-tasks while product-route candidates are available.

## Primary Executable Object

automation=secupilot-fast-mvp-5-day-queue prompt
closeout=docs/S6_FAST_PRODUCT_GOAL_AUTO_06_AUTOMATION_PROMPT_P3_PICKER_GUARD_CLOSEOUT_2026_05_09.md

## Inputs

- docs/goals/GOAL-AUTO-04_BACKLOG_PRIORITY_THROTTLE_AND_PRODUCT_ROUTE.md
- docs/S6_FAST_PRODUCT_GOAL_AUTO_04_BACKLOG_PRIORITY_THROTTLE_AND_PRODUCT_ROUTE_CLOSEOUT_2026_05_09.md
- C:\Users\Administrator\.codex\automations\secupilot-fast-mvp-5-day-queue\automation.toml

## Output Paths

- docs/goals/GOAL-AUTO-06_AUTOMATION_PROMPT_P3_PICKER_GUARD.md
- docs/S6_FAST_PRODUCT_GOAL_AUTO_06_AUTOMATION_PROMPT_P3_PICKER_GUARD_CLOSEOUT_2026_05_09.md
- active automation prompt for secupilot-fast-mvp-5-day-queue

## Allowed Files

- docs/goals/GOAL-AUTO-06_AUTOMATION_PROMPT_P3_PICKER_GUARD.md
- docs/S6_FAST_PRODUCT_GOAL_AUTO_06_AUTOMATION_PROMPT_P3_PICKER_GUARD_CLOSEOUT_2026_05_09.md

## Allowed Scope

- Add an explicit prompt-level rule requiring automation to run the picker before consuming reviewer backlog.
- Add an explicit prompt-level rule that P0/P1 backlog may preempt the product queue.
- Add an explicit prompt-level rule that P2 backlog is limited to at most one implementation attempt plus one closeout attempt for the same backlog item.
- Add an explicit prompt-level rule that P3 backlog must not preempt an open product queue and may only receive one bounded closeout attempt after queue exhaustion.
- Preserve existing automation schedule, model, working directory, batch controller, commit policy, and hard safety boundaries.

## Forbidden Scope

- real data
- masked-real data
- live Qwen/API/connectors
- production write-back
- customer-visible publish, deploy, or output
- external pilot
- production launch
- secrets, tokens, auth headers, raw logs, raw payloads, PoC, exploit steps, or attacker-readable topology
- autonomous containment, remediation, isolation, blocking, approval, rejection, or action-mode choice
- changing picker code or tests in this Goal
- changing automation schedule, model, cwd, or active status
- staging, committing, pushing, or rewriting history

## Acceptance Commands

```powershell
py -3 scripts\validate_codex_goal_card.py docs\goals\GOAL-AUTO-06_AUTOMATION_PROMPT_P3_PICKER_GUARD.md
Select-String -Path C:\Users\Administrator\.codex\automations\secupilot-fast-mvp-5-day-queue\automation.toml -Pattern "P3 backlog must not preempt an open product queue","Run scripts/pick_next_mvp_goal.py before consuming reviewer_backlog","P2 backlog may receive at most one implementation attempt plus one closeout attempt" -SimpleMatch
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- automation prompt still allows direct consumption of P3 backlog before picker execution
- automation prompt fails to preserve P0/P1 preemption
- automation prompt fails to limit P2 backlog to one implementation attempt plus one closeout attempt
- automation prompt changes schedule, model, cwd, active status, or hard safety boundaries
- validation command fails twice in the same way
- scope expands beyond listed files and the active automation prompt

## Rollback

- Restore the previous automation prompt from the pre-update automation.toml snapshot or Codex automation history.
- Leave GOAL-AUTO-04 picker code and prior commits untouched.
- Do not rewrite pushed or local commit history.

## Evidence Contract

- goal-card validation PASS output
- automation prompt text contains the picker-first P0/P1/P2/P3 policy
- git diff check PASS
- closeout report with exact command outcomes and no stage/commit/push

## Safety Sentinels

- no real_data=true
- no masked_real_data=true
- no live_qwen_api=true
- no production_writeback=true
- no customer_visible_output=true
- no Authorization
- no Bearer
- no token
- no raw_payload
- no action_command
- no attacker-readable attack_path

## Merge Rule

Acceptance commands must pass before this Goal is considered complete. Do not push. Reject unrelated changes. Do not stage or commit from the manual review window unless the human explicitly authorizes staging and commit.

## Next Unlock

If PASS, unlock automation continuation through the picker-selected product route. If HOLD, pause automation and repair only the prompt-level policy mismatch before allowing another run.

## Commit Posture

Manual window does not stage, commit, or push. Do not push. A later human-approved closeout commit may include only this goal card and closeout doc.
