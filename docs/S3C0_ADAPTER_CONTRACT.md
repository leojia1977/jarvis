# S3-C-0 Adapter Contract Skeleton

## Goal
- Cut `graph.py` loose from adapter internals such as `._cache`
- Freeze the minimum runtime contract that both mock and future production adapters must satisfy
- Route adapter failures into the existing `DEGRADED / PARTIAL` semantics instead of falling into `ERROR`

## Frozen Types

### `TimeRangeSpec`
- `start_utc: datetime`
- `end_utc: datetime`
- `tz_label: str`

Rules:
- All calculations use UTC
- `tz_label` exists for display and request tracing only
- String inputs like `24h`, `7d`, `30m` must be normalized into `TimeRangeSpec` before adapter calls

### `AdapterResult[T]`
- `status: "ok" | "timeout" | "partial" | "unavailable"`
- `data: T`
- `latency_ms: float`
- `gap_reason: Optional[str]`
- `metadata: dict[str, Any]`

Rules:
- Adapters return an envelope even when no data is available
- `timeout / partial / unavailable` must not crash the investigation
- Orchestrator maps non-`ok` statuses into `audit_trail.degraded_reasons`

## Frozen Protocol

`SIEMAdapterProtocol` must provide:
- `query_recent_summary(time_range: TimeRangeSpec) -> AdapterResult[dict]`
- `query_asset_alerts(asset_id: str, time_range: TimeRangeSpec) -> AdapterResult[list]`
- `query_intent_alerts(intent: str, user_input: str, time_range: TimeRangeSpec) -> AdapterResult[list]`
- `get_scenario_metadata(scenario_id: str) -> AdapterResult[Optional[dict]]`
- `get_asset_context(asset_id: str) -> AdapterResult[Optional[dict]]`
- `get_runtime_stats() -> dict[str, int]`

## Orchestrator Rules
- `SaiLouOrchestrator` must only talk to the adapter through protocol methods
- `_gather_alerts()` must return `AdapterResult[list]`
- `_assemble_case()` must consume scenario metadata from adapter results, not from `._cache`
- `siem_adapter_timeout / siem_adapter_partial / siem_adapter_unavailable` must flow into `investigation_status = "DEGRADED"` when applicable

## Runtime Rules
- `runtime_mode` must be consumed by a factory branch
- `mock` builds `MockSIEMAdapter`
- `production` builds `ProductionSIEMAdapter` placeholder in S3-C-0
- Production placeholder may remain `not ready`, but the adapter branch must exist

## Double-Stack Boundary
Only these two boundaries need mock/production split:
- SIEM adapter
- EDR process event ingestion

Algorithm engines remain single-track:
- `RealTriageEngine`
- `RealThreatIntelEngine`
- `RealBlastRadiusEngine`
- `ProcessTreeCompiler`

## Test Gate
S3-C-0 is not accepted unless all of the following are covered:
- `TimeRangeSpec` normalization
- `MockSIEMAdapter` returns `AdapterResult`
- Orchestrator no longer depends on `._cache`
- SIEM adapter timeout degrades the case instead of returning `ERROR`
