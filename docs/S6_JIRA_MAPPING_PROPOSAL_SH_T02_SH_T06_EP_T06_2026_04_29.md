# S6 Jira Mapping Proposal SH-T02 / SH-T06 / EP-T06 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Jira Mapping Proposal SH-T02 / SH-T06 / EP-T06 2026-04-29 |
| Status | JIRA_MAPPING_PROPOSAL_READY_NO_CLOUD_MUTATION |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Automation id | `secupilot-30m-bounded-burn-runner` |
| Trigger | Idle fallback after remaining PASS-row Jira parity audit |

## 2. Decision

```text
JIRA_MAPPING_PROPOSAL_READY_NO_CLOUD_MUTATION
```

This record proposes explicit Jira mapping options for repo PASS rows that do
not currently expose dedicated Jira cloud issue keys in the project search.

No Jira issue was created, no Jira issue was transitioned, and no Jira Done
state was inferred from this proposal.

## 3. Source Evidence

| Repo row | Repo evidence | Suggested parent if dedicated Jira issue is later authorized |
| --- | --- | --- |
| `SH-T02` | `docs\S6_SH_T02_DUAL_COVERAGE_CLAMP_CLOSEOUT_2026_04_28.md` | `SCRUM-31 [SH] Search / History` |
| `SH-T06` | `docs\S6_SH_T06_STRUCTURAL_DEGRADED_EMPTY_STATE_CLOSEOUT_2026_04_28.md` | `SCRUM-31 [SH] Search / History` |
| `EP-T06` | `docs\S6_EP_T06_EP_NEGATIVE_TEST_SUITE_RECONCILIATION_CLOSEOUT_2026_04_28.md` | `SCRUM-25 [EP] Evidence / Timeline / Blast Radius` |

## 4. Mapping Options

### Option A: Create Dedicated Jira Tasks

Use this option only if Jira burn-down parity must match the repo tracker at
the individual task level.

Required future GO:

```text
Authorize Jira Mapping Option A for SH-T02 / SH-T06 / EP-T06.
Create dedicated Jira child issues under the suggested parents, attach repo
closeout evidence comments, transition them Done only after read-back
verification, and update route/handoff/progress records.
```

Allowed cloud action after that future GO:

- create one dedicated Jira issue for `SH-T02`;
- create one dedicated Jira issue for `SH-T06`;
- create one dedicated Jira issue for `EP-T06`;
- attach the existing repo closeout evidence;
- transition only those newly created dedicated issues to Done after
  verification.

### Option B: Attach Evidence To Parent Issues Only

Use this option if the team wants audit traceability without increasing Jira
issue count.

Required future GO:

```text
Authorize Jira Mapping Option B for SH-T02 / SH-T06 / EP-T06.
Attach repo closeout evidence as comments to the suggested parent issues only.
Do not create child issues and do not transition additional Jira issues Done.
```

Allowed cloud action after that future GO:

- add repo evidence comments to `SCRUM-31` for `SH-T02` and `SH-T06`;
- add repo evidence comment to `SCRUM-25` for `EP-T06`;
- leave Jira Done count unchanged.

### Option C: Keep Repo-Only PASS

This is the default until Jarvis chooses a mapping option.

Allowed action:

- no Jira cloud mutation;
- keep the repo closeout records as the authority for these three PASS rows;
- continue the runner toward `SH-T09` reconciliation GO or the next idle
  fallback.

## 5. Non-Authorization

This proposal does not authorize:

- creating Jira issues;
- transitioning Jira issues Done;
- closing `SH-T09`;
- changing frontend, backend, fixture, script, config, or dependency files;
- backend/runtime/API/schema work;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext`
  changes;
- real data;
- secrets;
- deploy;
- public endpoint;
- external pilot.

## 6. Next Route

```text
WAIT_FOR_SH_T09_RECONCILIATION_GO_OR_JIRA_MAPPING_GO_OR_NEXT_IDLE_FALLBACK
```
