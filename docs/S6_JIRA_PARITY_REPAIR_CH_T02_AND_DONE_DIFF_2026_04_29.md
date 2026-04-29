# S6 Jira Parity Repair: CH-T02 And Repo Done vs Jira Done Diff

Date: 2026-04-29

Decision:

```text
CH_T02_JIRA_PARITY_REPAIR_NO_EXACT_ISSUE_FOUND_NO_CLOUD_DONE_TRANSITION
REPO_DONE_VS_JIRA_DONE_DIFF_RECORDED
NEXT_ROUTE_UNCHANGED_WAIT_FOR_AP_T06_OR_AP_T09_OR_CH_T04_OR_LOW_RISK_POOL
```

## 1. Scope

This repair was limited to:

- hydrate Jira credentials from User environment variables into the current process
- search for an exact `CH-T02` Jira cloud issue
- synchronize `CH-T02` only if one safe exact match exists
- record repo Done vs Jira Done differences

This repair does not authorize or perform:

- Jira issue creation
- marking blocked, HOLD, visual-missing, authority-missing, or non-ready tickets Done
- backend/runtime/API/schema work
- fixture/adapter/validator/`ResolvedSurfaceContext` changes
- real data, secrets, deploy, public endpoint, or external pilot

## 2. Jira Credential Hydration

Result:

```text
JIRA_BASE_URL: present from User env
JIRA_EMAIL: present from User env
JIRA_API_TOKEN: present from User env
```

The token was not printed or persisted. The earlier Jira gap was process-env
visibility, not loss of the credential from User scope.

## 3. CH-T02 Exact Issue Search

Jira project search result:

```text
Project: SCRUM
Issues returned: 67
Status counts: 已完成 43 / 待办 22 / 正在进行 2
Exact CH-T02 candidates: 0
```

Relevant cloud issues observed:

| Key | Status | Summary |
| --- | --- | --- |
| `SCRUM-41` | `待办` | `[CH] Coverage & Health` |
| `SCRUM-42` | `已完成` | `[CH-T01] Coverage & Health page skeleton` |
| `SCRUM-57` | `已完成` | `[CH-T03] Coverage & Health ui_messages rendering` |

No issue with `CH-T02` in key, summary, or visible labels was found. Therefore no
safe exact match exists and no Jira Done transition was performed for `CH-T02`.

Required future action if Jira parity matters:

```text
Create or map an exact [CH-T02] Coverage & Health main frame issue, then sync
repo closeout evidence from docs/S6_CH_T02_COVERAGE_HEALTH_MAIN_FRAME_CLOSEOUT_2026_04_29.md.
```

## 4. Repo Done vs Jira Done Diff

Repo Sprint 1-4 tracker state:

```text
Repo Done: 42 / 54
Running: 0
Blocked/HOLD/design/authority: 12
```

Jira SCRUM project state:

```text
Jira issues returned: 67
Jira Done: 43
```

These totals are not one-to-one because the Jira project includes Sprint 0,
non-tracker bootstrap issues, epics, split tickets, and repo-only reconciliations.

## 5. Can Be Repaired Later With Exact GO

These rows have repo Done evidence but were not mutated in this repair because
the current authorization targeted only exact `CH-T02` sync.

| Ticket | Jira state observed | Repair status |
| --- | --- | --- |
| `GS-T01` | Exact seeded issue `SCRUM-9` was `待办` at repair time | Superseded by `docs/S6_JIRA_PARITY_SYNC_BATCH0_P1_2026_04_29.md`; now Jira `已完成`. |
| `GS-T02` | Exact seeded issue `SCRUM-10` was `待办` at repair time | Superseded by `docs/S6_JIRA_PARITY_SYNC_BATCH0_P1_2026_04_29.md`; now Jira `已完成`. |
| `GS-T03` | Exact seeded issue `SCRUM-11` was `待办` at repair time | Superseded by `docs/S6_JIRA_PARITY_SYNC_BATCH0_P1_2026_04_29.md`; now Jira `已完成`. |
| `IN-T05` | Exact seeded issue `SCRUM-12` was `待办` at repair time | Superseded by `docs/S6_JIRA_PARITY_SYNC_BATCH0_P1_2026_04_29.md`; now Jira `已完成`. |
| `CD-T03` | Exact seeded issue `SCRUM-13` was `待办` at repair time | Superseded by `docs/S6_JIRA_PARITY_SYNC_BATCH0_P1_2026_04_29.md`; now Jira `已完成`. |
| `CH-T02` | No exact issue found | Needs exact Jira issue creation or mapping GO before sync. |
| `EP-T01` | No exact issue found | Needs exact Jira issue creation or mapping GO before sync. |

## 6. Already Synced Or Cloud Done

These rows are repo Done and already represented by Jira Done evidence or prior
safe parity sync.

| Bucket | Tickets |
| --- | --- |
| Sprint 1 P1 / EP / SH / AP / MV / CH synced rows | `IN-T01`, `IN-T02`, `IN-T04`, `CD-T01`, `CD-T02`, `CD-T04`, `CD-T05`, `CH-T01`, `EP-T02`, `EP-T03`, `EP-T04`, `EP-T05`, `SH-T01`, `SH-T03`, `SH-T05`, `SH-T07`, `SH-T08`, `AP-T10`, `AP-T01`, `AP-T03`, `AP-T04`, `AP-T05`, `AP-T07`, `AP-T08`, `CH-T03`, `MV-T01`, `MV-T03`, `MV-T04`, `SH-T04` |
| Repo-only no-code / parent evidence already handled | `SH-T02`, `SH-T06`, `EP-T06`, `SH-T09` |

## 7. Must Not Be Marked Done

These rows remain blocked or split-only and must not be transitioned to Jira
Done without later exact governed evidence.

| Ticket | Reason |
| --- | --- |
| `IN-T06` | Depends on unresolved `IN-T03` authority. |
| `CD-T06` | Full CLOSED Case Detail behavior remains HOLD; `CD-T06A` does not close parent `CD-T06`. |
| `CD-T07` | Depends on full `CD-T06`. |
| `AP-T02` | Missing governed P0 renderable approval context. |
| `AP-T06` | Full countdown/state-sync lacks governed state-sync input and test hook; `AP-T06A` is split-only. |
| `AP-T09` | Missing `VF-15` or equivalent audit empty/unavailable source. |
| `AP-T11` | Full ticket remains HOLD; `AP-T11A` is split-only. |
| `AP-T12` | Full acceptance remains dependent on `AP-T06` and `AP-T09`. |
| `CH-T04` | Runtime/source-health scope decision is still missing. |
| `MV-T02` | Missing governed P0/P2 Manager authority model. |
| `MV-T05` | Depends on Manager chain completion or explicit rescope. |

## 8. Next Route

```text
WAIT_FOR_AP_T06_STATE_SYNC_SOURCE_DELIVERY_OR_AP_T09_VF15_SOURCE_DELIVERY_OR_CH_T04_RUNTIME_SCOPE_DECISION_OR_NEXT_EXACT_LOW_RISK_BURN_POOL
```
