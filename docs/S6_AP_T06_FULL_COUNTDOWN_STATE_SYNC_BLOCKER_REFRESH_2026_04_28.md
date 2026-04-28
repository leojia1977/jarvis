# S6 AP-T06 Full Countdown / State-Sync Blocker Refresh 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T06` |
| Title | Full countdown / state-sync blocker refresh |
| Status | `AP_T06A_CLOSED_FULL_COUNTDOWN_STATE_SYNC_HOLD_CONFIRMED` |
| Date | 2026-04-28 |
| Automation | `SecuPilot Autonomous Ops Loop` |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Prior readiness | `docs\S6_AP_T06_OBSERVATION_WINDOW_READINESS_CHECKLIST_2026_04_28.md` |
| Related split closeout | `docs\S6_AP_T06A_STATIC_OBSERVATION_WINDOW_SKELETON_CLOSEOUT_2026_04_28.md` |
| Jira | `SCRUM-64` / not Done |

This refresh rechecks the parent `AP-T06` ticket after the static `AP-T06A`
split closed. It is docs-only and does not authorize implementation.

## 2. Decision

```text
AP_T06_BLOCKER_REFRESH_STATIC_SLICE_CLOSED
AP_T06_FULL_COUNTDOWN_STATE_SYNC_HOLD_CONFIRMED
```

`AP-T06A` is complete and no longer a blocker. Full `AP-T06` remains HOLD
because the missing authority is still the same:

- no exact frontend state-sync input contract for material migration;
- no exact `emitStateSync` or equivalent governed test hook;
- no governed rule that the frontend timer display is presentation-only and
  cannot trigger status migration;
- no safe renderable path for countdown/state-sync assertions without
  fixture/adapter/validator or `ResolvedSurfaceContext` expansion.

## 3. Evidence Checked

| Evidence | Result |
| --- | --- |
| `docs\S6_AP_T06_OBSERVATION_WINDOW_READINESS_CHECKLIST_2026_04_28.md` | Split remains explicit: `AP_T06A_STATIC_READONLY_OBSERVATION_WINDOW_SKELETON_IMPLEMENTATION_GO` and `AP_T06_FULL_COUNTDOWN_STATE_SYNC_HOLD`. |
| `docs\S6_AP_T06A_STATIC_OBSERVATION_WINDOW_SKELETON_CLOSEOUT_2026_04_28.md` | Static slice is closed as `SCRUM-65`; parent `SCRUM-64` was intentionally kept open. |
| `docs\S6_VISUAL_BASELINE_VF03_VF11_VF12_VF13_RECONCILIATION_2026_04_28.md` | `VF-11` is accepted only as static readonly skeleton input, not as countdown/state-sync authority. |
| `frontend/src/App.tsx` | Observation-window boundary still exposes `data-state-sync="not-implemented"`, `data-state-migration="none"`, and `data-timer-authority="none"`. |
| `frontend/src/App.test.tsx` | Existing tests assert the observation-window surface remains static/read-only and non-mutating. |
| `docs\S6_AP_T11_T12_READINESS_DECOMPOSITION_2026_04_28.md` | Downstream AP acceptance/state-transition work still treats full `AP-T06` as a blocking dependency. |

## 4. Why Full AP-T06 Cannot Implement Yet

`AP-T06` is not just a visible countdown label. A later exact checklist must
prove all of the following before implementation can start:

```text
exact state-sync input contract is named
exact display-vs-authority rule is governed
exact test hook exists for material migration assertions
countdown assertions do not rely on client clock as authority
no backend/runtime/API/schema dependency exists
no fixture/adapter/validator/ResolvedSurfaceContext change is needed
exact allowed files and exact tests are named
```

Current repo evidence does not yet satisfy that bar. The existing static
readonly boundary is intentionally marked `not-implemented` for state sync, and
changing that marker now would invent behavior rather than implement governed
scope.

## 5. Jira / Tracker Handling

Do not mark `SCRUM-64` Done.

Allowed Jira action, if credentials are visible:

```text
Add non-transition HOLD comment only:
AP-T06A static slice is closed; full AP-T06 countdown/state-sync remains HOLD
pending exact state-sync input contract, test hook, and non-authoritative timer
rule.
```

No Jira sync was attempted by this docs-only blocker refresh.

## 6. Next Route

```text
OPEN_AP_T02_MV_T02_RENDERABLE_AUTHORITY_CONTEXT_BLOCKER_REFRESH
```

Reason:

- `AP-T06` remains HOLD with no safe implementation split beyond the already
  closed `AP-T06A`.
- The extended bounded queue already lists `AP-T02` / `MV-T02` as the next
  authority/blocker refresh after `AP-T06`.

## 7. Non-Authorization

This refresh does not authorize:

- `AP-T06` implementation;
- countdown-driven state migration;
- `setTimeout` or client-clock authority;
- backend `STATE_SYNC`;
- Playwright time travel as product behavior;
- fixture/adapter/validator/`ResolvedSurfaceContext` changes;
- backend/runtime/API/schema changes;
- visual PASS claim;
- Jira Done transition;
- real data, secrets, deploy, public endpoint, or external pilot.
