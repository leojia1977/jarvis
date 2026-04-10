# S4-C-4 Case Lifecycle Regression Tests

## Scope
- Lock the persisted case lifecycle with deterministic regression coverage.
- Keep the focus on create, retrieve, review, approve, and close semantics.
- Do not introduce autonomous execution or workflow-engine behavior.

## What This Stage Freezes
- Closed cases must not accept `reject` or `cancel` updates on action requests.
- Lifecycle regression coverage must prove:
  - create
  - retrieve
  - review submission
  - approval
  - close
- Audit history must remain deterministic across persisted round-trips.

## Required Regression Coverage

### Contract-Level Coverage
- `test_case_action_request_contract.py`
  - closed case blocks `reject_action_request()`
  - closed case blocks `cancel_action_request()`
  - degraded case still cannot create action requests

### Lifecycle Flow Coverage
- `test_case_lifecycle_regression.py`
  - create persisted case through runtime service
  - retrieve persisted case by `case_id`
  - create one draft action request
  - submit it for review
  - approve it
  - close the case
  - verify the ordered audit chain is deterministic

### Retrieval Stability Coverage
- retrieving a closed case must not mutate stored payloads
- closed-case retrieval must preserve the frozen case schema shape

## Frozen Expectations
- The lifecycle audit chain for the happy path remains:
  - `case_created`
  - `action_request_created`
  - `status_changed` (`open -> in_review`)
  - `action_request_submitted`
  - `status_changed` (`in_review -> approved`)
  - `action_request_approved`
  - `case_closed`
- `PersistentCaseRecord` remains immutable-in-practice:
  - helpers return new records
  - retrieval reconstructs fresh objects

## Acceptance
- closed-case reject and cancel protections are enforced and tested
- lifecycle regression tests cover create / retrieve / review / approve / close
- audit history stays deterministic after persistence round-trips
- no new schema drift is introduced into `PersistentCaseRecord` or `case_view`
