# S6 AP-T09 Audit Empty / Unavailable Source Implementation Checklist

## Document Control

- Document: `S6_AP_T09_AUDIT_EMPTY_UNAVAILABLE_SOURCE_IMPLEMENTATION_CHECKLIST_2026_04_29`
- Date: 2026-04-29
- Ticket: `AP-T09`
- Mode: narrow implementation checklist only
- Source baseline: `VF-15 v0.1`
- Implementation authorization: NO

## Decision

```text
AP_T09_NARROW_IMPLEMENTATION_CHECKLIST_PASS_IMPLEMENTATION_GO_REQUIRED
```

## Source Evidence

- `docs/S6_R2_PARALLEL_WORK_PACK_VF15_APT06_CDT06_SOURCE_CLOSURE_2026_04_29.md`
- `docs/S6_R1_AP_T09_VF15_AUDIT_EMPTY_UNAVAILABLE_SOURCE_CHECKLIST_2026_04_29.md`
- External source package: `D:\产品设计\secupilot0421\visual negative\SecuPilot_Parallel_Work_Pack_VF15_APT06_CDT06_v0.1.zip`

## Narrow Scope

Future AP-T09 implementation may add only static, source-bound rendering for:

- `approval-audit-empty-state`;
- `approval-audit-unavailable-state`;
- `audit-source-unavailable-notice[data-message-source="ui_messages"]`;
- source/guard anchors proving `activeContext.audit_trail` and `source-data-availability` boundaries;
- tests proving no invented audit rows and no coverage-upgrade framing.

## Candidate Allowed Files

Future implementation must prove exact files before code changes. Current candidate files are:

```text
frontend/src/App.tsx
frontend/src/App.test.tsx
frontend/src/App.css
frontend/tests/e2e/core-surface.redline-expansion.spec.ts
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

- Empty audit source renders no `AUD-*` event rows.
- Unavailable source uses `data-message-source="ui_messages"`.
- Neither state renders `coverage-upgrade-prompt`.
- Neither state renders `approval-audit-source-invention`.
- Neither state invents `AUD-003`, `AUD-004`, or `AUD-005`.

## HOLD Conditions

HOLD if implementation requires:

- new audit fields;
- fixture/adapter/validator/`ResolvedSurfaceContext` changes;
- backend/runtime/API/schema;
- treating empty/unavailable as coverage insufficiency;
- copy not sourced from governed source / `ui_messages`;
- real data, secrets, deploy, external pilot, public endpoint, or launch.

## Non-Authorization

This checklist does not authorize implementation. It only makes AP-T09 eligible for a later exact implementation GO.

## Next Route

```text
WAIT_FOR_AP_T09_IMPLEMENTATION_GO_OR_CONTINUE_R2_DOCS_ONLY
```
