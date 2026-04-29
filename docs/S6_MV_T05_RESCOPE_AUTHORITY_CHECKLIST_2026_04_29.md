# S6 MV-T05 Rescope Authority Checklist 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `MV-T05` |
| Scope | Manager acceptance rescope / authority checklist |
| Status | `MV_T05_RESCOPE_AUTHORITY_CHECKLIST_RECORDED_IMPLEMENTATION_NOT_AUTHORIZED` |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |

## 2. Decision

```text
MV_T05_RESCOPE_AUTHORITY_CHECKLIST_RECORDED_IMPLEMENTATION_NOT_AUTHORIZED
```

`MV-T05` is not implementation-ready. It needs a rescope decision because
`MV-T02 = OPTION_A` explicitly closes P0/P2 Manager entry by hard redirect /
no Manager entry rather than implementing a P0/P2 readonly degraded Manager
variant.

## 3. Current Evidence

| Dependency | Current state | Impact |
| --- | --- | --- |
| `MV-T01` | Done | P3 Manager structure exists. |
| `MV-T02` | Done as P0/P2 hard redirect / no Manager entry | Cross-role Manager variant is not in scope. |
| `MV-T03` | Done | P3 deep-link handoff exists. |
| `MV-T04` | Done | P3 approval-audit summary exists. |
| `AP-T08` / `SH-T08` | Done | Source-bound audit evidence exists. |

## 4. Rescope Options

| Option | Meaning | Recommendation |
| --- | --- | --- |
| Option A | Rescope `MV-T05` to P3-only Manager acceptance over `MV-T01` / `MV-T03` / `MV-T04`, explicitly excluding P0/P2 variants. | Safe candidate, but requires Jarvis/Human rescope GO before closeout. |
| Option B | Keep original full/cross-role Manager acceptance including P0/P2 degraded variants. | HOLD; requires new governed field map and future implementation. |
| Option C | Defer `MV-T05` until a later Manager acceptance sprint. | Safe if Product accepts deferred acceptance. |

## 5. Guardrails

Any future `MV-T05` work must preserve:

- no P0/P2 Manager placeholder branch;
- no host raw evidence DOM attachment;
- no P2 evidence drawer under P3;
- no approval controls;
- no URL/storage/route-param authority;
- no backend/runtime/API/schema;
- no fixture/adapter/validator or `ResolvedSurfaceContext` change.

## 6. Jira

Exact cloud issue lookup result:

```text
MV-T05: no exact cloud issue found in SCRUM
Jira Done transition: not performed
```

No Jira Done transition is safe until Jarvis selects a rescope option.

## 7. Next Route

```text
WAIT_FOR_MV_T05_RESCOPE_DECISION_OR_NEXT_EXACT_LOW_RISK_BURN_POOL
```

