# S5-A-2 Dry-Run Evidence Template

## Document Control
- Status: `draft for review`
- Baseline: `S5-A-2026-04-13-001`
- Source of truth: `D:\产品设计\New folder`
- Purpose: dry-run evidence template only
- Non-goal: not external pilot execution
- Upstream checklist: `docs/S5A1_PILOT_PREPARATION_CHECKLIST.md`

## Goal
Create the fillable evidence template for S5-A-2 so the S5-A-1 pilot preparation checklist can be converted into repeatable dry-run evidence capture.

This document does not execute the dry run, connect real external SIEM / EDR / source systems, collect secret values, or authorize external pilot execution.

## Scope
- Capture evidence from the governed pilot validation gate.
- Capture evidence from the governed `POST /api/v1/pilot-smoke` path.
- Record readiness pre-check fields before smoke-path execution evidence is accepted.
- Record failure evidence without inventing new runtime states or failure categories.
- Hand off redaction, sign-off, and dry-run closeout decisions to later S5-A tickets.

## Evidence Rules
- Evidence should come from governed repo artifacts or local dry-run outputs.
- Dry-run completion does not equal external pilot start.
- No real external SIEM, EDR, source, customer environment, production credential, or sensitive customer data is required for S5-A-2.
- Raw logs are not required when they contain sensitive content; use redacted summaries, PASS / FAIL outcomes, and minimal excerpts instead.

## Evidence Path A: Pilot Validation Gate
Canonical command:

```powershell
py -3 scripts\git_preflight.py --mode pilot
```

Source: `docs/S4D4_PILOT_VALIDATION_GATE.md`.

Capture:

| Field | Captured Value |
| --- | --- |
| command | `py -3 scripts\git_preflight.py --mode pilot` |
| run timestamp |  |
| branch |  |
| commit hash |  |
| snapshot ID | `S5-A-2026-04-13-001` |
| exit result |  |
| key files summary |  |
| release zip summary |  |
| review pack summary |  |
| pilot validation summary |  |
| tests summary |  |

Notes:
- The evidence should prove whether the canonical pilot validation gate completed successfully.
- Do not paste raw logs if they contain secret values, bearer tokens, auth headers, cookies, connection strings, raw credentials, API keys, or sensitive customer content.
- If the command fails, record the failing gate section and the redacted operator-facing summary.

## Evidence Path B: `POST /api/v1/pilot-smoke`
This path must remain aligned with `docs/S4D2_PILOT_SMOKE_PATH.md`.

Capture:

| Field | Captured Value |
| --- | --- |
| execution timestamp |  |
| operator / actor identity | Record non-sensitive operator identity only; do not record tokens, cookies, auth headers, or connection strings. |
| redacted `POST /api/v1/pilot-smoke` request body | Record minimal `user_input`, `intent`, `time_range`, and `actor` fields when present; do not record secrets. |
| `/ready` pre-check fields | See `Readiness Pre-Check Fields` below. |
| HTTP status | Expected on success: `200 OK` |
| `smoke_path.path_id` | Expected: `pilot_local_production_case_round_trip` |
| `smoke_path.steps` order | Expected: `readiness -> investigate -> create_case -> get_case` |
| `failed_step` | Expected on success: `null` |
| `create_case` `http_status` | Expected on success: `201` |
| `case_id` |  |
| `persistent_case.case_id` |  |
| `case_id` and `persistent_case.case_id` alignment |  |
| `persistent_case.lifecycle_status` | Expected on success: `open` |

Notes:
- Successful smoke evidence should show the governed case round trip without requiring external pilot execution.
- `smoke_path.path_id` confirms that the governed pilot smoke path ran instead of an alternate path.
- If the HTTP status, path ID, step order, `failed_step`, case alignment, or lifecycle status differs from S4-D-2 expectations, record the mismatch and use the failure capture section.

## Readiness Pre-Check Fields
Record these fields before accepting `POST /api/v1/pilot-smoke` dry-run evidence.

| Field | Expected Value | Captured Value |
| --- | --- | --- |
| top-level `ready` | `true` |  |
| `environment_profile` | `pilot_local` |  |
| `profile_contract_ready` | `true` |  |
| `profile_contract_missing` | empty |  |
| `case_store_ready` | `true` |  |
| `state_class` | `READY` |  |
| `failure_category` | `none` |  |
| `reasons` | reviewed |  |
| `operator_message` | reviewed |  |
| `server_host` | see warning below |  |

Remote access warning:
- If the dry run or later pilot preparation includes remote analyst / manager access, `server_host` must not remain `127.0.0.1`.
- A loopback `server_host` should be recorded as a readiness warning for remote pilot access blocked, not as an ignorable cosmetic detail.

## Redaction Reminder
- Do not record secret values, bearer tokens, auth headers, cookies, connection strings, raw credentials, API keys, or sensitive customer data.
- It is acceptable to record missing secret names or missing environment field names.
- Do not define the full pilot run log evidence redaction boundary here; S5-A-3 owns that boundary.
- When in doubt, prefer a redacted evidence summary over raw command or HTTP output.

## Failure Capture
Do not invent new runtime states or failure categories. Use governed fields and S4-D-3 triage mapping.

### `/ready` Not READY
If `/ready` is not `READY`, record the following and stop before smoke-path evidence capture:

| Field | Captured Value |
| --- | --- |
| `state_class` |  |
| `failure_category` |  |
| `reasons` |  |
| `operator_message` |  |
| `profile_contract_missing` |  |
| missing secret names or missing environment field names, if present |  |
| stop reason | `/ready` did not meet readiness pre-check requirements. |
| S4-D-3 triage chapter |  |

### Pilot-Smoke Failure
If `POST /api/v1/pilot-smoke` fails, record:

| Field | Captured Value |
| --- | --- |
| HTTP status |  |
| `failed_step` |  |
| `smoke_path.steps` observed order |  |
| redacted operator-facing error summary |  |
| S4-D-3 triage chapter |  |

Suggested S4-D-3 mapping:
- `readiness`: use the S4-D-3 health, readiness, misconfiguration, or bootstrap triage guidance based on `state_class`, `failure_category`, `reasons`, and `operator_message`.
- `investigate`: use S4-D-3 pilot-smoke failure triage for source / adapter / investigation normalization evidence.
- `create_case`: use S4-D-3 case store failure triage for case creation failures.
- `get_case`: use S4-D-3 case store failure triage for persisted case retrieval failures.

## Handoff To Later Tickets
- S5-A-3 owns the full pilot run log evidence redaction boundary.
- S5-A-4 owns the pilot sign-off checklist.
- S5-A-5 owns the dry-run versus external pilot boundary closeout.
- S5-A-2 evidence may feed those later tickets, but it does not replace their acceptance criteria.

## Acceptance
- The template captures pilot validation gate evidence using the canonical S4-D-4 gate entry.
- The template captures `POST /api/v1/pilot-smoke` evidence using S4-D-2 success and failure fields.
- The template requires readiness pre-check evidence before smoke-path evidence is accepted.
- The template preserves the boundary between dry-run evidence capture and external pilot execution.
- The template avoids secret capture and leaves the full pilot run log redaction boundary to S5-A-3.
