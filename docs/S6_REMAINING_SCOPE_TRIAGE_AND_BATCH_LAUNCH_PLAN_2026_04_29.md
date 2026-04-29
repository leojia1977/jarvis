# S6 Remaining Scope Triage And Batch Launch Plan 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Remaining Scope Triage And Batch Launch Plan 2026-04-29 |
| Status | REMAINING_SCOPE_TRIAGE_OPENED_BATCH_R1_READY |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Source exit refresh | `docs\S6_SPRINT0_EXIT_REVIEW_REFRESH_AND_REMAINING_SCOPE_TRIAGE_2026_04_29.md` |
| Progress board | `docs\S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md` |
| Commit baseline | `66c7cdd docs: record Sprint 0 exit refresh and remaining scope triage` |

## 2. Purpose

This record opens the governed remaining-scope triage route after Sprint 0 foundation and Batch 0 closeout.

It splits the remaining blocked Sprint 1-4 work into exact narrow lanes so automation can continue without using a generic implementation GO.

This record does not authorize implementation. It authorizes docs-only launch/readiness/source-pack preparation for Batch R1.

## 3. Current Baseline

Closed foundations:

- Sprint 0 foundation: closed.
- Batch 0: closed; exact Jira parity done for `SCRUM-9`, `SCRUM-10`, `SCRUM-11`, `SCRUM-12`, and `SCRUM-13`.
- `E0-02B / SCRUM-19 / 633cc73`: closed; no further action unless fixture QA expansion is explicitly reopened.
- `AP-T08 / SCRUM-62`: Done; source/authority evidence only.
- `SH-T08 / SCRUM-63`: Done; source/authority evidence only.
- `MV-T04 / SCRUM-68`: Done; source/authority evidence only.

Current posture:

```text
Remaining work is a triage problem, not a Batch 0 relaunch.
```

## 4. Batch R1 Overview

Batch R1 is a docs-only launch/readiness batch across six narrow lanes.

| Lane | Ticket | Work type | Implementation GO |
| --- | --- | --- | --- |
| R1-A | `AP-T06` | State-sync input and test-hook checklist | NO |
| R1-B | `AP-T09` | `VF-15` / audit empty-unavailable source request | NO |
| R1-C | `CD-T06` | Renderable CLOSED Case Detail context checklist | NO |
| R1-D | `CH-T04` | Runtime/source-health authority review | NO |
| R1-E | `IN-T03` | P2 shortcut approval / close-entry authority review | NO |
| R1-F | `MV-T02` | P0/P2 Manager authority model review | NO |

Batch R1 may run in parallel as docs-only work. Any lane that discovers safe implementation scope must stop at `IMPLEMENTATION_GO_REQUIRED`.

## 5. R1-A: AP-T06 State-Sync Input And Test-Hook Checklist

Current evidence:

- `AP-T06A` static readonly observation-window skeleton is closed as `SCRUM-65`.
- Full `AP-T06` remains open / not Done as `SCRUM-64`.
- `VF-11` is accepted as static readonly frame input only.
- Full countdown/state-sync behavior remains HOLD.

Primary blocker:

```text
No governed state-sync input authority and no exact test hook exists for material state migration.
```

Open next:

```text
OPEN_AP_T06_STATE_SYNC_INPUT_AND_TEST_HOOK_CHECKLIST
```

Checklist must answer:

- What is the governed source of material state transition?
- Is there an allowed test-only `emitStateSync` or equivalent harness?
- Which fields may change from `OBSERVATION_WINDOW` to `PENDING_APPROVAL`?
- How does the UI prove frontend timer display is presentation-only and not state authority?
- Which exact files and tests would be touched if implementation later receives GO?

Implementation GO requires:

- exact governed state-sync input;
- exact test hook semantics;
- display-vs-authority rule;
- exact allowed files and test command;
- no backend protocol invention;
- no API/schema/runtime change;
- no `ResolvedSurfaceContext`, fixture adapter, or validator change unless separately authorized.

HOLD if:

- implementation requires backend/runtime/API/schema;
- implementation invents state-sync protocol;
- frontend timer becomes authority;
- exact files/tests cannot be named;
- P2 approval semantics become ambiguous.

## 6. R1-B: AP-T09 VF-15 / Audit Empty-Unavailable Source Request

Current evidence:

- `AP-T08` source boundary is Done.
- `AP-T09` remains blocked by missing governed audit empty/unavailable source.
- Existing enum fallback must not be treated as sufficient product/source copy authority.

