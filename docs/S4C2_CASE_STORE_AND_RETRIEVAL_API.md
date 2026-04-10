# S4-C-2 Case Store and Retrieval API

## Purpose
Implement governed persistence and retrieval for durable analyst cases without changing the frozen case schema from `S4-C-1`.

`S4-C-2` adds:
- one local SQLite case store
- one governed `create case` runtime path
- one governed `get case by case_id` runtime path
- diagnosable persistence failure output

`S4-C-2` does **not** add:
- lifecycle status mutation APIs
- approval submission or approval execution
- destructive remediation
- search or list endpoints beyond direct `case_id` retrieval

## Frozen Runtime Entry Points
Implemented runtime methods:
- `SecuPilotRuntimeService.create_case_sync(payload)`
- `SecuPilotRuntimeService.get_case_sync(case_id)`

Implemented HTTP routes:
- `POST /api/v1/cases`
- `GET /api/v1/cases/{case_id}`

Rules:
1. `POST /api/v1/cases` runs the governed investigation path first, then persists the resulting record.
2. `GET /api/v1/cases/{case_id}` returns the stored durable case record without mutating it.
3. `POST /api/v1/investigate` remains non-persistent and unchanged.

## Persistence Backend
Backend remains frozen to:
- `sqlite_local`

Implementation rules:
- case-store parent directory must be created automatically before first write
- writes must be serialized inside the process
- stored payload is the full governed `PersistentCaseRecord` JSON
- retrieval reconstructs a fresh record object from stored JSON, not a cached mutable reference

## Case Store Module
Primary module:
- `backend/app/tools/case_store.py`

Primary responsibilities:
- initialize SQLite schema if absent
- save one governed case record by `case_id`
- retrieve one governed case record by `case_id`
- expose minimal runtime stats for readiness and diagnostics

## Durable Storage Shape
The SQLite table stores:
- `case_id`
- `lifecycle_status`
- `created_at_utc`
- `updated_at_utc`
- `source_snapshot_id`
- `schema_version`
- `payload_json`

Rules:
- `payload_json` is authoritative for the full durable record
- indexed scalar columns exist only to keep retrieval and governance simple
- `payload_json` must round-trip back into `PersistentCaseRecord`

## Persistence Failure Semantics
Persistence failures must return structured runtime output.

Error envelope:
- `status = "error"`
- `error = "case_store_unavailable"`
- `storage.backend`
- `storage.store_path`
- `storage.reason`
- `storage.operator_message`
- `storage.detail`

Required diagnosable reasons:
- `case_store_backend_not_supported`
- `case_store_parent_init_failed`
- `case_store_connect_failed`
- `case_store_schema_init_failed`
- `case_store_write_failed`
- `case_store_read_failed`
- `case_store_payload_invalid`

## Follow-Up Constraints Carried From S4-C-1 Review
`S4-C-2` closes the first implementation follow-ups from the schema review:

- action-request IDs and audit IDs are no longer hard-coded to `001`; helper functions generate the next governed ID
- callers must not append into `action_requests[]` or `lifecycle_audit[]` in place
- durable changes must return a new `PersistentCaseRecord`
- moving a case into `in_review` requires a non-empty `review_owner`

## Retrieval Stability Rules
1. Retrieval must not mutate the stored durable payload.
2. Retrieval must return a fresh record shape on every call.
3. Callers may mutate the returned JSON copy, but that must never alter stored state.

## Acceptance
`S4-C-2` is complete when:
- a case can be created and saved through governed runtime code
- a case can be retrieved by `case_id`
- persistence failures return diagnosable storage details
- retrieval is proven not to mutate stored data
- `PersistentCaseRecord` helper functions prevent ID collisions and discourage in-place list mutation
