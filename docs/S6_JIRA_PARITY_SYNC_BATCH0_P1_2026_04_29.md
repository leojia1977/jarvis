# S6 Jira Parity Sync: Sprint 1 Batch-0 P1 Covered Tickets

Date: 2026-04-29

Decision:

```text
BATCH0_P1_JIRA_PARITY_SYNCED_DONE_FOR_EXACT_SEEDED_ISSUES
```

## 1. Scope

This record covers Jira parity sync for the five Sprint 1 Batch-0 P1 tickets
already accepted as repo-covered by:

```text
docs/S6_SPRINT1_BATCH0_P1_RECONCILIATION_CLOSEOUT_2026_04_27.md
```

No code, product semantics, backend/runtime/API/schema, fixture/adapter/validator,
`ResolvedSurfaceContext`, real data, secrets, deploy, public endpoint, or external
pilot scope was changed by this sync.

## 2. Guard And Evidence

Jira credentials were hydrated from User env into the current process. The token
was not printed or persisted.

Exact issue matching used Jira issue keys plus existing backlog labels:

| Ticket | Jira key | Required label |
| --- | --- | --- |
| `GS-T01` | `SCRUM-9` | `backlog-gs-t01` |
| `GS-T02` | `SCRUM-10` | `backlog-gs-t02` |
| `GS-T03` | `SCRUM-11` | `backlog-gs-t03` |
| `IN-T05` | `SCRUM-12` | `backlog-in-t05` |
| `CD-T03` | `SCRUM-13` | `backlog-cd-t03` |

The first transition attempt used Chinese text in a shell-embedded guard and
failed closed before mutation. The successful run used ASCII label guards and
Unicode-escaped completion transition matching.

## 3. Jira Actions

| Ticket | Jira key | Comment | Transition | Verified status |
| --- | --- | --- | --- | --- |
| `GS-T01` | `SCRUM-9` | Repo parity comment `10040` | `完成` | `已完成` |
| `GS-T02` | `SCRUM-10` | Repo parity comment `10041` | `完成` | `已完成` |
| `GS-T03` | `SCRUM-11` | Repo parity comment `10042` | `完成` | `已完成` |
| `IN-T05` | `SCRUM-12` | Repo parity comment `10043` | `完成` | `已完成` |
| `CD-T03` | `SCRUM-13` | Repo parity comment `10044` | `完成` | `已完成` |

Project status after sync:

```text
SCRUM issues returned: 67
Jira status counts: 已完成 48 / 待办 17 / 正在进行 2
```

## 4. Non-Goals Preserved

This sync did not mark any of the following Done:

- `CH-T02`, because no exact cloud issue exists
- `EP-T01`, because no exact cloud issue exists
- `CD-T06`, because full CLOSED Case Detail remains HOLD
- `AP-T06`, because full countdown/state-sync remains HOLD
- `AP-T09`, because `VF-15` or equivalent source is missing
- `CH-T04`, because runtime/source-health scope is undecided
- any blocked, HOLD, visual-missing, authority-missing, or split-only ticket

## 5. Next Route

```text
WAIT_FOR_AP_T06_STATE_SYNC_SOURCE_DELIVERY_OR_AP_T09_VF15_SOURCE_DELIVERY_OR_CH_T04_RUNTIME_SCOPE_DECISION_OR_NEXT_EXACT_LOW_RISK_BURN_POOL
```
