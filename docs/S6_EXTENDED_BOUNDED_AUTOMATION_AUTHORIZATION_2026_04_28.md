# S6 Extended Bounded Automation Authorization 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Extended Bounded Automation Authorization 2026-04-28 |
| Status | ACTIVE_30M_RUNNER_EXTENDED_QUEUE_WITH_IDLE_FALLBACK_AUTHORIZED |
| Date | 2026-04-28 |
| Automation | `secupilot-30m-bounded-burn-runner` |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |

Jarvis authorized the 30-minute bounded burn runner to execute a longer Sprint 1-4 automation queue so it does not exhaust after a short checklist pass.

Jarvis also authorized an idle fallback on 2026-04-28 so the runner can keep producing bounded docs/Jira hygiene work when no exact implementation ticket is safe to start.

## 2. Batch A - Implementation If Checklist GO

The runner may execute these tickets in order. Implementation is allowed only if each launch/readiness checklist returns GO with exact files, exact tests, no scope expansion, and no authority ambiguity.

| Order | Ticket | Authorized path |
| ---: | --- | --- |
| 1 | `AP-T08` | Narrow approval-audit source-boundary checklist and implementation if GO. |
| 2 | `SH-T02` | Dual coverage / clamp semantics checklist and implementation if GO. |
| 3 | `SH-T06` | Structural/degraded empty-state checklist and implementation if GO. |
| 4 | `CD-T06A` | Existing-state header skeleton checklist and implementation if GO. |
| 5 | `SH-T08` | Narrow approval-audit source boundary checklist and implementation only after `AP-T08` closeout/source-order confirmation. |

### AP-T08 Scope Limit

`AP-T08` may only implement:

```text
display-only activeContext.audit_trail source boundary in /approval
fixed enum derived-status mapping
```

It must not implement AP mutation, `ActionMode` creation, P3 Manager output, Search / History output, audit source invention, backend/runtime/API/schema, fixture registry/adapter, `ContextValidator`, or `ResolvedSurfaceContext` changes.

### CD-T06A Scope Limit

`CD-T06A` may only target existing renderable non-CLOSED states. It must not claim or simulate CLOSED behavior.

## 3. Batch B - No-Code / Reconciliation

| Order | Ticket | Authorized path |
| ---: | --- | --- |
| 6 | `EP-T06` | Dependency reconciliation / no-code closeout if existing evidence is sufficient. |
| 7 | `IN-T06` | Dependency readiness / no-code reconciliation if dependencies are already satisfied. |
| 8 | `CD-T07` | Dependency readiness / no-code reconciliation only after `CD-T06A` or `CD-T06` status is clear. |
| 9 | `AP-T11` / `AP-T12` | Readiness decomposition checklists after `AP-T08` status is known. |
| 10 | `MV-T05` | Readiness checklist after `MV-T04` remains gated or source path is clarified. |

## 4. Batch C - Authority / Blocker Packs

| Order | Item | Authorized path |
| ---: | --- | --- |
| 11 | `MV-T04` | Source-order follow-up checklist after `AP-T08` and `SH-T08` evidence. |
| 12 | `AP-T09` | Audit empty/unavailable blocker refresh. |
| 13 | `AP-T06` | Full countdown/state-sync blocker refresh. |
| 14 | `AP-T02` / `MV-T02` | Renderable authority-context blocker refresh. |
| 15 | `CH-T02` / `CH-T04` | Design/runtime blocker refresh. |

## 5. Batch D - Jira / Tracker Parity

The runner may:

- Sync Jira comments/status only for PASS or no-code reconciled tickets.
- Update Progress / Risk Board, route, handoff, and closeout records after each PASS/HOLD.
- Stage/commit/push for PASS implementation or authorized docs-only closeout batches.

The runner must not:

- Mark HOLD, blocked, visual-missing, authority-missing, or non-ready tickets Done.
- Treat a checklist-only PASS as implementation closeout.
- Treat visual PASS as launch, deploy, real-data, or external-pilot authorization.

## 6. Required Gates For PASS Implementation

For every PASS implementation:

```text
run required gates
obtain Claude Code focused review when required
sync Jira safely
stage/commit/push
```

## 7. Global HOLD Conditions

HOLD immediately on:

- scope expansion;
- missing exact files;
- failed tests/build;
- visual ambiguity;
- P2/P3 authority ambiguity;
- backend/runtime/API/schema need;
- fixture/adapter/validator/`ResolvedSurfaceContext` change;
- raw evidence DOM attachment;
- real data;
- secrets;
- deploy;
- public endpoint;
- external pilot;
- mandatory external review trigger;
- non-ready ticket.

## 8. Next Runner Route

`AP-T08` has since closed as implemented and Jira-synced. The runner must not repeat `AP-T08`.

`SH-T02` has since closed as implemented with gate PASS and Claude Code PASS. Jira sync remains pending because Jira environment variables were not visible to the runner. The runner must not repeat `SH-T02`.

`SH-T06` has since closed as implemented with gate PASS and Claude Code PASS. Jira sync remains pending because Jira environment variables were not visible to the runner. The runner must not repeat `SH-T06`.

`CD-T06A` has since closed as implemented with gate PASS and Claude Code PASS. Jira sync remains pending because Jira environment variables were not visible to the runner. The runner must not repeat `CD-T06A`, and must not treat `CD-T06A` as full `CD-T06` closeout.

Idle fallback is governed by:

```text
docs/S6_30M_RUNNER_IDLE_FALLBACK_2026_04_28.md
```

If the remaining queue cannot safely start implementation, the runner may perform one idle fallback action per heartbeat:

- Progress / Risk Board refresh;
- Jira parity audit for already PASS or no-code reconciled tickets;
- next exact checklist preparation;
- blocker / authority pack refresh;
- design-frame request refresh;
- idle report.

Idle fallback is docs-only unless a separate exact implementation checklist gives a narrow GO.

## 9. Current Runner Route

```text
CONTINUE_EXTENDED_QUEUE_WITH_IDLE_FALLBACK_AFTER_CD_T06A_CLOSEOUT
```
