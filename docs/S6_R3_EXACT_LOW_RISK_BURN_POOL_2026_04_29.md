# S6 R3 Exact Low-Risk Burn Pool 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 R3 Exact Low-Risk Burn Pool 2026-04-29 |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Mode | docs-only / checklist-only / no implementation |
| Status | `R3_EXACT_LOW_RISK_BURN_POOL_OPEN` |

## 2. Decision

```text
R3_EXACT_LOW_RISK_BURN_POOL_OPEN
STOP_AT_IMPLEMENTATION_GO_REQUIRED
```

R3 keeps automation productive after Jira parity repair and dependent
acceptance reconciliation. It authorizes only docs-only planning, reconciliation,
blocker mapping, and exact future launch/checklist prep.

## 3. Authorized Queue

Run in this order unless a lane HOLDs:

| Order | Lane | Allowed output | Stop condition |
| --- | --- | --- | --- |
| 1 | `AP-T12A` acceptance evidence index checklist | docs-only checklist over current AP route/CTA/audit/state-sync evidence | Stop before code or full AP Done. |
| 2 | `MV-T05A` P3-only Manager acceptance reconciliation checklist | docs-only checklist using `MV-T01/MV-T03/MV-T04/MV-T02` evidence | Stop before Jira Done unless checklist PASS is explicit. |
| 3 | `AP-T02` blocker refresh | docs-only P0 readonly approval container blocker map | Stop before implementation GO. |
| 4 | Parent epic closure readiness board | docs-only map for `GS/IN/CD/EP/SH/CH/AP/MV` parents | No parent epic Done transition. |
| 5 | Jira stale seed cleanup proposal | docs-only proposal for `SCRUM-1` through `SCRUM-5` demo/seed issues | No Jira mutation unless later exact GO. |
| 6 | Next implementation candidate board | docs-only ranking of remaining tickets that could be made exact | Stop at `IMPLEMENTATION_GO_REQUIRED`. |

## 4. Forbidden Scope

R3 does not authorize:

- frontend source changes;
- Storybook or Playwright changes;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- backend/runtime/API/schema;
- real data;
- anonymized real data;
- secrets;
- deploy;
- public endpoint;
- external pilot;
- launch;
- Jira Done transitions for HOLD/non-ready rows;
- parent epic Done transitions.

## 5. Next Route

```text
OPEN_R3_LOW_RISK_BURN_POOL_RUNNER_OR_WAIT_FOR_EXACT_IMPLEMENTATION_GO
```

