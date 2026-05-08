# SecuPilot Next MVP Goal Candidate

Generated at: 2026-05-08T14:50:33

Selection mode: QUEUE_FALLBACK

## Candidate Goal

- queue_key: GOAL-MVP-95_PRIVATE_PREVIEW_LAUNCH_SHELL
- goal_id: GOAL-MVP-100_PRIVATE_PREVIEW_LAUNCH_SHELL
- goal_type: script
- statement: Refresh the private-preview launch shell so RC-019 opens as a product preview entry with current package paths, local-only boundaries, and check-only verification.

## Exact Files

- docs/goals/GOAL-MVP-100_PRIVATE_PREVIEW_LAUNCH_SHELL.md
- scripts/launch_s1_local_offline_trial.ps1
- backend/tests/test_s1_local_offline_launcher_contract.py
- artifacts/local_trial_launches/local-offline-trial-rc-019/launch_info.json
- docs/S6_FAST_MVP_GOAL_MVP_100_PRIVATE_PREVIEW_LAUNCH_SHELL_2026_05_08.md

## Acceptance Commands

- py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-100_PRIVATE_PREVIEW_LAUNCH_SHELL.md
- py -3 -m unittest backend.tests.test_s1_local_offline_launcher_contract
- powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/launch_s1_local_offline_trial.ps1 -PackageDir artifacts\local_demo_packages\local-offline-trial-rc-019-cn-review -DeliveryDir artifacts\local_trial_packages\local-offline-trial-rc-006 -Route /s1-trial -CheckOnly -SkipBuild -NoServer
- git -c core.quotepath=false diff --check

## HOLD Conditions

- launcher references RC-006 or RC-004 as the current candidate
- launcher starts a server, opens a browser, deploys, or calls live Qwen/API/connectors during check-only verification
- launcher omits local-only, no-writeback, no-customer-visible, or stop instructions
- unit test or check-only command fails twice in the same way
- scope expands beyond listed files
