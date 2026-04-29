# S6 AP-T02 P0 Readonly Approval Context Source Checklist 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `AP-T02` |
| Jira issue | `SCRUM-54` |
| Scope | P0 readonly approval context source / implementation readiness |
| Status | `AP_T02_CONTEXT_SOURCE_CHECKLIST_HOLD_GOVERNED_P0_APPROVAL_CONTEXT_MISSING` |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Mode | source/checklist only |

## 2. Decision

```text
AP_T02_CONTEXT_SOURCE_CHECKLIST_HOLD_GOVERNED_P0_APPROVAL_CONTEXT_MISSING
IMPLEMENTATION_NOT_AUTHORIZED
```

`AP-T02` remains HOLD. The code contains a P0 readonly approval shell branch if
a P0 context is supplied, but the repo does not yet contain a governed renderable
P0 approval context source or approved test harness.

## 3. Source Check

| Requirement | Current result | Evidence |
| --- | --- | --- |
| `/approval` route shell exists | PASS | Existing route guard / AP-T01 evidence. |
| P0 branch is readonly if supplied | PARTIAL | `ApprovalRouteShell` has `role === "P0"` read-only branch behavior. |
| P0 approval route is reachable without URL/storage authority | HOLD | No governed P0 approval fixture or route entry exists. |
| P0 approval context source is governed | HOLD | Current fixture phases cover P1/P2/P3 surfaces; no P0 approval phase. |
| AP controls remain absent for P0 | PASS candidate | Existing branch logic is read-only, but cannot be accepted until context source is governed. |
| No fixture/adapter/validator/ResolvedSurfaceContext change needed | HOLD | A source/harness may require separate governed route if not already available. |

## 4. Required Input To Unlock

A future implementation GO requires one of these governed inputs:

### Option A - Governed P0 Approval Fixture / Context Source

```text
P0 context has role = P0
surface is valid for readonly approval container
case/action_request fields are source-bound and mock-only
coverage_level remains hard ceiling
no URL/storage/route-param authority
```

### Option B - Approved Test Harness Only

```text
P0 approval context can be constructed only inside test scope
helper validates through ContextValidator
helper is not used by product route or Storybook/Playwright production-like paths
no fixture/adapter/validator/ResolvedSurfaceContext changes inside AP-T02
```

## 5. Future Implementation Envelope If HOLD Clears

Likely allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
```

Required tests:

```text
P0 /approval renders readonly approval container
P0 /approval does not render approve/reject/delay/observe controls
P0 /approval does not create ActionMode
P0 /approval does not mutate AP state
P0 authority is not derived from URL/localStorage/sessionStorage
P1/P3 guards remain unchanged
```

## 6. HOLD Conditions

HOLD immediately if AP-T02 would require:

- backend/runtime/API/schema;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes without separate governed GO;
- URL/storage authority;
- approval controls;
- state mutation;
- real data, secrets, deploy, public endpoint, external pilot, or launch.

## 7. Jira

`SCRUM-54` remains `待办`.

No Jira Done transition is authorized by this checklist.

## 8. Next Route

```text
WAIT_FOR_AP_T02_GOVERNED_P0_CONTEXT_SOURCE_OR_APPROVED_TEST_HARNESS
```

