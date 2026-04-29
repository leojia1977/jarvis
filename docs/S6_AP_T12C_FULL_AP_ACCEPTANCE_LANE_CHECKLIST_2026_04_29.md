# S6 AP-T12C Full AP Acceptance Lane Checklist 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Document | `S6_AP_T12C_FULL_AP_ACCEPTANCE_LANE_CHECKLIST_2026_04_29` |
| Ticket | `AP-T12C` |
| Parent ticket | `AP-T12` |
| Jira parent candidate | `SCRUM-74` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `53ec876` |
| Mode | Docs-only checklist |
| Implementation authorization | NO |
| Jira Done transition authorization | NO |

## 2. Checklist Decision

```text
AP_T12C_ACCEPTANCE_LANE_CHECKLIST_OPENED
UNIT_COMPONENT_AP_EVIDENCE_READY
STORYBOOK_PLAYWRIGHT_FULL_ACCEPTANCE_LANE_IMPLEMENTATION_GO_REQUIRED
AP_T12_PARENT_DONE_HOLD
```

`AP-T12C` is the next implementation-adjacent AP acceptance candidate, but this
checklist does not grant implementation GO. Current unit/component evidence is
strong enough to index as ready. Full AP acceptance still needs an exact
Storybook / Playwright acceptance lane or an explicit no-code rescope decision.

## 3. Source Inputs

| Source | Use |
| --- | --- |
| `docs\S6_AP_T12_FULL_ACCEPTANCE_RECHECK_AND_PARENT_EPIC_CLOSURE_REVIEW_2026_04_29.md` | Confirms `AP-T12` remains HOLD and `AP-T12C` is the next candidate. |
| `docs\S6_AP_T12_ACCEPTANCE_SCOPE_DECISION_2026_04_29.md` | Defines `AP-T12C` as the Playwright / Storybook acceptance lane candidate. |
| `docs\S6_AP_T12A_ACCEPTANCE_EVIDENCE_INDEX_CHECKLIST_2026_04_29.md` | Provides the prior AP evidence index, now superseded where it still described `AP-T02` as source-missing. |
| `docs\S6_AP_T02_P0_READONLY_APPROVAL_TEST_HARNESS_CLOSEOUT_2026_04_29.md` | Closes the prior P0 readonly approval source blocker via test harness only. |
| `docs\S6_AP_T06_STATE_SYNC_TEST_HOOK_CLOSEOUT_2026_04_29.md` | Closes full AP-T06 within mock/test state-sync boundaries. |
| `docs\S6_AP_T09_AUDIT_EMPTY_UNAVAILABLE_SOURCE_CLOSEOUT_2026_04_29.md` | Closes AP-T09 audit empty / unavailable source-bound UI. |
| `docs\S6_AP_T11_T12_ACCEPTANCE_RECONCILIATION_2026_04_29.md` | Confirms full `AP-T12` remains acceptance-scoped and must not be inferred from slices. |

## 4. Existing Acceptance Evidence

### Unit / Component Evidence

`frontend/src/App.test.tsx` already contains AP-focused evidence for:

- P2 approval shell / route guard with no state mutation;
- approve / reject / delay / observe CTA boundaries with disabled final mutation;
- AP-T09 audit empty / unavailable states without coverage upgrade framing;
- AP-T02 P0 readonly approval from governed test harness only;
- AP-T07 approved-pending execution lock;
- AP-T06 observation-window state sync where clock fast-forward is not authority;
- AP-T11A static no-mutation boundary;
- non-P2 approval route redirect and URL/storage authority rejection;
- P2 Inbox navigation-only approval entry.

This lane is ready as evidence, but it is not enough by itself to mark full
`AP-T12` Done because `AP-T12` is a full AP acceptance-suite row.

### Storybook Evidence

`frontend/src/secupilot/surface/storybook/CoreSurfaceStories.stories.tsx`
currently exposes:

- `P2 / Approval / Pending Review`;
- `P2 / Approval / Observation Window Active`;
- `P2 / Approval / Window Expired Return Pending`;
- `P2 / Approval / Terminal Lock`.

