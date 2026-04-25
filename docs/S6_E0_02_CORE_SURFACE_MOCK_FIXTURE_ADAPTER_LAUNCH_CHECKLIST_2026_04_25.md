# S6 E0-02 Core Surface Mock Fixture Adapter Launch Checklist 2026-04-25

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 E0-02 Core Surface Mock Fixture Adapter Launch Checklist 2026-04-25 |
| Ticket | `E0-02` |
| Status | READY_FOR_JARVIS_IMPLEMENTATION_GO |
| Date | 2026-04-25 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `aaaa199` |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review |
| Review surface | `claude-cmd` |
| External review | conditional |
| SWE | disabled |

This checklist prepares Sprint 0 `E0-02` only.

It converts the repo-local mock fixture Phase 0-6 state into validated `ResolvedSurfaceContext` objects from `E0-01`, so Storybook and Playwright can consume one root context path instead of each surface parsing role, coverage, case state, AR status, or action mode independently.

## 2. Human Authorization

Jarvis authorized this preparation step:

```text
Create the E0-02 per-ticket launch checklist.
Generate Jira delta CSV and update notes.
Do not mutate Jira cloud yet.
```

This authorization does not start implementation. Implementation requires a later explicit Jarvis GO.

## 3. Source Authority

Current governed source-of-truth:

- `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版.md`
- `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2.1.md`
- `SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx`
- `SecuPilot_Visual_Kickoff_Frame_Checklist_v0.3.xlsx`
- `docs\S6_G0_PRE_START_CONFIRMATION_2026_04_25.md`
- `docs\S6_E0_01_RESOLVED_SURFACE_CONTEXT_TICKET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs\S6_MF_A_CORE_SURFACE_MOCK_FIXTURE_INTEGRATION_TICKET_PREP_2026_04_25.md`

Fixture sources:

- incoming source: `D:\产品设计\secupilot0421\incoming_pending\secupilot_core_surface_fixture_v0.1.json`
- repo-local fixture: `frontend/fixtures/secupilot_core_surface_fixture_v0_1.json`
- expected SHA256: `814F21AACFE2E2B25514990188F9801D81F0ED4A464F7A03B05DD235E4A02B47`

Fixture hash precheck on 2026-04-25:

```text
incoming fixture hash:   814F21AACFE2E2B25514990188F9801D81F0ED4A464F7A03B05DD235E4A02B47
repo-local fixture hash: 814F21AACFE2E2B25514990188F9801D81F0ED4A464F7A03B05DD235E4A02B47
```

Version reconciliation:

```text
E0-01 is closed in commit aaaa199.
S6-MF-A already copied and displayed the fixture through existing app-local mappings.
E0-02 does not re-open S6-MF-A scope. It aligns fixture phase state with the E0-01 root context contract.
```

## 4. Exact Scope

Implement only:

1. A small fixture adapter that maps fixture Phase 0-6 records into `ResolvedSurfaceContext`.
2. Validation of every adapted phase through `validateResolvedSurfaceContext`.
3. Minimal app wiring only if needed to replace existing app-local phase/role/coverage/case-state derivation with adapter output while preserving current visible behavior.
4. Focused unit/component tests for adapter output, validation, and unchanged fixture authority boundaries.

The adapter may normalize fixture naming differences, but it must not invent product behavior beyond the fixture and E0-01 contract.

## 5. Exact Allowed Files

Allowed files:

- `docs/S6_E0_02_CORE_SURFACE_MOCK_FIXTURE_ADAPTER_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/src/secupilot/surface/fixtures/coreSurfaceFixtureAdapter.ts`
- `frontend/src/secupilot/surface/fixtures/__tests__/coreSurfaceFixtureAdapter.test.ts`
- `frontend/src/App.tsx`
- `frontend/src/App.test.tsx`

Read-only references:

- `frontend/fixtures/secupilot_core_surface_fixture_v0_1.json`
- `frontend/src/secupilot/surface/context/types.ts`
- `frontend/src/secupilot/surface/context/validateResolvedSurfaceContext.ts`
- `frontend/src/secupilot/surface/context/ResolvedSurfaceContextProvider.tsx`
- `frontend/src/secupilot/surface/components/SecurityHalt.tsx`

No other file may be changed unless a HOLD is triggered and Jarvis explicitly expands scope.

## 6. Exact Non-Goals

This ticket must not implement:

- P1/P2/P3 new page implementation;
- Storybook stories or Storybook configuration;
- Playwright E2E or Playwright dependency/configuration;
- backend/runtime/API/schema changes;
- cross-surface route handoff;
- P1 to P2 AR propagation;
- P2 to P3 audit propagation;
- observation-window backend signaling, polling, WebSocket, or concurrency handling;
- real data, sanitized real data, customer data, secrets, credentials, tokens, public endpoints;
- launch, deploy, external pilot, or readiness claims;
- static HTML prototype copy/paste;
- broad data layer, service registry, component registry, global store, route framework, or cleanup refactor.

