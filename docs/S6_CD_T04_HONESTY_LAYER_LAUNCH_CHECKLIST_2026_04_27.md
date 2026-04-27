# S6 CD-T04 Honesty Layer Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 CD-T04 Honesty Layer Launch Checklist 2026-04-27 |
| Ticket | `CD-T04` |
| Scope | Honesty layer display / fold / no silent disappearance |
| Status | READY_FOR_SEPARATE_IMPLEMENTATION_GO_WITH_BOUNDS |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Route | `OPEN_CD_T04_HONESTY_LAYER_LAUNCH_CHECKLIST` |
| Primary implementor | Codex if later authorized |
| Execution surface | `codex` |
| Reviewer | Claude Code focused review after implementation diff |
| Review surface | `claude-cmd` |
| External review | not required unless Go/NoGo Section 9 or AI_COLLAB mandatory trigger fires |
| SWE | disabled unless Jarvis creates a separate exact SWE sub-ticket |

This launch checklist prepares `CD-T04 - honesty layer display/fold/no silent disappearance`.

It does not authorize implementation. It defines exact bounds for a later implementation GO.

## 2. Decision

Decision:

```text
READY_FOR_SEPARATE_IMPLEMENTATION_GO_WITH_BOUNDS
```

Meaning:

- Current repo behavior already shows the `HONESTY` narrative section and unsupported claims.
- `CD-T04` is not closed because fold/no-silent-disappearance behavior needs an exact implementation pass.
- The next code step requires a separate Jarvis implementation GO.

## 3. Current Repo Evidence

Current coverage:

- `CaseDetail` renders `HONESTY` as one narrative-spine section.
- `buildWorkbenchCase` populates honesty text from `unsupported_claims`, `what_would_raise_confidence`, and `what_would_disprove_current_verdict`.
- Existing tests assert the `HONESTY` heading and unsupported-claims text are visible.

## 4. Exact Future Scope

If implementation is later authorized, it may do only the following:

- make the honesty layer explicitly persistent and testable;
- add a minimal fold/expand affordance if needed, without hiding unsupported claims silently;
- ensure unsupported claims remain visible or explicitly restorable after fold interaction;
- add tests proving honesty content does not disappear under lower coverage or interaction.

## 5. Exact Allowed Files For Later Implementation

Allowed files for a later implementation GO:

- `docs/S6_CD_T04_HONESTY_LAYER_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

No other files may be changed without HOLD.

## 6. Required Tests For Later Implementation

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

## 7. Non-Goals

This ticket must not implement:

- new product summary claims;
- P2/P3 approval or manager behavior;
- Search/History;
- route handoff or cross-surface propagation;
- fixture registry, adapter, validator, or resolved-context changes;
- backend/runtime/API/schema changes;
- Storybook or Playwright changes;
- real data, secrets, deploy, public endpoint, or external pilot behavior.

## 8. HOLD Conditions

HOLD if:

- implementation requires files outside the allowed list;
- implementation requires visual interpretation beyond the exact honesty/fold/no-silent-disappearance scope;
- unsupported claims are hidden without an explicit visible affordance to restore them;
- implementation changes P1/P2/P3 authority, route, fixtures, adapter, validator, backend/runtime/API/schema, real data, secrets, deploy, public endpoint, or external pilot behavior;
- tests cannot be named exactly.

## 9. Jira Sync

Jira cloud mutation:

```text
NOT_SYNCED_LAUNCH_ONLY
```

Reason: launch checklist only. Do not mark Done and do not start implementation without separate GO.

## 10. Next Safe Action

Next safe automation action:

```text
WAIT_FOR_JARVIS_CD_T04_IMPLEMENTATION_GO_OR_NEXT_EXACT_BOUNDED_TICKET_SELECTION
```