Primary blocker:

```text
No VF-15 or equivalent governed audit empty-unavailable source exists.
```

Open next:

```text
OPEN_VF_15_AUDIT_EMPTY_UNAVAILABLE_SOURCE_FRAME
```

Source request must answer:

- What is the visual/source distinction between empty audit, unavailable audit, degraded audit, and loading?
- Which copy source owns each message?
- Which selectors/test ids are required?
- What must never be displayed as a substitute for missing audit evidence?
- Whether `ui_messages` owns any displayed copy.

Implementation GO requires:

- `VF-15` or equivalent governed source;
- exact copy/source rules;
- exact allowed files and tests;
- no audit source invention;
- no AP mutation or action-mode creation.

HOLD if:

- no governed source frame exists;
- copy semantics remain ambiguous;
- implementation would infer audit state from generic unavailable enum only;
- implementation touches backend/runtime/API/schema, fixture/adapter/validator, or `ResolvedSurfaceContext`.

## 7. R1-C: CD-T06 Closed Case Detail Context Checklist

Current evidence:

- `VF-11`, `VF-12`, and `VF-13` are accepted visual inputs.
- `CD-T06A` closed existing non-CLOSED state header skeletons only.
- Full `CD-T06` remains HOLD as `SCRUM-53`.

Primary blocker:

```text
No governed renderable CLOSED Case Detail context exists.
```

Open next:

```text
OPEN_CD_T06_CLOSED_CASE_DETAIL_CONTEXT_CHECKLIST
```

Checklist must answer:

- Which source can provide a renderable `CLOSED` Case Detail context?
- Can current fixtures/resolved context render CLOSED without changing fixture registry, adapter, validator, or root context?
- What exact DOM and test assertions are required for `VF-13`?
- Can dialogue readonly input use `input[disabled]` or `textarea[disabled]` as required by prior notes?
- What must remain absent: reopen CTA, P2 approval controls, action controls, raw evidence DOM, hidden workflow.

Implementation GO requires:

- exact renderable CLOSED context;
- exact files and tests;
- no fixture/context expansion unless separately authorized;
- no reopening, mutation, or route handoff behavior;
- no backend/runtime/API/schema.

HOLD if:

- CLOSED context requires fixture/adapter/validator or `ResolvedSurfaceContext` change;
- implementation cannot name exact source evidence;
- closed-state behavior would be inferred from visual HTML alone;
- any reopen or hidden workflow appears.

## 8. R1-D: CH-T04 Runtime / Source-Health Authority Review

Current evidence:

- `CH-T01`, `CH-T02`, and `CH-T03` are closed or safe within bounded frontend scope.
- `CH-T02` is repo Done but has no exact cloud Jira issue.
- `CH-T04` remains HOLD pending runtime/source-health authority.

Primary blocker:

```text
No governed decision exists for runtime/source-health scope.
```

Open next:

```text
OPEN_CH_T04_RUNTIME_SOURCE_HEALTH_AUTHORITY_REVIEW
```

Authority review must answer:

- Is `CH-T04` frontend-only mock/source-status rendering, or does it require runtime/backend source health?
- If runtime is required, which governed decision record must authorize it?
- Which source-health values may be displayed without real telemetry?
- What unavailable/degraded copy must be driven by `ui_messages`?
- Which exact files/tests are allowed for any frontend-only slice?

Implementation GO requires:

- explicit frontend-only scope or separate human go/no-go for backend/runtime work;
- exact source-health authority;
- exact files and tests;
- no real health endpoint, live telemetry, public endpoint, real data, secrets, deploy, or external pilot.

HOLD if:

- backend/runtime/API/schema is needed;
- real telemetry or live health is requested;
- source health would be invented from mock UI;
- exact authority cannot be named.

## 9. R1-E: IN-T03 P2 Shortcut Approval / Close-Entry Authority Review

Current evidence:

- `IN-T04` P1 escalation / close-request skeleton is closed.
- `AP-T10` display mapping is available but not sufficient to authorize P2 shortcut behavior.
- `AP-T03` provides inert P2 CTA boundary, but not broad shortcut authority.
- `IN-T06` remains HOLD behind `IN-T03`.

Primary blocker:

```text
P2 shortcut approval / close-entry authority is not yet governed for Inbox.
```

Open next:

```text
OPEN_IN_T03_P2_SHORTCUT_AUTHORITY_REVIEW
```

Authority review must answer:

