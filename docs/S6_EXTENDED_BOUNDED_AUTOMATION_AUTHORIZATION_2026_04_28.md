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

`SH-T08` has since closed as implemented with gate PASS and Claude Code PASS. Jira sync remains pending because Jira environment variables were not visible to the runner. The runner must not repeat `SH-T08`.

`EP-T06` has since closed as a no-code dependency reconciliation with gate PASS. Jira sync remains pending because Jira environment variables were not visible to the runner. The runner must not repeat `EP-T06`.

`IN-T06` has since been checked and remains HOLD because `IN-T03` is not authority-resolved. The runner must not mark `IN-T06` Done.

`CD-T07` has since been checked and remains HOLD because full `CD-T06` is not resolved. The runner must not mark `CD-T07` Done.

`AP-T11` / `AP-T12` have since been decomposed. Full AP-T11/AP-T12 remain HOLD. `AP-T11A` static no-mutation assertion prep has since been recorded in `docs/S6_AP_T11A_STATIC_NO_MUTATION_ASSERTION_PREP_2026_04_29.md`, but it remains no-implementation prep only. The runner must not start `AP-T11A`, create Jira issues, or mark AP-T11/AP-T12 Done without a later exact `AP-T11A static no-mutation assertion implementation GO`.

`MV-T05` has since been checked and remains HOLD because `MV-T04` approval audit summary is not implemented and `MV-T02` P0/P2 Manager variants remain authority-gated. The runner must not mark `MV-T05` Done.

`MV-T04` source-order follow-up has since passed. The source-order blocker is closed, but implementation remains unauthorized until a separate implementation GO. The runner must not mark `MV-T04` Done from the source-order checklist.

`AP-T09` blocker refresh has since partially unblocked the ticket by closing the AP-T08 dependency. `AP-T09` remains HOLD pending `VF-15` or equivalent governed audit empty/unavailable source and exact copy rules. The runner must not mark `AP-T09` Done or implement it from the generic `UNAVAILABLE` enum fallback alone.

`AP-T06` full countdown/state-sync blocker refresh has since reconfirmed that
the already closed `AP-T06A` static slice is the maximum safe split under the
current governed evidence. Full `AP-T06` remains HOLD pending exact state-sync
input authority, exact test hook, and an explicit display-vs-authority rule for
the timer. The runner must not mark `AP-T06` / `SCRUM-64` Done or implement the
countdown/state-sync path from the current static readonly surface.

`AP-T02` / `MV-T02` renderable authority-context blocker refresh has since
reconfirmed HOLD. `AP-T02` still lacks a governed P0 readonly approval context
or approved harness. `MV-T02` still lacks a governed P0/P2 Manager authority
model and renderable context. The runner must not mark `SCRUM-54` or `SCRUM-55`
Done and must not infer either context from URL, storage, route params, or the
existing P2/P3 audit-source work.

`CH-T02` / `CH-T04` design/runtime blocker refresh has since reconfirmed HOLD.
`CH-T02` still lacks `VF-01` final or approved semantic frame anchors. `CH-T04`
still depends on `CH-T02` plus an exact governed runtime/source-health scope.
The runner must not mark either ticket Done and must not infer final Coverage &
Health visual or runtime semantics from the current skeleton.

`SH-T09` acceptance checklist has since been prepared. The Search / History
chain evidence is ready for a later reconciliation pass, but `SH-T09`
reconciliation, Jira Done transition, or implementation still requires a
separate exact GO.

Safe Jira parity sync has since transitioned `SCRUM-63` for `SH-T08` to
`已完成` with repo closeout evidence. The runner must not repeat `SH-T08` Jira
sync and must not mark HOLD or non-ready tickets Done.

Remaining PASS-row Jira parity audit has since confirmed no additional safe
Jira transitions are available without explicit issue mapping. Repo PASS rows
`SH-T02`, `SH-T06`, and `EP-T06` have closeout evidence, but no dedicated cloud
issue key was exposed in the current project search. The runner must not create
or infer Jira issues for them without a later exact mapping decision.

Jira mapping proposal has since been prepared for `SH-T02`, `SH-T06`, and
`EP-T06`. It records explicit mapping options but performs no cloud mutation.
The runner must not create dedicated Jira issues, attach parent comments, or
transition any additional Jira issues Done without a later exact mapping GO.

`SH-T09` reconciliation closeout prep has since been prepared. It makes the
future no-code closeout executable after explicit GO, but it does not close
`SH-T09`, mutate Jira, or authorize implementation. The runner must not mark
`SH-T09` Done without later reconciliation GO and gate evidence.

`MV-T04` implementation GO prep has since been prepared. It makes `MV-T04` an
exact future implementation candidate after explicit GO, but it does not
implement, mutate Jira, close `MV-T04`, or close `MV-T05`. The runner must not
start MV-T04 implementation without later explicit GO.

`AP-T09` VF-15 design source request has since been prepared. It does not
implement AP-T09 or mutate Jira; it only defines the missing governed
empty/unavailable audit source needed before AP-T09 can return to a launch
checklist.

`AP-T06` state-sync harness source request has since been prepared. It does not
implement full AP-T06 or mutate Jira; it only defines the missing state-sync
input authority, display-vs-authority rule, and test-harness source needed
before full AP-T06 can return to a launch checklist.

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
WAIT_FOR_MV_T04_IMPLEMENTATION_GO_OR_AP_T11A_STATIC_ASSERTION_GO_OR_AP_T06_STATE_SYNC_SOURCE_DELIVERY_OR_AP_T09_VF15_SOURCE_DELIVERY_OR_SH_T09_RECONCILIATION_GO_OR_JIRA_MAPPING_GO_OR_NEXT_IDLE_FALLBACK
```
