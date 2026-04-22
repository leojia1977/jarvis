# Ticket Readiness Checklist

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Ticket Readiness Checklist |
| Status | Green docs-only readiness checklist baseline |
| Scope | Define the hard admission checks before any PRD-driven work becomes an exact ticket or uses SWE acceleration |
| Snapshot | S5-TICKET-READINESS-CHECKLIST-2026-04-22-001 |
| Stage | s5-ticket-readiness-checklist |
| Baseline commit | `becc4d9491d1b54a7593ee5b8fa47e7f119bd17d` |
| Baseline snapshot | S5-SWE-AUTONOMOUS-DELIVERY-ACCELERATION-BASELINE-2026-04-22-001 |
| Baseline manifest status | PASS |
| Lane | Green docs-only |

This checklist is the admission gate between PRD/route selection and any exact Yellow ticket or SWE-assisted implementation loop.

It does not authorize implementation, code/test changes, SWE product execution, release changes, staging, commit, push, launch, deployment, external pilot execution, real-data handling, credential handling, public endpoint work, parked-stream reopen, Red execution, or AI_COLLAB changes.

## 2. Decision Outcomes

Allowed checklist outcomes:

- `READY_FOR_EXACT_TICKET`
- `READY_FOR_SWE_ACCELERATION`
- `NEEDS_GREEN_DOCS_ONLY_TICKET_PREP`
- `NEEDS_CLAUDE_WEB_REVIEW`
- `NEEDS_HUMAN_OR_JARVIS_GO`
- `HOLD`

No item may enter implementation unless the governing artifact reaches `READY_FOR_EXACT_TICKET` and later receives the required lane-specific authorization.

No item may use SWE unless it reaches `READY_FOR_SWE_ACCELERATION` and the later exact Yellow item explicitly names SWE as:

```text
bounded implementation accelerator
```

## 3. Required Inputs

Before this checklist can be evaluated, these inputs must exist:

| Input | Required evidence | Missing means |
| --- | --- | --- |
| Product source | Latest PRD or explicit product direction | `HOLD` |
| Current baseline | Manifest snapshot, commit, release PASS status | `HOLD` |
| Route candidate | Named route and candidate lane | `NEEDS_GREEN_DOCS_ONLY_TICKET_PREP` |
| Current boundaries | Parked items, Red/HOLD boundaries, non-authorizations | `HOLD` |
| Scope owner | Human/product/governance source or governed artifact | `HOLD` |

If the latest PRD or explicit product direction is missing, continue:

```text
WAIT_FOR_LATEST_PRD_OR_EXPLICIT_PRODUCT_DIRECTION
```

Do not invent scope to satisfy the checklist.

## 4. Baseline And Authority Checks

All must be true:

- current repo root is `D:\产品设计\New folder`
- manifest snapshot and branch are known
- prior release verification is PASS
- current route is named
- lane is classified or defaults to the higher-restriction lane
- authorization window is checked when autonomous policy applies
- no unresolved HOLD blocks the proposed work
- commit/push authority is explicitly available through current stage, standing Green docs-only rule, or recorded approval

If any item is false, outcome is `HOLD`.

## 5. Scope Exactness Checks

All implementation or test tickets must answer:

| Check | Required answer |
| --- | --- |
| Exact behavior | One or more observable behaviors, not a theme |
| Exact non-goals | What must not change |
| Exact allowed files | File list, no glob-only scope |
| Exact tests | Commands and required assertions |
| Exact data mode | Synthetic/local only unless separately authorized |
| Exact review path | Claude Code, Claude Web, external, Human/Jarvis, or combination |
| Exact closeout path | targeted test, full gate, release verification, manifest update, staged files |
| Exact HOLD conditions | Stop rules for scope, risk, failures, or ambiguity |

If any field cannot be named, outcome is:

```text
NEEDS_GREEN_DOCS_ONLY_TICKET_PREP
```

or `HOLD` if the missing field is high-risk.

## 6. Risk And Lane Checks

Escalate or HOLD if the item touches:

- external pilot readiness or execution
- launch or deployment
- production/customer system access
- credentials, tokens, API keys, cookies, auth headers, browser sessions, or secrets
- real data or raw evidence
- evidence retention, deletion, expiry, replay, or redaction policy freeze
- public endpoint work
- S5-B/S5-D reopen
- ORDIV report, CSV, workbook, L1B, syslog, or real-data validation
- S4-A resolver order or identity authority
- schema/API breaking change
- AI_COLLAB changes
- Red-3 action

