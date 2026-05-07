# GOAL-MVP-36_RESULT_TECH_CODE_DISCLOSURE

## Goal ID

```text
GOAL-MVP-36_RESULT_TECH_CODE_DISCLOSURE
```

## Goal type

```text
page
```

## Goal statement

```text
Weaken first-screen English technical code exposure on /s1-run, add Chinese tooltip guidance, and preserve technical reconciliation access.
```

## Primary executable object

```text
page=/s1-run
test=frontend/src/App.test.tsx
test=frontend/tests/e2e/s1-artifact-viewer.spec.ts
closeout=docs/S6_FAST_MVP_MVP_36_RESULT_TECH_CODE_DISCLOSURE_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-011-cn-review/reviewer_backlog.json
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.css
```

## Output paths

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
docs/goals/GOAL-MVP-36_RESULT_TECH_CODE_DISCLOSURE.md
docs/S6_FAST_MVP_MVP_36_RESULT_TECH_CODE_DISCLOSURE_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts
docs/goals/GOAL-MVP-36_RESULT_TECH_CODE_DISCLOSURE.md
docs/S6_FAST_MVP_MVP_36_RESULT_TECH_CODE_DISCLOSURE_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
frontend page copy and layout polish for /s1-run
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-36_RESULT_TECH_CODE_DISCLOSURE.md
npm run test -- src/App.test.tsx
npm run build
npx playwright test tests/e2e/s1-artifact-viewer.spec.ts
```

## HOLD conditions

```text
/s1-run first-screen primary conclusion shows raw S1_CLOSED_SHADOW_PASS_WITH_NOTES as visible text
technical status codes are removed entirely and audit trace is lost
technical reconciliation details are open by default
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
Playwright smoke screenshot in test output
closeout note with exact commands
```

## Safety sentinels

```text
no visible first-screen S1_CLOSED_SHADOW_PASS_WITH_NOTES primary status text
no customer_visible_output=true
no production_writeback=true
no live_qwen_api=true
no live_connectors=true
no Authorization: / Bearer / refresh_token in artifacts
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock a future RC-012 package if reviewer wants a fresh screenshot package.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-36 result tech code disclosure
do not push unless separately authorized
```
