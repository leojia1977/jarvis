# S6 E0-01 ResolvedSurfaceContext Launch Checklist 2026-04-25

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 E0-01 ResolvedSurfaceContext Launch Checklist 2026-04-25 |
| Ticket | `E0-01` |
| Status | CLOSED_COMMITTED_PUSHED |
| Date | 2026-04-25 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Baseline commit | `d4a8d70` |
| Primary implementor | Codex |
| Execution surface | `codex` |
| Workspace surface | VS Code / local repo |
| Reviewer | Claude Code focused review |
| Review surface | `claude-cmd` |
| External review | Claude Web architecture/governance review PASS obtained |
| SWE | disabled |

This ticket launches Sprint 0 `E0-01` only.

It creates the root frontend surface-context authority and fail-closed validation foundation required before Storybook first story set, Playwright seed, or P1/P2/P3 page composition.

## 2. Human Authorization

Jarvis authorized:

```text
Approve Sprint 0 E0-01 launch.
Codex is Primary Implementor.
Execution surface: codex.
Workspace: VS Code / local repo.
SWE disabled.
Claude Code performs focused code review.
Claude Web performs architecture/governance review because E0-01 defines root rendering authority and fail-closed validation behavior.
Scope is limited to ResolvedSurfaceContext + ContextValidator + SH-08 + unit/component tests.
No page implementation.
No Storybook cross-surface stories.
No Playwright E2E.
No backend/runtime/API/schema.
No real data.
No secrets.
No deploy.
No external pilot.
No stage/commit/push without Jarvis approval.
First create/update the exact E0-01 ticket launch checklist and route/handoff records, then implement E0-01 only.
Proceed with E0-01 only.
```

## 3. Source Authority

Current governed source-of-truth remains:

- `SecuPilot_Engineering_Executable_PRD_v1.0_冻结版.md`
- `SecuPilot_Build_Ready_Implementation_GoNoGo_Record_v0.2.1.md`
- `SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx`
- `SecuPilot_Visual_Kickoff_Frame_Checklist_v0.3.xlsx`
- `docs\S6_G0_PRE_START_CONFIRMATION_2026_04_25.md`

New incoming execution-gate inputs:

- `SecuPilot_Frontend_Sprint_0_Execution_Checklist_and_PR_Review_Gate_v0.2.md`
- `SecuPilot_PR_Brief_E0-01_ResolvedSurfaceContext_ContextValidator_SH-08_v0.2.md`

Version reconciliation:

```text
Accept the new Sprint 0 / E0-01 technical gate and PR brief.
Do not roll tracker source of truth back to Backlog Tracker v0.2.
GoNoGo v0.2.1, Backlog Tracker v0.4, Visual Kickoff v0.3, and G0 confirmation remain current.
```

## 4. Exact Scope

Implement only:

1. `ResolvedSurfaceContext` TypeScript type contract.
2. `ContextValidator` fail-closed validation.
3. `SH-08 / Security Halt` sanitized component.
4. Minimal `ResolvedSurfaceContextProvider` / fixture-provider skeleton that validates input before rendering children.
5. Unit/component tests for the above.

No current page route, app shell, Storybook story, Playwright test, backend/runtime/API/schema, data model, or product behavior may be implemented under this ticket.

## 5. Exact Allowed Files

Allowed files:

- `docs/S6_E0_01_RESOLVED_SURFACE_CONTEXT_TICKET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/src/secupilot/surface/context/types.ts`
- `frontend/src/secupilot/surface/context/validateResolvedSurfaceContext.ts`
- `frontend/src/secupilot/surface/context/ResolvedSurfaceContextProvider.tsx`
- `frontend/src/secupilot/surface/components/SecurityHalt.tsx`
- `frontend/src/secupilot/surface/context/__tests__/validateResolvedSurfaceContext.test.ts`
- `frontend/src/secupilot/surface/context/__tests__/ResolvedSurfaceContextProvider.test.tsx`

No other file may be changed unless a HOLD is triggered and Jarvis explicitly expands scope.

## 6. Exact Non-Goals

This ticket must not implement:

- P1/P2/P3 page implementation or route handoff;
- Storybook cross-surface stories;
- Playwright E2E or Playwright dependency/config;
- backend/runtime/API/schema changes;
- existing `App.tsx` page refactor;
- real data, sanitized real data, external customer data, secrets, credentials, tokens, public endpoints;
- launch, deploy, external pilot, or readiness claims;
- new product requirements, design-system abstraction, service registry, platform layer, generalized framework, or cleanup refactor.

## 7. Required Semantics

Required:

- `surface` is required and must be validated.
- `role`, `coverageLevel`, `caseState`, `arStatus`, `actionMode`, and `surface` are governed enums.
- `action_request` absent means no AR submitted.
- `action_mode === null` means AR exists, but P2 has not decided ActionMode yet.
- P1 must never set or choose `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY`.
- `ContextValidator` must reject missing required fields.
- `ContextValidator` must reject unsupported enums.
- `ContextValidator` must reject surface-role mismatch.
- `ContextValidator` must reject P3 privileged raw technical payloads before rendering.
- `ContextValidator` must reject URL/storage authority attempts if such fields appear in context input.
- `ContextValidator` must reject fixture data that appears real or lacks `fixture_meta`.
- Invalid context must render `SH-08` without fallback, guessed defaults, or partial surface rendering.
- Business dialogue chips / product copy hardcoding is checked by review/lint/checklist, not by runtime shape validation.

Current Sprint 0 surface allowlist:

| Surface | Allowed role |
| --- | --- |
| `P1_CASE_DETAIL` | `P1` |
| `P2_APPROVAL` | `P2` |
| `P3_MANAGER` | `P3` |
| `CROSS_SURFACE` | test harness / walkthrough only |

