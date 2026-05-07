# GOAL-MVP-22_RESULT_PAGE

## Goal ID

```text
GOAL-MVP-22_RESULT_PAGE
```

## Goal type

```text
page
```

## Goal statement

```text
Turn /s1-run into a product-style local trial result page with the artifact table hidden under technical reconciliation.
```

## Primary executable object

```text
page=/s1-run
test=frontend/src/App.test.tsx
test=frontend/tests/e2e/s1-artifact-viewer.spec.ts
artifact=local screenshots if the page changes visually
closeout=docs/S6_FAST_MVP_MVP_22_RESULT_PAGE_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
artifacts/local_demo_packages/local-offline-trial-rc-008-cn-review/
artifacts/local_demo_packages/local-offline-trial-rc-008-cn-review/evidence/final_status.json
artifacts/local_demo_packages/local-offline-trial-rc-008-cn-review/evidence/case_summary.json
artifacts/local_demo_packages/local-offline-trial-rc-008-cn-review/evidence/artifact_manifest.json
artifacts/local_demo_packages/local-offline-trial-rc-008-cn-review/evidence/safety_scan.json
```

## Output paths

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
docs/S6_FAST_MVP_MVP_22_RESULT_PAGE_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
frontend/src/secupilot/s1/S1ArtifactView.tsx
frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts
frontend/src/App.css
frontend/src/App.test.tsx
frontend/tests/e2e/s1-artifact-viewer.spec.ts
docs/S6_FAST_MVP_MVP_22_RESULT_PAGE_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
frontend page changes for /s1-run
local fixture/package artifact reads
local tests
local screenshots if needed
local closeout note
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
backend API/schema migration unless separately named
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-22_RESULT_PAGE.md
npm run test -- src/App.test.tsx
npm run build
npx playwright test tests/e2e/s1-artifact-viewer.spec.ts
```

## HOLD conditions

```text
/s1-run exposes P1/P2/P3, Mock Fixture, Expert Mode, or debug controls
safety_scan finding_count > 0
customer_visible_output != false
production_writeback != false
package manifest missing SHA256
final_status candidate/source_candidate inconsistent
tests fail twice in the same way
```

## Rollback

```text
revert changed frontend files listed in Allowed files
delete generated local screenshots for this Goal only
preserve failure log in the closeout note
do not hide failed evidence
```

## Evidence contract

```text
command transcript or test output
Playwright smoke output
screenshots if page/UI changed
closeout note with exact commands
```

## Safety sentinels

```text
no P1/P2/P3 in reviewer-clean screenshots
no Mock Fixture in reviewer-clean screenshots
no Expert Mode in reviewer-clean screenshots
no Authorization: / Bearer / refresh_token in artifacts
no writeback_enabled=true
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
If PASS, unlock GOAL-MVP-24_LOCAL_TRIAL_PACKAGE_BUILDER_V2.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-22 result page local review UI
do not push unless separately authorized
```
