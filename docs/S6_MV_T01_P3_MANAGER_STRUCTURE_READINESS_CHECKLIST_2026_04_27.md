# S6 MV-T01 P3 Manager Structure Readiness Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 MV-T01 P3 Manager Structure Readiness Checklist 2026-04-27 |
| Ticket | `MV-T01` |
| Scope | `/manager page structure and KPI cards readiness only` |
| Status | READINESS_CHECKLIST_PASS_IMPLEMENTATION_REQUIRES_G0_05_AND_SEPARATE_GO |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| P3 contract source | `D:\产品设计\secupilot0421\incoming_pending\SecuPilot_P3_Manager_View_Model_Contract_v0.1.md` |
| Authority pack | `docs\S6_P2_P3_AUTHORITY_REVIEW_PACK_2026_04_27.md` |
| Claude Web review | `docs\S6_P2_P3_AUTHORITY_CLAUDE_WEB_REVIEW_2026_04_27.md` |
| G0 pre-start record | `docs\S6_G0_PRE_START_CONFIRMATION_2026_04_25.md` |
| Staged authorization | `docs\S6_STAGED_ACCELERATION_AUTHORIZATION_2026_04_27.md` |
| Primary implementor | Codex if later implementation GO is granted |
| Execution surface | codex |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review if implementation diff exists |
| Review surface | claude-cmd |
| External review | Claude Web returned `PASS_WITH_NOTE`; note is converted into launch guard |
| SWE | disabled |

This checklist is readiness-only. It does not implement `/manager`, does not mark `MV-T01` Done, and does not authorize P3 Manager View implementation.

## 2. Checklist Decision

Decision:

```text
READINESS_CHECKLIST_PASS_IMPLEMENTATION_REQUIRES_G0_05_AND_SEPARATE_GO
```

Interpretation:

- `MV-T01` authority questions have been externally reviewed by Claude Web.
- Claude Web returned `PASS_WITH_NOTE`.
- The note can be converted into a concrete future implementation guard.
- Implementation remains unauthorized until:
  - `G0-05 P3 Contract full ratification` is repo-locally confirmed for first P3-MV implementation;
  - a separate explicit `MV-T01 implementation GO` is granted;
  - exact files and tests remain limited to the narrow scope below.

## 3. Authority Evidence

Claude Web confirmed:

- `/manager` is the P3 main work surface.
- `MV-T01` scope is P3 page structure and KPI cards only.
- P0/P2 degraded/read-only manager variants remain later `MV-T02` scope.
- KPI values must come from mock fixture fields and must not be inferred by frontend logic.
- `MV-T01` must not implement approval audit summary; that remains `MV-T04` scope.
- `MV-T01` must not implement deep-link handoff; that remains `MV-T03` scope.
- P3 context missing must fail closed through SH-08 rather than guessed defaults.
- Host raw evidence must not be attached to the DOM.

Claude Web non-blocking note converted into hard launch guard:

```text
MV-T01 must not pre-reserve conditional rendering slots or placeholders for P0/P2 variants.
The MV-T01 implementation should not add role === P0 or role === P2 branches.
```

## 4. Current Repo Discovery

Current app state:

- `frontend/src/App.tsx` already declares a `manager_view` nav item for P3, but it is inactive.
- There is no active `/manager` route.
- Existing P3-related renderability hooks are limited to cautious summary / raw-evidence absence checks inside current mock redline and Case Detail flows.
- No Manager View page structure, KPI cards, deep-link handoff, approval audit summary, or P0/P2 manager variant exists.

This means `MV-T01` can be a narrow future implementation candidate, but it is not already repo-covered.

## 5. Required Before Implementation GO

Before implementation can start, a governed record must confirm:

```text
G0-05 P3 Contract full ratification confirmed for first P3-MV implementation: YES
MV-T01 implementation GO granted: YES
No P0/P2 placeholder or conditional branch in MV-T01: YES
No approval audit summary in MV-T01: YES
No deep-link handoff in MV-T01: YES
No host raw evidence DOM: YES
```

If `G0-05` remains only scheduled, `MV-T01` stays readiness-complete but implementation-HOLD.

## 6. Future Implementation Scope If Separately Authorized

A later implementation may do only:

- add a bounded `/manager` route shell for resolved role `P3`;
- activate the existing `Manager View` navigation only for P3;
- render P3 page structure / skeleton for Manager View main regions;
- render KPI card shells using mock fixture fields only, with `—` / data-unavailable when fields are absent;
- render read-only boundary anchors proving no approval workflow action is available;
- fail closed through SH-08 or a data-unavailable safe state when P3 context is missing;
- add stable test ids and semantic attributes proving P3-only route authority comes from `ResolvedSurfaceContext`;
- add regression tests proving host raw evidence, approval controls, approval audit summary, deep-link handoff, and P0/P2 placeholders are not attached.

## 7. Exact Non-Goals

Do not implement:

- P0/P2 Manager View variants, placeholders, conditional branches, or reserved slots;
- approval audit summary (`MV-T04`);
- Manager deep-link handoff (`MV-T03`);
- approval CTA, approval queue, state migration, observation-window behavior, stale-approve behavior, or AP acceptance suite;
- P2 approval controls or P1 action controls;
- host raw evidence, process raw evidence, technical panels, or evidence drawer content inside Manager View;
- frontend-inferred KPI values, ROI numbers, queue counts, MTTA, MTTR, or business chips;
- new P3 summary fields, new unsupported-claims semantics, or over-certain management copy;
- fixture registry changes, fixture adapter changes, validator changes, or `ResolvedSurfaceContext` changes;
- backend/runtime/API/schema changes;
- Storybook, Playwright, real data, anonymized real data, secrets, deploy, public endpoint, or external pilot.

## 8. Exact Files For Later Narrow Implementation

If `G0-05` is confirmed and implementation is separately authorized, current repo discovery indicates the likely exact implementation files are:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

No other implementation files are justified by this checklist without a new launch record.

Governance files for a later implementation closeout may include:

```text
docs/S6_MV_T01_P3_MANAGER_STRUCTURE_READINESS_CHECKLIST_2026_04_27.md
docs/S6_MV_T01_P3_MANAGER_STRUCTURE_CLOSEOUT_2026_04_27.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
```

## 9. Required Gate For Later Implementation

Minimum gate:

```powershell
cd frontend
npm run test -- --run
npm run build
cd ..
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
git diff --check
```

Claude Code focused review is required for any implementation diff.

## 10. HOLD Conditions

HOLD implementation if:

- `G0-05 P3 Contract full ratification` is not repo-locally confirmed;
- implementation needs files outside the exact list;
- implementation needs P0/P2 Manager placeholders, conditional branches, or variants;
- implementation needs approval audit summary, deep-link handoff, or cross-page summary output;
- implementation needs approval controls, AP workflow, state transition behavior, confirmation modal, audit chain, observation-window countdown, or stale-approve handling;
- implementation needs host raw evidence, process raw evidence, technical panels, inferred KPI values, ROI numbers, queue counts, MTTA, MTTR, or static business chips;
- implementation needs fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- implementation needs backend/runtime/API/schema work;
- tests/build fail and cannot be corrected inside the exact ticket scope;
- Claude Code review raises a blocking finding;
- any mandatory external-review trigger fires.

## 11. Next Safe Action

Next safe action:

```text
OPEN_SH_T07_RECONCILIATION_OR_GS_T05_REGRESSION_CHECKLIST_OR_CREATE_G0_05_REPO_LOCAL_SIGNOFF_RECORD
```
