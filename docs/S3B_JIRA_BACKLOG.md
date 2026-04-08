# S3-B Jira Backlog

## Epic S3-B Analyst Case And Jarvis Experience

### SP3-B-1 Freeze Case View Contract
- Type: `DEV`
- Goal: freeze the analyst-facing case contract
- Files:
  - `backend/app/agents/graph.py`
  - contract docs under `docs/`
- Acceptance:
  - one stable case-facing structure
  - summary, evidence, Jarvis plan, and limits all represented

### SP3-B-2 Add Backend Case Shaping Layer
- Type: `DEV`
- Goal: build a view-model layer on top of raw tool results
- Files:
  - `backend/app/agents/graph.py`
  - new serializer or helper module if needed
- Acceptance:
  - raw tool results still exist
  - case-facing sections derived consistently

### SP3-B-3 Jarvis Embedding
- Type: `DEV`
- Goal: ensure Jarvis output is first-class in the case
- Files:
  - `backend/app/agents/graph.py`
  - `backend/app/agents/jarvis_hunt_engine.py`
- Acceptance:
  - hypothesis, next steps, and scope visible in one stable section

### SP3-B-4 Degraded UX Contract
- Type: `DEV`
- Goal: freeze backend fields needed to disable unsafe actions
- Files:
  - `backend/app/agents/graph.py`
  - docs
- Acceptance:
  - case includes action-disabled reason when applicable
  - degraded state is visible without reading raw audit fields

### SP3-B-5 Case Contract Tests
- Type: `QA`
- Goal: verify case-facing output shape and semantics
- Files:
  - `backend/tests/test_secupilot_drafts.py`
  - new case-facing tests if needed
- Acceptance:
  - summary fields tested
  - degraded fields tested
  - Jarvis section tested

### SP3-B-6 Product Review With Claude
- Type: `INT`
- Goal: run a focused product review against the case contract
- Inputs:
  - PRD
  - backlog
  - manifest-backed review pack
- Acceptance:
  - no unresolved P1 ambiguity in first-screen case design

## Suggested Sequence
1. `SP3-B-1`
2. `SP3-B-2`
3. `SP3-B-3`
4. `SP3-B-4`
5. `SP3-B-5`
6. `SP3-B-6`
