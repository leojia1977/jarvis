# GOAL-AUTO-01 Automation Product Acceleration Restore

## Goal ID

GOAL-AUTO-01_AUTOMATION_PRODUCT_ACCELERATION_RESTORE

## Goal Type

script

## Goal Statement

Restore the SecuPilot automation loop so it uses the current product acceleration Goal queue, skips stale pre-RC016 fallback work after MVP-94, and continues to the next eligible Goal inside the same automation run when a Goal completes cleanly.

## Primary Executable Object

script=scripts/pick_next_mvp_goal.py
artifact=artifacts/product_acceleration/next_goal_candidate.json
artifact=artifacts/product_acceleration/next_goal_candidate.md
automation=codex_app automation id secupilot-fast-mvp-5-day-queue
closeout=docs/S6_FAST_MVP_GOAL_AUTO_01_AUTOMATION_PRODUCT_ACCELERATION_RESTORE_2026_05_08.md

## Inputs

- docs/goals/GOAL-MVP-94_PRIVATE_PREVIEW_SHELL_ROUTE_MAP.md
- artifacts/product_backlog/**/reviewer_backlog.json
- C:\Users\Administrator\.codex\automations\secupilot-fast-mvp-5-day-queue\automation.toml
- Current user instruction authorizing GOAL-AUTO-01 product acceleration restore.

## Output Paths

- scripts/pick_next_mvp_goal.py
- backend/tests/test_pick_next_mvp_goal.py
- artifacts/product_acceleration/next_goal_candidate.json
- artifacts/product_acceleration/next_goal_candidate.md
- docs/goals/GOAL-AUTO-01_AUTOMATION_PRODUCT_ACCELERATION_RESTORE.md
- docs/S6_FAST_MVP_GOAL_AUTO_01_AUTOMATION_PRODUCT_ACCELERATION_RESTORE_2026_05_08.md

## Allowed Files

- scripts/pick_next_mvp_goal.py
- backend/tests/test_pick_next_mvp_goal.py
- artifacts/product_acceleration/next_goal_candidate.json
- artifacts/product_acceleration/next_goal_candidate.md
- docs/goals/GOAL-AUTO-01_AUTOMATION_PRODUCT_ACCELERATION_RESTORE.md
- docs/S6_FAST_MVP_GOAL_AUTO_01_AUTOMATION_PRODUCT_ACCELERATION_RESTORE_2026_05_08.md

## Allowed Scope

- Product-acceleration automation queue selection logic.
- Local/offline automation prompt refresh for `secupilot-fast-mvp-5-day-queue`.
- Skip stale legacy queue candidates after the private-preview route-map reset marker is present.
- Generate the next bounded executable candidate for the private-preview product lane.
- Local tests and local repo artifacts only.

## Forbidden Scope

- No real data.
- No masked-real data.
- No live Qwen or live API call.
- No live connector or connector mutation.
- No production write-back or production writeback.
- No customer-visible publish, deploy, output, staging, external pilot, or production launch.
- No secret, token, auth header, API key, raw customer log, or raw customer payload.
- No backend API/schema migration.
- No push.

## Acceptance Commands

```powershell
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-AUTO-01_AUTOMATION_PRODUCT_ACCELERATION_RESTORE.md
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts/pick_next_mvp_goal.py --repo-root . --output-json artifacts/product_acceleration/next_goal_candidate.json --output-md artifacts/product_acceleration/next_goal_candidate.md
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- Picker still selects GOAL-MVP-62/legacy RC016 queue work after GOAL-MVP-94_PRIVATE_PREVIEW_SHELL_ROUTE_MAP exists.
- Picker output misses exact files, acceptance commands, or HOLD conditions.
- Automation prompt still treats the expired DELEGATED_APPROVER_CHARTER window as a blocker for this product-acceleration queue.
- Automation prompt stops after one clean Goal even when the next eligible Goal is available and time remains.
- Unit test fails twice in the same way.
- Scope expands beyond listed files or changes unrelated product artifacts.
- Any selected next Goal would require real data, masked-real data, live Qwen/API, connectors, secrets, production write-back, customer-visible output, deploy, external pilot, production launch, or backend API/schema migration.

## Rollback

- Revert `scripts/pick_next_mvp_goal.py` and `backend/tests/test_pick_next_mvp_goal.py`.
- Re-run the picker to restore the previous candidate artifact if needed.
- Restore the previous automation prompt from `C:\Users\Administrator\.codex\automations\secupilot-fast-mvp-5-day-queue\automation.toml` history if the app update is incorrect.
- Preserve any failed run evidence instead of deleting it.

## Evidence Contract

- Command transcript for goal-card validation.
- Unit test output for the picker.
- Generated `next_goal_candidate.json` and `.md`.
- Closeout doc with automation prompt update result.
- `git diff --check` output.

## Safety Sentinels

- no real data
- no masked-real data
- no live_qwen_api
- no connector mutation
- customer_visible_output false
- production_writeback false
- writeback_enabled false
- no Authorization header
- no Bearer token
- no secret or token artifact

## Merge Rule

May stage and commit only if all acceptance commands PASS, the generated next candidate is a current private-preview product acceleration Goal, and no HOLD condition is observed. Do not push. Do not merge unrelated changes.

## Next Unlock

If PASS, unlock the restored product acceleration automation run to execute GOAL-MVP-95_PRIVATE_PREVIEW_LAUNCH_SHELL or the next eligible higher-priority reviewer backlog item. If HOLD, stop automation and report the exact blocker instead of looping on stale queue-exhausted candidates.

## Commit Posture

One commit for GOAL-AUTO-01 restore. Commit only selected files and generated candidate artifacts. Do not push.
