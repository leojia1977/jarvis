# S5-A-3 Pilot Run Log Evidence Redaction Boundary

## Document Control
- Status: `draft for review`
- Baseline: `S5-A-2026-04-13-002`
- Source of truth: `D:\产品设计\New folder`
- Purpose: pilot run log evidence redaction boundary
- Non-goal: not operator escalation triage replacement, not sign-off checklist, not external pilot execution
- Upstream checklist: `docs/S5A1_PILOT_PREPARATION_CHECKLIST.md`
- Upstream evidence template: `docs/S5A2_DRY_RUN_EVIDENCE_TEMPLATE.md`

## Goal
Define the redaction boundary for evidence that may be retained in dry-run evidence, pilot-prep run logs, and future sign-off records.

This document does not execute a dry run, connect real SIEM / EDR / source systems, create a sign-off checklist, or authorize external pilot execution.

## Scope
- Define what pilot run log evidence may be recorded and retained.
- Define what evidence must be omitted or redacted.
- Define name-only fields that may be captured as labels but never as values.
- Provide guidance for the two S5-A-2 evidence paths:
  - `py -3 scripts\git_preflight.py --mode pilot`
  - `POST /api/v1/pilot-smoke`
- Keep S5-A-3 compatible with the governed S4-D-3 and `RELEASE_PROCESS` escalation redaction rules without replacing them.

## Boundary Definition
S5-A-3 defines the pilot run log evidence redaction boundary. It is related to, but distinct from, the operator escalation triage boundary.

Operator escalation triage redaction:
- governed by `docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md` and `docs/RELEASE_PROCESS.md`
- used when an operator asks for help on readiness, smoke-path, case-store, or runtime failures
- focuses on the small redacted artifact set needed for troubleshooting escalation

Pilot run log evidence redaction:
- governed by this S5-A-3 document
- used for dry-run evidence, pilot-prep run logs, and future sign-off records
- focuses on what evidence may be saved as part of the pilot-prep record

S5-A-3 does not modify S4-D-3 or `RELEASE_PROCESS` triage rules. If evidence is collected for escalation, use the S4-D-3 and `RELEASE_PROCESS` rules. If evidence is retained for dry-run or pilot-prep records, use this document.

## Allowed Evidence
The following evidence types may be recorded when they do not contain secret values or sensitive customer data:

- snapshot ID
- branch
- commit hash
- command name and arguments, for example `py -3 scripts\git_preflight.py --mode pilot`
- run timestamp
- operator / actor identity if non-sensitive
- gate exit result
- PASS / FAIL summary for key files
- PASS / FAIL summary for release zip
- PASS / FAIL summary for review pack
- PASS / FAIL summary for pilot validation
- PASS / FAIL summary for tests
- `auth_header_present=true/false`, as a presence boolean only
- `cookie_present=true/false`, as a presence boolean only
- HTTP status
- `smoke_path.path_id`
- `smoke_path` step names and statuses
- `failed_step`
- `state_class`
- `failure_category`
- `reasons` after confirming they contain no secret values
- `operator_message` after confirming it contains no secret values
- missing environment field names
- missing secret names, names only
- `case_id` and `persistent_case.case_id` if governed docs already treat them as non-secret operational identifiers
- `persistent_case.lifecycle_status` only in the S4-D-2 / S5-A-2 governed smoke evidence context
- redacted clean runtime log excerpts only when needed to explain a failure stage and only under the boundary below

## Prohibited Evidence
The following evidence types must not be recorded in dry-run evidence, pilot-prep run logs, or future sign-off records:

- secret values
- bearer tokens
- auth headers
- cookies
- connection strings
- raw credentials
- API keys
- unredacted request bodies
- unredacted response bodies
- raw vendor SIEM payloads if they include sensitive identifiers or customer data
- raw vendor EDR payloads if they include sensitive identifiers or customer data
- local filesystem paths containing private user or customer information, unless redacted
- stack traces or logs that include secret values
- environment dumps that include secret values or local private paths

## Clean Runtime Log Excerpts Boundary
Pilot-prep records do not require runtime log excerpts by default.

If a failure stage cannot be explained clearly without a clean runtime log excerpt, the retained evidence may include a short redacted excerpt only when it excludes:
- secret values
- auth material
- raw credentials
- customer-identifying payloads
- private filesystem paths
- bearer tokens, auth headers, cookies, connection strings, or API keys

