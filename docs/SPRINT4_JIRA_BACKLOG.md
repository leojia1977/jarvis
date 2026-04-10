# Sprint 4 Jira Backlog

## Usage
- Use this backlog with `docs/SPRINT4_PRD.md`.
- Claude should review scope, sequencing, case-lifecycle semantics, and pilot-readiness wording.
- Codex should implement only against canonical files under `backend/`, `scripts/`, `mock_data/`, and governed docs.

## Epic S4-A Static Data and Identity Source Integration

### SP4-A-1 Static Data Source Contract Freeze
- Type: `DEV`
- Goal: freeze source contracts for asset inventory, baselines, intel seed, and topology data
- Files:
  - `backend/app/config.py`
  - `docs/SPRINT4_PRD.md`
  - new contract docs under `docs/` or `contracts/`
- Acceptance:
  - each static-data domain has one normalized source contract
  - source ownership and refresh expectations are documented
  - no hidden file-read assumptions remain undocumented

### SP4-A-2 Static Data Adapter Layer
- Type: `DEV`
- Goal: replace direct local initialization reads for T1/T4/T5 with explicit source adapters
- Files:
  - `backend/app/agents/graph.py`
  - `backend/app/config.py`
  - new adapter modules under `backend/app/tools/`
- Acceptance:
  - asset, baseline, intel-seed, and topology reads pass through explicit adapter interfaces
  - mock and production-shaped paths share one return envelope
  - configuration failure maps to diagnosable categories

### SP4-A-3 Host Identity Resolver
- Type: `DEV`
- Goal: create one authoritative host-identity resolver shared by SIEM, EDR, and blast-radius logic
- Files:
  - `backend/app/tools/siem_adapter.py`
  - new canonical identity module if needed
  - `backend/app/agents/graph.py`
- Acceptance:
  - one normalized host identity structure exists
  - SIEM and T3 host selection use the same resolver
  - identity ambiguity is explicit, not silently guessed
  - `SP4-B-1` may not freeze host-identity expectations until this resolver contract is accepted

### SP4-A-4 Static Data Cache and Contract Tests
- Type: `QA`
- Goal: add regression coverage for source contracts, refresh semantics, and identity resolution
- Files:
  - new tests under `backend/tests/`
- Acceptance:
  - mock and production-shaped adapter results are covered
  - stale or missing static data produces governed degraded or misconfigured outcomes
  - identity-resolution edge cases are tested

### SP4-A-5 Source Integration Review
- Type: `INT`
- Goal: review source contracts and identity semantics before EDR work depends on them
- Acceptance:
  - no unresolved P1 product ambiguity around identity authority
  - unsupported source fields and deferred items are explicitly listed

## Epic S4-B EDR Telemetry Productionization

### SP4-B-1 EDR Adapter Contract
- Type: `DEV`
- Goal: freeze the production-facing contract for process-event ingestion
- Files:
  - `backend/app/tools/process_tree_t3.py`
  - new EDR adapter module or contract doc
- Acceptance:
  - one canonical process-event schema
  - `TimeRangeSpec` usage matches SIEM semantics
  - host identity expectations align with `S4-A`

### SP4-B-2 Production EDR Ingestion Path
- Type: `DEV`
- Goal: add a production-facing EDR adapter path without leaking vendor fields into T3 logic
- Files:
  - T3 modules
  - new adapter modules under `backend/app/tools/`
  - config and runtime modules if needed
- Acceptance:
  - production EDR adapter can return canonical process events
  - T3 output shape remains unchanged
  - adapter errors map to governed degraded semantics

### SP4-B-3 EDR Replay Transport and Fixtures
- Type: `QA`
- Goal: provide offline replay coverage for at least two production-shaped EDR payload sets
- Files:
  - `backend/tests/test_vendor_replay.py` or new EDR replay tests
  - fixture files under `backend/tests/fixtures/`
- Acceptance:
  - at least two EDR fixture sets exist
  - replay transport matches endpoint keys deterministically
  - replay tests prove canonical normalization

### SP4-B-4 T3 Production Parity Tests
- Type: `QA`
- Goal: prove T3 anomaly detection, persistence detection, and IOC extraction behave consistently under EDR replay
- Files:
  - `backend/tests/test_t3_hunt.py`
  - new production-style T3 tests if needed
- Acceptance:
  - T3 outputs keep frozen contract values
  - degraded and partial telemetry semantics remain explicit
  - no vendor-specific field names appear in T3 output

### SP4-B-5 Telemetry Review Pass
- Type: `INT`
- Goal: review real-field parity and unsupported EDR gaps before case persistence depends on them
- Acceptance:
  - required EDR fields are documented
  - unsupported artifact types are clearly deferred

## Epic S4-C Persistent Case Lifecycle

