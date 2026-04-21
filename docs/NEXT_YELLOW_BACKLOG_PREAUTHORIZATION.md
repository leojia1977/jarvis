# Next Yellow Backlog Preauthorization

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Next Yellow Backlog Preauthorization |
| Status | Green docs-only conditional Yellow preauthorization package |
| Scope | Define the next exact bounded Yellow backlog items after S5C-YB-04 |
| Snapshot | S5-NEXT-YELLOW-BACKLOG-PREAUTHORIZATION-2026-04-21-001 |
| Stage | s5-next-yellow-backlog-preauthorization |
| Baseline commit | `8147407bfb7e0babeae539957fde5142528fce73` |
| Baseline snapshot | S5-NEXT-PRODUCT-DEVELOPMENT-ROUTE-SELECTION-2026-04-21-001 |
| Baseline stage | s5-next-product-development-route-selection |
| Baseline manifest status | PASS |
| Baseline release sha256 | `fd1e52ae1aaa576000d0344b37a70daf8c786b8825f6dae014c1669eb2a7fea4` |
| Route | `OPEN_NEXT_YELLOW_BACKLOG_PREAUTHORIZATION_STAGE` |
| Lane of this document | Green docs-only preauthorization package |
| Lane of listed future items | Yellow test-only or Yellow implementation as item-scoped below |

This package is not implementation authority until this stage closes with review PASS, full gate PASS, release verification PASS, manifest PASS, closeout commit, and push. After that, it may be used only for the listed items and only under each item's exact file, behavior, test, review, closeout, and HOLD rules.

## 2. Standing Preconditions

Every listed Yellow item must satisfy all standing preconditions before work starts:

1. Current repo baseline manifest is PASS.
2. `docs\DELEGATED_APPROVER_CHARTER.md` is readable and `delegation_expires` has not passed.
3. Core governance docs are loaded.
4. The selected item appears in this document.
5. Only one Yellow backlog item is implemented per autonomous run.
6. Implementation starts from the latest governed baseline and clean git status except known unrelated untracked files.
7. The implementation touches only item-specific allowed files plus later closeout docs/manifest.
8. Review PASS or PASS_WITH_FINDINGS with no blocking finding is required before closeout.
9. Targeted tests and `py -3 scripts\git_preflight.py --mode all` must PASS before closeout.
10. Release package and manifest verification must PASS before implementation closeout commit/push.
11. Exact staged files are limited to the implementation files, closeout docs, rolling maps, and manifest for that item.
12. Any ambiguity, missing scope, failing test outside allowed files, or Red trigger means HOLD.

This preauthorization includes staging, commit, and push for each listed Yellow item only after that item's review PASS, targeted tests PASS, full gate PASS, release verification PASS, manifest PASS, exact staged scope, and no-HOLD checks pass. It does not authorize staging, commit, or push for any unlisted item or excluded file.

## 3. Anti-Overengineering Rules

Every item below must follow these rules:

1. Implement the smallest change that satisfies the exact item behavior and required tests.
2. Do not introduce a new abstraction, helper, registry, vocabulary, adapter, service, module, or generalized framework unless the item explicitly names it.
3. Do not generalize for future routes, states, statuses, formats, roles, backends, transports, or workflows.
4. Do not perform unrelated renames, reorganizations, cleanup refactors, or while-we-are-here improvements.
5. Prefer local assertions and narrowly scoped tests over framework-level changes.
6. Every changed line must map to an explicit item sentence, exact allowed behavior, or required test.
7. If a broader abstraction seems desirable, HOLD and record a scoped design note instead of implementing it.
8. Reviews must flag unnecessary abstraction, speculative generalization, and hidden scope expansion.
9. Any scope expansion means HOLD.

## 4. Backlog Item 05 - Reopen Lifecycle Audit Regression