- Is Inbox allowed to expose a shortcut entry, or only a link/context handoff?
- Which role and surface may see it?
- Does it create, select, or mutate `ActionMode`?
- Does it enter `/approval`, open Case Detail, or remain inert?
- Which AP tickets are prerequisites?

Implementation GO requires:

- explicit authority model;
- exact no-mutation / route behavior;
- exact allowed files and tests;
- no P2 authority leak into P1;
- no AP mutation, backend/runtime/API/schema, fixture/adapter/validator, or `ResolvedSurfaceContext` change.

HOLD if:

- the shortcut would create approval state;
- P1 can select or imply `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY`;
- route handoff semantics are ambiguous;
- exact files/tests cannot be named.

## 10. R1-F: MV-T02 P0/P2 Manager Authority Model Review

Current evidence:

- `MV-T01` is P3-only and explicitly avoided P0/P2 placeholders.
- `MV-T03` and `MV-T04` are Done.
- `MV-T05` remains HOLD until `MV-T02` is resolved or explicitly rescoped.
- `SCRUM-55` remains not Done.

Primary blocker:

```text
No governed P0/P2 Manager authority model exists.
```

Open next:

```text
OPEN_MV_T02_P0_P2_MANAGER_AUTHORITY_REVIEW
```

Authority review must answer:

- Are P0/P2 allowed to enter `/manager` at all?
- If yes, what readonly/degraded variant is allowed?
- Which data fields are visible by role and coverage ceiling?
- Does the variant reuse P3 components or require separate guarded components?
- What must not mount in the DOM?

Implementation GO requires:

- explicit P0/P2 Manager authority model;
- exact fields and forbidden DOM list;
- exact files and tests;
- no P0/P2 placeholder retrofitting into `MV-T01` without review;
- no raw evidence DOM, approval controls, backend/runtime/API/schema, fixture/adapter/validator, or `ResolvedSurfaceContext` change.

HOLD if:

- P0/P2 visibility rules remain ambiguous;
- implementation would infer authority from URL/storage;
- implementation needs new data source;
- exact allowed files/tests cannot be named.

## 11. Dependent Acceptance Tickets

These tickets remain HOLD until parent lanes close:

| Dependent ticket | Dependency |
| --- | --- |
| `AP-T11` | Full `AP-T06` plus `AP-T09`; `AP-T11A` is only a closed static split. |
| `AP-T12` | Full `AP-T06` plus `AP-T09`. |
| `CD-T07` | Full `CD-T06`. |
| `IN-T06` | `IN-T03` authority resolution. |
| `MV-T05` | `MV-T02` or explicit rescope. |
| `CH-T04` acceptance closure | Its own runtime/source-health authority decision. |

Do not mark these Done from partial splits or parent evidence comments.

## 12. Batch R1 Automation Rules

Allowed in Batch R1:

- create docs-only checklist/source/authority-pack records for R1-A through R1-F;
- update route, handoff, progress board, and blocker maps;
- add Jira comments only if exact issue mapping is already known and the comment does not transition status;
- record `IMPLEMENTATION_GO_REQUIRED` when a lane becomes implementable;
- run docs gates and pilot preflight.

Forbidden in Batch R1:

- implementation;
- frontend source changes;
- Storybook changes;
- Playwright changes;
- fixture / adapter / validator changes;
- `ResolvedSurfaceContext` changes;
- backend / runtime / API / schema changes;
- real data or anonymized real data;
- secrets;
- deploy;
- public endpoint;
- external pilot;
- Jira Done transition for HOLD, partial split, blocked, or non-ready tickets.

## 13. Suggested Batch R1 Execution Order

For maximum automation burn-down without scope invention:

1. Run `R1-A` and `R1-B` first because they unblock `AP-T11` / `AP-T12`.
2. Run `R1-C` next because it unblocks `CD-T07`.
3. Run `R1-E` and `R1-F` next because they unblock `IN-T06` and `MV-T05`.
4. Run `R1-D` as an authority review, with backend/runtime scope explicitly separated before any implementation.

Parallelism is allowed for docs-only checklist/source-pack work because all six lanes have disjoint decision surfaces and no implementation writes.

## 14. Next Route

Next governed route:

```text
OPEN_REMAINING_SCOPE_TRIAGE_BATCH_R1_CHECKLISTS
```

Implementation remains:

```text
NOT_AUTHORIZED
```

Any lane that returns `GO_FOR_IMPLEMENTATION_CANDIDATE` must stop and request a later exact implementation GO with allowed files, tests, rollback, reviewer path, and HOLD conditions.
