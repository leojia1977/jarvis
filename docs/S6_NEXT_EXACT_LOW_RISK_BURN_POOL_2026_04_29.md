# S6 Next Exact Low-Risk Burn Pool 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Document | `S6_NEXT_EXACT_LOW_RISK_BURN_POOL_2026_04_29` |
| Purpose | Keep automation productive after AP parent closure |
| Mode | Docs/Jira governance, parity, readiness only |
| Implementation | NO |

## 2. Decision

```text
NEXT_EXACT_LOW_RISK_BURN_POOL_OPEN
NO_IDLE_FALLBACK_TO_EMPTY_WORK
STOP_AT_IMPLEMENTATION_GO_REQUIRED_FOR_CODE
```

This pool gives the runner exact low-risk work after `SCRUM-43 [AP]` closure.
It prevents idle loops while preserving bounded implementation controls.

## 3. Queue

| Order | Lane | Allowed action | Stop condition |
| --- | --- | --- | --- |
| `LR4-01` | `E0` parent closure review | Verify `SCRUM-14` children, create closure review, sync parent only if all exact children are Done. | HOLD if any child is non-Done or unmapped. |
| `LR4-02` | `GS` parent closure review | Verify `SCRUM-6` children, create closure review, sync parent only if all exact children are Done. | HOLD if any child is non-Done or unmapped. |
| `LR4-03` | `IN` parent closure review | Verify `SCRUM-7` children, create closure review, sync parent only if all exact children are Done. | HOLD if any child is non-Done or unmapped. |
| `LR4-04` | `CD` parent closure review | Verify `SCRUM-8` children, create closure review, sync parent only if all exact children are Done. | HOLD if any child is non-Done or unmapped. |
| `LR4-05` | `MV` P3-only closure review | Review `SCRUM-48` only under P3-only `MV-T05A` scope; do not claim P0/P2 Manager variants. | HOLD if parent closure would imply P0/P2 Manager acceptance. |
| `LR4-06` | `EP` parent parity audit | Audit `SCRUM-25` child/existing evidence mapping. | No parent Done unless exact child parity is proven. |
| `LR4-07` | `SH` parent parity audit | Audit `SCRUM-31` child/existing evidence mapping. | No parent Done unless exact child parity is proven. |
| `LR4-08` | `CH` parent parity audit | Audit `SCRUM-41` child/existing evidence mapping. | No parent Done unless exact child parity is proven. |
| `LR4-09` | Sprint planning board refresh | Refresh progress/risk board and remaining Jira Done diff. | Docs-only; no Jira Done for HOLD rows. |

## 4. Runner Rules

- Prefer exact Jira read-back over inferred status.
- Use parent transition only when every exposed child is verified Done and the
  parent closure does not overclaim product readiness.
- If any lane would need code, Storybook, Playwright, fixture, validator,
  backend, runtime, API, schema, real data, secrets, deploy, external pilot, or
  launch, stop at `IMPLEMENTATION_GO_REQUIRED` or `HOLD`.
- Do not create new product scope.
- Do not mark blocked, visual-missing, authority-missing, or non-ready tickets
  Done.

## 5. Non-Authorization

This pool does not authorize:

- implementation;
- frontend source changes;
- Storybook or Playwright changes;
- fixture/adapter/validator/`ResolvedSurfaceContext` changes;
- backend/runtime/API/schema;
- real data or anonymized real data;
- secrets;
- deploy, public endpoint, external pilot, or launch.

## 6. Next Route

```text
RUN_LR4_PARENT_CLOSURE_AND_PARITY_BURN_POOL
```
