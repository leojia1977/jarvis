# GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT

## Goal ID

```text
GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT
```

## Goal type

```text
script
```

## Goal statement

```text
Turn the MVP-77 Windows prerequisite draft into a runnable local PowerShell precheck script that verifies OS, PowerShell, Python launcher, and package write permissions without deployment or live service calls.
```

## Primary executable object

```text
script=scripts/generate_private_deployment_precheck.py
script=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/scripts/RUN_PRIVATE_DEPLOYMENT_PRECHECK.ps1
artifact=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_precheck_contract.json
artifact=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_precheck_result.json
test=backend/tests/test_generate_private_deployment_precheck.py
closeout=docs/S6_FAST_MVP_MVP_78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/package_manifest.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft.json
```

## Output paths

```text
docs/goals/GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT.md
scripts/generate_private_deployment_precheck.py
backend/tests/test_generate_private_deployment_precheck.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/scripts/RUN_PRIVATE_DEPLOYMENT_PRECHECK.ps1
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_precheck_contract.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_precheck_result.json
docs/S6_FAST_MVP_MVP_78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT.md
scripts/generate_private_deployment_precheck.py
backend/tests/test_generate_private_deployment_precheck.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/scripts/RUN_PRIVATE_DEPLOYMENT_PRECHECK.ps1
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_precheck_contract.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_precheck_result.json
docs/S6_FAST_MVP_MVP_78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
local/offline precheck generation only
local PowerShell execution
local package and prereq draft artifact reads
local precheck result artifact generation
local tests
docs-only closeout evidence for this Goal
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
external pilot
production launch
backend API/schema migration
push
```

## Acceptance commands

```text
py -3 scripts/generate_private_deployment_precheck.py --package-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1 --draft-json artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft.json --output-script artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/scripts/RUN_PRIVATE_DEPLOYMENT_PRECHECK.ps1 --contract-path artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_precheck_contract.json --repo-root .
powershell.exe -NoProfile -ExecutionPolicy Bypass -File artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/scripts/RUN_PRIVATE_DEPLOYMENT_PRECHECK.ps1
py -3 -m unittest -q backend.tests.test_generate_private_deployment_precheck
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
precheck generator or generated script performs deployment, starts production service, calls live API, sends network request, reads API key, calls connector, writes production, or pushes
generated precheck script omits WIN-PREQ-01, WIN-PREQ-02, WIN-PREQ-03, or WIN-PREQ-04
precheck result reports deploy_executed, network_request, live_qwen_api, live_connectors, production_writeback, customer_visible_output, real_data, or masked_real_data as true
precheck result status is not PRIVATE_DEPLOYMENT_PRECHECK_PASS on the local Windows test machine
generated artifacts contain real data, masked-real data, raw payload, auth header, token, secret, customer log, or production connector output
unit tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
delete generated precheck script, contract, and result artifacts for this Goal
preserve failed command output in closeout if failure occurred
```

## Evidence contract

```text
goal card validator output
precheck generator output
PowerShell precheck output
unit test output
private_deployment_precheck_contract.json
private_deployment_precheck_result.json
git diff --check output
closeout report with exact commands
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no network_request=true
no live_connectors=true
no production_writeback=true
no customer_visible_output=true
no deploy_executed=true
no Authorization/Bearer/refresh_token in generated precheck artifacts
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT.
If HOLD, stop and report failing command plus blocker evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-78 private deployment precheck script
stage and commit only Goal files
do not push
```
