# GOAL-MVP-25_QWEN_PROVIDER_DRY_CONTRACT

## Goal ID

```text
GOAL-MVP-25_QWEN_PROVIDER_DRY_CONTRACT
```

## Goal type

```text
interface
```

## Goal statement

```text
Define and validate a Qwen provider dry contract that permits metadata-only HITL summaries and rejects live calls, autonomous actions, action commands, secrets, raw evidence, and write-back fields.
```

## Primary executable object

```text
interface=secupilot.qwen_provider_dry_response.v1
script=scripts/validate_qwen_provider_contract.py
test=backend/tests/test_qwen_provider_contract.py
artifact=mock_data/qwen_provider_contract/valid_response.json
artifact=mock_data/qwen_provider_contract/forbidden_action_command.json
closeout=docs/S6_FAST_MVP_MVP_25_QWEN_PROVIDER_DRY_CONTRACT_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
mock_data/qwen_provider_contract/valid_response.json
mock_data/qwen_provider_contract/forbidden_action_command.json
docs/S6_FAST_MVP_CLIENT_TRIAL_READINESS_REPORT_2026_05_07.md
```

## Output paths

```text
scripts/validate_qwen_provider_contract.py
backend/tests/test_qwen_provider_contract.py
mock_data/qwen_provider_contract/valid_response.json
mock_data/qwen_provider_contract/forbidden_action_command.json
docs/goals/GOAL-MVP-25_QWEN_PROVIDER_DRY_CONTRACT.md
docs/S6_FAST_MVP_MVP_25_QWEN_PROVIDER_DRY_CONTRACT_CLOSEOUT_2026_05_07.md
artifacts/qwen_provider_contract/mvp-25-validation.json
```

## Allowed files

```text
scripts/validate_qwen_provider_contract.py
backend/tests/test_qwen_provider_contract.py
mock_data/qwen_provider_contract/**
docs/goals/GOAL-MVP-25_QWEN_PROVIDER_DRY_CONTRACT.md
docs/S6_FAST_MVP_MVP_25_QWEN_PROVIDER_DRY_CONTRACT_CLOSEOUT_2026_05_07.md
artifacts/qwen_provider_contract/mvp-25-validation.json
```

## Allowed scope

```text
local/offline only
dry interface contract validation
local fixtures
local tests
local validation artifact
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
production write-back
customer-visible publish/deploy/output
secrets/tokens/auth headers/raw customer logs
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-25_QWEN_PROVIDER_DRY_CONTRACT.md
py -3 -m unittest backend.tests.test_qwen_provider_contract
py -3 scripts/validate_qwen_provider_contract.py mock_data/qwen_provider_contract/valid_response.json --output-json artifacts/qwen_provider_contract/mvp-25-validation.json
py -3 scripts/validate_qwen_provider_contract.py mock_data/qwen_provider_contract/forbidden_action_command.json
```

## HOLD conditions

```text
valid dry contract fixture fails validation
forbidden action_command fixture passes validation
contract includes autonomous approval/rejection/blocking/closure
contract accepts action_command
contract accepts raw payload or raw evidence
contract stores secrets/tokens/auth headers
contract requires API key or network access to test
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
delete generated validation artifact only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
validation JSON artifact
positive and negative fixture results
closeout note with exact commands
```

## Safety sentinels

```text
no Authorization: / Bearer / refresh_token in artifacts
no raw_payload in accepted contract
no action_command in accepted contract
no writeback_enabled=true
no customer_visible_output=true
live_qwen_api = false
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-27_SCREENSHOT_SAFETY_VALIDATOR or GOAL-MVP-28_RC_DIFF_CHECKER.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-25 qwen provider dry contract
do not push unless separately authorized
```