These stories cover the main AP visual phases, but they do not yet prove a full
AP-T12 acceptance lane for P0 readonly harness behavior, AP-T09 empty /
unavailable source states, AP-T06 state-sync hook behavior, and AP-T11 static
no-mutation boundaries as a named acceptance set.

### Playwright Evidence

Current Playwright tests cover:

- core phase seed transitions across P1 / P2 / terminal / P3;
- permission guards against URL / browser-storage role or coverage injection;
- invalid approval deep-link guard;
- P3 DOM isolation and approval-control absence;
- redline renderability for missing signal, stale approve, resolver degradation,
  and P3 manager summary.

They are useful AP-adjacent evidence, but they are not a complete AP-T12 suite.

## 5. Gaps Before Full AP-T12 Done

| Gap | Current status | Required next action |
| --- | --- | --- |
| Named AP acceptance lane | Missing | Create an exact Storybook / Playwright acceptance lane or explicitly rescope `AP-T12`. |
| P0 readonly approval in product-like flow | Not authorized | Current evidence is test-harness-only; do not promote it to product route or Storybook without separate GO. |
| AP-T09 in Storybook / Playwright | Not fully proven | Future lane may add source-bound empty / unavailable assertions without product source changes. |
| AP-T06 state-sync in Storybook / Playwright | Not fully proven | Future lane may use mock/test `emitStateSync` only; no real backend protocol. |
| Parent AP closure | HOLD | Keep `SCRUM-43` open until `SCRUM-74 AP-T12` resolves or is explicitly rescoped. |

## 6. Candidate Future Implementation Envelope

If Jarvis later grants `AP-T12C implementation GO`, the narrowest acceptable
scope is acceptance-only:

```text
Allowed candidate files:
- frontend/src/secupilot/surface/storybook/CoreSurfaceStories.stories.tsx
- frontend/tests/e2e/core-surface.logic-collision.spec.ts
- frontend/tests/e2e/core-surface.permission-guards.spec.ts
- frontend/tests/e2e/core-surface.redline-expansion.spec.ts
- or one new frontend/tests/e2e/approval.acceptance.spec.ts if the checklist
  names it explicitly

Candidate commands:
- npm test
- npm run build
- npm run build-storybook
- npm run test:e2e
```

Product source files such as `frontend/src/App.tsx`, `frontend/src/App.css`,
fixture files, validators, providers, backend files, runtime files, API files,
schema files, and dependency files are not included in the default AP-T12C
acceptance lane. If any implementation requires them, HOLD and request a new
exact ticket.

## 7. Implementation GO Discussion

| Candidate | Why YES | Why NO / HOLD |
| --- | --- | --- |
| `AP-T12C` Storybook / Playwright acceptance lane | It is exact, acceptance-only, high leverage for closing `AP-T12`, and can avoid product behavior changes. | It still needs explicit implementation GO because it may add Storybook or Playwright files and must prove exact assertions first. |
| `AP-T12` full ticket Done | AP child tickets except AP-T12 are Jira Done. | Do not mark Done yet; full acceptance lane is not closed. |
| `SCRUM-43 [AP]` parent closure | Parent closure becomes possible after AP-T12 closes or is rescoped. | HOLD now because `SCRUM-74 AP-T12` remains To Do. |
| P0 readonly production route | Could provide stronger end-to-end evidence later. | Not authorized by AP-T02; current path is test-harness-only. |

## 8. HOLD Conditions

HOLD immediately if any future AP-T12C work requires:

- product behavior changes outside acceptance coverage;
- `frontend/src/App.tsx` or `frontend/src/App.css` without a new exact ticket;
- fixture, adapter, validator, provider, or `ResolvedSurfaceContext` changes;
- backend/runtime/API/schema work;
- URL/storage authority;
- real data, anonymized real data, secrets, deploy, public endpoint, external
  pilot, or launch;
- Jira Done transition for `SCRUM-74` or parent `SCRUM-43` before acceptance
  closure or explicit rescope.

## 9. Next Route

```text
WAIT_FOR_AP_T12C_IMPLEMENTATION_GO_OR_AP_T12_RESCOPE_OR_PARENT_CLOSURE_REVIEW_GO
```

