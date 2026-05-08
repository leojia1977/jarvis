# GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT

## Goal ID

```text
GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT
```

## Goal type

```text
test-report
```

## Goal statement

```text
Turn the MVP-76 feedback sample into a local/offline private deployment prerequisite and sizing draft covering Windows prerequisites, resource sizing profiles, and the dry-run model provider path.
```

## Primary executable object

```text
script=scripts/generate_private_deployment_prereq_sizing_draft.py
test=backend/tests/test_generate_private_deployment_prereq_sizing_draft.py
report=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft.json
report=artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft_中文.md
closeout=docs/S6_FAST_MVP_MVP_77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/package_manifest.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_status.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_feedback.sample.json
```

## Output paths

```text
docs/goals/GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT.md
scripts/generate_private_deployment_prereq_sizing_draft.py
backend/tests/test_generate_private_deployment_prereq_sizing_draft.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft_中文.md
docs/S6_FAST_MVP_MVP_77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT.md
scripts/generate_private_deployment_prereq_sizing_draft.py
backend/tests/test_generate_private_deployment_prereq_sizing_draft.py
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft.json
artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/private_deployment_prereq_sizing_draft_中文.md
docs/S6_FAST_MVP_MVP_77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
local/offline draft report generation only
local package, trial status, and feedback sample reads
local JSON/Markdown output
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
py -3 scripts/generate_private_deployment_prereq_sizing_draft.py --package-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1 --feedback-json artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output/customer_trial_feedback.sample.json --output-dir artifacts/private_deployment_packages/secupilot-private-deployment-windows-local-v0_1/trial_output --repo-root .
py -3 -m unittest -q backend.tests.test_generate_private_deployment_prereq_sizing_draft
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
draft generator performs deployment, starts production service, calls live API, sends network request, reads API key, calls connector, writes production, or pushes
trial status reports any forbidden boundary as true
package_id mismatches between manifest, trial status, and feedback sample
feedback sample contains real data, masked-real data, raw payload, auth header, token, secret, customer log, or production connector output
generated draft omits Windows prerequisites, resource sizing profiles, model provider path, follow-up actions, or non-authorization boundary
generated draft claims production benchmark, customer pilot, deployment execution, or live Qwen/API readiness
unit tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
delete generated prereq/sizing draft JSON/MD for this Goal
preserve failed command output in closeout if failure occurred
```

## Evidence contract

```text
goal card validator output
prereq/sizing draft generator output
unit test output
private_deployment_prereq_sizing_draft.json
private_deployment_prereq_sizing_draft_中文.md
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
no Authorization/Bearer/refresh_token in generated draft
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-78_PRIVATE_DEPLOYMENT_PRECHECK_SCRIPT.
If HOLD, stop and report failing command plus blocker evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-77 private deployment prereq sizing draft
stage and commit only Goal files
do not push
```
