# S6 AP Batch Authority Decomposition 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 AP Batch Authority Decomposition 2026-04-27 |
| Status | LOW_RISK_QUEUE_OUTPUT_CHECKLIST_ORDER |
| Queue item | `LR-05` |
| Date | 2026-04-27 |
| AP predecessors closed | `AP-T10`, `AP-T01` |

This document decomposes the remaining AP tickets into safe checklist order.

It does not authorize broad AP implementation, approval actions, state transitions, backend/runtime/API/schema changes, real data, secrets, deploy, public endpoint, or external pilot.

## 2. Current AP Baseline

Closed:

| Ticket | Current evidence |
| --- | --- |
| `AP-T10` | Display-only AR status badge/pill mapping implemented. |
| `AP-T01` | `/approval` route shell/guard implemented; no controls or transitions. |

Still blocked or authority-sensitive:

```text
AP-T02
AP-T03
AP-T04
AP-T05
AP-T06
AP-T07
AP-T08
AP-T09
AP-T11
AP-T12
```

## 3. Safe Order

| Order | Ticket | Category | Why this order |
| ---: | --- | --- | --- |
| 1 | `AP-T03` | CTA/action boundary | First real AP control boundary; must define which controls can attach and when. |
| 2 | `AP-T07` | Lock-state affordance | Can be constrained after AP status mapping and before transitions expand. |
| 3 | `AP-T05` | Observe/delay configuration | Needs AP CTA boundary; must avoid timer/state-sync implementation creep. |
| 4 | `AP-T04` | Strong confirm modal | Needs CTA semantics and exact confirm fields. |
| 5 | `AP-T06` | Observation-window countdown/state-sync | Depends on AP-T05 and must not use frontend timer as authority. |
| 6 | `AP-T08` | Approval audit chain | Needs action semantics and P2/P3 read boundaries. |
| 7 | `AP-T09` | Audit empty/unavailable states | Depends on AP-T08 source legality. |
| 8 | `AP-T11` | State-transition assertions | Acceptance assertions after implementation chain exists. |
| 9 | `AP-T12` | AP acceptance suite | Final AP acceptance after route, CTA, audit, and state work. |

`AP-T02` remains separate because it is P0 readonly context work and is currently HOLD pending P0 renderable approval context.

## 4. Ticket-Specific Checklist Requirements

| Ticket | Checklist must prove | External review trigger |
| --- | --- | --- |
| `AP-T03` | Exact CTA attach rules, P2-only action authority, no P1/P3/P0 operation | Likely yes: first AP action-control boundary |
| `AP-T04` | Confirm modal fields, no state mutation before confirm, no hidden controls | Conditional |
| `AP-T05` | Delay/observe options, no frontend-created state authority, no timer migration | Likely yes |
| `AP-T06` | Countdown display vs `STATE_SYNC` migration, no `setTimeout` authority | Likely yes |
| `AP-T07` | Approved-pending-execution read-only lock, no stale controls | Conditional |
| `AP-T08` | Audit source fields and P2/P3 read boundary | Likely yes |
| `AP-T09` | Empty/unavailable audit state, honest degradation | Conditional |
| `AP-T11` | Assertion-only scope over existing AP behavior | No if no implementation |
| `AP-T12` | Acceptance-only scope over completed AP chain | No if no implementation |

## 5. Recommended Next AP Candidate

Recommended next AP item:

```text
AP-T03 authority checklist only
```

Reason:

- `AP-T01` route shell/guard is closed.
- `AP-T10` display mapping is closed.
- Any useful AP acceleration now depends on the approval CTA/action boundary.

Implementation remains unauthorized until a later exact checklist returns `GO` and Jarvis grants implementation GO.

## 6. Non-Authorization

This decomposition does not authorize:

- approve/reject/delay/observe controls;
- confirm modal implementation;
- state transition;
- observation-window countdown;
- stale-approve behavior;
- approval audit;
- AP acceptance suite;
- backend/runtime/API/schema;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes.

