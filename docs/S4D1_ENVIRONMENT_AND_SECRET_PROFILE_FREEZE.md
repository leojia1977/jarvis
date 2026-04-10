# S4-D-1 Environment and Secret Profile Freeze

## Goal
Freeze the minimum environment and secret contract required for a Sprint 4 pilot deployment.

## Profiles

### `mock_local`
- Purpose:
  - local development
  - contract tests
  - deterministic replay and regression work
- Required environment fields:
  - `project_root`
  - `runtime_mode`
  - `mock_data_path`
  - `case_store_backend`
  - `case_store_path`
- Required secrets:
  - none
- Optional secrets:
  - `siem_auth_token`
  - `edr_auth_token`
  - `llm_api_key`

### `pilot_local`
- Purpose:
  - one governed pilot instance running inside the local deployment boundary
  - operator validation before `SP4-D-2` smoke-path work
- Required environment fields:
  - `project_root`
  - `runtime_mode=production`
  - `static_data_mode`
  - `static_data_path`
  - `siem_vendor` and it must be `splunk_like` or `elastic_like`
  - `siem_base_url`
  - `edr_source_mode`
  - `case_store_backend=sqlite_local`
  - `case_store_path`
- Required secrets:
  - `siem_auth_token`
  - `edr_auth_token` only when `edr_source_mode=api`
- Optional secrets:
  - `llm_api_key`

Pilot notes:
- if the pilot is hosted on a separate server for remote analyst or manager access, `server_host` must not remain the default `127.0.0.1`
- when `server_host` remains loopback, readiness should warn that remote pilot access is blocked by configuration
- `mock_data_path` is a legacy alias and is not part of `pilot_local` acceptance

## Frozen Grouping

### Runtime
- `project_root`
- `runtime_mode`
- `business_timezone`

### Static Data
- `mock_data_path`
- `static_data_mode`
- `static_data_path`
- `static_data_refresh_seconds`
- `asset_source_mode`
- `baseline_source_mode`
- `intel_seed_source_mode`
- `topology_source_mode`

### SIEM
- `siem_vendor`
- `siem_base_url`
- `siem_auth_token`
- `siem_request_timeout_seconds`

### EDR
- `edr_source_mode`
- `edr_vendor`
- `edr_base_url`
- `edr_auth_token`
- `edr_request_timeout_seconds`

### Case Store
- `case_store_backend`
- `case_store_path`
- `case_store_retention_days`

### Server
- `service_name`
- `service_version`
- `server_host`
- `server_port`
- `cors_origins`
- `log_level`

## Secret Handling Rules
- Secret values must never be emitted through `readiness()`, `health()`, logs, review packs, or handoff docs.
- Runtime may expose:
  - `required_secret_names`
  - `optional_secret_names`
  - `profile_contract_missing`
- Runtime must not expose:
  - raw `*_auth_token` values
  - `llm_api_key`

## Runtime Contract
- `Settings.get_environment_profile()` is the authoritative profile selector.
- `Settings.get_environment_contract()` is the authoritative contract summary for readiness and operator tooling.
- `readiness()` must expose:
  - `environment_profile`
  - `profile_contract_ready`
  - `profile_contract_missing`
  - `required_environment_fields`
  - `required_secret_names`
  - `optional_secret_names`

## Frozen Distinctions
- `mock_local` may continue to use `mock_data_path` as the active data root.
- `pilot_local` must set `static_data_path` explicitly and must not rely on the legacy `mock_data_path` fallback for acceptance.
- `pilot_local` always requires a configured SIEM profile and must not use `siem_vendor=generic_http`.
- `pilot_local` only requires EDR secrets when `edr_source_mode=api`; replay and local-file modes remain valid for pilot staging.
- `llm_api_key` is not required for the Sprint 4 pilot runtime path.

## Explicit Precondition Before `SP4-D-2`
Before `SP4-D-2 Pilot Smoke Path` starts, the project must add one of the following:
- `docs/S4A5_SOURCE_INTEGRATION_REVIEW_PASS.md`
- an equivalent governed `HANDOFF.md` record explicitly closing `SP4-A-5`

`SP4-D-1` does not close that source-integration governance gap. It records it as a required predecessor for the pilot smoke path.

## Acceptance
- required variables are explicit
- optional variables and defaults are documented
- mock versus pilot distinctions are clear
- readiness can report profile-level missing requirements without leaking secret values
