# S6 Jira Sync AP-T12 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Document | `S6_JIRA_SYNC_AP_T12_2026_04_29` |
| Jira issue | `SCRUM-74` |
| Summary | `[AP-T12] Full AP acceptance suite scope decision` |
| Parent | `SCRUM-43` |
| Sync mode | Evidence comment + Done transition |

## 2. Decision

```text
AP_T12_JIRA_SYNCED_DONE_AS_SCRUM_74
AP_PARENT_SCRUM_43_REMAINS_SEPARATE_CLOSURE_REVIEW
```

## 3. Sync Evidence

`SCRUM-74` was read back as the exact AP-T12 issue, received AP-T12C closeout
evidence, and transitioned from `待办` to `已完成`.

The evidence comment references:

- `docs/S6_AP_T12C_FULL_AP_ACCEPTANCE_LANE_CLOSEOUT_2026_04_29.md`;
- acceptance-only Storybook / Playwright lane coverage;
- local gates and Claude Code `PASS_WITH_FINDINGS` with no blocking findings;
- the non-authorization boundary for product behavior, backend/runtime/API/schema,
  real data, secrets, deploy, external pilot, and launch.

## 4. Non-Authorization

This sync does not authorize or perform:

- `SCRUM-43` AP parent epic closure;
- product behavior changes;
- backend/runtime/API/schema;
- fixture/adapter/validator/`ResolvedSurfaceContext` changes;
- real data or anonymized real data;
- secrets;
- deploy, public endpoint, external pilot, or launch.
