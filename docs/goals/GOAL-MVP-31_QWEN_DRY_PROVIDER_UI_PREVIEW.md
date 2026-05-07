# GOAL-MVP-31_QWEN_DRY_PROVIDER_UI_PREVIEW

## Goal ID

```text
GOAL-MVP-31_QWEN_DRY_PROVIDER_UI_PREVIEW
```

## Goal type

```text
page
```

## Goal statement

```text
Expose the Qwen dry provider contract as a local/offline product UI preview on /s1-trial without enabling live Qwen/API calls.
```

## Primary executable object

```text
page=/s1-trial
test=frontend/tests/e2e/s1-qwen-dry-provider-preview.spec.ts
artifact=artifacts/qwen_provider_dry_ui_preview/2026-05-07/s1-qwen-dry-provider-preview.png
closeout=docs/S6_FAST_MVP_MVP_31_QWEN_DRY_PROVIDER_UI_PREVIEW_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
mock_data/qwen_provider_contract/valid_response.json
frontend/src/secupilot/s1/s1QwenProviderContract.ts
frontend/src/secupilot/s1/S1LocalTrialView.tsx
```

## Output paths

```text
frontend/src/secupilot/s1/s1QwenProviderDryPreview.ts
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-qwen-dry-provider-preview.spec.ts
artifacts/qwen_provider_dry_ui_preview/2026-05-07/s1-qwen-dry-provider-preview.png
artifacts/qwen_provider_dry_ui_preview/2026-05-07/s1-qwen-dry-provider-preview.text.json
artifacts/qwen_provider_contract/mvp-31-ui-preview-validation.json
docs/goals/GOAL-MVP-31_QWEN_DRY_PROVIDER_UI_PREVIEW.md
docs/S6_FAST_MVP_MVP_31_QWEN_DRY_PROVIDER_UI_PREVIEW_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
frontend/src/secupilot/s1/s1QwenProviderDryPreview.ts
frontend/src/secupilot/s1/S1LocalTrialView.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-qwen-dry-provider-preview.spec.ts
artifacts/qwen_provider_dry_ui_preview/2026-05-07/s1-qwen-dry-provider-preview.png
artifacts/qwen_provider_dry_ui_preview/2026-05-07/s1-qwen-dry-provider-preview.text.json
artifacts/qwen_provider_contract/mvp-31-ui-preview-validation.json
docs/goals/GOAL-MVP-31_QWEN_DRY_PROVIDER_UI_PREVIEW.md
docs/S6_FAST_MVP_MVP_31_QWEN_DRY_PROVIDER_UI_PREVIEW_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
frontend UI preview
local dry contract validation
local tests
local screenshot artifact
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
API keys
secrets/tokens/auth headers
live connectors
production write-back
customer-visible publish/deploy/output
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-31_QWEN_DRY_PROVIDER_UI_PREVIEW.md
py -3 scripts/validate_qwen_provider_contract.py mock_data/qwen_provider_contract/valid_response.json --output-json artifacts/qwen_provider_contract/mvp-31-ui-preview-validation.json
npm run test -- src/App.test.tsx
npm run build
npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-qwen-dry-provider-preview.spec.ts
```

## HOLD conditions

```text
dry contract validator returns HOLD
/s1-trial does not render the dry provider preview
preview exposes live Qwen/API/connectors/write-back/autonomous action as true
preview contains raw payload/action command/auth marker text
preview includes send/call/connect/deploy/publish controls
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files
delete generated qwen dry preview screenshot and validation artifact only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
dry contract validation JSON
Playwright screenshot and visible-text sidecar
closeout note with exact commands
```

## Safety sentinels

```text
no live_qwen_api=true
no live_connectors=true
no production_writeback=true
no autonomous_qwen_action=true
no Authorization: / Bearer / refresh_token in artifacts
no action_command in UI preview
no customer_visible_output=true
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock product discussion for a future non-live provider adapter route.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-31 qwen dry provider ui preview
do not push unless separately authorized
```
