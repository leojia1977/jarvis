# Governance Context Model

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Governance Context Model |
| Status | Docs-only draft for governance-context-model review |
| Snapshot | S5-GOVERNANCE-CONTEXT-MODEL-2026-04-17-001 |
| Stage | s5-governance-context-model |
| Baseline snapshot | S5-POST-S5C-IMPL5-MAINLINE-ROUTE-SELECTION-2026-04-17-001 |
| Baseline commit | `d972f3f32ada525ee04124be501f3521a3586c01` |
| Route | OPEN_GOVERNANCE_CONTEXT_MODEL_DOCS_ONLY_STAGE |
| Scope | Docs-only governance memory and context discipline |

This document defines the long-term governance context model for SecuPilot work. It does not authorize implementation, alter product behavior, change AI_COLLAB, or reopen any parked route.

## 2. Core Principle

Chat windows are execution context, not long-term product memory.

Repo-governed docs, manifest state, snapshots, route decisions, closeouts, release verification records, and periodic reviews are product memory. Any future new-window prompt should use the latest governed baseline and these repo artifacts as the source of truth rather than relying on old free-form discussion.

## 3. Authority Hierarchy

1. Current committed repo baseline and `releases\release_manifest.json`.
2. Governed source artifacts named in manifest key files.
3. Latest HANDOFF snapshot and stage guidance.
4. Route decisions, tickets, review passes, and closeouts in governed docs.
5. Rolling maps: `docs\PRODUCT_STATE.md`, `docs\GOVERNANCE_DECISION_LOG.md`, and `docs\ROADMAP_AND_PARKED_ITEMS.md`.
6. Current-stage prompt and human instructions.
7. Chat history and non-repo notes.

Rolling maps summarize governed truth. They do not override source docs, modify contracts, reopen routes, create readiness, or authorize implementation.

## 4. Three-Layer Context Model

### Layer 1: Per-Stage Minimal Input

Each new governance window should carry only:

- latest formal baseline commit, snapshot, stage, and manifest status
- governing source artifact for the requested stage
- inherited boundaries that must remain unchanged
- the specific stage task and allowed files
- explicit no-go, HOLD, review, gate, staging, commit, and push rules

The prompt should not paste old free-form conversations as authority. It may reference governed rolling maps for memory, but the stage prompt must still carry the latest formal baseline and inherited boundaries.

### Layer 2: Rolling Product Maps

Rolling maps are concise governed summaries:

- `docs\PRODUCT_STATE.md` summarizes the current governed product state.
- `docs\GOVERNANCE_DECISION_LOG.md` records compact append-only decision entries.
- `docs\ROADMAP_AND_PARKED_ITEMS.md` tracks parked, deferred, and possible future routes.

Rolling maps help humans and AI agents orient quickly. They are not implementation tickets, contract freezes, route authorizations, external pilot packages, or evidence stores.

### Layer 3: Periodic Synthesis And Review

Periodic synthesis should occur:

- every 5-10 governed stages
- before stream or milestone closeout
- before high-risk route selection
- before any route that might be misread as implementation, readiness, evidence retention, public endpoint work, real-data handling, source/telemetry reopen, or contract freeze

Synthesis may summarize and reconcile governed artifacts. It must not silently change authority, implementation scope, product semantics, or inherited boundaries.

## 5. Update Cadence

- Update `PRODUCT_STATE.md` when a governed baseline materially changes product state.
- Update `GOVERNANCE_DECISION_LOG.md` when a route, ticket, implementation, review pass, closeout, or governance model stage is accepted.
- Update `ROADMAP_AND_PARKED_ITEMS.md` when parked/deferred state changes or a reopen trigger is accepted.
- Recompute manifest key-file hashes only through governed docs/release process.
- Run full gate and release packaging only when explicitly authorized for closeout.

## 6. Implementation Authorization Rule

No implementation may proceed from a rolling map, handoff note, route-selection summary, or chat instruction alone.

Any implementation still requires:

- a separate scoped implementation ticket
- named files and exact behavioral scope
- review requirements
- human GO
- targeted tests and full gate
- release verification
- closeout artifact

If any step is missing, implementation is HOLD.

## 7. Inherited Boundaries

This governance model preserves:

- ORDIV-L1A remains `PARK_LOCAL_VALIDATION_NO_REPORT`.
- S5-B remains `PASS_AND_PARK`.
- S5-D remains `PASS_AND_PARK`.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- External pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- AI_COLLAB remains unchanged.

## 8. Non-Authorization

This document does not authorize:

- code changes
- test changes
- dependency changes
- fixture creation or modification
- runtime behavior changes
- API behavior changes
- schema or contract changes
- release script changes
- public close-case endpoint work
- real SIEM/EDR/source/telemetry access
- real-data validation, report creation, workbook access, CSV processing, or L1B syslog/log parsing
- evidence retention, storage, replay, deletion, expiry, evidence-pack behavior, or redaction policy freeze
- secrets handling implementation
- credentials, tokens, API keys, auth headers, cookies, or secret material
- external pilot readiness, execution, or sign-off
- S5-B or S5-D reopen
- S4-A resolver changes
- AI_COLLAB changes

## 9. HOLD Conditions

Hold the stage if any of the following occur:

- A rolling map is treated as implementation authorization.
- A rolling map is treated as overriding a governed source artifact.
- A chat window or old non-repo note is treated as product memory over the repo baseline.
- Any external pilot input is claimed `READY`.
- Any implementation begins without a separate scoped ticket, review, human GO, full gate, and closeout.
- Any high-risk route is selected without required review.
- Any parked boundary is weakened or reopened without a governed route decision.
- Full gate, release packaging, staging, commit, or push is requested before explicit human closeout authorization.

