# S4-B-4 T3 Production Parity Tests

## Goal
- Prove that T3 keeps its frozen evidence, persistence, IOC, and status semantics when fed by production-shaped EDR adapters.
- Validate that replayed EDR payloads normalize into canonical process events before T3 sees them.
- Ensure `partial` and `degraded` telemetry outcomes stay explicit under production-style ingestion.

## Delivered
- `backend/tests/test_t3_production_parity.py`
  - validates `crowdstrike_like` replay against frozen T3 contract values
  - validates `elastic_defend_like` replay against IOC extraction and persistence detection
  - validates orchestrator-level `partial` semantics for replayed EDR batches
  - validates orchestrator-level `degraded` semantics for unavailable production EDR transport
- `backend/tests/fixtures/vendor_replay/elastic_defend_like_process_events_ransomware.json`
  - now includes a `registry_set` event so replay coverage spans persistence detection as well as IOC extraction

## Parity Guarantees
- T3 still consumes only the frozen runtime payload schema produced by `process_event_batch_to_runtime_payload()`.
- No vendor-shaped keys such as `process`, `event`, `host`, `dns`, or `file` may appear in the runtime payload sent to T3.
- T3 output must keep the frozen contract:
  - `analysis_status` in `COMPLETE / PARTIAL / DEGRADED / FAILED`
  - typed IOC objects (`ip / domain / hash`)
  - persistence evidence objects with explicit `type`
  - chain and node identifiers remain host-scoped and deterministic

## Replay Coverage
- `crowdstrike_like` lateral replay
  - verifies attack-tool and hash extraction behavior survives vendor normalization
- `elastic_defend_like` ransomware replay
  - verifies `partial` transport status is explicit
  - verifies IOC extraction for `ip / domain / hash`
  - verifies `registry_run_key` persistence detection under vendor-shaped ECS payloads
- unavailable transport path
  - verifies `_run_t3()` returns `degraded` instead of silently hiding EDR failure

## Out Of Scope
- changes to T3 scoring thresholds or attack heuristics
- live EDR connectivity
- persistence of raw EDR telemetry
- case-view wording changes
