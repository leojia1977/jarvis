# S4-B-2 Production EDR Ingestion Baseline

## Goal
- Replace the last direct `process_events` bootstrap read with an explicit EDR adapter path.
- Keep T3 consuming the frozen runtime payload shape from Sprint 2 / SP4-B-1.
- Introduce a governed production EDR skeleton without leaking vendor fields into orchestrator logic.

## Delivered
- `backend/app/tools/edr_adapter.py`
  - adds `InMemoryEDRAdapter` for backward-compatible test and wrapper paths
  - adds `LocalFileEDRAdapter` for governed mock/local-file ingestion from `mock_data/process_events/`
  - adds `ProductionEDRAdapter` skeleton with `AdapterResult`-based timeout/unavailable/bad-response handling
  - adds `build_edr_adapter()` as the authoritative factory
- `backend/app/agents/graph.py`
  - `InvestigationPipeline` now builds or accepts an explicit `EDRAdapterProtocol`
  - `SaiLouOrchestrator._run_t3()` queries EDR through the adapter and converts batches with `process_event_batch_to_runtime_payload()`
  - `_determine_t3_hosts()` stops relying on direct process-event cache availability when the adapter is authoritative
- `backend/app/runtime_service.py`
  - runtime readiness now reads `process_event_hosts` from the EDR adapter runtime stats instead of direct cache length

## Compatibility Rules
- T3 input shape remains the frozen runtime payload schema consumed by `ProcessTreeCompiler`.
- `process_events_cache` is still accepted as a compatibility path and is wrapped by `InMemoryEDRAdapter`.
- Local-file and in-memory EDR sources intentionally preserve historical replay semantics and do not drop static mock events on relative time-window filtering.
- Production EDR continues to consume `TimeRangeSpec` and may apply real filtering at the adapter boundary.

## Failure Semantics
- Missing or unreadable local process-event files do not silently fallback to other sources.
- Production EDR maps:
  - timeout -> `production_edr_timeout`
  - invalid JSON / bad response -> `production_edr_bad_response:*`
  - transport unavailable -> `production_edr_unavailable:*`
  - not configured -> `production_edr_not_configured`
- `_run_t3()` records adapter-originated gaps explicitly and preserves `complete / partial / degraded` output semantics for the case layer.

## Test Gate
- `backend.tests.test_edr_adapter_contract`
  - contract batch bridge
  - local-file adapter load
  - production adapter normalization
  - not-configured production adapter
- `backend.tests.test_secupilot_drafts`
  - injected EDR adapter path for `_run_t3()`
- `backend.tests.test_runtime_service`
  - mock and production runtime readiness continue to expose governed `process_event_hosts`

## Out of Scope
- Real vendor authentication refresh flows
- Replay transport for EDR vendor fixtures
- Process-event persistence or retrieval APIs
- Any redesign of T3 analysis semantics
