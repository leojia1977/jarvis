# S6 Sprint 1 RQ-02 Visual Dependency Unblock Queue 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Sprint 1 RQ-02 Visual Dependency Unblock Queue 2026-04-27 |
| Queue item | `RQ-02` |
| Status | VISUAL_UNBLOCK_QUEUE_OPEN_NO_IMPLEMENTATION_GO |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Parent record | `docs\S6_SPRINT1_RQ01_REMAINING_STATUS_RECONCILIATION_2026_04_27.md` |
| Visual SoT | `D:\产品设计\secupilot0421\SecuPilot_Visual_Kickoff_Frame_Checklist_v0.3.xlsx` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Route | `OPEN_VISUAL_DEPENDENCY_UNBLOCK_QUEUE` |

This record converts Visual Kickoff v0.3 frame dependencies into an implementation-unblock queue.

It is docs-only. It does not authorize implementation, Jira mutation, backend/runtime/API/schema changes, real data, secrets, deployment, public endpoint work, external pilot execution, or patch-gate implementation.

## 2. Decision

Decision:

```text
VISUAL_UNBLOCK_QUEUE_OPEN_NO_IMPLEMENTATION_GO
```

Meaning:

- Visual frames remain the main blocker for several remaining Sprint 1 and later-sprint tickets.
- The queue below names which tickets become eligible for a new launch checklist when each visual frame moves out of `未开始`.
- A frame becoming available does not automatically authorize code. It only unlocks an exact launch checklist.

## 3. Current Visual Frame State

Visual Kickoff v0.3 read-only check shows the relevant frames below are still:

```text
Frame Status = 未开始
```

This means all implementation tickets depending on these frames remain HOLD unless their current repo behavior has already been separately reconciled and closed.

## 4. Sprint 1 P1-Adjacent Unblock Queue

| Frame | Current status | Direct implementation tickets | Current handling |
| --- | --- | --- | --- |
| `VF-02` | `未开始` | `IN-T01`, `IN-T02`, `IN-T03`, `IN-T04` | `IN-T01` already implemented; use future frame for visual reconciliation only. `IN-T02` is P3-sensitive, `IN-T03` is P2-sensitive, `IN-T04` remains HOLD until exact P1 upgrade/close request semantics exist. |
| `VF-03` | `未开始` | `CD-T01`, `CD-T02`, `CD-T04`, `GS-T04` | `CD-T01`, `CD-T02`, and `CD-T04` already implemented; use future frame for visual reconciliation only. `GS-T04` remains HOLD until frame exists. |
| `VF-07` | `未开始` | `CD-T01`, `CD-T05` | `CD-T01` already implemented; `CD-T05` remains HOLD for P3 executive summary and P3 ratification. |
| `VF-09` | `未开始` | `CD-T04` | `CD-T04` already implemented; use future frame for visual reconciliation only. |
| `VF-10` | `未开始` | `CD-T04`, `EP-T02`, `EP-T03` | `CD-T04` already implemented; `EP-T02` and `EP-T03` remain HOLD because weakening/degradation style must not be invented. |
| `VF-13` | `未开始` | `CD-T06` | HOLD; patch-gate possible state-header ticket. |

## 5. Future P2/AP Unblock Queue

| Frame | Current status | Direct implementation tickets | Current handling |
| --- | --- | --- | --- |
| `HF-AU-02` | `未开始` | `AP-T08`, `AP-T10`, `MV-T04`, `SH-T08` | HOLD for AP/P3/audit semantics; schedule before AP audit implementation. |
| `VF-04` | `未开始` | `AP-T03`, `AP-T10`, `IN-T03` | HOLD for P2 approval surface and D-02 semantics. |
| `VF-05` | `未开始` | `AP-T04`, `AP-T10` | HOLD for approve confirmation flow. |
| `VF-11` | `未开始` | `AP-T06`, `AP-T10`, `CD-T06` | HOLD for observation-window state display and patch-gate sensitive semantics. |
| `VF-12` | `未开始` | `AP-T07`, `AP-T10`, `CD-T06` | HOLD for approved-pending-execution state display and patch-gate sensitive semantics. |
| `VF-15` | `未开始` | `AP-T09`, `SH-T08` | HOLD for approval audit no-event / unavailable states. |
| `HF-01` | `未开始` | `AP-T06` | HOLD for observation-window active read-only timer frame. |
| `HF-AU-01` | `未开始` | `AP-T08`, `AP-T10` | HOLD for approval audit chain. |

## 6. Future History / Manager / Coverage Unblock Queue

| Frame | Current status | Direct implementation tickets | Current handling |
| --- | --- | --- | --- |
| `VF-01` | `未开始` | `CH-T01`, `CH-T02` | HOLD for Coverage & Health page frame. |
| `VF-06` | `未开始` | `MV-T01`, `MV-T02` | HOLD for P3 Manager surface and P3 ratification. |
| `HF-SH-01` | `未开始` | `SH-T01`, `SH-T02` | HOLD for history list visual frame. |
| `HF-SH-02` | `未开始` | `SH-T02`, `SH-T06` | HOLD for degraded/empty history visual states. |
| `HF-SH-04` | `未开始` | `SH-T08` | HOLD for approval-audit focus visual frame. |
| `VF-14` | `未开始` | `SH-T02` | HOLD for history upgrade-prohibition visual frame. |

## 7. Immediate Design Ask For Sprint 1 Acceleration

If design capacity is limited, the highest-leverage P1-adjacent delivery order is:

1. `VF-03` - unlocks `GS-T04` and validates already implemented `CD-T01` / `CD-T02` / `CD-T04`.
2. `VF-02` - unlocks `IN-T04` and validates already implemented `IN-T01`.
3. `VF-10` - unlocks `EP-T02` / `EP-T03` without inventing degradation style.
4. `VF-13` - enables a future patch-gate isolated `CD-T06` state-header checklist.

If the team wants to accelerate P2 instead, the first design batch should be:

```text
VF-04 / VF-05 / VF-11 / VF-12 / HF-01 / HF-AU-01 / HF-AU-02
```

But those remain Sprint 2 / AP-governed surfaces and should not be mixed into normal Sprint 1 P1 burn-down.

## 8. Launch Checklist Rule

When a frame moves out of `未开始`, automation may create a new launch checklist only if all of the following are true:

- the frame has a concrete deliverable or reviewable visual artifact;
- the target ticket has exact allowed files;
- the target ticket has an exact test command;
- the target ticket does not require P2/P3 ratification unless that ratification is complete;
- patch-gate possible tickets are isolated;
- implementation can remain mock-only / bounded;
- no backend/runtime/API/schema, real data, secrets, deploy, public endpoint, or external pilot work is needed.

## 9. HOLD Conditions

HOLD if:

- a ticket tries to treat a `未开始` frame as delivered;
- implementation invents visual treatment in place of frame delivery;
- a frame unlock is used to smuggle P2/P3 authority changes into Sprint 1;
- a patch-gate possible ticket is placed in a normal burn-down batch;
- exact allowed files or test commands cannot be named.

## 10. Next Safe Action

Next safe automation action:

```text
OPEN_PATCH_GATE_BATCH_ISOLATION_CHECKLIST_OR_WAIT_FOR_VISUAL_FRAME_DELIVERY
```

Related authorized parallel docs-only action:

```text
OPEN_SH_T03_PATCH_GATE_ISOLATED_LAUNCH_CHECKLIST
```
