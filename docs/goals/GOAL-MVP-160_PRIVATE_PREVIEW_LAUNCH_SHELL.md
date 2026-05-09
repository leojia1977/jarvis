# GOAL-MVP-160 Private Preview Launch Shell

## Goal ID

```text
GOAL-MVP-160_PRIVATE_PREVIEW_LAUNCH_SHELL
```

## Goal type

```text
script
```

## Goal statement

```text
Refresh the private-preview launch shell so RC-019 opens as a product preview entry with current package paths, local-only boundaries, and check-only verification.
```

## Primary executable object

```text
script=scripts/launch_s1_local_offline_trial.ps1
test=backend/tests/test_s1_local_offline_launcher_contract.py
artifact=artifacts/local_trial_launches/local-offline-trial-rc-019/launch_info.json
closeout=docs/S6_FAST_MVP_GOAL_MVP_160_PRIVATE_PREVIEW_LAUNCH_SHELL_2026_05_09.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review/**
artifacts/local_trial_packages/local-offline-trial-rc-006/**
```

## Output paths

```text
docs/goals/GOAL-MVP-160_PRIVATE_PREVIEW_LAUNCH_SHELL.md
scripts/launch_s1_local_offline_trial.ps1
backend/tests/test_s1_local_offline_launcher_contract.py
artifacts/local_trial_launches/local-offline-trial-rc-019/launch_info.json
docs/S6_FAST_MVP_GOAL_MVP_160_PRIVATE_PREVIEW_LAUNCH_SHELL_2026_05_09.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-160_PRIVATE_PREVIEW_LAUNCH_SHELL.md
scripts/launch_s1_local_offline_trial.ps1
backend/tests/test_s1_local_offline_launcher_contract.py
artifacts/local_trial_launches/local-offline-trial-rc-019/launch_info.json
docs/S6_FAST_MVP_GOAL_MVP_160_PRIVATE_PREVIEW_LAUNCH_SHELL_2026_05_09.md
```

## Allowed scope

```text
private-preview launcher defaults and boundary checks for RC-019 package
launcher contract unittest coverage for check-only and local artifact write path
launcher output artifact refresh for RC-019
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
production write-back
customer-visible publish/deploy/output
external pilot
production launch
secrets/tokens/auth headers/raw customer logs
autonomous remediation/action-mode choice
backend API/schema migration
push
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-160_PRIVATE_PREVIEW_LAUNCH_SHELL.md
py -3 -m unittest backend.tests.test_s1_local_offline_launcher_contract
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/launch_s1_local_offline_trial.ps1 -PackageDir artifacts\local_demo_packages\local-offline-trial-rc-019-cn-review -DeliveryDir artifacts\local_trial_packages\local-offline-trial-rc-006 -Route /s1-trial -CheckOnly -SkipBuild -NoServer
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
launcher references RC-006 or RC-004 as the current candidate
launcher starts a server, opens a browser, deploys, or calls live Qwen/API/connectors during check-only verification
launcher omits local-only, no-writeback, no-customer-visible, or stop instructions
unit test or check-only command fails twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
leave unrelated dirty/untracked residue untouched
```

## Evidence contract

```text
goal card validator PASS output
launcher contract unittest PASS output
check-only launcher command JSON output
launch_info.json updated to RC-019 path and candidate
diff --check PASS output
closeout record with exact command outcomes
```

## Safety sentinels

```text
real_data=false
masked_real_data=false
live_qwen_api=false
live_connectors=false
production_writeback=false
customer_visible_output=false
push=false
```

## Merge rule

```text
Stage and commit only allowed files after all acceptance commands PASS and no HOLD condition triggers.
Reject unrelated changes; do not stage unrelated files.
Do not push.
```

## Next unlock

```text
PASS unlock: continue picker-selected private-preview lane goals.
HOLD behavior: report exact failing check and stop this run.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-160 private preview launch shell
stage only Goal files
do not push
```
