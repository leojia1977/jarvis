# S5-C YB-07 SWE Workflow Summary Immutability Ticket

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S5-C YB-07 SWE Workflow Summary Immutability Ticket |
| Status | Governed docs-only Yellow ticket; implementation not started |
| Scope | First exact SWE-enabled Yellow item ticket |
| Snapshot | S5C-YB07-SWE-WORKFLOW-SUMMARY-IMMUTABILITY-TICKET-2026-04-22-001 |
| Stage | s5c-yb07-swe-workflow-summary-immutability-ticket |
| Baseline commit | `8e81dfdd2332a3e51fe8cb318276e7eb892b0bae` |
| Baseline snapshot | S5C-IMPL13-ACTION-REQUEST-TERMINAL-GUARDS-IMPLEMENTATION-CLOSEOUT-2026-04-22-001 |
| Baseline stage | s5c-impl13-action-request-terminal-guards-implementation-closeout |
| Baseline manifest status | PASS |
| Baseline release sha256 | `cb6bee444f4d34f52b00dd83808ecfc9e749e550c5bfbfec57f50b73fc3d95dd` |
| Route | `OPEN_S5C_YB07_SWE_WORKFLOW_SUMMARY_IMMUTABILITY_TICKET` |
| Future implementation route | `OPEN_S5C_YB07_SWE_WORKFLOW_SUMMARY_IMMUTABILITY` |
| Future item ID | `S5C-YB-07-SWE` |
| Future lane | Yellow test-only |
| Reviewer | Claude Web / external review or governed Claude Code review-only evidence |

This ticket opens the first exact Yellow item that may name SWE agent as a bounded implementation accelerator. This document is docs-only. It does not itself authorize implementation, file edits, tests, SWE agent execution against product work, staging, commit, or push.

## 2. Baseline And Prior Item State

The current PASS baseline already closed:

- `S5C-YB-05` reopen lifecycle audit regression
- `S5C-YB-06` action-request terminal guard regression
- SWE agent Yellow backlog template integration

`S5C-YB-06` is closed and committed. It is not part of this ticket and is not retroactively SWE-enabled.

This ticket supersedes only the original non-SWE `S5C-YB-07` route selection when a later implementation GO explicitly chooses `S5C-YB-07-SWE`. It does not mutate the original backlog package or authorize any current or past Yellow item to use SWE agent.

## 3. Future Implementation Scope

Future implementation may be authorized only by a later exact Yellow implementation GO.

Allowed file:

- `backend\tests\test_case_lifecycle_regression.py`

Exact allowed behavior:

- Add one synthetic regression test using existing `persistent_case_workflow_summary(record)`.
- Mutate the returned summary dict.
- Mutate the nested `action_request_counts` dict.
- Call `persistent_case_workflow_summary(record)` again.
- Assert the second summary still reflects record-derived values.
- Assert `execution_authorized` remains `False` in the second summary.

Required targeted test:

```text
py -3 -m unittest -q backend.tests.test_case_lifecycle_regression
```

Required full closeout gate for future implementation:

```text
py -3 scripts\git_preflight.py --mode all
```

Max new helpers: `0`.

Max new concept names:

- `S5C-YB-07-SWE`
- `S5C-IMPL14-WORKFLOW-SUMMARY-IMMUTABILITY`

## 4. SWE Agent Role

SWE agent use for the future implementation item is authorized only as:

```text
bounded implementation accelerator
```

First-item SWE mode:

- no-write patch-suggestion / implementation-plan only
- output outside repo under `/tmp/secupilot-mini-swe-yb07`
- before/after git status must be recorded by Codex
- Codex/VS Code owns actual edits
- Codex owns test execution, review routing, manifest, gate, release, staging plan, commit, and push

SWE agent may not:

- write repo files directly
- run tests as authority
- review itself
- approve work
- select or expand route scope
- own manifest, release, or closeout
- stage, commit, push, or force-push
- access secrets, real data, browser sessions, cookies, tokens, auth headers, browser storage, or profile files

If no governed non-secret model credential path is available for the SWE dry-run or patch-suggestion mode, the future implementation must HOLD and continue without SWE agent.

## 5. HOLD Conditions

Future implementation must HOLD if:

- production code is required
- a new helper or summary field is needed
- runtime/API/schema/public endpoint behavior is needed
- any file outside `backend\tests\test_case_lifecycle_regression.py` is needed
- the test cannot be expressed as a local synthetic assertion
- SWE agent attempts or requires repo writes
- SWE agent requires model credentials to be displayed, logged, pasted into chat, committed, or recorded
- SWE agent output proposes broad refactors, reusable frameworks, route expansion, helper extraction, new concepts, or unrelated cleanup
- review, targeted tests, full gate, release verification, exact staging, or push becomes ambiguous

## 6. Review Evidence

External review assessed this ticket route as safe to close after focused fixes.

Review outcome:

- initial review returned `PASS_WITH_FINDINGS`
- blocking findings were fixed
- focused re-review closed the blocking findings
- remaining review note `RR-01` is informational only

This review evidence does not authorize implementation. It authorizes only docs-only closeout gate/package/release verification for this ticket stage when separately approved.

## 7. Non-Authorization

This ticket does not authorize:

- implementation during this docs-only stage
- production code changes
- runtime/API/schema behavior
- public endpoint work
- dependency changes
- fixture changes
- release-script changes
- contract changes
- AI_COLLAB changes
- direct SWE agent repo writes
- model-backed SWE execution without a later governed non-secret credential path
- review replacement
- route selection by SWE agent
- manifest/gate/release ownership by SWE agent
- staging, commit, or push without separate authorization
- launch execution
- production deployment
- external pilot execution or readiness
- credential handling
- real-data handling
- evidence retention or redaction policy freeze
- S5-B/S5-D reopen
- ORDIV work
- S4-A resolver change
- Red-3 action
- AdsPower profile creation or switching
- Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection

## 8. Closeout Recommendation

```text
CLOSEOUT_ACCEPTED_AFTER_FULL_GATE_AND_RELEASE_VERIFICATION_PASS
```

After this docs-only ticket reaches manifest PASS and is committed/pushed, the next route may be the exact future Yellow implementation route:

```text
OPEN_S5C_YB07_SWE_WORKFLOW_SUMMARY_IMMUTABILITY
```