If a Red/HOLD trigger is present, do not downgrade it into a Yellow ticket. Route to Claude Web, Human/Jarvis, or HOLD as required.

## 7. Anti-Generalization Checks

A ticket is not ready if it requires or quietly encourages:

- a new helper not explicitly named
- a new module
- a registry
- a framework
- a service layer
- reusable architecture
- future-proofing for unknown routes
- cleanup refactor
- unrelated rename
- directory reorganization
- hidden product requirement
- new status, event vocabulary, panel, route, adapter, backend, role, or workflow
- broad tests for future generality instead of exact behavior

Allowed abstraction exception:

```text
1. The ticket explicitly names the abstraction.
2. Current duplication or complexity blocks the exact behavior.
3. A smaller alternative cannot satisfy required tests.
4. Review explicitly accepts the abstraction.
5. Exact file and test scope remains intact.
```

Otherwise, record the broader idea as a HOLD/design note and keep the current ticket narrow.

## 8. SWE Eligibility Checks

SWE is disabled by default.

SWE may be considered only when all are true:

- lane is Yellow implementation or Yellow test-only
- exact Yellow item exists
- exact item explicitly states `SWE agent use: authorized only as bounded implementation accelerator for this item`
- exact repo root is named
- exact allowed files are named
- exact behavior is named
- exact tests are named
- max-change budget is named
- output location is named
- command path/version check is named
- model/credential mode is `not used` or governed non-secret path
- default execution mode is no-write plan / patch suggestion
- independent review path is named
- before/after git status checks are named if writes are ever separately authorized
- HOLD triggers include unlisted files, unexpected mutation, staged files, secrets, real data, browser/session access, network/model ambiguity, Red triggers, and out-of-scope test failures

If any item is false, set:

```text
SWE agent use: not authorized for this item
```

## 9. Review And Verification Checks

Before implementation starts, the ticket must name:

- Claude Code focused review requirement, unless explicitly exempted
- Claude Web review requirement when product, architecture, governance, high-risk, Red/HOLD, external pilot, public endpoint, evidence, real-data, launch, deployment, or parked-stream boundaries are involved
- targeted tests
- full gate requirement
- release verification requirement
- manifest update requirement
- exact staged files
- commit/push rule

Review output is evidence. It is not implementation authority unless the governing role has approval authority under the policy.

## 10. Ticket Readiness Record Template

Use this fillable record before opening an implementation ticket:

```text
TICKET_READINESS_RECORD
Snapshot:
Baseline commit:
Product source:
Route:
Lane:
Outcome:
Exact behavior:
Exact non-goals:
Allowed files:
Required tests:
Required assertions:
Max-change budget:
SWE agent use:
SWE mode:
Review path:
Full gate:
Release verification:
Commit/push authority:
HOLD conditions:
Anti-generalization check:
Red/HOLD trigger check:
Decision:
```

Allowed `Decision` values:

- `READY_FOR_EXACT_TICKET`
- `READY_FOR_SWE_ACCELERATION`
- `NEEDS_GREEN_DOCS_ONLY_TICKET_PREP`
- `NEEDS_CLAUDE_WEB_REVIEW`
- `NEEDS_HUMAN_OR_JARVIS_GO`
- `HOLD`

## 11. Non-Authorization

This checklist does not authorize:

- implementation
- code changes
- test changes
- dependency changes
- fixture creation or modification
- runtime/API/schema behavior changes
- release script changes
- contract changes
- AI_COLLAB changes
- Yellow implementation
- Red execution
- launch execution
- production deployment
- external pilot execution or readiness claims
- credential handling
- real-data handling
- evidence retention or redaction policy freeze
- public endpoint work
- S5-B/S5-D reopen
- ORDIV work
- S4-A resolver change
- Red-3 action
- AdsPower profile creation/switching
- Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection
- SWE agent product execution without a later exact Yellow item
- staging, commit, or push outside governed closeout rules

## 12. Next Use

When the latest PRD or explicit product direction arrives, use this checklist after PRD intake and before any exact implementation ticket.

If the checklist produces `HOLD`, do not ask SWE or Codex to implement. Route the missing input to the appropriate owner.
