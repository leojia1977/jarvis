# S6 CD-T06 State Header Isolated Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `CD-T06` |
| Title | Case Detail state header for `CLOSED / OBSERVATION_WINDOW / APPROVED_PENDING_EXECUTION` |
| Decision | `ISOLATED_CHECKLIST_HOLD_MISSING_CLOSED_FIXTURE_AND_VISUAL_FRAMES` |
| Primary implementor | Codex for checklist only |
| Execution surface | codex |
| Reviewer | Claude Code required if later implementation diff exists |
| Review surface | claude-cmd |
| Workspace | VS Code / local repo |
| Implementation status | `NOT_STARTED` |
| Jira issue | `SCRUM-53` |
| Jira status | `To Do / HOLD comment synced` |

This checklist is isolation/readiness only. It does not implement `CD-T06`, does not mark `CD-T06` Done, and does not authorize a state-header implementation.

## 2. Checklist Decision

Decision:

```text
ISOLATED_CHECKLIST_HOLD_MISSING_CLOSED_FIXTURE_AND_VISUAL_FRAMES
```

Meaning:

- `AP-T10` has closed the display-only D-02 badge/pill mapping dependency.
- Existing repo can render `OBSERVATION_WINDOW` and `APPROVED_PENDING_EXECUTION` through Phase 3 / Phase 5 fixture states.
- Existing repo does not provide a renderable `CLOSED` fixture state.
- `VF-11`, `VF-12`, and `VF-13` remain missing as final visual frames for observation-window, approved-pending-execution, and closed-state header treatment.
- Implementing full `CD-T06` now would either leave `CLOSED` untestable or require fixture/adapter/validator changes, which are outside this ticket's current allowed scope.

Therefore the checklist returns `HOLD`, and the authorized conditional implementation GO does not activate.

## 3. Exact Current Repo Evidence

Existing files already contain:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

Current useful evidence:

- `CASE_STATE_LABELS` includes `CLOSED`, `OBSERVATION_WINDOW`, and `APPROVED_PENDING_EXECUTION`.
- `AR_STATUS_DISPLAY` includes D-02-derived display labels for `OBSERVATION_WINDOW` and `APPROVED_PENDING_EXECUTION`.
- `case-state-pill` already reflects the current resolved case state.
- `ar-status-pill` already records `data-ar-status`, `data-interaction-class`, `data-action-authority`, and `data-state-migration="none"`.

Current missing evidence:

- no renderable mock fixture phase with `case_state=CLOSED`;
- no `CLOSED` Case Detail state-header assertion;
- no delivered `VF-11`, `VF-12`, or `VF-13` final visual frame;
- no exact implementation plan that covers all three required states without touching fixture/adapter/validator or `ResolvedSurfaceContext`.

## 4. Future Implementation Conditions

A later `CD-T06` implementation may proceed only after a new checklist proves all of:

```text
CLOSED renderable fixture/context exists: YES
VF-11/VF-12/VF-13 or approved semantic skeleton substitute exists: YES
Allowed files are exact: YES
Test command is exact: YES
No fixture/adapter/validator/ResolvedSurfaceContext change required: YES
No D-02/product/contract conflict: YES
```

Likely allowed implementation files if the HOLD clears:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

## 5. Non-Authorization

This checklist does not authorize:

- implementing `CD-T06`;
- adding or modifying mock fixture phases;
- changing fixture registry, fixture adapter, ContextValidator, or `ResolvedSurfaceContext`;
- creating final visual treatment for `VF-11`, `VF-12`, or `VF-13`;
- adding approval controls, action controls, state transitions, observation-window timers, stale-approve behavior, or audit summaries;
- backend/runtime/API/schema changes;
- Storybook, Playwright, real data, anonymized real data, secrets, deploy, public endpoint, or external pilot.

## 6. HOLD Conditions

HOLD remains active while:

- `CLOSED` cannot be rendered under the current fixture/context model;
- visual-frame semantics for state header remain missing or ambiguous;
- implementation requires files outside the allowed frontend three-file scope;
- implementation requires fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- implementation would weaken D-02 labels, terminal-lock semantics, or observation-window return-to-pending semantics.

## 7. Next Route

```text
OPEN_AP_T02_P0_READONLY_APPROVAL_READINESS_CHECKLIST
```
