# S6 CD-T06 Unblock Pack 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `CD-T06` |
| Title | Case Detail state header unblock pack |
| Status | LOW_RISK_QUEUE_OUTPUT_HOLD_REMAINS |
| Queue item | `LR-02` |
| Date | 2026-04-27 |
| Current checklist | `docs\S6_CD_T06_STATE_HEADER_ISOLATED_CHECKLIST_2026_04_27.md` |

This pack explains exactly what is missing before `CD-T06` can reopen.

It does not authorize implementation, fixture changes, visual PASS, backend/runtime/API/schema changes, or `ResolvedSurfaceContext` changes.

## 2. Current HOLD

Decision remains:

```text
ISOLATED_CHECKLIST_HOLD_MISSING_CLOSED_FIXTURE_AND_VISUAL_FRAMES
```

Why:

- `AP-T10` already closed display-only D-02 badge/pill mapping.
- Current repo can render `OBSERVATION_WINDOW` and `APPROVED_PENDING_EXECUTION`.
- Current repo cannot render a `CLOSED` Case Detail fixture/context.
- `VF-11`, `VF-12`, and `VF-13` are missing for full state-header treatment.

## 3. Three Separate Missing Inputs

| Input type | Missing item | Why it matters |
| --- | --- | --- |
| Fixture reachability | Renderable `CLOSED` context | Tests cannot prove the third required state without it. |
| Visual semantics | `VF-11`, `VF-12`, `VF-13` or approved semantic substitutes | State-header treatment must not be invented by implementation. |
| File/test scope | Exact allowed implementation files and test command after inputs exist | Prevents state-header work from leaking into fixture/validator or backend scope. |

## 4. Minimum Reopen Conditions

`CD-T06` can move from HOLD to launch checklist only when all are true:

```text
CLOSED renderable context exists: YES
OBSERVATION_WINDOW renderable context remains available: YES
APPROVED_PENDING_EXECUTION renderable context remains available: YES
VF-11/VF-12/VF-13 or approved semantic substitutes exist: YES
No fixture/adapter/validator/ResolvedSurfaceContext change is needed inside CD-T06: YES
Exact frontend files are named: YES
Exact test command is named: YES
```

## 5. Safe Future Scope If Reopened

Likely allowed implementation scope after inputs exist:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

Likely implementation shape:

- state-header semantic slot only;
- render current case state and AR status mapping;
- verify terminal/locked/read-only treatment;
- assert no approval/action controls are introduced;
- assert no timer/state migration is introduced.

## 6. Explicit Non-Authorization

This pack does not authorize:

- creating a new fixture phase;
- changing fixture registry, fixture adapter, ContextValidator, or `ResolvedSurfaceContext`;
- inventing final visual style for `VF-11`, `VF-12`, or `VF-13`;
- implementing observation-window timer or state migration;
- implementing approval controls, stale-approve behavior, audit summary, Storybook, Playwright, backend/runtime/API/schema, real data, secrets, deploy, public endpoint, or external pilot.

## 7. Recommended Request To Design / Fixture Owner

```text
Please provide renderable CLOSED state evidence and VF-11/VF-12/VF-13 state-header frame anchors for the already frozen CD-T06 semantics. This request is for existing state-header semantics only and does not request new workflow behavior.
```

