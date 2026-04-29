# S6 Jira Stale Seed Cleanup Proposal 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Jira Stale Seed Cleanup Proposal 2026-04-29 |
| Date | 2026-04-29 |
| Jira project | `SCRUM` |
| Scope | Jira seed/demo issue cleanup proposal |
| Status | `JIRA_STALE_SEED_CLEANUP_PROPOSAL_RECORDED_NO_MUTATION` |

## 2. Decision

```text
JIRA_STALE_SEED_CLEANUP_PROPOSAL_RECORDED_NO_MUTATION
```

The Jira project still contains starter/demo issues that do not map cleanly to
SecuPilot governed tickets.

## 3. Candidate Stale Rows

| Issue | Current status | Reason to review |
| --- | --- | --- |
| `SCRUM-1` | `待办` | Generic seed row, not a governed SecuPilot ticket. |
| `SCRUM-2` | `正在进行` | Generic seed row, not a governed SecuPilot ticket. |
| `SCRUM-3` | `正在进行` | Generic seed row, not a governed SecuPilot ticket. |
| `SCRUM-4` | `待办` | Generic subtask under seed row, not governed SecuPilot scope. |
| `SCRUM-5` | `待办` | Early `jarvis agent` row, not part of current governed backlog taxonomy. |

## 4. Cleanup Options

| Option | Meaning | Risk |
| --- | --- | --- |
| Option A | Leave as-is and ignore in SecuPilot burn-down metrics. | Safest; dashboard count remains noisy. |
| Option B | Add comments/labels marking them `seed-ignore`. | Low risk; requires Jira mutation GO. |
| Option C | Move to Done as non-product demo cleanup. | Not recommended unless the team accepts burn-down metric effects. |
| Option D | Delete/archive if project permissions allow. | Highest risk; requires explicit human GO and backup/export. |

## 5. Recommendation

```text
RECOMMEND_OPTION_B_LABEL_OR_COMMENT_SEED_IGNORE
```

Do not delete or transition these rows until Jarvis explicitly authorizes Jira
cleanup mutation.

## 6. Non-Authorization

This proposal does not authorize:

- deleting Jira issues;
- transitioning Jira issues;
- changing labels/comments;
- changing Sprint scope;
- implementation or repo code changes.

## 7. Next Route

```text
WAIT_FOR_JIRA_STALE_SEED_CLEANUP_GO_OR_IGNORE_IN_METRICS
```

