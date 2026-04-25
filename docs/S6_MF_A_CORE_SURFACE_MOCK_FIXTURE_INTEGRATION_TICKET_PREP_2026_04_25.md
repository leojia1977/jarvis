# S6-MF-A Core Surface Mock Fixture Integration Ticket Prep 2026-04-25

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6-MF-A Core Surface Mock Fixture Integration Ticket Prep 2026-04-25 |
| Ticket | `S6-MF-A` |
| Scope | Core Surface mock fixture integration |
| Status | IMPLEMENTED_GATE_PASS_PENDING_STAGE_COMMIT_PUSH |
| Date | 2026-04-25 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `66b45c8` |
| Source fixture | `D:\产品设计\secupilot0421\incoming_pending\secupilot_core_surface_fixture_v0.1.json` |
| Source fixture SHA256 | `814F21AACFE2E2B25514990188F9801D81F0ED4A464F7A03B05DD235E4A02B47` |
| Fixture planning record | `SecuPilot_Core_Surface_Mock_Fixture_Integration_v0.1.md` |
| Storybook plan | `SecuPilot_Storybook_Cross_Surface_Stories_v0.1.md` |
| Playwright plan | `SecuPilot_Playwright_E2E_Acceptance_Plan_v0.1.md` |
| Lane | Yellow bounded frontend implementation after this prep |
| Execution surface | `codex` |
| Review surface | `claude-cmd` focused review, if available at closeout |

This record converts the core-surface fixture package into a repo-local, mock-only implementation ticket.

It does not authorize launch, deploy, public endpoint work, external pilot execution, real-data handling, credential handling, backend/API/schema changes, static HTML copy, Storybook dependency setup, Playwright dependency setup, P1 to P2 AR propagation, P2 to P3 audit propagation, cross-surface route handoff, AI_COLLAB changes, SWE execution, staging, commit, or push by itself.

## 2. Governing Product Sources

Use this authority order:

1. `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版 (2).md`
2. `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2 (1).md`
3. `SecuPilot_Core_Surface_Logic_Collision_Walkthrough_v0.2.md`
4. `SecuPilot_Core_Surface_Mock_Fixture_Integration_v0.1.md`
5. `secupilot_core_surface_fixture_v0.1.json`
6. P1/P2/P3 Model Contracts
7. Storybook and Playwright planning records as later-tooling guidance only

Binding team instruction:

```text
HTML is visual and interaction prototype. Model Contract, PRD, Walkthrough v0.2, fixture, and Playwright plan are the implementation basis. All implementation must remain mock-only / bounded implementation, with no real data, no launch, and no deploy.
```

## 3. Exact Behavior

Implement repo-local mock fixture integration for the current frontend app.

Required behavior:

| Area | Required behavior |
| --- | --- |
| Fixture import | Copy the source fixture exactly into `frontend/fixtures/secupilot_core_surface_fixture_v0_1.json` and verify SHA256 match against the incoming source. |
| Mock-only resolved context | Add a local resolved context derived from the fixture `phases` array. Role, coverage, case id, case state, AR status, and surface label must come from the selected fixture phase/context, not URL/localStorage/sessionStorage. |
| Phase selector | Add a visible mock phase selector for Phase 0-6. It may be simple and local, but must clearly label itself as mock fixture context. |
| P1 Case Detail bridge | Use the fixture case, evidence panels, honesty layer, and phase state to drive the existing Case Detail surface. |
| Data boundary | Keep fixture data local and synthetic. No network calls, no real data, no persistence, no browser storage source-of-truth. |
| Existing controls | Preserve P1-CD-A and P1-CD-B behavior: narrative spine, evidence Auto/Manual, Pin/Unpin, click/focus fallback, and always-visible follow-up input. |

Known fixture v0.1 alignment notes:

- Walkthrough examples use `AR-2847-001`; fixture uses `AR-2847-ISO-001`.
- Walkthrough observation-window example uses `30m`; fixture uses `60`.
- Walkthrough approval event name is `APPROVE_NOW_CONFIRMED`; fixture uses `APPROVED_AFTER_WINDOW`.

These notes do not block S6-MF-A because this ticket imports the fixture as-is and records the current source-of-truth values. They should be reconciled before Playwright E2E assertions are frozen.

## 4. Exact Non-Goals

This ticket must not implement:

- Storybook dependency installation or story files;
- Playwright dependency installation or E2E files;
- P2 Approval Surface implementation;
- P3 Manager View implementation;
- P1 Action Request modal;
- P1 submission to P2;
- P1 post-submit `Waiting on P2` propagation beyond fixture-driven local display;
- P2 to P3 audit propagation;
- cross-surface route handoff;
- AR status migration E2E;
- observation-window backend signaling, polling, WebSocket, or concurrency conflict handling;
- backend/API/schema changes;
- real-data integration;
- localStorage/sessionStorage/URL-based authorization or coverage;
- static HTML prototype copy/paste;
- launch/deploy/public endpoint/external pilot behavior.

## 5. Exact Allowed Files

Allowed files for this ticket:

- `docs/S6_MF_A_CORE_SURFACE_MOCK_FIXTURE_INTEGRATION_TICKET_PREP_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `frontend/fixtures/secupilot_core_surface_fixture_v0_1.json`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`
- `frontend/tsconfig.json` only if TypeScript JSON import requires include-path adjustment

No other file may be changed for S6-MF-A unless a HOLD is triggered and a new decision record expands scope.

## 6. Required Tests

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

## 7. Required Assertions

