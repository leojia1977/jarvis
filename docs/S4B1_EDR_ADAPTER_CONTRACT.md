# S4-B-1 EDR Adapter Contract

## Purpose
Freeze the production-facing EDR process-event contract before Sprint 4 starts implementation work on telemetry ingestion.

`S4-B-1` does not productionize EDR yet. It freezes:
- one canonical process-event schema
- one adapter protocol
- `TimeRangeSpec` parity with SIEM
- host-identity expectations inherited from `S4-A-3`
- one compatibility bridge back into the frozen T3 runtime payload

## Current Direct Read To Be Eliminated In S4-B-2
`backend/app/agents/graph.py` still loads process-event files directly during `InvestigationPipeline.__init__()`:
- `mock_data/process_events/process_events_<host>.json`

That path is intentionally still present in `S4-B-1`.
`S4-B-2` must replace it with an explicit EDR adapter path.

## Common Contract Rules
1. T3 must never consume vendor-shaped EDR payloads directly.
2. Every production-facing EDR adapter must return one canonical `ProcessEventBatch`.
3. Every EDR batch must be wrapped in `AdapterResult`.
4. `TimeRangeSpec` must be reused exactly as frozen in `S3-C`; EDR must not invent a second time-range model.
5. Host queries must align with `HostIdentityResolverProtocol` from `S4-A-3`.
6. `canonical_asset_id` is the authoritative host identifier for T3-facing telemetry.
7. Unsupported telemetry must degrade explicitly through `AdapterResult`, never via silent fallback to local files.

## Source Modes
Allowed `edr_source_mode` values:
- `local_files`
- `api`
- `replay`
- `bundle`
- `hybrid`

Sprint 4 baseline defaults:
- `edr_source_mode = local_files`
- `edr_vendor = generic_http`

## Canonical Process-Event Schema
Contract object:
- `CanonicalProcessEvent`

Required base fields on every event:
- `event_type`
- `host_id`
- `timestamp`
- `pid`
- `ppid`
- `process_name`
- `exe_path`
- `command_line`
- `user`

Allowed `event_type` values:
- `process_create`
- `network_connect`
- `dns_query`
- `registry_set`
- `file_write`

Event-type specific optional fields:

### network_connect
- `src_ip`
- `dst_ip`
- `dst_port`
- `protocol`

### dns_query
- `query_domain`
- `query_type`

### registry_set
- `key_path`
- `value_name`
- `value_data`

### file_write
- `file_path`
- `file_hash_sha256`

Additional vendor-specific or source-specific fields:
- must stay under `extra{}`
- must not leak into T3 output or case contracts

## Canonical Batch Contract
Contract object:
- `ProcessEventBatch`

Required fields:
- `metadata`
- `host_identity`
- `time_range`
- `events[]`

Batch metadata object:
- `EDRSourceMetadata`

Required metadata fields:
- `source_name`
- `source_mode`
- `vendor`
- `ownership`
- `collected_at_utc`
- `record_count`

## Adapter Protocol
Contract object:
- `EDRAdapterProtocol`

Frozen method:
- `query_process_events(host_identity: HostIdentityRecord, time_range: TimeRangeSpec) -> AdapterResult[ProcessEventBatch]`

Runtime stats:
- `get_runtime_stats() -> dict[str, int]`

## TimeRangeSpec Parity
EDR must reuse:
- `app.tools.siem_adapter.TimeRangeSpec`

Parity rules:
- all time comparisons remain UTC-based
- `tz_label` remains display metadata, not a second execution timezone
- `24h`, `12h`, and absolute derived windows must behave the same way in SIEM and EDR

## Host Identity Expectations
`S4-B-1` depends on `S4-A-3`.

Rules:
- callers must obtain `HostIdentityRecord` through the authoritative resolver, not ad hoc string guessing
- `ProcessEventBatch.host_identity.canonical_asset_id` is the authority for T3-facing host attribution
- `CanonicalProcessEvent.host_id` must resolve to that same canonical asset identity
- if production EDR telemetry cannot be mapped to one canonical asset identity, the adapter must return an explicit governed gap through `AdapterResult.partial(...)` or `AdapterResult.unavailable(...)`

## T3 Compatibility Bridge
`S4-B-1` freezes one compatibility bridge:
- `process_event_batch_to_runtime_payload(batch) -> list[dict]`

Rules:
- the bridge produces the same runtime event shape T3 already consumes today
- `S4-B-2` may replace the loader path, but must not change `ProcessTreeCompiler.analyze(host_id, events)` input shape
- vendor-specific fields remain inside the adapter layer

## Config Freeze For Sprint 4
`backend/app/config.py` must expose:
- `edr_source_mode`
- `edr_vendor`
- `edr_base_url`
- `edr_auth_token`
- `edr_request_timeout_seconds`

## Explicit Deferrals
Not in `S4-B-1`:
- real EDR HTTP implementation
- replay transport implementation
- replacement of `graph.py` local `process_events` bootstrap path
- artifact collection beyond process events
- file download or memory acquisition
- deep vendor-specific optimization

## Acceptance
`S4-B-1` is complete when:
- one canonical process-event schema exists
- `TimeRangeSpec` parity with SIEM is explicit
- host-identity expectations align with `S4-A-3`
- one T3 compatibility bridge is frozen so later adapterization does not mutate T3 contracts