## 7. Required Semantics

Required:

- role, surface, coverage level, case state, AR status, and action mode must come from the fixture phase/context, then be validated by `validateResolvedSurfaceContext`.
- URL, localStorage, sessionStorage, query params, or route path must not become authority sources for role, coverage, case state, AR status, action mode, or surface.
- Phase 0 maps to P1 `P1_CASE_DETAIL` with no submitted AR.
- Phase 1 maps to P1 `P1_CASE_DETAIL` with submitted AR, `PENDING_APPROVAL`, and `action_mode === null`.
- Phase 2 maps to P2 `P2_APPROVAL` with `PENDING_APPROVAL` and no selected action mode.
- Phase 3 maps to P2 `P2_APPROVAL` with `OBSERVATION_WINDOW` and `OBSERVE_ONLY`.
- Phase 4 maps to P2 `P2_APPROVAL` after window expiry, back to pending approval with `action_mode === null`.
- Phase 5 maps to P2 `P2_APPROVAL` with approved pending execution and `IMMEDIATE`.
- Phase 6 maps to P3 `P3_MANAGER` as read-only review context without host-level raw evidence payload in the adapted context or DOM.
- `fixture_meta` must mark fully artificial mock-only bounded frontend use.
- The adapter must fail closed or throw a test-visible error if a fixture phase is missing required data.

## 8. Required Tests

Unit tests must cover:

- repo-local fixture hash matches expected SHA256 or equivalent fixture integrity assertion is recorded in closeout;
- adapter returns exactly seven phase contexts for Phase 0-6;
- each adapted phase passes `validateResolvedSurfaceContext`;
- Phase 0 has no `action_request`;
- Phase 1 has `action_mode === null`;
- Phase 2 has P2 role and `P2_APPROVAL` surface;
- Phase 3 has `OBSERVE_ONLY` and observation-window context;
- Phase 4 returns to pending approval without browser timer authority;
- Phase 5 has `IMMEDIATE` only under P2;
- Phase 6 has P3 role and `P3_MANAGER` surface without privileged raw technical payload;
- URL/localStorage/sessionStorage authority injection is not used by the adapter.

Component tests, if `App.tsx` is touched, must also cover:

- existing mock phase selector remains visible and labeled as mock fixture context;
- selecting Phase 1 still shows Waiting on P2 / pending approval state;
- selecting Phase 6 still keeps host-level raw evidence absent from DOM;
- coverage badge remains fixture-derived `Coverage L2` even if URL or storage claims `L3`;
- P1 still does not expose `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` controls.

## 9. Required Commands

Frontend:

```powershell
cd frontend
npm run test -- --run
npm run build
```

Backend guard:

```powershell
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
```

Repo hygiene:

```powershell
git diff --check
```

Review:

```text
Claude Code focused review via claude-cmd after implementation diff.
```

Claude Web/external review is conditional and required only if implementation:

- changes root authority semantics from E0-01;
- loosens `ContextValidator`;
- changes product semantics beyond fixture phase adaptation;
- introduces Storybook, Playwright, backend/runtime/API/schema, route handoff, cross-surface propagation, or real-data behavior;
- conflicts with PRD, Model Contracts, Walkthrough v0.2, fixture v0.1, or Go/No-Go mandatory trigger categories.

## 10. HOLD Conditions

HOLD immediately if:

- implementation requires files outside the allowed list;
- fixture hash differs from expected source hash;
- adapter needs to loosen `ContextValidator`;
- a fixture phase cannot be represented as a valid `ResolvedSurfaceContext`;
- URL/localStorage/sessionStorage is used as an authority source;
- P3 raw host evidence is attached to the adapted context or DOM and merely hidden;
- implementation requires Storybook, Playwright, backend/runtime/API/schema, route handoff, P1/P2/P3 new page scope, or cross-surface propagation;
- implementation introduces real data, sanitized real data, secrets, credentials, network calls, launch, deploy, public endpoint, or external pilot behavior;
- implementation adds broad abstraction, registry, platform helper, global store, service layer, or cleanup refactor;
- tests cannot be run;
- review surface is unavailable and closeout would claim review PASS anyway.

## 11. Rollback

Rollback condition:

```text
Revert E0-02 adapter/app/test/checklist/route/handoff changes if fixture integrity fails, adapted phases fail validation, frontend tests/build fail, backend guard fails, review finds blocking issues, scope expands outside allowed files, or HOLD triggers fire.
```

## 12. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- execution surface is `codex`;
- scope is small and authority-sensitive;
- E0-02 depends directly on the E0-01 validator contract;
- no separate SWE exact sub-ticket has been created.

## 13. Decision

Decision:

```text
READY_FOR_JARVIS_IMPLEMENTATION_GO
```

Authorized next technical action after Jarvis GO:

```text
Implement E0-02 inside the exact allowed file scope, then run the required gates and focused review.
```

Not authorized yet:

```text
implementation, stage, commit, push, Jira cloud mutation, launch, deploy, real data, external pilot
```
