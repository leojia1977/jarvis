# S3-D-3 Runtime Operability Contract

## Purpose
Freeze a small operator-facing contract for runtime health, readiness, misconfiguration, bootstrap failure, and degraded startup conditions without redesigning the existing investigation-state model.

## Scope
- document current `health()` and `readiness()` semantics
- expose a stable `state_class` and `failure_category`
- keep `AdapterResult` and case-level degraded semantics unchanged
- add at least one structured runtime logging path for startup and readiness failures

## Non-Goals
- no redesign of `AdapterResult`
- no redesign of case-level `DEGRADED` / `PARTIAL` semantics
- no full metrics or tracing platform
- no replacement of runtime bootstrap with a new framework

## Runtime State Contract

### Health
`GET /health` answers whether the runtime process is broadly healthy enough to answer liveness checks.

Returned fields:
- `status`
  - `healthy` when runtime `state_class == READY`
  - `degraded` otherwise
- `state_class`
- `failure_category`
- `operator_message`
- `reasons`
- `service`
- `version`
- `mode`
- `uptime_seconds`
- `timestamp`

### Readiness
`GET /ready` answers whether the runtime can currently serve `investigate` requests.

Returned fields:
- `ready`
- `state_class`
- `failure_category`
- `operator_message`
- `adapter_type`
- `adapter_configured`
- `static_data_path`
- `static_data_present`
- `scenarios_loaded`
- `process_event_hosts`
- `reasons`

## State Classes

### `READY`
- meaning: runtime pipeline and adapter are available
- failure category: `none`
- operator message: runtime ready

### `MISCONFIGURED`
- meaning: runtime cannot start because required configuration or required local static datasets are missing
- failure categories:
  - `adapter_config`
  - `static_data`

### `BOOTSTRAP_FAILED`
- meaning: runtime had the required inputs but failed while constructing the investigation pipeline
- failure category:
  - `bootstrap`

### `DEGRADED`
- meaning: runtime started in a reduced state that is neither a pure configuration miss nor a clean bootstrap failure
- failure category:
  - `runtime`

## Failure Category Mapping
- `production_adapter_not_configured` -> `MISCONFIGURED` / `adapter_config`
- `mock_data_missing:*` -> `MISCONFIGURED` / `static_data`
- `bootstrap_failed:*` -> `BOOTSTRAP_FAILED` / `bootstrap`
- any future non-startup readiness problem -> `DEGRADED` / `runtime`

## Structured Logging
Runtime startup and readiness failures must emit one structured log event under the `secupilot.runtime` logger.

Current required events:
- `runtime.context.not_ready`
- `runtime.context.bootstrap_failed`
- `runtime.investigate.not_ready`
- `runtime.investigate.invalid_request`

Required log fields:
- `event`
- `service`
- `mode`
- `failure_category`
- `reasons` or `reason`

## Operator Guidance
- `adapter_type` and `adapter_configured` tell operators whether the runtime is using `MockSIEMAdapter` or `ProductionSIEMAdapter`
- `static_data_path` and `static_data_present` clarify why production mode may still fail startup if local governed datasets are absent
- `state_class` should be treated as the top-level operational status; `reasons` remain the detailed trace

## Exit Criteria
- runtime health and readiness outputs expose the fields above
- runtime failure taxonomy is documented once and reused
- tests cover `READY`, `MISCONFIGURED`, and `BOOTSTRAP_FAILED`
- at least one structured runtime failure log path is regression tested
