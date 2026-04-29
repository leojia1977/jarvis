# S6 AP-T12 Acceptance Scope Decision 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T12` |
| Jira issue | `SCRUM-74` |
| Scope | Full AP acceptance suite scope decision |
| Status | `AP_T12_SCOPE_DECISION_HOLD_FULL_SUITE_SPLIT_CANDIDATES_READY` |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |

## 2. Decision

```text
AP_T12_SCOPE_DECISION_HOLD_FULL_SUITE_SPLIT_CANDIDATES_READY
```

Full `AP-T12` must remain HOLD. It is not safe to mark the full AP acceptance
suite Done from `AP-T06`, `AP-T09`, or `AP-T11` evidence alone.

## 3. Rationale

`AP-T12` is the full AP acceptance suite, not a single bounded implementation or
static assertion row. Current evidence is strong but still partial:

| Evidence | Current state | Impact |
| --- | --- | --- |
| AP route / guard | Done | Required base is present. |
| P2 CTA / modal / config shells | Done | Static and non-mutating boundaries present. |
| AP-T06 mock/test state sync | Done | Test hook semantics present, no real backend protocol. |
| AP-T09 audit empty/unavailable | Done | Source-bound audit states present. |
| AP-T11 static/state-sync assertion boundary | Done | Assertion boundary reconciled. |
| `AP-T02` P0 readonly approval container | HOLD | Blocks full cross-role AP acceptance. |
| Full Playwright / Storybook AP acceptance lane | Not separately governed | Blocks full-suite closeout. |

## 4. Allowed Split Candidates

Future automation may create docs-only or checklist-only split candidates:

| Candidate | Allowed scope | Implementation authorization |
| --- | --- | --- |
| `AP-T12A` | AP bounded acceptance evidence index over current route, CTA, audit, state-sync, and source-bound states. | No implementation unless later exact GO. |
| `AP-T12B` | P0 readonly approval container blocker map tied to `AP-T02`. | No implementation unless later exact GO. |
| `AP-T12C` | Playwright / Storybook acceptance lane checklist. | No implementation unless later exact GO. |

## 5. HOLD Conditions

`AP-T12` must HOLD if future work needs:

- real AP mutation;
- production state transition protocol;
- backend/runtime/API/schema;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- URL/storage authority;
- real data, secrets, deploy, public endpoint, external pilot, or launch.

## 6. Jira

`SCRUM-74` was created and intentionally left `待办`.

No Jira Done transition is allowed until the full AP acceptance suite is either
completed under a governed route or explicitly rescoped by Jarvis/Human.

## 7. Next Route

```text
OPEN_AP_T12A_ACCEPTANCE_EVIDENCE_INDEX_CHECKLIST_OR_AP_T02_BLOCKER_REVIEW
```

