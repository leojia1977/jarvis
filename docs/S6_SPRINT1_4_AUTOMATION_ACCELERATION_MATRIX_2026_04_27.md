# S6 Sprint 1-4 Automation Acceleration Matrix 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Sprint 1-4 Automation Acceleration Matrix 2026-04-27 |
| Status | ACCELERATION_MATRIX_ACTIVE_WITH_QUALITY_GATES |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Active runner | `secupilot-bounded-backend-automation-runner` |
| Predecessor queue | `docs\S6_SPRINT1_RQ04_EXACT_BOUNDED_RUNNER_QUEUE_2026_04_27.md` |
| Route | `OPEN_SPRINT1_4_AUTOMATION_ACCELERATION_MATRIX` |

This matrix records Jarvis's Sprint 1-4 batch authorization and converts it into quality-preserving automation lanes.

It accelerates ticket launch/reconciliation/implementation/review/sync/commit loops, but it does not relax product authority, safety gates, test requirements, external-review triggers, or launch/deploy prohibitions.

## 2. Jarvis Batch Authorization

Jarvis authorized Sprint 1-4 automation acceleration under quality-preserving gates:

1. `Normal-Batch GO`
2. `Visual-Dependent Skeleton GO`
3. `Patch-Gate Isolation GO`
4. `Regression Lane GO`
5. `Jira/Tracker Sync GO`

Universal HOLD conditions remain:

```text
scope expansion
missing exact files
failed tests/build
visual semantic ambiguity
patch-gate conflict
P2/P3 authority change
backend/runtime/API/schema need
fixture/adapter/validator change
real data
secrets
deploy
public endpoint
external pilot
mandatory external review trigger
```

## 3. Lane Definitions

### Lane A - Normal-Batch Automation

Allowed when all are true:

- `Design Dependency = none`
- `Patch Gate Impact = none`
- `External Review Required != mandatory`
- no P2/P3 authority change
- no backend/runtime/API/schema
- exact allowed files and test command exist

Allowed actions:

```text
launch checklist -> reconcile or implement -> gate -> Claude Code review -> Jira sync -> stage/commit/push
```

### Lane B - Visual-Dependent Skeleton

Allowed when:

- product semantics are frozen enough to avoid invention;
- implementation can be limited to semantic skeleton, test ids, accessibility landmarks, layout slots, and regression tests;
- final visual styling / visual PASS is deferred until the required frame exists.

Forbidden in this lane:

- final visual styling claims;
- visual PASS;
- inventing product semantics from missing frames;
- P2/P3 authority change.

### Lane C - Patch-Gate Isolation

Allowed when:

- a patch-gate possible ticket has high leverage;
- an isolated checklist proves exact files, exact tests, no product/contract conflict, and no required external-review blocker;
- only one implementation ticket is active in the patch-gate isolation lane at a time.

Forbidden in this lane:

- mixing patch-gate tickets into normal sprint burn-down;
- batch implementation across multiple patch-gate rows;
- bypassing mandatory external review.

### Lane D - Regression Lane

Allowed immediately after each PASS implementation:

- Storybook regression follow-up inside exact files;
- Playwright regression follow-up inside exact files;
- unit/component regression tests inside exact files;
- no new product scope.

### Lane E - Jira / Tracker Sync

Allowed only for:

- PASS implementation tickets;
- no-code reconciled PASS tickets;
- already repo-closed rows explicitly identified as safe for parity sync.

Forbidden:

- marking blocked, visual-missing, P2/P3-ratification-missing, patch-conflicted, or non-ready tickets Done.

## 4. Current Sprint 1-4 Lane Map

### Immediate Lane A Queue

| Priority | Ticket | Sprint | Reason |
| --- | --- | --- | --- |
| 1 | `EP-T05` | Sprint 1 | Depends only on closed `EP-T01`; no visual dependency; no patch gate; no external review required by tracker. |
| 2 | `SH-T05` | Sprint 3A | Depends only on closed `SH-T03`; no visual dependency; no patch gate; no external review required by tracker. |
| 3 | `SH-T07` | Sprint 3A | May start only after `SH-T05` closeout; limited to write CTA absence/disablement. |

Current active queue remains:

```text
docs/S6_SPRINT1_RQ04_EXACT_BOUNDED_RUNNER_QUEUE_2026_04_27.md
```

### Lane B Visual Skeleton Candidates

These may be opened as skeleton-only checklists. Implementation is allowed only if the ticket checklist proves semantic freeze and exact files/tests.

| Priority | Ticket | Sprint | Skeleton-only scope |
| --- | --- | --- | --- |
| 1 | `GS-T04` | Sprint 1 | Expert-mode entry skeleton / disabled affordance semantics only; no final visual styling. |
| 2 | `IN-T02` | Sprint 1 | P3 read-only inbox variant skeleton only; no P3 authority expansion. |
| 3 | `IN-T04` | Sprint 1 | P1 escalation/close-request entry skeleton only; no P2 approval or close execution. |
| 4 | `EP-T02` | Sprint 1 | Inferred-node weakening slot/test ids only; no final visual treatment until `VF-10`. |
| 5 | `EP-T03` | Sprint 1 | L1 lineage degradation semantics/test ids only; no final visual treatment until `VF-10`. |
| 6 | `SH-T01` | Sprint 3A | Historical list item skeleton only after `SH-T03`; no final list styling until `HF-SH-01` / `VF-08`. |
| 7 | `CH-T01` | Sprint 4 | Coverage & Health page skeleton only; no final visual styling until `VF-01`. |

P3-heavy visual work remains checklist-first only until ratification evidence is explicit:

