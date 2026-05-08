# GOAL-MVP-74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT

## Goal ID

```text
GOAL-MVP-74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT
```

## Goal type

```text
package
```

## Goal statement

```text
Turn the MVP-73 private deployment structure into a local/offline trial entry package with a customer-readable start-here README, one-click Windows entry script, and generated dry-run status file.
```

## Primary executable object

```text
script=scripts/build_private_deployment_package.py
script=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/START_SECUPILOT_LOCAL_TRIAL.cmd
script=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/scripts/START_CUSTOMER_TRIAL.ps1
package=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/
package=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1.zip
artifact=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_status.json
test=backend/tests/test_build_private_deployment_package.py
closeout=docs/S6_FAST_MVP_MVP_74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
scripts/build_private_deployment_package.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/package_manifest.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/scripts/VERIFY_BOUNDARIES.ps1
```

## Output paths

```text
docs/goals/GOAL-MVP-74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT.md
scripts/build_private_deployment_package.py
backend/tests/test_build_private_deployment_package.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1.zip
docs/S6_FAST_MVP_MVP_74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT.md
scripts/build_private_deployment_package.py
backend/tests/test_build_private_deployment_package.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/**
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1.zip
docs/S6_FAST_MVP_MVP_74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
local/offline trial entry only
Windows/local-first one-click dry-run script
local package/artifact generation
local boundary verification
unit tests and docs-only closeout evidence for this Goal
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
py -3 scripts/build_private_deployment_package.py --package-id secupilot-private-deployment-windows-local-v0_1 --output-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1 --zip-path artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1.zip --repo-root .
powershell.exe -NoProfile -ExecutionPolicy Bypass -File artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/scripts/START_CUSTOMER_TRIAL.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/scripts/VERIFY_BOUNDARIES.ps1
py -3 -m unittest -q backend.tests.test_build_private_deployment_package
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-74_CUSTOMER_TRIAL_README_AND_ONE_CLICK_START_SCRIPT.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
one-click script deploys, starts production service, calls live API, sends network request, reads API key, calls connector, writes production, or pushes
generated trial status omits boundary fields or reports any forbidden boundary as true
generated package contains real data, masked-real data, raw payload, auth header, token, secret, customer log, or production connector output
package manifest omits one-click entry points or SHA256 entries
unit tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
delete regenerated private deployment package directory and zip for this Goal
preserve failed command output in closeout if failure occurred
```

## Evidence contract

```text
goal card validator output
private deployment package generator output
one-click PowerShell dry-run output
boundary verification output
unit test output
package manifest with SHA256 entries and entry_points
trial_output/customer_trial_status.json
zip SHA256 in package manifest
git diff --check output
closeout report with exact commands
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no network_request=true
no api_key_required=true
no live_connectors=true
no production_writeback=true
no customer_visible_output=true
no deploy_executed=true
no Authorization/Bearer/refresh_token in generated files
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-75_INTERNAL_TRIAL_KPI_REPORT.
If HOLD, stop and report failing command plus blocker evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-74 customer trial one-click entry
stage and commit only Goal files
do not push
```
