# S3-C-1 SIEM Adapter Boundary

## Goal
- Implement the first production-facing `SIEMAdapterProtocol` path
- Keep orchestrator logic vendor-neutral
- Do not expand scope into T1/T4/T5 initialization data adapterization

## In Scope
- `ProductionSIEMAdapter` consumes runtime configuration
- production adapter sends normalized requests through a transport abstraction
- production adapter returns `AdapterResult` with the same shape as mock
- runtime `production` mode is bootstrappable when SIEM adapter configuration is present
- contract tests cover request normalization and response normalization

## Out Of Scope
- replacing `asset_dictionary.json`, `false_positive_baseline.json`, `mock_ioc_database.json`, or `entity_relationships.json`
- CMDB / asset inventory API integration
- EDR process-event adapterization
- vendor-specific detection logic inside orchestrator

## Boundary Decision
`S3-C-1` replaces only the alert-querying edge.

The following remain local bootstrap dependencies for now:
- T1 asset and baseline inputs
- T4 intelligence corpus bootstrap
- T5 topology bootstrap
- T3 mock process-event loading

These are intentionally deferred to `S3-D` or a later sprint.

## Collaboration Split
- `Codex`: implementation, tests, governed docs, manifest, release artifacts
- `Claude Code`: local repo review for contract soundness and degraded semantics
- `Claude Web`: milestone product review only when a governed review pack is ready