| Field | Value |
| --- | --- |
| Item ID | `S5C-YB-05` |
| Route name | `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_05` |
| Future implementation snapshot prefix | `S5C-IMPL12-REOPEN-LIFECYCLE-AUDIT` |
| Lane | Yellow test-only |
| Purpose | Add synthetic regression coverage for the existing internal closed-to-open lifecycle transition audit semantics. |

Allowed files:

- `backend\tests\test_case_lifecycle_regression.py`

Exact allowed behavior:

- Add a synthetic test that closes a persistent case through `close_persistent_case()`.
- Reopen the same case through existing `transition_persistent_case_status(..., to_status="open", ...)`.
- Assert the reopened record has lifecycle status `open`.
- Assert the final audit event type is `case_reopened`.
- Assert the final audit event case status is `open`.
- Assert the final audit reason matches the test's reopen reason.
- Assert the earlier close audit still retains its existing `close_reason` details.

Required tests:

- `py -3 -m unittest -q backend.tests.test_case_lifecycle_regression`

Required assertions:

- `lifecycle_status == "open"` after reopen.
- `lifecycle_audit[-1].event_type == "case_reopened"`.
- `lifecycle_audit[-1].case_status == "open"`.
- Previous close audit `details["close_reason"]` remains unchanged.

Max new helpers: `0`.

Max new concept names:

- `S5C-IMPL12-REOPEN-LIFECYCLE-AUDIT`
- `case_reopened`

Explicit non-goals:

- no production code changes
- no public reopen endpoint
- no runtime/API/schema behavior
- no new lifecycle status
- no new audit event type
- no new close reason
- no S5-B/S5-D, ORDIV, Red-3, real-data, credential, launch, deploy, or AI_COLLAB work

HOLD if:

- production code is required
- runtime/API/public endpoint behavior is required
- a new lifecycle status, close reason, or audit event type is needed
- the existing internal closed-to-open transition does not support the required assertion without changing product semantics
- any file outside the allowed file is needed

## 5. Backlog Item 06 - Action Request Terminal Guard Regression

| Field | Value |
| --- | --- |
| Item ID | `S5C-YB-06` |
| Route name | `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_06` |
| Future implementation snapshot prefix | `S5C-IMPL13-ACTION-REQUEST-TERMINAL-GUARDS` |
| Lane | Yellow implementation only if needed; expected test-only |
| Purpose | Freeze synthetic regression coverage that approved, rejected, and cancelled action requests remain terminal unless existing governed transitions allow otherwise. |

Allowed files:

- `backend\tests\test_case_action_request_contract.py`
- `backend\app\tools\persistent_case.py` only if tests expose a bounded terminal-transition bug in the existing helper enforcement

Exact allowed behavior:

- Add synthetic tests for terminal action-request statuses.
- Verify an approved action request cannot be submitted, rejected, or cancelled afterward.
- Verify a rejected action request cannot be approved or submitted afterward.
- Verify a cancelled action request cannot be approved or submitted afterward.
- Preserve the existing action-request vocabulary exactly.
- Preserve `FROZEN_ACTION_REQUEST_TRANSITIONS` unless a test reveals that helper enforcement fails to honor the existing matrix.

Required tests:

- `py -3 -m unittest -q backend.tests.test_case_action_request_contract`

Required assertions:

- Terminal-status mutation attempts raise `ValueError` with `invalid_action_request_transition:*`.
- No new action-request status appears in `governed_action_request_statuses()`.
- No lifecycle/API/runtime behavior is introduced.

Max new helpers: `0`.

Max new concept names:

- `S5C-IMPL13-ACTION-REQUEST-TERMINAL-GUARDS`

Explicit non-goals:

- no new action-request status
- no transition-matrix expansion
- no endpoint behavior
- no runtime/API/schema behavior
- no action execution, RBAC, ticketing, workflow-engine, external-system, or destructive-response semantics
- no fixtures, dependencies, release scripts, contracts, AI_COLLAB, real data, credentials, launch, deploy, S5-B/S5-D, ORDIV, or Red-3 work

HOLD if:

- a new status or transition is required
- runtime/API/public endpoint behavior is required
- helper enforcement requires a broad refactor
- any file outside the allowed files is needed
- fixing a failing assertion would change existing governed product semantics

## 6. Backlog Item 07 - Workflow Summary Immutability Regression

| Field | Value |
| --- | --- |
| Item ID | `S5C-YB-07` |
| Route name | `OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_07` |
| Future implementation snapshot prefix | `S5C-IMPL14-WORKFLOW-SUMMARY-IMMUTABILITY` |
| Lane | Yellow test-only |
| Purpose | Add synthetic regression coverage that mutating a returned workflow summary cannot mutate the persistent case record or future summaries. |

Allowed files:

- `backend\tests\test_case_lifecycle_regression.py`

Exact allowed behavior:

- Add a synthetic test using existing `persistent_case_workflow_summary(record)`.
- Mutate the returned summary dict and nested `action_request_counts` dict.
- Call `persistent_case_workflow_summary(record)` again.
- Assert the second summary still reflects the record-derived values.
- Assert `execution_authorized` remains `False` in the second summary.

Required tests:

- `py -3 -m unittest -q backend.tests.test_case_lifecycle_regression`

Required assertions:

- Mutating the first returned summary does not change the next returned summary.
- Mutating nested `action_request_counts` does not alter record-derived counts.
- `execution_authorized` remains `False`.

Max new helpers: `0`.

Max new concept names:

- `S5C-IMPL14-WORKFLOW-SUMMARY-IMMUTABILITY`

Explicit non-goals:

- no production code changes
- no new helper
- no new summary field
- no runtime/API/schema behavior
- no public endpoint work
- no fixtures, dependencies, release scripts, contracts, AI_COLLAB, real data, credentials, launch, deploy, S5-B/S5-D, ORDIV, or Red-3 work

HOLD if:

- production code is required
- a new helper or summary field is needed
- runtime/API/public endpoint behavior is needed
- any file outside the allowed file is needed
- the test cannot be expressed as a local synthetic assertion

## 7. SWE Agent Posture

SWE agent remains:

```text
NOT_INSTALLED_OR_NOT_VERIFIED
```

SWE agent is not part of this package. It may not implement, review, stage, commit, push, or unblock any item until a separate `OPEN_SWE_AGENT_CAPABILITY_VERIFICATION_STAGE` passes and a later governed package explicitly allows its bounded participation.

## 8. Closeout Sequence Per Item

Each listed item may close only after this exact order:

1. Item route opens from a PASS baseline.
2. Item-specific allowed files are confirmed.
3. Implementation or test-only changes stay within allowed files.
4. Claude Code review-only PASS or PASS_WITH_FINDINGS with no blocking finding, or verified Claude Web fallback if local review spawn fails before verdict.
5. Item-targeted tests PASS.
6. `py -3 scripts\git_preflight.py --mode all` PASS.
7. Release package produced.
8. Release verification PASS.
9. Manifest updated from PENDING to PASS by verification.
10. Exact files staged.
11. Commit.
12. Push.

No gate may be skipped, reordered, inferred, or satisfied retroactively.

## 9. Standing Non-Authorization

This package does not authorize:

- implementation during this docs-only package stage
- unlisted Yellow items
- unlisted files
- broad refactors
- reusable framework work not named by an item
- runtime/API/schema behavior
- public endpoint work
- dependency or fixture changes
- release-script or contract changes
- AI_COLLAB changes
- launch or deployment
- external pilot execution or readiness
- credential handling
- real-data handling
- evidence retention or redaction policy freeze
- S5-B/S5-D reopen
- ORDIV work
- Red-3 action
- AdsPower profile creation/switching or Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection
- SWE agent installation, execution, or integration

## 10. Next Default Route

After this package closes PASS, the next default autonomous route is:

```text
OPEN_S5C_PREAUTHORIZED_YELLOW_BACKLOG_ITEM_05
```