| Ticket | Reason |
| --- | --- |
| `CD-T05` | P3 executive summary authority and `VF-07`; skeleton may be considered only after P3 contract evidence is explicit. |
| `MV-T01` | P3 Manager View authority and `VF-06`; skeleton may be considered only after P3 contract evidence is explicit. |

### Lane C Patch-Gate Isolation Candidates

Checklist creation is allowed. Implementation is one-at-a-time only if the isolated checklist proves exact files, exact test command, no product/contract conflict, and no mandatory external-review blocker.

| Ticket | Sprint | Isolation note |
| --- | --- | --- |
| `AP-T10` | Sprint 2 | High leverage state badge/pill mapping; P2 authority gate remains active. |
| `AP-T01` | Sprint 2 | Approval route guard; P2 authority gate remains active. |
| `CD-T06` | Sprint 1 | State header is patch-gate possible and depends on `AP-T10`; HOLD until dependency resolves. |
| `CH-T03` | Sprint 4 | `ui_messages` hard-constraint copy; depends on `CH-T01`. |
| `MV-T04` | Sprint 3B | P3 approval audit summary; P3 authority and visual frame gates remain active. |
| `SH-T08` | Sprint 3A | P3 approval-audit source/data availability; depends on `SH-T05` and `AP-T08`. |

### Lane D Regression Follow-Ups

Open automatically only after dependencies close:

| Ticket | Opens after |
| --- | --- |
| `GS-T05` | `GS-T04` skeleton/implementation closeout |
| `IN-T06` | `IN-T03` and `IN-T04` closeout |
| `CD-T07` | `CD-T05` and `CD-T06` closeout |
| `EP-T06` | `EP-T02`, `EP-T03`, and `EP-T05` closeout |
| `SH-T09` | `SH-T01`, `SH-T02`, `SH-T05`, `SH-T06`, `SH-T07`, and `SH-T08` closeout |
| `CH-T04` | `CH-T01`, `CH-T02`, and `CH-T03` closeout |
| `MV-T05` | `MV-T01`, `MV-T02`, `MV-T03`, and `MV-T04` closeout |

### Lane E Jira / Tracker Parity

Allowed immediate parity sync candidates from RQ-01:

```text
GS-T01
GS-T02
GS-T03
IN-T05
CD-T03
EP-T01
```

No other ticket may be marked Done unless its repo closeout is PASS or no-code reconciled PASS.

## 5. Sprint-by-Sprint Acceleration Plan

### Sprint 1 - P1 Case Detail / Evidence

Run now:

```text
EP-T05
```

Then skeleton lane:

```text
GS-T04
IN-T02
IN-T04
EP-T02
EP-T03
```

Then regression:

```text
GS-T05
EP-T06
```

Still gated:

```text
CD-T05
CD-T06
CD-T07
IN-T03
IN-T06
```

### Sprint 2 - P2 Approval Surface

Open checklist-first:

```text
AP-T10
AP-T01
```

Do not implement P2 authority-changing work unless the isolated checklist proves exact files/tests, no D-02 conflict, no authority ambiguity, and external-review requirements are satisfied.

### Sprint 3A - Search / History

Run now:

```text
SH-T05
```

Then:

```text
SH-T07
SH-T01 skeleton
```

Still gated:

```text
SH-T02
SH-T06
SH-T08
SH-T09
```

### Sprint 3B - P3 Manager View

Checklist-first only until P3 contract evidence is explicit:

```text
MV-T01
```

Implementation remains HOLD if it changes P3 authority, approval audit semantics, route handoff, or manager summary contract.

### Sprint 4 - Coverage & Health / Hardening

Skeleton lane:

```text
CH-T01
```

Patch isolation later:

```text
CH-T03
```

Regression lane:

```text
CH-T04
cross-surface regression follow-ups after each PASS implementation
```

## 6. Runner Queue After RQ-04

After RQ-04 completes or HOLDs, the runner may continue in this order:

1. `JIRA-PARITY-SAFE-SYNC` for RQ-01 already repo-closed rows.
2. `GS-T04-SKELETON-LAUNCH`.
3. `IN-T02-SKELETON-LAUNCH`.
4. `IN-T04-SKELETON-LAUNCH`.
5. `EP-T02-SKELETON-LAUNCH`.
6. `EP-T03-SKELETON-LAUNCH`.
7. `SH-T01-SKELETON-LAUNCH`.
8. `AP-T10-PATCH-ISOLATION-CHECKLIST`.
9. `AP-T01-PATCH-ISOLATION-CHECKLIST`.
10. `CH-T01-SKELETON-LAUNCH`.

Each launch checklist must decide independently:

```text
GO
RECONCILED_GATE_PASS_NO_CODE
IMPLEMENTATION_HOLD
HOLD_FOR_VISUAL_OR_AUTHORITY
```

## 7. Non-Override Clause

This matrix does not override:

- `docs/DELEGATED_APPROVER_CHARTER.md`
- `docs/AUTONOMOUS_AUTHORIZATION_POLICY.md`
- `docs/AUTONOMOUS_DELIVERY_PIPELINE.md`
- `docs/AUTONOMOUS_HOLD_QUEUE.md`
- `docs/PRODUCT_STATE.md`
- `docs/ROADMAP_AND_PARKED_ITEMS.md`
- `docs/GOVERNANCE_DECISION_LOG.md`
- `docs/HANDOFF.md`
- PRD / Model Contract / D-02 hard constraints
- AI_COLLAB execution-surface and review rules

## 8. Next Safe Action

Next safe automation action:

```text
CONTINUE_RQ04_EP_T05_SH_T05_THEN_APPLY_ACCELERATION_MATRIX
```