Escalation-purpose log collection remains governed by `docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md` and `docs/RELEASE_PROCESS.md`. S5-A-3 does not replace those escalation rules.

## Name-Only Fields
These fields may be recorded as names or schema labels only. Their values must not be recorded.

- missing secret names
- required secret names
- missing environment variable names
- config field names
- vendor field names when used as schema labels only

Examples:
- Allowed: `missing secret name: siem_auth_token`
- Prohibited: `siem_auth_token=<value>`
- Allowed: `missing environment field: siem_base_url`
- Prohibited: `siem_base_url=https://private.example.internal`

## Evidence Path A Guidance: Pilot Validation Gate
Canonical command:

```powershell
py -3 scripts\git_preflight.py --mode pilot
```

Allowed:
- command name and arguments
- run timestamp
- branch
- commit hash
- snapshot ID
- exit result
- PASS / FAIL summaries for key files, release zip, review pack, pilot validation, and tests
- failing stage name when the gate fails
- redacted operator-facing summary when the gate fails
- redacted clean runtime log excerpt only when it is necessary to explain a failure stage

Prohibited:
- raw logs containing credentials
- local secret paths
- full environment dumps
- bearer tokens, auth headers, cookies, connection strings, raw credentials, or API keys
- stack traces that include secret values
- private filesystem paths that identify a user, customer, or local secret location

If failure occurs:
- record the failing stage
- record the redacted operator-facing summary only
- do not paste raw logs if they include credentials, local secret paths, private filesystem paths, or environment dumps

## Evidence Path B Guidance: `POST /api/v1/pilot-smoke`
Allowed:
- redacted request body shape
- `user_input`, `intent`, `time_range`, and `actor` when present and non-sensitive
- actor identity if non-sensitive
- HTTP status
- `smoke_path.path_id`
- `smoke_path.steps`
- `failed_step`
- `create_case` HTTP status
- `case_id` and `persistent_case.case_id` alignment
- `persistent_case.lifecycle_status`
- readiness fields such as `state_class`, `failure_category`, `reasons`, and `operator_message` after confirming they contain no secret values
- `auth_header_present=true/false` and `cookie_present=true/false` as presence booleans only

Prohibited:
- secret values
- auth headers
- cookies
- bearer tokens
- raw external SIEM payloads
- raw external EDR payloads
- unredacted request bodies
- unredacted response bodies
- header or cookie values

If failure occurs:
- record `failed_step`
- record the S4-D-3 triage mapping
- record governed fields such as `state_class`, `failure_category`, `reasons`, and `operator_message` only after confirming they contain no secret values
- do not invent new failure categories
- do not reinterpret failed smoke evidence as external pilot feedback

## Examples

### Acceptable Evidence Snippet

```json
{
  "snapshot_id": "S5-A-2026-04-13-002",
  "branch": "codex/s3-a-runtime",
  "commit_hash": "example123",
  "command": "py -3 scripts\\git_preflight.py --mode pilot",
  "run_timestamp": "2026-04-13T15:00:00+08:00",
  "operator_identity": "pilot.operator",
  "gate_exit_result": "PASS",
  "pilot_validation_summary": "PASS",
  "tests_summary": "PASS"
}
```

### Prohibited Evidence Rewritten As Redacted Evidence

Prohibited:

```text
Authorization: Bearer <raw-token-value>
Cookie: <raw-cookie-value>
siem_auth_token=<raw-secret-value>
siem_base_url=https://private-customer-host.example.internal
```

Acceptable redacted form:

```json
{
  "auth_header_present": true,
  "cookie_present": true,
  "required_secret_names": ["siem_auth_token"],
  "missing_environment_field_names": [],
  "siem_base_url_status": "configured",
  "secret_values_recorded": false
}
```

## Handoff To Later Tickets
- S5-A-4 owns the pilot sign-off checklist.
- S5-A-5 owns the dry-run versus external pilot boundary closeout.
- S5-A-3 may be referenced by S5-A-4 and S5-A-5, but it does not replace their acceptance criteria.
- Future sign-off records may reuse this redaction boundary, but sign-off approval remains out of scope for this document.

## Acceptance
- Pilot run log evidence redaction is documented separately from operator escalation triage redaction.
- The boundary is compatible with S4-D-3 and `RELEASE_PROCESS` escalation redaction without replacing them.
- Allowed, prohibited, and name-only evidence categories are explicit.
- Evidence Path A and Evidence Path B guidance are aligned to S5-A-2.
- The document does not start external pilot execution or create a sign-off checklist.
