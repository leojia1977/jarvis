# S6 Jira Mapping Proposal IN-T03 / CH-T04 / Dependent Acceptance 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Jira Mapping Proposal IN-T03 / CH-T04 / Dependent Acceptance |
| Date | 2026-04-29 |
| Jira project | `SCRUM` |
| Status | `JIRA_MAPPING_PROPOSAL_RECORDED_NO_ISSUE_CREATION` |

## 2. Jira Lookup Result

Jira credentials were hydrated from User environment variables and project
`SCRUM` was read successfully. Exact issue matching found:

| Ticket | Exact issue found | Cloud action |
| --- | --- | --- |
| `IN-T03` | No | No transition. |
| `CH-T04` | No | No transition. |
| `IN-T06` | No | No transition. |
| `CD-T07` | No | No transition. |
| `AP-T11` | No | No transition. |
| `AP-T12` | No | No transition. |
| `MV-T05` | No | No transition. |

## 3. Proposed Cloud Mapping

If cloud parity is required, create dedicated child issues rather than marking
parent epics Done:

| Ticket | Proposed parent | Proposed cloud status |
| --- | --- | --- |
| `IN-T03` | `SCRUM-7 [IN] Inbox...` | Done, because repo closeout exists. |
| `IN-T06` | `SCRUM-7 [IN] Inbox...` | Done, if Jarvis accepts this no-code reconciliation. |
| `CH-T04` | `SCRUM-41 [CH] Coverage & Health` | Done, because repo closeout exists. |
| `CD-T07` | `SCRUM-8 [CD] Case Detail...` | Done, if Jarvis accepts this no-code reconciliation. |
| `AP-T11` | `SCRUM-43 [AP] Approval Surface` | Done or reconciled, only as current static/state-sync assertion boundary. |
| `AP-T12` | `SCRUM-43 [AP] Approval Surface` | HOLD; do not mark Done. |
| `MV-T05` | `SCRUM-48 [MV] Manager View` | HOLD until rescope decision. |

## 4. Non-Action

This proposal does not create Jira issues and does not transition any Jira issue.
It is only a safe cloud-parity map for a later explicit Jira creation/sync GO.

## 5. Next Route

```text
WAIT_FOR_JIRA_CREATION_GO_FOR_MISSING_DEPENDENT_TICKETS_OR_NEXT_EXACT_LOW_RISK_BURN_POOL
```

