# S6 CD-T06 Closed Context Implementation Checklist

## Document Control

- Document: `S6_CD_T06_CLOSED_CONTEXT_IMPLEMENTATION_CHECKLIST_2026_04_29`
- Date: 2026-04-29
- Ticket: `CD-T06`
- Mode: narrow implementation checklist only
- Source baseline: `CD-T06 Renderable CLOSED Case Detail Context Checklist v0.1`
- Implementation authorization: NO

## Decision

```text
CD_T06_NARROW_IMPLEMENTATION_CHECKLIST_PASS_IMPLEMENTATION_GO_REQUIRED
```

## Source Evidence

- `docs/S6_R2_PARALLEL_WORK_PACK_VF15_APT06_CDT06_SOURCE_CLOSURE_2026_04_29.md`
- `docs/S6_R1_CD_T06_CLOSED_CONTEXT_CHECKLIST_2026_04_29.md`
- External source package: `D:\产品设计\secupilot0421\visual negative\SecuPilot_Parallel_Work_Pack_VF15_APT06_CDT06_v0.1.zip`

## Narrow Scope

Future CD-T06 implementation may add only renderable CLOSED Case Detail behavior:

- `case_state = CLOSED` visual/header anchors;
- `AUD-001` through `AUD-006` readonly trail for P1/P2;
- absent write controls;
- Dialogue Dock visible with disabled input/send;
- P3 independent `p3-approval-audit-summary` guardrail.

## Candidate Allowed Files

Future implementation must prove exact files before code changes. Current candidate files are:

```text
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/src/App.css
frontend/tests/e2e/core-surface.redline-expansion.spec.ts
frontend/tests/e2e/core-surface.p3-dom-isolation.spec.ts
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

- `closed-case-banner` and `closed-state-pill[data-case-state="CLOSED"]` render.
- `AUD-001` through `AUD-006` render where P1/P2 full audit trail is allowed.
- Write controls are `not.toBeAttached()`, not only hidden by CSS.
- `dialogue-input-readonly` is an input or textarea that can satisfy disabled assertions.
- P3 renders `p3-approval-audit-summary` and does not attach `full-audit-trail`, `host-raw-evidence`, `p2-evidence-drawer`, or approval controls.

## HOLD Conditions

HOLD if implementation requires:

- backend/runtime/API/schema;
- invented audit events from UI copy;
- CSS-hidden write controls instead of physical absence;
- P3 reuse of full P1/P2 audit trail component;
- fixture/adapter/validator/`ResolvedSurfaceContext` changes;
- real data, secrets, deploy, external pilot, public endpoint, or launch.

## Non-Authorization

This checklist does not authorize implementation. It only makes CD-T06 eligible for a later exact implementation GO.

## Next Route

```text
WAIT_FOR_CD_T06_IMPLEMENTATION_GO_OR_CONTINUE_R2_DOCS_ONLY
```
