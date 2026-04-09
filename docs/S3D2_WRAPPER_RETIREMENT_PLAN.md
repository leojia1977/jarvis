# S3-D-2 Wrapper Retirement Plan

## Purpose
This document defines how SecuPilot will retire root-level compatibility wrappers without breaking supported workflows.

## Current Position
The repository already has a canonical structure:
- implementation under `backend/app/`
- structured tests under `backend/tests/`
- scripts under `scripts/`
- governed docs under `docs/`

Root-level wrappers still exist only to preserve older invocation paths and transition safety.

## Wrapper Categories

### Category A: Runtime and Bootstrap
- `_project_bootstrap.py`
- `run_runtime.py`

Risk:
- removal too early would break current shortcut startup flows

Retire only when:
- canonical startup command is the only documented runtime path
- no governed tests or docs still rely on `run_runtime.py`
- import bootstrap is no longer required for supported entrypoints

### Category B: Agent and Tool Re-Exports
- `graph_v3_orchestrator.py`
- `jarvis_hunt_engine.py`
- `process_tree_t3.py`
- `triage_engine.py`
- `threat_intel_T4.py`
- `blast_radius.py`
- `generate_mock_data.py`
- `generate_process_events.py`

Risk:
- old scripts, notebooks, or user habits may still import the root path

Retire only when:
- all governed docs point to canonical files
- all structured tests and release gates use canonical imports
- no manifest-backed release still depends on the compat roles

### Category C: Compatibility Test Entrypoints
- `test_t3_hunt.py`
- `test_secupilot_drafts.py`
- `selfcheck_t1_t5.py`

Risk:
- older commands and operator habits may still use root-level test shortcuts

Retire only when:
- test instructions in `HANDOFF.md`, `RELEASE_PROCESS.md`, and governance docs are canonical-only
- `git_preflight.py` and manifest-backed tests no longer depend on root-level invocations
- two consecutive governed snapshots complete without requiring wrapper-based test commands

## Retirement Method
Retirement must happen in this order:
1. Move all docs and governed commands to canonical paths.
2. Remove compat-role references from the manifest.
3. Keep wrappers present but unused for two consecutive governed snapshots.
4. Delete wrappers in a dedicated cleanup snapshot.
5. Re-run full release gate and Claude review on the cleanup snapshot.

## Explicit Non-Goals
- Do not remove wrappers during `S3-D-2`.
- Do not combine wrapper deletion with unrelated runtime or adapter changes.
- Do not delete wrappers based on assumption; use governed evidence from docs, tests, and manifest.

## Exit Criteria for S3-D-2
`S3-D-2` is complete when:
- wrapper inventory is documented
- canonical import guidance is frozen
- retirement criteria are explicit
- no wrapper deletion has occurred yet