## 8. Required Tests

Unit tests must cover:

- valid P1 context passes;
- valid P2 context passes;
- valid P3 context passes;
- missing `fixture_meta` fails;
- missing `surface` fails;
- unsupported `surface` fails;
- surface-role mismatch fails;
- missing required field fails;
- unsupported enum fails;
- unexpected top-level field fails;
- non-artificial / real-data-derived fixture fails;
- P3 context with host raw evidence fails;
- P1 context with P2-only action permission fails;
- URL/localStorage/sessionStorage authority injection field fails;
- coverage ceiling promotion attempt fails;
- action request absent is valid;
- action request present with `action_mode === null` is valid.

Component tests must cover:

- invalid context renders `SH-08`;
- `SH-08` does not render case evidence;
- `SH-08` does not render raw context JSON;
- valid context renders child surface placeholder.

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
Claude Web architecture/governance review required before closeout can claim full review pass.
```

## 10. HOLD Conditions

HOLD immediately if:

- implementation requires files outside allowed list;
- implementation requires existing page implementation or `App.tsx` refactor;
- implementation requires Storybook stories or Playwright E2E;
- implementation requires backend/runtime/API/schema changes;
- implementation requires real data, sanitized real data, secrets, credentials, production endpoint, launch, deploy, or external pilot;
- validator needs to be loosened to make fixture pass;
- invalid context requires fallback rendering, guessed role, guessed coverage, or partial surface rendering;
- P3 raw host evidence is attached to DOM and merely hidden;
- Claude Web mandatory architecture/governance review is unavailable at final closeout.

## 11. Rollback

Rollback condition:

```text
Delete E0-01 new frontend foundation files and revert route/handoff/checklist updates if tests fail, build fails, review finds blocking issues, Claude Web mandatory review cannot be queued/obtained for closeout, or HOLD triggers fire.
```

## 12. Decision

Decision:

```text
READY_FOR_EXACT_IMPLEMENTATION
```

Next action:

```text
Implement E0-01 only.
```

## 13. Implementation Result 2026-04-25

Implementation result:

```text
IMPLEMENTED_GATE_PASS_CLAUDE_WEB_PASS
```

Implemented files:

- `frontend/src/secupilot/surface/context/types.ts`
- `frontend/src/secupilot/surface/context/validateResolvedSurfaceContext.ts`
- `frontend/src/secupilot/surface/context/ResolvedSurfaceContextProvider.tsx`
- `frontend/src/secupilot/surface/components/SecurityHalt.tsx`
- `frontend/src/secupilot/surface/context/__tests__/validateResolvedSurfaceContext.test.ts`
- `frontend/src/secupilot/surface/context/__tests__/ResolvedSurfaceContextProvider.test.tsx`

Documentation files updated:

- `docs/S6_E0_01_RESOLVED_SURFACE_CONTEXT_TICKET_LAUNCH_CHECKLIST_2026_04_25.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`

Scope confirmation:

- no P1/P2/P3 page implementation;
- no Storybook story implementation;
- no Playwright E2E;
- no backend/runtime/API/schema changes;
- no real data, sanitized real data, secrets, deploy, launch, or external pilot work;
- no SWE execution.

E01-N01 surface validation disposition:

- `surface` is a required root `ResolvedSurfaceContext` field;
- missing `surface` fails closed with `SH-08_INVALID_CONTEXT_SHAPE`;
- unsupported `surface` fails closed with `SH-08_UNSUPPORTED_ENUM`;
- surface/role mismatch fails closed with `SH-08_SURFACE_ROLE_MISMATCH`;
- downstream fixture adapters must not introduce fallback rendering for missing or unsupported `surface`.

## 14. Gate Evidence 2026-04-25

Gate evidence:

- `npm run test -- --run` PASS, 25 tests passed;
- `npm run build` PASS;
- `py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view` PASS, 42 tests passed;
- `git diff --check` PASS;
- Claude Code focused review returned `NO BLOCKING FINDINGS` with one P2 closeout-before-finish finding;
- P2 finding fixed by applying raw technical payload rejection across all surfaces, not only P3;
- Claude Code follow-up review: prior P2 finding closed, `NO BLOCKING FINDINGS`;
- Claude Web architecture/governance review via governed AdsPower review-prompt transfer returned `E0-01_DECISION: PASS`.

Claude Web informational notes:

- simple real-data-like domain marker detection may produce false positives in future synthetic fixtures; this is acceptable for Sprint 0 because fail-closed behavior is intended;
- visible `SecurityHaltCode` reason text is acceptable for the current development/test surface, with possible future hardening;
- non-P2 `action_mode === null` behavior is intentional and matches ticket semantics.

Claude Web architecture/governance review:

```text
PASS
```

Reason:

`E0-01` defines root rendering authority and fail-closed validation behavior. Claude Code review did not replace the mandatory Claude Web architecture/governance review; Claude Web review was obtained on 2026-04-25 through the governed AdsPower review-prompt transfer path and returned `E0-01_DECISION: PASS`.

Non-authorization:

```text
Claude Web PASS is review evidence only. It does not authorize launch, deploy, real data, external pilot, stage, commit, or push.
```

## 15. Closeout State

Current closeout state:

```text
CLOSED_COMMITTED_PUSHED
```

Closeout commit:

```text
aaaa199 Implement Sprint 0 E0-01 surface context
```

The Claude Web architecture/governance review gate no longer blocks E0-01. `E0-02`, `E0-03`, and `E0-04` remain subject to their own per-ticket launch checklists and Jarvis GO before implementation.
