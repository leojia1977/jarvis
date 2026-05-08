# GOAL-MVP-118 Backlog Item RFB-RC016-004

## Goal ID

```text
GOAL-MVP-118_BACKLOG_ITEM_RFB_RC016_004
```

## Goal type

```text
page
```

## Goal statement

```text
Shorten the mobile navigation label to "AI 建议来源 ▸" to reduce repetitive wording while preserving current local/offline AI advice source workflow.
```

## Primary executable object

```text
page=frontend/src/App.tsx
test=frontend/src/App.test.tsx
test=frontend/tests/e2e/incident-product-page.spec.ts
closeout=docs/S6_FAST_MVP_GOAL_MVP_118_BACKLOG_ITEM_RFB_RC016_004_2026_05_08.md
```

## Inputs

```text
artifacts/product_acceleration/next_goal_candidate.json
artifacts/product_backlog/local-offline-trial-rc-016-cn-review/reviewer_backlog.json
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/incident-product-page.spec.ts
```

## Output paths

```text
docs/goals/GOAL-MVP-118_BACKLOG_ITEM_RFB_RC016_004.md
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/incident-product-page.spec.ts
docs/S6_FAST_MVP_GOAL_MVP_118_BACKLOG_ITEM_RFB_RC016_004_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-118_BACKLOG_ITEM_RFB_RC016_004.md
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/tests/e2e/incident-product-page.spec.ts
docs/S6_FAST_MVP_GOAL_MVP_118_BACKLOG_ITEM_RFB_RC016_004_2026_05_08.md
```

## Allowed scope

```text
single-label UI copy update for incident-page quick navigation link
unit/e2e assertion alignment for the updated label
no runtime logic changes
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-118_BACKLOG_ITEM_RFB_RC016_004.md
npm run test -- src/App.test.tsx
npm run build
npx playwright test tests/e2e/incident-product-page.spec.ts
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
incident navigation label change requires broader IA/copy rewrite beyond this item
frontend test command fails twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
keep historical residue untouched
```

## Evidence contract

```text
goal card validator PASS output
App.test.tsx PASS output
frontend build PASS output
incident-product-page Playwright PASS output
diff --check PASS output
closeout report with exact label delta
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no production_writeback=true
no customer_visible_output=true
no Authorization header
no Bearer token
no raw_payload
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock one follow-up backlog closeout Goal for RFB-RC016-004 or next picker-selected backlog item.
If HOLD, stop and report exact failing command and artifact.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-118 shorten ai advice nav label
stage and commit only Goal files
do not push
```
