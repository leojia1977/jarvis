# Sprint 3 Jira Backlog

## Usage
- Use this backlog with `docs/SPRINT3_PRD.md`.
- Claude should review scope, sequencing, risks, and acceptance quality.
- Codex should implement only against canonical files under `backend/`, `scripts/`, `mock_data/`, and governed docs.

## Epic S3-A Runtime Productization

### SP3-A-1 Service Entrypoint
- Type: `DEV`
- Goal: expose the orchestrator through a stable runtime entrypoint
- Files:
  - `backend/app/agents/graph.py`
  - `backend/app/config.py`
  - new service entry module if needed
- Acceptance:
  - one documented local startup command
  - one callable investigate endpoint or equivalent service interface
  - consistent error envelope on invalid requests

### SP3-A-2 Health and Readiness
- Type: `DEV`
- Goal: add runtime health and readiness checks
- Files:
  - service entry module
  - `backend/app/config.py`
- Acceptance:
  - health check returns process status
  - readiness check reports dependency availability and mode

### SP3-A-3 Runtime Config Freeze
- Type: `DEV`
- Goal: standardize mock versus production configuration
- Files:
  - `backend/app/config.py`
  - `backend/app/tools/siem_adapter.py`
- Acceptance:
  - explicit mode flag
  - no hidden path fallbacks outside source-of-truth root
  - configuration errors return actionable messages

### SP3-A-4 Runtime Smoke Tests
- Type: `QA`
- Goal: add startup and request smoke coverage
- Files:
  - new test module under `backend/tests/`
- Acceptance:
  - healthy startup tested
  - one mock investigation request tested
  - degraded response path tested

### SP3-A-5 Runtime Integration Review
- Type: `INT`
- Goal: validate local startup and payload flow with product expectations
- Acceptance:
  - payload contract reviewed against PRD
  - startup command captured in docs

## Epic S3-B Analyst Case and Jarvis Experience

### SP3-B-1 Case Schema Freeze
- Type: `DEV`
- Goal: freeze the Sprint 3 case schema
- Files:
  - `backend/app/agents/graph.py`
  - contract docs under `docs/` or `contracts/`
- Acceptance:
  - one canonical case schema
  - `forensic_result`, `hunt_plan`, `blast_radius`, and degraded semantics all represented consistently

### SP3-B-2 Jarvis Case Embedding
- Type: `DEV`
- Goal: ensure Jarvis output is first-class inside the final case
- Files:
  - `backend/app/agents/graph.py`
  - `backend/app/agents/jarvis_hunt_engine.py`
- Acceptance:
  - `hunt_plan` present when applicable
  - `hunt_plan` omitted or null only when not applicable
  - degraded reasoning remains explicit

### SP3-B-3 Analyst View Contract
- Type: `DEV`
- Goal: produce a frontend-ready contract for case summary and evidence sections
- Files:
  - docs or contract files
  - backend serializer or shaping logic
- Acceptance:
  - first screen fields frozen
  - evidence grouping documented
  - approval block schema frozen

### SP3-B-4 Case Regression Coverage
- Type: `QA`
- Goal: add regression tests for case output semantics
- Files:
  - `backend/tests/test_secupilot_drafts.py`
  - new case-schema tests if needed
- Acceptance:
  - hunt plan presence tested
  - degraded action suppression tested
  - approval-ready wording tested

### SP3-B-5 Product Review Pass
- Type: `INT`
- Goal: review case readability with Claude
- Acceptance:
  - findings mapped to schema or UI contract updates
  - no unresolved P1 product ambiguities before frontend build

## Epic S3-C Real Telemetry Integration

### SP3-C-1 SIEM Adapter Contract
- Type: `DEV`
- Goal: normalize SIEM query inputs and outputs
- Files:
  - `backend/app/tools/siem_adapter.py`
  - `backend/app/config.py`
- Acceptance:
  - time range honored
  - target scope honored
  - mock and production adapters share one return shape

### SP3-C-2 EDR Process Event Contract
- Type: `DEV`
- Goal: standardize process event ingestion for T3
- Files:
  - `backend/app/tools/process_tree_t3.py`
  - `scripts/generate_process_events.py`
  - contract docs
- Acceptance:
  - one normalized event schema
  - host identity and timestamps validated
  - typed IOC extraction remains stable

### SP3-C-3 Adapter Test Matrix
- Type: `QA`
- Goal: verify mock and production code paths without breaking canonical algorithms
- Files:
  - new tests under `backend/tests/`
- Acceptance:
  - mock mode tests pass
  - production adapter stubs pass contract tests
  - no direct vendor-specific assumptions leak into core tools

### SP3-C-4 Integration Data Review
- Type: `INT`
- Goal: review real-world field mapping and telemetry coverage
- Acceptance:
  - required fields documented
  - unsupported fields and gaps explicitly listed

## Epic S3-D Engineering and Release Hardening

### SP3-D-1 Claude Review Pack Automation
- Type: `DEV`
- Goal: generate a deterministic Claude Web review pack from the current manifest
- Files:
  - `scripts/build_claude_review_pack.py`
  - `docs/CLAUDE_WEB_UPLOAD_CHECKLIST.md`
  - `docs/CLAUDE_WEB_ALIGNMENT_GUIDE.md`
- Acceptance:
  - one command produces one review pack folder and zip
  - generated prompt header matches manifest snapshot

### SP3-D-2 Governance Doc Synchronization
- Type: `DEV`
- Goal: keep handoff, manifest, and prompt instructions aligned
- Files:
  - `docs/HANDOFF.md`
  - `releases/release_manifest.json`
  - `docs/RELEASE_PROCESS.md`
- Acceptance:
  - snapshot IDs are consistent
  - review flow is documented once and reused

### SP3-D-3 Release Gate Expansion
- Type: `QA`
- Goal: extend the governed validation set
- Files:
  - `scripts/package_release.py`
  - `scripts/verify_release.py`
  - manifest
- Acceptance:
  - governed docs tracked in manifest
  - release artifacts verified from source-of-truth root only

### SP3-D-4 Wrapper Retirement Plan
- Type: `INT`
- Goal: define when compatibility wrappers can be safely removed
- Files:
  - `docs/PROJECT_STRUCTURE.md`
  - `docs/HANDOFF.md`
- Acceptance:
  - wrapper deprecation criteria documented
  - removal is not scheduled before runtime and API stability

## Recommended Sprint 3 Sequence
1. `S3-A`
2. `S3-B`
3. `S3-C`
4. `S3-D`

## Claude Review Focus
- Validate scope and sequencing
- Challenge case schema clarity and degraded semantics
- Review analyst-facing contract and approval language
- Flag any product ambiguity before Codex implementation

## Codex Implementation Focus
- Keep canonical changes under `backend/`, `scripts/`, and `mock_data/`
- Update governed docs and manifest together
- Package and verify from source-of-truth root only
