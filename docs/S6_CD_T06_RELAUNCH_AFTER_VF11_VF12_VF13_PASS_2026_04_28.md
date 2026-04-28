# S6 CD-T06 Relaunch After VF-11 / VF-12 / VF-13 PASS 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `CD-T06` |
| Title | Case Detail state header relaunch after visual-frame PASS |
| Status | `PARTIAL_UNBLOCK_FULL_HOLD_MISSING_CLOSED_CONTEXT` |
| Date | 2026-04-28 |
| Jira | `SCRUM-53` remains `待办` |

## 2. Relaunch Inputs

Visual baseline reconciliation:

```text
docs/S6_VISUAL_BASELINE_VF03_VF11_VF12_VF13_RECONCILIATION_2026_04_28.md
```

Relevant accepted frames:

- `VF-11` for `OBSERVATION_WINDOW`;
- `VF-12` for `APPROVED_PENDING_EXECUTION`;
- `VF-13` for `CLOSED`.

## 3. Decision

```text
CD_T06_RELAUNCH_PARTIAL_UNBLOCK_FULL_HOLD_MISSING_CLOSED_RENDERABLE_CONTEXT
```

The previous visual-frame blocker is removed. The full `CD-T06` ticket remains HOLD because current renderable fixture phases still do not provide a `CLOSED` Case Detail context without fixture/adapter/context expansion.

## 4. Current Repo Evidence

Already renderable:

- `OBSERVATION_WINDOW` through phase 3;
- `APPROVED_PENDING_EXECUTION` through phase 5;
- `CASE_STATE_LABELS.CLOSED` as a label only.

Still missing:

- renderable `CLOSED` resolved context / phase;
- Case Detail test that can assert `CLOSED` state header without changing fixtures;
- exact proof that full `CD-T06` can be implemented inside frontend-only files.

## 5. Safe Split Recommendation

To keep automation moving without inventing fixture scope, split future work:

```text
CD-T06A: existing renderable states header skeleton
  - OBSERVATION_WINDOW
  - APPROVED_PENDING_EXECUTION
  - no CLOSED claim

CD-T06B: CLOSED state header
  - only after a governed CLOSED context source exists
```

This record does not open either child ticket; it only records the safest route.

## 6. HOLD Conditions

Full `CD-T06` HOLD remains active if:

- `CLOSED` cannot be rendered under current context/fixture evidence;
- implementation requires fixture/adapter/validator/ResolvedSurfaceContext changes;
- implementation adds approval controls, state transitions, timers, audit summaries, backend/runtime/API/schema, real data, secrets, deploy, public endpoint, or external pilot.

## 7. Non-Authorization

This relaunch does not authorize implementation or Jira Done transition.
