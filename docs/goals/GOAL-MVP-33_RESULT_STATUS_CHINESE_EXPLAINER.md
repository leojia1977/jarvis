# GOAL-MVP-33_RESULT_STATUS_CHINESE_EXPLAINER

## Goal ID

```text
GOAL-MVP-33_RESULT_STATUS_CHINESE_EXPLAINER
```

## Goal type

```text
page
```

## Goal statement

```text
Make /s1-run present the run result and next step as reviewer-readable Chinese first, while preserving technical status codes as audit details.
```

## Primary executable object

```text
page=/s1-run
test=frontend/src/App.test.tsx
test=frontend/tests/e2e/s1-artifact-viewer.spec.ts
closeout=docs/S6_FAST_MVP_MVP_33_RESULT_STATUS_CHINESE_EXPLAINER_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
artifacts/local_demo_packages/local-offline-trial-rc-010-cn-review/
```

## Output paths

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
docs/goals/GOAL-MVP-33_RESULT_STATUS_CHINESE_EXPLAINER.md
docs/S6_FAST_MVP_MVP_33_RESULT_STATUS_CHINESE_EXPLAINER_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
docs/goals/GOAL-MVP-33_RESULT_STATUS_CHINESE_EXPLAINER.md
docs/S6_FAST_MVP_MVP_33_RESULT_STATUS_CHINESE_EXPLAINER_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
frontend page copy and layout polish for /s1-run
local fixture/package artifact reads
local tests
local screenshots from Playwright test output only
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-33_RESULT_STATUS_CHINESE_EXPLAINER.md
npm run test -- src/App.test.tsx
npm run build
npx playwright test tests/e2e/s1-artifact-viewer.spec.ts
```

## HOLD conditions

```text
/s1-run still presents S1_CLOSED_SHADOW_PASS_WITH_NOTES as the primary reviewer conclusion
technical status code is removed entirely and audit trace is lost
/s1-run implies customer-visible publish/deploy/pilot/production authorization
/s1-run implies live Qwen/API/connectors or production write-back
customer_visible_output is not false
production_writeback is not false
tests fail twice in the same way
```

## Rollback

```text
revert changed files listed in Allowed files only
delete generated local artifacts for this Goal candidate only
preserve failure evidence
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
Playwright screenshot in test output when e2e runs
closeout note with exact commands
```

## Safety sentinels

```text
no customer_visible_output=true
no production_writeback=true
no live_qwen_api=true
no live_connectors=true
no Authorization: / Bearer / refresh_token in artifacts
no primary reviewer status text equal to S1_CLOSED_SHADOW_PASS_WITH_NOTES
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock the next concrete GOAL-* selected by the user.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-33 result status chinese explainer
do not push unless separately authorized
```
