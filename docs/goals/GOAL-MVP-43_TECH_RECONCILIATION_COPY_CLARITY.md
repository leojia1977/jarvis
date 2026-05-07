# GOAL-MVP-43_TECH_RECONCILIATION_COPY_CLARITY

## Goal ID

```text
GOAL-MVP-43_TECH_RECONCILIATION_COPY_CLARITY
```

## Goal type

```text
page
```

## Goal statement

```text
Clarify the /s1-run technical reconciliation explainer copy so reviewers cannot misread the phrase around candidate version checking.
```

## Primary executable object

```text
page=/s1-run
test=frontend/src/App.test.tsx
test=frontend/tests/e2e/s1-artifact-viewer.spec.ts
closeout=docs/S6_FAST_MVP_MVP_43_TECH_RECONCILIATION_COPY_CLARITY_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-013-cn-review/reviewer_backlog.json
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
```

## Output paths

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
docs/goals/GOAL-MVP-43_TECH_RECONCILIATION_COPY_CLARITY.md
docs/S6_FAST_MVP_MVP_43_TECH_RECONCILIATION_COPY_CLARITY_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
docs/goals/GOAL-MVP-43_TECH_RECONCILIATION_COPY_CLARITY.md
docs/S6_FAST_MVP_MVP_43_TECH_RECONCILIATION_COPY_CLARITY_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
frontend page copy for /s1-run
local tests
no new RC package generation
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
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-43_TECH_RECONCILIATION_COPY_CLARITY.md
Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
/s1-run no longer shows the technical reconciliation entry point
technical reconciliation details are open by default
technical reconciliation explainer implies customer-visible, deploy, live Qwen/API, connector, or production write-back authority
customer_visible_output is not false
production_writeback is not false
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files only
preserve failure evidence
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
Playwright smoke screenshot in test output
closeout note with exact commands
```

## Safety sentinels

```text
no customer_visible_output=true
no production_writeback=true
no live_qwen_api=true
no live_connectors=true
no Authorization: / Bearer / refresh_token in artifacts
technical reconciliation remains closed by default
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock closing RFB-RC013-004 after commit evidence exists.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-43 tech reconciliation copy clarity
do not push unless separately authorized
```
