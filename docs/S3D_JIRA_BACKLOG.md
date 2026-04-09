# S3-D Jira Backlog

## Usage
- Use this backlog with [S3D_ENGINEERING_HARDENING_PRD.md](/D:/产品设计/New%20folder/docs/S3D_ENGINEERING_HARDENING_PRD.md).
- Claude should review scope, risk, sequencing, and operability language.
- Codex should implement only against canonical files under `backend/`, `scripts/`, `docs/`, and `releases/`.

## Epic S3-D-1 CI and Release Gate Hardening

### SP3-D-1 Release Gate Matrix Freeze
- Type: `DEV`
- Goal: define one governed local gate for fast validation and release validation
- Files:
  - `scripts/git_preflight.py`
  - `docs/RELEASE_PROCESS.md`
  - `docs/HANDOFF.md`
- Acceptance:
  - fast path and full path are both documented
  - test scope is explicit
  - manifest-backed review-pack generation is part of the release gate

### SP3-D-2 Review Pack Completeness Checks
- Type: `DEV`
- Goal: ensure review packs always include governed docs, tests, and fixtures required by the current stage
- Files:
  - `scripts/build_claude_review_pack.py`
  - `releases/release_manifest.json`
- Acceptance:
  - fixture directories are included deterministically
  - manifest-declared key files are automatically considered
  - missing files fail the pack step with actionable output

### SP3-D-3 Verify Gate Expansion
- Type: `QA`
- Goal: expand release verification to cover review-pack completeness and governed artifact presence
- Files:
  - `scripts/verify_release.py`
  - `releases/release_manifest.json`
- Acceptance:
  - verify checks artifact existence, snapshot consistency, and required review-pack coverage
  - verification failure reasons are explicit and reproducible

### SP3-D-4 Release Flow Review
- Type: `INT`
- Goal: review whether the release gate is understandable for both maintainers and reviewers
- Acceptance:
  - one documented release flow
  - no contradictory instructions between handoff, manifest, and release docs

## Epic S3-D-2 Wrapper and Path Cleanup

### SP3-D-5 Wrapper Inventory
- Type: `DEV`
- Goal: inventory all compatibility wrappers and alternate entrypoints
- Files:
  - `docs/PROJECT_STRUCTURE.md`
  - `docs/HANDOFF.md`
- Acceptance:
  - wrapper file list exists
  - each wrapper has a purpose and retirement trigger

### SP3-D-6 Import Path Guidance
- Type: `DEV`
- Goal: freeze canonical import-path guidance for future implementation work
- Files:
  - `docs/PROJECT_STRUCTURE.md`
  - `docs/GIT_WORKFLOW.md`
- Acceptance:
  - canonical modules and legacy entrypoints are clearly separated
  - future work instructions point only to canonical paths

### SP3-D-7 Wrapper Retirement Plan
- Type: `INT`
- Goal: define when wrappers may be removed without breaking supported workflows
- Files:
  - `docs/PROJECT_STRUCTURE.md`
  - `docs/HANDOFF.md`
- Acceptance:
  - retirement criteria are explicit
  - no wrapper removal is scheduled before criteria are met

## Epic S3-D-3 Runtime Operability

### SP3-D-8 Runtime Status Contract
- Type: `DEV`
- Goal: freeze a small but useful operational contract for health, readiness, degraded, and misconfiguration states
- Files:
  - `backend/app/runtime_service.py`
  - `backend/app/config.py`
  - new docs if needed
- Acceptance:
  - health and readiness semantics are documented
  - adapter state wording is operationally understandable
  - degraded causes are distinguishable from configuration failures

### SP3-D-9 Logging and Failure Taxonomy
- Type: `DEV`
- Goal: define structured logging expectations and failure categories for runtime and adapter behavior
- Files:
  - `backend/app/runtime_service.py`
  - `backend/app/tools/siem_adapter.py`
  - docs under `docs/`
- Acceptance:
  - failure categories are enumerated
  - at least one structured logging path exists for runtime failures
  - wording is suitable for operators rather than only developers

### SP3-D-10 Runtime Operability Tests
- Type: `QA`
- Goal: add regression coverage for readiness wording, adapter state exposure, and degraded-state diagnostics
- Files:
  - `backend/tests/test_runtime_service.py`
  - `backend/tests/test_secupilot_drafts.py`
- Acceptance:
  - readiness output assertions cover state wording
  - degraded diagnostics assertions cover operator-facing fields

## Epic S3-D-4 Collaboration and Review Governance

### SP3-D-11 Snapshot Transition Checklist
- Type: `DEV`
- Goal: define a single checklist for moving from one stage snapshot to the next
- Files:
  - `docs/HANDOFF.md`
  - `docs/RELEASE_PROCESS.md`
  - `releases/release_manifest.json`
- Acceptance:
  - snapshot transition steps are documented once
  - release, review-pack, and verify expectations stay aligned

### SP3-D-12 Claude Review Discipline Refresh
- Type: `DEV`
- Goal: update Claude-facing review guidance to match current repo and release reality
- Files:
  - `docs/CLAUDE_WEB_UPLOAD_CHECKLIST.md`
  - `docs/CLAUDE_WEB_ALIGNMENT_GUIDE.md`
  - `scripts/build_claude_review_pack.py`
- Acceptance:
  - Claude upload guidance no longer requires manual file hunting
  - review prompts can assume review-pack completeness

### SP3-D-13 Governance Review Pass
- Type: `INT`
- Goal: do one governance-focused review before declaring S3-D complete
- Acceptance:
  - no unresolved P1 governance issues
  - release and review instructions are internally consistent

## Recommended Sequence
1. `SP3-D-1` to `SP3-D-4`
2. `SP3-D-5` to `SP3-D-7`
3. `SP3-D-8` to `SP3-D-10`
4. `SP3-D-11` to `SP3-D-13`

## Claude Review Focus
- challenge whether release gating is complete enough
- review wrapper retirement timing and risk
- review runtime operability wording from an operator perspective
- flag any governance ambiguity that could recreate source-of-truth drift

## Codex Implementation Focus
- keep changes inside canonical repo paths
- avoid destructive wrapper cleanup until retirement criteria are frozen
- prefer deterministic scripts over checklist-only governance