### SP4-C-1 Persistent Case Schema Freeze
- Type: `DEV`
- Goal: freeze the durable stored-case schema and status model
- Files:
  - `backend/app/agents/case_view.py`
  - `backend/app/agents/graph.py`
  - new contract docs under `docs/` or `contracts/`
- Acceptance:
  - stored case schema aligns with Sprint 3 case-view contract
  - status transitions are explicit
  - audit and action-request fields are first-class
  - the persistence backend choice is frozen and justified against SecuPilot data-sovereignty and audit requirements before `SP4-C-2`

### SP4-C-2 Case Store and Retrieval API
- Type: `DEV`
- Goal: add governed persistence and retrieval for investigated cases
- Files:
  - `backend/app/main.py`
  - `backend/app/runtime_service.py`
  - new case-store module if needed
- Acceptance:
  - case can be saved and retrieved by `case_id`
  - persistence failure returns diagnosable runtime output
  - retrieval does not mutate stored case data

### SP4-C-3 Action Request and Approval Contract
- Type: `DEV`
- Goal: make recommended actions reviewable and approvable as stored data, not transient text
- Files:
  - case shaping modules
  - runtime modules
  - new docs if needed
- Acceptance:
  - action requests are non-destructive by default
  - approval history is auditable
  - degraded cases suppress unsafe action enablement

### SP4-C-4 Case Lifecycle Regression Tests
- Type: `QA`
- Goal: add coverage for create, retrieve, review, approve, and close semantics
- Files:
  - `backend/tests/test_runtime_service.py`
  - `backend/tests/test_case_view.py`
  - new persistence tests if needed
- Acceptance:
  - case retrieval returns stable schema
  - approval and closure semantics are tested
  - audit history remains deterministic

### SP4-C-5 Product Review Pass
- Type: `INT`
- Goal: review whether the persisted case lifecycle is suitable for analyst and manager usage
- Acceptance:
  - no unresolved P1 ambiguity in case status or approval semantics
  - operator and analyst wording stay non-destructive and auditable

## Epic S4-D Pilot Deployment and Operability

### SP4-D-1 Environment and Secret Profile Freeze
- Type: `DEV`
- Goal: define the minimum environment and secret contract for a pilot deployment
- Files:
  - `backend/app/config.py`
  - docs under `docs/`
- Acceptance:
  - required variables are explicit
  - optional variables and defaults are documented
  - mock versus pilot distinctions are clear

### SP4-D-2 Pilot Smoke Path
- Type: `DEV`
- Goal: define one governed end-to-end pilot smoke path using production-shaped adapters and persistent case flow
- Files:
  - runtime modules
  - test modules
  - new operator docs if needed
- Acceptance:
  - one pilot path is documented step-by-step
  - the path covers ingestion, investigation, persistence, and retrieval
  - failure points map to runtime status categories
  - `SP4-A-5` must have an explicit governed closeout record before this ticket starts

### SP4-D-3 Operator Runbooks and Failure Triage
- Type: `DEV`
- Goal: document operator actions for common readiness, misconfiguration, and dependency failures
- Files:
  - `docs/RELEASE_PROCESS.md`
  - runtime-operability docs
  - new runbook docs if needed
- Acceptance:
  - operator message categories map to a documented runbook
  - no runbook relies on hidden local knowledge

### SP4-D-4 Pilot Validation Gate
- Type: `QA`
- Goal: extend governed validation to cover the pilot smoke path and persistent-case flow
- Files:
  - `scripts/git_preflight.py`
  - `scripts/verify_release.py`
  - test modules as needed
- Acceptance:
  - pilot path has a deterministic gate entry
  - release verification can prove pilot artifacts and checks are present

### SP4-D-5 Pilot Readiness Review
- Type: `INT`
- Goal: do one operator-focused readiness review before any external pilot begins
- Acceptance:
  - no unresolved P1 operator ambiguity
  - source contracts, runtime states, and case persistence are judged coherent enough for pilot use

## Recommended Sprint 4 Sequence
1. `S4-A`
2. `S4-B`
3. `S4-C`
4. `S4-D`

Execution note:
- `SP4-A-3` is the hard prerequisite that unlocks `SP4-B-1`
- `SP4-D-1` and `SP4-D-3` can begin in parallel once Sprint 4 scope is accepted
- `SP4-D-2`, `SP4-D-4`, and `SP4-D-5` stay after `S4-A + S4-B + S4-C`

## Claude Review Focus
- challenge source-contract scope and identity authority
- review EDR parity and degraded semantics
- challenge case lifecycle and approval semantics
- flag pilot-readiness wording that could mislead operators or analysts

## Codex Implementation Focus
- keep source contracts explicit and canonical
- do not leak vendor or persistence shortcuts into core algorithms
- update governed docs, manifest, and review-pack flow together
- prefer replayable fixtures and deterministic gates over ad hoc manual checks
