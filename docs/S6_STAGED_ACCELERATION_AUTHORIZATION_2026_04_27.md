# S6 Staged Acceleration Authorization 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Staged Acceleration Authorization 2026-04-27 |
| Status | STAGED_ACCELERATION_AUTHORIZED_WITH_BOUNDS |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Parent matrix | `docs\S6_SPRINT1_4_AUTOMATION_ACCELERATION_MATRIX_2026_04_27.md` |
| Active runner | `secupilot-bounded-backend-automation-runner` |
| Route | `OPEN_STAGED_ACCELERATION_AUTHORIZATION` |

This record captures Jarvis's staged authorization for selected Sprint 1-4 acceleration work.

It does not authorize real data, secrets, deployment, public endpoint activation, external pilot, backend/runtime/API/schema changes, broad P2 approval implementation, broad P3 manager/audit implementation, or mandatory external-review bypass.

## 2. Authorization Summary

Decision:

```text
STAGED_ACCELERATION_AUTHORIZED_WITH_BOUNDS
```

Authorized lanes:

1. `P2/P3 checklist-only GO`
2. `Visual Skeleton GO`
3. `Patch-Isolation Checklist GO`

## 3. P2/P3 Checklist-Only GO

Authorized checklist-only tickets:

```text
AP-T10
AP-T01
CD-T05
MV-T01
```

Allowed action:

```text
launch/readiness checklist only
```

Implementation remains unauthorized unless a later checklist proves all of:

- exact allowed files;
- exact test commands;
- no authority ambiguity;
- no PRD / Model Contract / D-02 / visual-frame conflict;
- external review condition resolved where required;
- explicit later implementation GO if the checklist requires it.

## 4. Visual Skeleton GO

Authorized skeleton candidates:

```text
GS-T04
IN-T02
IN-T04
EP-T02
EP-T03
SH-T01
CH-T01
```

Allowed skeleton implementation scope:

- semantic skeleton;
- test ids;
- accessibility landmarks;
- layout slots;
- regression tests;
- no final visual styling;
- no final visual PASS;
- no product-scope invention from missing visual frames.

Each skeleton ticket must still have its own launch checklist. Skeleton implementation is allowed only if that checklist returns `GO`.

## 5. Patch-Isolation Checklist GO

Authorized patch-isolation checklists:

```text
AP-T10
AP-T01
```

Implementation remains HOLD until the isolated checklist returns a narrow `GO` and proves:

- exact files;
- exact test command;
- no product/contract conflict;
- no authority ambiguity;
- external review condition clear.

Only one patch-isolation implementation ticket may be active at a time.

## 6. Explicit Non-Authorizations

Still not authorized:

```text
real data
secrets
deploy / public endpoint
external pilot
backend/runtime/API/schema
broad P2 approval implementation
broad P3 manager/audit implementation
```

Also not authorized:

- final visual PASS before visual frames are delivered;
- blocked/non-ready ticket Done transitions in Jira;
- route handoff beyond ticket scope;
- fixture registry, adapter, validator, or `ResolvedSurfaceContext` changes;
- P2/P3 authority changes without later explicit authority-resolution evidence.

## 7. Runner Order

After RQ-04 completes or HOLDs, the runner may proceed in this staged order:

1. `GS-T04-SKELETON-LAUNCH`.
2. `IN-T02-SKELETON-LAUNCH`.
3. `IN-T04-SKELETON-LAUNCH`.
4. `EP-T02-SKELETON-LAUNCH`.
5. `EP-T03-SKELETON-LAUNCH`.
6. `SH-T01-SKELETON-LAUNCH`.
7. `CH-T01-SKELETON-LAUNCH`.
8. `AP-T10-PATCH-ISOLATION-CHECKLIST`.
9. `AP-T01-PATCH-ISOLATION-CHECKLIST`.
10. `CD-T05-P2P3-READINESS-CHECKLIST`.
11. `MV-T01-P2P3-READINESS-CHECKLIST`.
12. `JIRA-PARITY-SAFE-SYNC` for already repo-closed rows.

If any item returns HOLD, record the HOLD and continue only to the next item whose dependencies and authority gates are still satisfied.

## 8. HOLD Conditions

HOLD immediately if:

- allowed files are missing or insufficient;
- test command is missing or insufficient;
- visual frame ambiguity requires product/design interpretation;
- implementation needs final visual styling;
- P2/P3 authority ambiguity appears;
- AP/D-02 state semantics conflict;
- backend/runtime/API/schema is needed;
- fixture registry, adapter, validator, or `ResolvedSurfaceContext` changes are needed;
- real data, secrets, deploy, public endpoint, or external pilot is requested;
- mandatory external-review trigger fires;
- tests/build fail and cannot be corrected inside the exact ticket scope.

## 9. Next Safe Action

Next safe automation action:

```text
CONTINUE_RQ04_THEN_APPLY_STAGED_ACCELERATION_AUTHORIZATION
```
