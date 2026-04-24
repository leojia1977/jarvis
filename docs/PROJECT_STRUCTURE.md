# Project Structure

## Canonical Layout
- `backend/app/agents/`: canonical agent implementations
- `backend/app/tools/`: canonical tool implementations
- `backend/app/main.py`: canonical runtime entry module
- `backend/app/runtime_service.py`: canonical runtime service boundary
- `backend/app/config.py`: canonical runtime and adapter configuration
- `backend/tests/`: structured test entrypoints
- `frontend/`: canonical Vite React TypeScript Web workbench surface
- `scripts/`: canonical data/build utilities
- `mock_data/`: canonical generated datasets
- `docs/`: governed design, contract, release, and collaboration documents
- `releases/`: generated manifests, review packs, release zips, and verification reports
- `.githooks/`: repository hook entrypoints
- `.gitignore`, `.gitattributes`, `.gitmessage.txt`: Git workflow controls

## Compatibility Layer
- Root-level `.py` files remain as thin wrappers.
- Their only purpose is to preserve the current runnable snapshot and commands.
- New feature work should target canonical files in `backend/` and `scripts/`.

## Wrapper Inventory

### Bootstrap Shim
- `_project_bootstrap.py`
  - Purpose: insert the repo root and `backend/` onto `sys.path`
  - Canonical dependency: the `backend/` application tree
  - Wrapper status: temporary

### Runtime Wrapper
- `run_runtime.py`
  - Canonical target: `backend/app/main.py`
  - Purpose: preserve the current root-level runtime command
  - Wrapper status: temporary

### Agent and Tool Re-Export Wrappers
- `graph_v3_orchestrator.py` -> `backend/app/agents/graph.py`
- `jarvis_hunt_engine.py` -> `backend/app/agents/jarvis_hunt_engine.py`
- `process_tree_t3.py` -> `backend/app/tools/process_tree_t3.py`
- `triage_engine.py` -> `backend/app/tools/triage_engine.py`
- `threat_intel_T4.py` -> `backend/app/tools/threat_intel.py`
- `blast_radius.py` -> `backend/app/tools/blast_radius.py`
- `generate_mock_data.py` -> `scripts/generate_mock_data.py`
- `generate_process_events.py` -> `scripts/generate_process_events.py`
  - Purpose: preserve legacy import and invocation paths
  - Wrapper status: temporary

### Compatibility Test Entrypoints
- `test_t3_hunt.py` -> `backend/tests/test_t3_hunt.py`
- `test_secupilot_drafts.py` -> `backend/tests/test_secupilot_drafts.py`
  - Purpose: preserve older test commands and smoke shortcuts
  - Wrapper status: temporary

### Standalone Smoke Script
- `selfcheck_t1_t5.py`
  - Current role: root-level T1/T5 smoke script with no canonical structured-test equivalent yet
  - Canonical replacement status: not created yet
  - Wrapper status: temporary until a backend/tests canonical replacement exists

## Canonical Import and Execution Rules
- New backend/runtime implementation work must target `backend/app/`, `backend/tests/`, and `scripts/`.
- New frontend Web workbench implementation work must target `frontend/` after the S6 scaffold decision.
- New docs and governance updates must target `docs/` and `releases/`.
- New imports should use canonical modules, for example:
  - `from app.agents.graph import ...`
  - `from app.tools.siem_adapter import ...`
  - `from backend.tests.test_vendor_replay import ...`
- The `app.*` examples are valid while `_project_bootstrap.py` or an equivalent `sys.path` setup is present.
- After Category A wrappers are retired, canonical imports should move to explicit package paths such as `backend.app.agents.graph`.
- Root-level wrappers may be used only for compatibility. They must not gain new business logic.

## Path Cleanup Rule
- If a change can be made once, make it in the canonical file and let wrappers re-export it.
- Do not duplicate business logic between root wrappers and canonical modules.
- Do not add new root-level wrappers unless there is an explicit compatibility need and a documented retirement path.

## Current Rule
- Canonical backend/runtime code lives under `backend/` and `scripts/`.
- Canonical frontend Web workbench code lives under `frontend/`.
- Root files are compatibility shims only.
- Git workflow and release governance are part of the controlled project structure.

## Wrapper Retirement Criteria
A wrapper may be deleted only when all of the following are true:
1. All governed tests and documented run commands have switched to canonical paths.
2. `release_manifest.json` no longer needs the corresponding `compat-*` role entries.
3. Two consecutive governed snapshots have shipped without any required workflow depending on the wrapper.
4. Removal has been explicitly recorded in the wrapper retirement plan and reviewed as non-breaking.
