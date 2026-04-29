# S6 AP-T12C Full AP Acceptance Lane Closeout 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Document | `S6_AP_T12C_FULL_AP_ACCEPTANCE_LANE_CLOSEOUT_2026_04_29` |
| Ticket | `AP-T12C` |
| Parent ticket | `AP-T12` |
| Jira parent candidate | `SCRUM-74` |
| Branch | `codex/s3-a-runtime` |
| Implementation mode | Acceptance-only Storybook / Playwright lane |
| Product behavior changes | NO |
| Backend / runtime / API / schema | NO |
| Fixture / adapter / validator / `ResolvedSurfaceContext` changes | NO |
| Real data / secrets / deploy / external pilot / launch | NO |

## 2. Closeout Decision

```text
AP_T12C_ACCEPTANCE_LANE_IMPLEMENTED_GATE_PASS
AP_T12_FULL_ACCEPTANCE_SCOPE_JIRA_SYNCED_DONE_AS_SCRUM_74
AP_PARENT_CLOSURE_REVIEW_STILL_REQUIRED
```

`AP-T12C` implements the missing named AP acceptance lane without changing
product behavior. The lane combines Storybook AP route states with Playwright
AP acceptance assertions and preserves the bounded evidence hierarchy for
unit/component-only AP evidence.

## 3. Changed Files

| File | Purpose |
| --- | --- |
| `frontend/src/secupilot/surface/storybook/CoreSurfaceStories.stories.tsx` | Adds AP-T12C route-state stories for P2 pending, observation window, window-expired, and terminal lock. |
| `frontend/tests/e2e/approval.acceptance.spec.ts` | Adds AP-T12C Playwright acceptance lane for P2 shell/no-mutation, mock state-sync observation-window exit, and URL/storage authority rejection. |
| `docs/S6_AP_T12C_FULL_AP_ACCEPTANCE_LANE_CLOSEOUT_2026_04_29.md` | Records this closeout. |
| `docs/S6_JIRA_SYNC_AP_T12_2026_04_29.md` | Records exact Jira sync for `SCRUM-74 [AP-T12]`. |
| `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md` | Route update. |
| `docs/HANDOFF.md` | Handoff update. |
| `docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md` | Progress board update. |

## 4. Acceptance Coverage Added

### Storybook

Added named AP-T12C acceptance route stories:

- `AP-T12C / Acceptance / P2 Pending Route`;
- `AP-T12C / Acceptance / Observation Window Route`;
- `AP-T12C / Acceptance / Window Expired Route`;
- `AP-T12C / Acceptance / Terminal Lock Route`.

### Playwright

Added `frontend/tests/e2e/approval.acceptance.spec.ts` with:

- P2 approval route shell stays source-bound to `ResolvedSurfaceContext`;
- approval CTA boundary remains `data-state-mutation="none"`;
- approve strong-confirm and observe configuration shells cannot submit state;
- observation-window exit requires mock `STATE_SYNC`;
- clock / timer authority remains absent;
- URL and storage cannot create AP role, AR status, or `ActionMode` authority.

## 5. Evidence Boundary

This closeout intentionally does not promote unit/component-only evidence into a
product route:

- `AP-T02` P0 readonly approval remains test-harness-only and does not create a
  production P0 `/approval` route entry.
- `AP-T09` audit empty / unavailable source behavior remains covered by
  unit/component evidence and the source-bound AP route implementation; no new
  fixture or product source path was invented for e2e.
- `AP-T06` uses mock/test `STATE_SYNC` helper semantics only; no real websocket,
  polling, backend protocol, runtime endpoint, or schema is introduced.

## 6. Gate Evidence

```text
npm run test:e2e -- approval.acceptance.spec.ts: PASS / 3 tests
npm test -- --run App.test.tsx: PASS / 59 tests
npm test: PASS / 96 tests
npm run build: PASS
npm run build-storybook: PASS
npm run test:e2e: PASS / 13 tests
```

Final deterministic repo gate and Claude Code review are recorded in the final
automation response for this ticket.

## 6.1 Claude Code Focused Review

```text
VERDICT: PASS_WITH_FINDINGS
BLOCKING FINDINGS: none
```

Non-blocking notes:

- the URL/storage rejection e2e test is intentionally coupled to the current
  default fixture role `P1`;
- Storybook route stories use the existing synchronous `resetStoryRoute`
  pattern and should not be treated as equivalent to Playwright navigation;
- gate evidence is recorded from local command output and deterministic
  preflight;
- `emitMockStateSync` remains a mock/test helper only and does not introduce a
  real backend protocol.

## 7. Jira Handling

`SCRUM-74 [AP-T12]` is the exact Jira mapping for this acceptance lane.
It received AP-T12C closeout evidence and was transitioned from `待办` to
`已完成` after read-back verification.

`SCRUM-43 [AP]` parent epic remains a separate closure review. Do not transition
the AP parent from this closeout without a distinct parent closure action.

## 8. Non-Authorization

This record does not authorize:

- product behavior changes;
- `frontend/src/App.tsx` or `frontend/src/App.css`;
- fixture, adapter, validator, provider, or `ResolvedSurfaceContext` changes;
- backend/runtime/API/schema;
- real data or anonymized real data;
- secrets;
- deploy, public endpoint, external pilot, or launch;
- AP parent epic closure.

## 9. Next Route

```text
OPEN_AP_PARENT_CLOSURE_REVIEW_OR_NEXT_EXACT_LOW_RISK_BURN_POOL
```
