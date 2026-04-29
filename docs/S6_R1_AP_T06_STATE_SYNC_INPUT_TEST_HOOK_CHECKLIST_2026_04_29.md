# S6 R1 AP-T06 State-Sync Input And Test-Hook Checklist

## Document Control

- Document: `S6_R1_AP_T06_STATE_SYNC_INPUT_TEST_HOOK_CHECKLIST_2026_04_29`
- Date: 2026-04-29
- Lane: `R1-A / AP-T06`
- Mode: docs-only checklist / source lane
- Implementation authorization: NO

## Decision

```text
R1_AP_T06_HOLD_PENDING_STATE_SYNC_SOURCE_DELIVERY
IMPLEMENTATION_GO_REQUIRED_BEFORE_CODE
```

## Source Evidence

- `docs/S6_AP_T06_STATE_SYNC_HARNESS_SOURCE_REQUEST_2026_04_29.md`
- `docs/S6_AP_T06_FULL_COUNTDOWN_STATE_SYNC_BLOCKER_REFRESH_2026_04_28.md`
- `docs/S6_REMAINING_SCOPE_TRIAGE_AND_BATCH_LAUNCH_PLAN_2026_04_29.md`
- `AP-T06A / SCRUM-65` is closed only as the static observation-window readonly skeleton split.

## Checklist

| Check | Result | Evidence |
| --- | --- | --- |
| Is the static AP-T06A slice closed? | YES | `AP-T06A / SCRUM-65` Done |
| Is full AP-T06 closed? | NO | Parent `SCRUM-64` remains open |
| Is an exact state-sync input contract available? | NO | Source request remains open |
| Is an exact governed `emitStateSync` or equivalent test hook available? | NO | Source request remains open |
| Can frontend timer display become state authority? | NO | Timer remains presentation-only |
| Are exact implementation files/tests proven? | NO | Must wait for source delivery |

## Required Future Source

Full AP-T06 may only relaunch when a governed source defines:

- input authority for state migration into and out of `OBSERVATION_WINDOW`;
- display-vs-authority rule for timer rendering;
- exact test-only harness semantics, if any;
- exact allowed files and test command.

## Result

AP-T06 remains HOLD. The current repo only supports static readonly observation-window presentation. It does not provide authority for state migration, countdown expiry, or backend `STATE_SYNC`.

## Non-Authorization

This checklist does not authorize implementation, frontend source changes, Playwright changes, backend/runtime/API/schema, fixture/adapter/validator changes, `ResolvedSurfaceContext` changes, real data, secrets, deploy, public endpoint, external pilot, Jira Done transition, or launch.

## Next Route

```text
WAIT_FOR_AP_T06_STATE_SYNC_SOURCE_DELIVERY
```
