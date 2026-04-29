# S6 Jira Mapping Sync SH-T02 / SH-T06 / EP-T06 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Jira Mapping Sync SH-T02 / SH-T06 / EP-T06 2026-04-29 |
| Status | `JIRA_MAPPING_PARENT_EVIDENCE_SYNCED_NO_CHILD_ISSUES_NO_DONE_TRANSITIONS` |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Mapping proposal | `docs\S6_JIRA_MAPPING_PROPOSAL_SH_T02_SH_T06_EP_T06_2026_04_29.md` |

## 2. Decision

```text
JIRA_MAPPING_PARENT_EVIDENCE_SYNCED_NO_CHILD_ISSUES_NO_DONE_TRANSITIONS
```

Jarvis authorized `Jira mapping GO` without selecting Option A or Option B by
name. To avoid inflating Jira issue count or falsely increasing Done count, this
runner uses the conservative mapping behavior:

```text
Attach repo evidence to parent issues only.
Do not create child issues.
Do not transition additional issues Done.
```

This is equivalent to the proposal's parent-evidence traceability path and is
safer than creating new cloud issues from an ambiguous option phrase.

## 3. Mapping Targets

| Repo row | Repo evidence | Parent evidence target |
| --- | --- | --- |
| `SH-T02` | `docs\S6_SH_T02_DUAL_COVERAGE_CLAMP_CLOSEOUT_2026_04_28.md` | `SCRUM-31 [SH] Search / History` |
| `SH-T06` | `docs\S6_SH_T06_STRUCTURAL_DEGRADED_EMPTY_STATE_CLOSEOUT_2026_04_28.md` | `SCRUM-31 [SH] Search / History` |
| `EP-T06` | `docs\S6_EP_T06_EP_NEGATIVE_TEST_SUITE_RECONCILIATION_CLOSEOUT_2026_04_28.md` | `SCRUM-25 [EP] Evidence / Timeline / Blast Radius` |

## 4. Cloud Action Boundary

Allowed cloud actions:

- add parent evidence comments to `SCRUM-31` for `SH-T02` and `SH-T06`;
- add parent evidence comment to `SCRUM-25` for `EP-T06`.

Prohibited cloud actions:

- no new Jira issue creation;
- no Done transition for `SCRUM-31` or `SCRUM-25`;
- no inferred Done transition for rows without dedicated issue keys;
- no update to HOLD, blocked, visual-missing, authority-missing, or non-ready
  tickets.

## 5. Sync Status

Cloud sync completed:

```text
SCRUM-31: parent evidence comment added for SH-T02 and SH-T06
SCRUM-25: parent evidence comment added for EP-T06
```

No Jira child issue was created.
No parent issue was transitioned Done.
No HOLD, blocked, visual-missing, authority-missing, or non-ready ticket was
marked Done.

## 6. Next Route

```text
JIRA_MAPPING_PARENT_EVIDENCE_SYNC_COMPLETE
```
