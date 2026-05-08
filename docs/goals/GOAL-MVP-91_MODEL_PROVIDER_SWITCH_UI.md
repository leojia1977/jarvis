# GOAL-MVP-91_MODEL_PROVIDER_SWITCH_UI

## Goal ID

```text
GOAL-MVP-91_MODEL_PROVIDER_SWITCH_UI
```

## Goal type

```text
page
interface
```

## Goal statement

```text
Expose the Qwen synthetic provider stub readiness in the product UI so reviewers can understand the model path is prepared for preview but still no-network and no-live-call.
```

## Primary executable object

```text
page=frontend/src/secupilot/s1/S1LocalTrialView.tsx
page=frontend/src/App.tsx
interface=frontend/src/secupilot/s1/s1QwenProviderReadiness.ts
interface=frontend/src/secupilot/s1/s1QwenProviderContract.ts
test=frontend/src/App.test.tsx
closeout=docs/S6_FAST_MVP_MVP_91_MODEL_PROVIDER_SWITCH_UI_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
frontend/src/secupilot/s1/s1QwenProviderContract.ts
frontend/src/secupilot/s1/s1QwenProviderDryPreview.ts
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report.json
```

## Output paths

```text
docs/goals/GOAL-MVP-91_MODEL_PROVIDER_SWITCH_UI.md
frontend/src/secupilot/s1/s1QwenProviderReadiness.ts
frontend/src/secupilot/s1/s1QwenProviderContract.ts
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
docs/S6_FAST_MVP_MVP_91_MODEL_PROVIDER_SWITCH_UI_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-91_MODEL_PROVIDER_SWITCH_UI.md
frontend/src/secupilot/s1/s1QwenProviderReadiness.ts
frontend/src/secupilot/s1/s1QwenProviderContract.ts
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
docs/S6_FAST_MVP_MVP_91_MODEL_PROVIDER_SWITCH_UI_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
frontend product UI only
local static readiness metadata
unit/e2e assertion updates for no-live-call model provider status
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
Set-Location -LiteralPath frontend; npm run test -- --run src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-91_MODEL_PROVIDER_SWITCH_UI.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
UI says live Qwen/API is enabled
UI says API key is read, required for current preview, or retained
UI hides no-network/no-live-call boundary from the model provider section
provider contract active mode is inconsistent with the readiness card
tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
preserve failed test output in closeout if failure occurred
```

## Evidence contract

```text
frontend unit test output
frontend build output
goal card validator output
git diff --check output
closeout report with exact commands
```

## Safety sentinels

```text
no data-live-qwen-api=true
no data-network-request=true
no data-api-key-required=true
no data-secret-values-read=true
no live connector, production write-back, customer-visible output, or autonomous Qwen action
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-92_LOCAL_PRIVATE_TRIAL_RC_WITH_QWEN_READINESS.
If HOLD, stop and report the failing UI or test item.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-91 model provider switch UI
stage and commit only Goal files
do not push
```
