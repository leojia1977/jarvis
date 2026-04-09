# S4-B-3 EDR Replay Transport and Fixtures

## Goal
- Provide governed offline replay coverage for production-shaped EDR payloads.
- Prove canonical EDR normalization without live network access.
- Keep replay semantics isolated at the adapter boundary so T3 stays vendor-agnostic.

## Delivered
- `backend/tests/test_edr_replay.py`
  - adds `EDRReplayTransport`
  - validates deterministic endpoint-key matching for EDR replay
  - validates canonical normalization for two vendor-shaped payload sets
  - validates end-to-end investigation output for both replay fixtures
- `backend/tests/fixtures/vendor_replay/crowdstrike_like_process_events_lateral.json`
  - covers a lateral-movement process-event chain for `WKST-047`
- `backend/tests/fixtures/vendor_replay/elastic_defend_like_process_events_ransomware.json`
  - covers a ransomware precursor process-event set for `HR-PORTAL-01`

## Fixture Convention
- Path: `backend/tests/fixtures/vendor_replay/{vendor}_{endpoint_key}_{scenario}.json`
- One file represents one replayable request/response pair.
- Required top-level fields:
  - `vendor`
  - `endpoint_key`
  - `scenario`
  - `request`
  - `response`
- For `SP4-B-3`, the frozen EDR replay endpoint key is `process_events`.

## Replay Rules
- Replay transport must match endpoint keys deterministically from the requested URL suffix.
- Unknown endpoints must fail loudly instead of returning empty data.
- Replay fixtures must preserve vendor-shaped nesting and field names until canonical normalization occurs in `ProductionEDRAdapter`.

## Validation Scope
- `crowdstrike_like`
  - validates `process_create`, `network_connect`, and `file_write` normalization
  - validates `WKST-047` end-to-end investigation path
- `elastic_defend_like`
  - validates ECS-style nested payload normalization
  - validates `partial` status propagation without leaking raw vendor fields
  - validates `HR-PORTAL-01` end-to-end investigation path

## Out Of Scope
- live EDR authentication flows
- real network replay against vendor infrastructure
- changes to frozen T3 analysis semantics
- persistence or retrieval of raw EDR events
