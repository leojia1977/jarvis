# S6 Jira Missing Child Issue Creation Sync 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Jira Missing Child Issue Creation Sync 2026-04-29 |
| Date | 2026-04-29 |
| Jira project | `SCRUM` |
| Status | `JIRA_MISSING_CHILD_ISSUES_CREATED_AND_SAFE_ROWS_SYNCED` |

## 2. Decision

```text
JIRA_MISSING_CHILD_ISSUES_CREATED_AND_SAFE_ROWS_SYNCED
AP_T12_AND_MV_T05_LEFT_TODO_HOLD
```

Jira cloud parity was repaired for the dependent acceptance pool by creating
dedicated child issues instead of overloading parent epics.

## 3. Sync Result

| Ticket | Jira key | Parent | Action | Final cloud status |
| --- | --- | --- | --- | --- |
| `IN-T03` | `SCRUM-69` | `SCRUM-7` | existing created row found, synced | `已完成` |
| `IN-T06` | `SCRUM-70` | `SCRUM-7` | created and synced | `已完成` |
| `CH-T04` | `SCRUM-71` | `SCRUM-41` | created and synced | `已完成` |
| `CD-T07` | `SCRUM-72` | `SCRUM-8` | created and synced | `已完成` |
| `AP-T11` | `SCRUM-73` | `SCRUM-43` | created and synced | `已完成` |
| `AP-T12` | `SCRUM-74` | `SCRUM-43` | created as HOLD/scope decision | `待办` |
| `MV-T05` | `SCRUM-75` | `SCRUM-48` | created as HOLD/rescope decision | `待办` |

Project status after sync:

```text
已完成: 57
待办: 15
正在进行: 2
```

## 4. Scope Guard

`AP-T11 / SCRUM-73` is Done only for the current static no-mutation plus
mock/test `STATE_SYNC` assertion boundary. It does not claim real AP mutation or
backend state transition.

`AP-T12 / SCRUM-74` remains To Do because the full AP acceptance suite requires
an explicit scope decision.

`MV-T05 / SCRUM-75` remains To Do because `MV-T02 = OPTION_A` does not create a
P0/P2 Manager variant.

## 5. Non-Authorization

This sync does not authorize:

- new implementation;
- Jira Done transition for `AP-T12` or `MV-T05`;
- parent epic Done transitions;
- backend/runtime/API/schema;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- real data, secrets, deploy, public endpoint, external pilot, or launch.

## 6. Next Route

```text
OPEN_AP_T12_ACCEPTANCE_SCOPE_DECISION_AND_MV_T05_RESCOPE_DECISION
```

