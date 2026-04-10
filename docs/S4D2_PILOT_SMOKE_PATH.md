# S4-D-2 Pilot Smoke Path

## Goal
Define one governed pilot smoke path that proves production-shaped ingestion, investigation, persistence, and retrieval work together before Sprint 4 pilot validation expands further.

## Governed Path ID
- `pilot_local_production_case_round_trip`

## Preconditions
- `SP4-A-5` is closed through `docs/S4A5_SOURCE_INTEGRATION_REVIEW_PASS.md`.
- runtime profile is `pilot_local`
- `runtime_mode=production`
- `static_data_path` is explicitly configured
- `siem_vendor` is `splunk_like` or `elastic_like`
- `siem_base_url` and `siem_auth_token` are configured
- `case_store_backend=sqlite_local`
- `case_store_path` is writable
- `edr_source_mode` is explicitly set

## Endpoint
- `POST /api/v1/pilot-smoke`
- success response: `200 OK`
- request validation failures inherited from investigation remain `400`
- readiness, persistence, or retrieval failures remain `503`

This endpoint runs one governed round trip:
1. readiness gate
2. production-shaped investigation request
3. persistent case creation
4. persisted case retrieval by `case_id`

## Request Shape
Minimum request body:

```json
{
  "user_input": "请检查是否存在横向移动",
  "intent": "threat_hunt",
  "time_range": "24h"
}
```

Recommended pilot request body:

```json
{
  "user_input": "请检查是否存在横向移动",
  "intent": "threat_hunt",
  "time_range": "24h",
  "actor": "pilot.operator"
}
```

## Step-By-Step Operator Flow
1. Call `GET /ready`.
2. Confirm:
   - `ready=true`
   - `environment_profile=pilot_local`
   - `state_class=READY`
   - `failure_category=none`
   - `case_store_ready=true`
3. Call `POST /api/v1/pilot-smoke` with the governed request body.
4. Confirm `smoke_path.path_id=pilot_local_production_case_round_trip`.
5. Confirm `smoke_path.steps` reports:
   - `readiness`
   - `investigate`
   - `create_case`
   - `get_case`
6. Confirm the response includes:
   - `case_id`
   - `persistent_case.case_id`
   - `persistent_case.lifecycle_status=open`
7. Treat the returned `persistent_case` payload as the governed retrieval proof for the smoke run.

## Success Contract
The pilot smoke path is successful only when:
- the runtime enters through `pilot_local`
- production-shaped SIEM ingestion succeeds
- the investigation returns a governed `threat_case`
- the case is persisted through the governed case store
- retrieval returns the same `case_id`
- the endpoint itself returns `200 OK` while the internal `create_case` step reports `http_status=201`
- `smoke_path.failed_step` is `null`

## Success Evidence Checklist
- a redacted `GET /ready` response excerpt showing `ready=true`, `state_class=READY`, and `failure_category=none`
- a redacted `POST /api/v1/pilot-smoke` request body
- a response excerpt showing `smoke_path.path_id=pilot_local_production_case_round_trip`
- a response excerpt showing `smoke_path.failed_step=null`
- a response excerpt showing `smoke_path.steps` in the governed order:
  - `readiness`
  - `investigate`
  - `create_case`
  - `get_case`
- evidence that `smoke_path.steps[2].http_status=201`
- evidence that `case_id == persistent_case.case_id`
- evidence that `persistent_case.lifecycle_status=open`
- operator identity or execution timestamp recorded alongside the redacted artifacts

## Failure Mapping

### `readiness`
- `MISCONFIGURED / adapter_config`
  - example: missing or incomplete production SIEM configuration
- `MISCONFIGURED / static_data`
  - example: missing `static_data_path` root or unsupported static source mode
- `BOOTSTRAP_FAILED / bootstrap`
  - example: runtime bootstrap exception while building the pipeline
- runbook sections:
  - [Health And Readiness](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md#health-and-readiness)
  - [Misconfigured Adapter Config](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md#misconfigured-adapter-config)
  - [Misconfigured Static Data](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md#misconfigured-static-data)
  - [Bootstrap Failed](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md#bootstrap-failed)

### `investigate`
- returns the existing governed investigation error payload if runtime is not ready or request validation fails
- `smoke_path.failed_step=investigate` must identify this stage explicitly
- runbook sections:
  - [Health And Readiness](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md#health-and-readiness)
  - [Pilot Smoke Failure Triage](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md#pilot-smoke-failure-triage)

### `create_case`
- persistence build or write failures remain governed runtime failures
- example: `case_store_unavailable`
- `smoke_path.failed_step=create_case` must identify that persistence failed after ingestion and investigation succeeded
- runbook sections:
  - [Pilot Smoke Failure Triage](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md#pilot-smoke-failure-triage)
  - [Case Store Failures](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md#case-store-failures)

### `get_case`
- retrieval failures remain governed runtime failures
- `smoke_path.failed_step=get_case` must identify that retrieval failed after persistence was attempted
- runbook sections:
  - [Pilot Smoke Failure Triage](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md#pilot-smoke-failure-triage)
  - [Case Store Failures](./S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md#case-store-failures)

## Scope Notes
- this path proves one governed pilot round trip, not full pilot operations coverage
- it does not add autonomous execution or containment
- it does not replace later operator runbooks or validation-gate work in `SP4-D-3` and `SP4-D-4`

## Acceptance
- one pilot path is documented step-by-step
- the path covers ingestion, investigation, persistence, and retrieval
- failure points map to governed runtime status categories
- the path is suitable as the deterministic baseline for later pilot validation work