Automated or closeout-visible assertions must cover:

- fixture case `CASE-2847` renders in Inbox and Case Detail;
- coverage badge renders fixture-derived `Coverage L2`;
- phase selector renders Phase 0-6 and is labelled as mock fixture context;
- selecting Phase 1 renders `PENDING_APPROVAL` / Waiting on P2 fixture state;
- selecting Phase 6 renders role/surface context from the fixture without exposing P3 host raw evidence DOM;
- P1 evidence Auto/Manual + Pin controls still work after fixture integration;
- no `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` controls are exposed to P1;
- no URL/localStorage/sessionStorage is used as role or coverage source of truth.

## 8. Max Change Budget

Maximum expected implementation scope:

- one repo-local fixture JSON file copied from incoming source;
- one local fixture-to-workbench view-model mapping inside the current frontend app;
- one mock phase selector UI;
- focused CSS for phase selector and resolved context labels;
- focused test assertions for fixture loading and phase context.

Do not introduce new modules, helpers, directories beyond `frontend/fixtures`, dependencies, Storybook, Playwright, routers, stores, service layers, or generalized component registries.

## 9. SWE Agent Use

```text
SWE agent use: not authorized for this ticket.
```

Reason:

- execution surface is currently `codex`;
- the ticket is small and tightly coupled to the current frontend scaffold;
- no separate SWE command path is required for this bounded implementation.

## 10. Review Path

Required review path:

```text
Focused code review after implementation diff, preferably via claude-cmd / Claude Code if available.
```

Claude Web / external product-architecture-governance review is not required for this ticket unless implementation:

- changes product semantics beyond mock fixture integration;
- claims broad P1/P2/P3 architecture readiness;
- introduces Storybook/Playwright tooling dependencies;
- introduces backend/API/schema behavior;
- implements cross-surface state propagation;
- conflicts with PRD, Model Contracts, Walkthrough v0.2, or fixture v0.1;
- touches Red/HOLD trigger categories from the Go/No-Go record.

## 11. Rollback

Rollback condition:

```text
Revert S6-MF-A frontend and ticket-prep changes if frontend tests/build fail, backend guard fails, fixture hash does not match source, scope expands outside allowed files, or HOLD triggers fire.
```

## 12. HOLD Conditions

HOLD if:

- fixture source hash cannot be verified;
- implementation requires files outside the allowed file list;
- implementation needs backend/API/schema work;
- implementation introduces Storybook or Playwright dependencies;
- implementation tries to copy static HTML prototype code into the app;
- implementation starts implementing P2 Approval Surface or P3 Manager View pages;
- implementation begins P1 to P2 AR propagation or P2 to P3 audit propagation;
- URL/localStorage/sessionStorage becomes a source of authority for role, coverage, or state;
- real data, credentials, network calls, launch, deploy, public endpoint, or external pilot behavior appear;
- hardcoded final business chips, unlock messages, ROI values, queue windows, or CMDB tags are introduced outside the fixture;
- a broad abstraction, registry, platform helper, new module, or service layer appears;
- tests cannot be run;
- review surface is unavailable and closeout would claim review PASS anyway.

## 13. Decision

Decision:

```text
READY_FOR_EXACT_TICKET
```

Authorized next technical action:

```text
Implement S6-MF-A inside the exact allowed file scope, then run the required gates.
```

## 14. Implementation Closeout 2026-04-25

Implementation status:

```text
S6-MF-A IMPLEMENTED_GATE_PASS
```

Files changed:

- `docs/S6_MF_A_CORE_SURFACE_MOCK_FIXTURE_INTEGRATION_TICKET_PREP_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `frontend/fixtures/secupilot_core_surface_fixture_v0_1.json`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

Implemented behavior:

- copied `secupilot_core_surface_fixture_v0.1.json` into repo-local `frontend/fixtures/secupilot_core_surface_fixture_v0_1.json`;
- verified repo-local fixture SHA256 matches incoming source SHA256 `814F21AACFE2E2B25514990188F9801D81F0ED4A464F7A03B05DD235E4A02B47`;
- added mock-only resolved context from fixture phases;
- added visible Phase 0-6 mock fixture selector;
- mapped fixture case, evidence panels, honesty layer, phase state, role, surface, and AR status into the existing frontend app;
- preserved P1-CD-A/P1-CD-B Case Detail behavior, evidence Auto/Manual, Pin/Unpin, click/focus fallback, and follow-up input;
- filtered host-level raw evidence from the Phase 6 P3 resolved context;
- kept role/coverage/case_state sourced from fixture context, not URL/localStorage/sessionStorage.

Out-of-scope work not done:

- no Storybook setup;
- no Playwright setup;
- no P2 Approval Surface implementation;
- no P3 Manager View implementation;
- no P1 to P2 AR propagation;
- no P2 to P3 audit propagation;
- no route handoff;
- no backend/API/schema work;
- no real data, launch, deploy, public endpoint, or external pilot behavior.

Focused review:

```text
claude.cmd --print focused review: P1 issues found and fixed
claude.cmd --print re-review: NO BLOCKING FINDINGS
```

Review notes accepted:

- disabled unavailable role buttons with native `disabled`;
- derived WHY / INTENT evidence mapping and tests from fixture helpers;
- replaced UI separator glyphs in code with ASCII separators.

Gate results:

```text
npm run test -- --run
Result: PASS, 9 tests passed

npm run build
Result: PASS

py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
Result: PASS, 42 tests passed
```

Commit state:

```text
Not staged, not committed, not pushed in this closeout.
```
