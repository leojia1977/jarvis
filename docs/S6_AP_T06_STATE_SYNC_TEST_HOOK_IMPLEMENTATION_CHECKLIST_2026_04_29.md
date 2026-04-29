# S6 AP-T06 State Sync Test Hook Implementation Checklist

## Document Control

- Document: `S6_AP_T06_STATE_SYNC_TEST_HOOK_IMPLEMENTATION_CHECKLIST_2026_04_29`
- Date: 2026-04-29
- Ticket: `AP-T06`
- Mode: narrow implementation checklist only
- Source baseline: `AP-T06 State Sync Input + Test Hook Checklist v0.1`
- Implementation authorization: NO

## Decision

```text
AP_T06_NARROW_IMPLEMENTATION_CHECKLIST_PASS_IMPLEMENTATION_GO_REQUIRED
```

## Source Evidence

- `docs/S6_R2_PARALLEL_WORK_PACK_VF15_APT06_CDT06_SOURCE_CLOSURE_2026_04_29.md`
- `docs/S6_R1_AP_T06_STATE_SYNC_INPUT_TEST_HOOK_CHECKLIST_2026_04_29.md`
- External source package: `D:\产品设计\secupilot0421\visual negative\SecuPilot_Parallel_Work_Pack_VF15_APT06_CDT06_v0.1.zip`

## Narrow Scope

Future AP-T06 implementation may add only mock/test state-sync behavior for observation-window UI migration:

- active `OBSERVATION_WINDOW` state;
- clock fast-forward does not migrate state by itself;
- mock/test state sync migrates to `PENDING_APPROVAL`;
- stale approve / dirty update static feedback anchors if exact files prove safe.

The implementation must preserve:

```text
emitStateSync is Storybook / Playwright / mock-backend helper semantics only.
No real websocket, polling, backend API, runtime protocol, or schema is defined.
```

## Candidate Allowed Files

Future implementation must prove exact files before code changes. Current candidate files are:

```text
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/src/App.css
frontend/tests/e2e/core-surface.logic-collision.spec.ts
```

Any fixture/adapter/validator/`ResolvedSurfaceContext` change requires a separate ticket.

## Required Tests

Future implementation should run at minimum:

```text
cd frontend; npm test
cd frontend; npm run build
py -3 scripts/git_preflight.py --mode pilot
```

If Playwright assertions are touched:

```text
cd frontend; npm run test:e2e
```

## Mandatory Assertions

- Observation-window banner and remaining/total anchors render.
- Approve/reject/delay/observe/detail controls are disabled during active observation window.
- Clock fast-forward alone leaves `data-case-state="OBSERVATION_WINDOW"`.
- Mock/test state sync moves to `PENDING_APPROVAL`.
- No `APPROVED_PENDING_EXECUTION` or auto-execute UI appears from expiry.

## HOLD Conditions

HOLD if implementation requires:

- frontend `setTimeout` as state authority;
- `emitStateSync` treated as real backend protocol;
- backend/runtime/API/schema;
- fixture/adapter/validator/`ResolvedSurfaceContext` changes;
- observation expiry to `APPROVED_PENDING_EXECUTION`;
- invented `AUD-004` from UI copy;
- real data, secrets, deploy, external pilot, public endpoint, or launch.

## Non-Authorization

This checklist does not authorize implementation. It only makes AP-T06 eligible for a later exact implementation GO.

## Next Route

```text
WAIT_FOR_AP_T06_IMPLEMENTATION_GO_OR_CONTINUE_R2_DOCS_ONLY
```
