# S6 Remaining Blocker Map 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Remaining Blocker Map 2026-04-27 |
| Status | LOW_RISK_QUEUE_OUTPUT |
| Queue item | `LR-01` |
| Date | 2026-04-27 |
| Source board | `docs\S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md` |

This map classifies every non-Done Sprint 1-4 tracker ticket after the latest completed batch.

It is blocker analysis only. It does not authorize implementation, Jira Done transition, product-scope expansion, visual PASS, backend/runtime/API/schema changes, fixture/adapter/validator changes, or `ResolvedSurfaceContext` changes.

## 2. Current Counts

| State | Count |
| --- | ---: |
| Done | 27 |
| Needs authority review | 14 |
| Needs design | 3 |
| HOLD | 10 |
| Auto-ready implementation | 0 |
| Skeleton-ready implementation | 0 |
| Checklist-only currently open | 0 |

Total Sprint 1-4 tracker tasks covered: `54`.

## 3. Needs Authority Review

| Ticket | Blocker class | Missing artifact | Next safe action |
| --- | --- | --- | --- |
| `IN-T03` | AP/P2 authority | P2 shortcut approval/close authority and AP CTA boundary | `authority-pack` before checklist |
| `AP-T03` | AP CTA authority | Exact approval CTA/action boundary after AP-T01/AP-T10 | `checklist-only` then implementation GO if PASS |
| `AP-T04` | Confirm-modal authority | AP-T03 CTA semantics and strong-confirm field list | `checklist-only` after AP-T03 |
| `AP-T05` | Observe/delay authority | Delay/observe config authority and D-02 state constraints | `checklist-only` after AP-T03 |
| `AP-T06` | Observation-window/state-sync | AP-T05 plus state-sync/timer authority; likely visual `HF-01` dependency | `authority-pack` and design check |
| `AP-T07` | Lock-state authority | Approved-pending-execution lock semantics and allowed read-only affordances | `checklist-only` after AP-T10/AP-T03 |
| `AP-T08` | Approval-audit authority | Audit source path and P2/P3 read boundary | `authority-pack` before implementation |
| `AP-T09` | Audit empty/unavailable | AP-T08 audit-chain source legality | `checklist-only` after AP-T08 |
| `AP-T11` | State-transition assertions | AP-T03 through AP-T08 implementation chain | `not safe to start` |
| `AP-T12` | AP acceptance suite | AP route, CTA, audit, and state implementation chain | `not safe to start` |
| `MV-T03` | Manager deep-link handoff | Handoff source/target legality after MV-T01 | `authority-pack` before checklist |
| `MV-T04` | P3 approval audit summary | AP-T08 audit source plus P3 raw-evidence absence guard | `authority-pack` before checklist |
| `MV-T05` | Manager acceptance | MV-T03/MV-T04 implementation evidence | `not safe to start` |
| `SH-T08` | P3 approval-audit source | SH history source plus AP-T08 audit source | `authority-pack` before checklist |

## 4. Needs Design

| Ticket | Blocker class | Missing artifact | Next safe action |
| --- | --- | --- | --- |
| `CH-T02` | Visual frame | `VF-01` final or approved semantic frame anchors | `design-frame` request |
| `SH-T02` | Visual frames | `HF-SH-01`, `HF-SH-02`, `VF-08`, `VF-14` | `design-frame` request |
| `SH-T06` | Visual frame | `HF-SH-02` | `design-frame` request |

## 5. HOLD

| Ticket | HOLD reason | Exact unblock artifact | Next safe action |
| --- | --- | --- | --- |
| `IN-T06` | Depends on `IN-T03` and `IN-T04` | `IN-T03` authority resolved and implemented/reconciled | `not safe to start` |
| `CD-T06` | Missing `CLOSED` renderable fixture and `VF-11/VF-12/VF-13` | Renderable `CLOSED` context plus state-header visual semantics | `fixture-context` and `design-frame` |
| `CD-T07` | Depends on `CD-T05` and `CD-T06` | `CD-T06` accepted | `not safe to start` |
| `EP-T06` | Depends on `EP-T02`, `EP-T03`, and `EP-T05` | Acceptance evidence for the EP chain | `checklist-only` later |
| `AP-T02` | Missing P0 renderable approval context | Governed P0 readonly approval context/harness | `fixture-context` or authority-reviewed harness |
| `CH-T03` | Patch-gate possible after `CH-T01` | Isolated checklist for `ui_messages` rendering | `checklist-only` |
| `CH-T04` | Depends on `CH-T01`, `CH-T02`, and `CH-T03` | `CH-T02` and `CH-T03` accepted | `not safe to start` |
| `MV-T02` | Missing P0/P2 Manager authority model | Governed P0/P2 degraded readonly Manager model | `authority-pack` |
| `SH-T04` | Depends on `SH-T01` | Exact route/query/filter scope and evidence that no new route handoff is needed | `checklist-only` candidate |
| `SH-T09` | Depends on SH chain | `SH-T02`, `SH-T06`, `SH-T08`, and others accepted | `not safe to start` |

## 6. Possible No-Code Reconciliation

No ticket is currently proven safe for no-code closeout from repo evidence alone.

Possible future candidates can be reassessed after exact checklists:

| Ticket | Why not closed now |
| --- | --- |
| `SH-T04` | Current board lists dependency on `SH-T01`, but exact filter/query behavior has not been reconciled. |
| `EP-T06` | EP acceptance depends on existing EP chain evidence but needs a dedicated acceptance checklist before no-code closeout. |

## 7. Possible Checklist-Only

| Ticket | Checklist type | Why safe as checklist-only |
| --- | --- | --- |
| `AP-T03` | AP CTA authority checklist | AP-T01 and AP-T10 are closed; broad implementation still unauthorized. |
| `AP-T05` | Observe/delay authority checklist | Can clarify boundaries without implementing countdown or state sync. |
| `AP-T07` | Lock-state display/affordance checklist | Can constrain read-only lock behavior before code. |
| `AP-T08` | Audit-source authority checklist | Needed before AP audit implementation. |
| `CH-T03` | Patch-gate isolated checklist | `CH-T01` exists; implementation remains separate. |
| `MV-T03` | Deep-link handoff authority checklist | Can define source/target boundaries without route handoff code. |
| `MV-T04` | P3 approval audit summary authority checklist | Can define raw-evidence absence and audit source legality. |
| `SH-T04` | Search/history scope checklist | Can verify whether implementation is actually needed. |
| `SH-T08` | P3 approval audit source checklist | Can map dependency on AP-T08 and history source. |

## 8. Not Safe To Start

| Ticket | Reason |
| --- | --- |
| `IN-T06` | Upstream P2 shortcut semantics are unresolved. |
| `CD-T07` | Depends on `CD-T06`, which is HOLD. |
| `AP-T11` | Acceptance assertions require earlier AP implementation tickets. |
| `AP-T12` | AP suite acceptance requires AP route/CTA/audit/state chain. |
| `CH-T04` | Depends on `CH-T02` visual frame and `CH-T03` patch-gate path. |
| `MV-T05` | Manager acceptance depends on MV chain. |
| `SH-T09` | Search/History acceptance depends on SH visual and authority chain. |

## 9. Recommended Next Candidate Set

Low-risk next candidates for tomorrow's human review:

```text
AP-T03 authority checklist
CH-T03 patch-gate isolated checklist
SH-T04 search/history scope checklist
MV-T03 deep-link authority checklist
```

None of the above is an implementation GO.

