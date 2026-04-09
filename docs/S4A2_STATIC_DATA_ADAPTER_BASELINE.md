# S4-A-2 Static Data Adapter Baseline

## Purpose
Replace the remaining direct local bootstrap reads for T1, T4, and T5 with explicit static-data adapters while keeping the current investigation algorithms unchanged.

This baseline does not introduce real CMDB or topology APIs yet. It establishes the adapter layer and the governed failure envelope that later `api` or `hybrid` modes must reuse.

## What Changed
- `InvestigationPipeline.__init__()` no longer reads the four static JSON files directly.
- The pipeline now loads:
  - asset inventory
  - false-positive baselines
  - threat-intel seed data
  - topology data
  through explicit adapters under `backend/app/tools/static_data_adapters.py`.
- The local bootstrap path and future production-shaped paths now share one envelope:
  - `AdapterResult.ok`
  - `AdapterResult.unavailable`

## Adapter Baseline

### Local Files
The Sprint 4 bootstrap mode remains `local_files` (and `bundle`, which currently reuses the same local-file implementation).

Implemented sources:
- `LocalFileAssetInventorySource`
- `LocalFileBaselineSource`
- `LocalFileThreatIntelSeedSource`
- `LocalFileTopologySource`

Each source:
- reads one governed file under `static_data_path`
- returns one normalized snapshot object
- carries `StaticSourceMetadata`
- never returns a raw file blob directly to the pipeline

### Production-Shaped Placeholder
Modes not yet implemented in Sprint 4 baseline:
- `api`
- `hybrid`

These modes now return an explicit `AdapterResult.unavailable(...)` with:
- `gap_reason = static_source_mode_not_implemented:<source_kind>:<mode>`

That keeps the envelope stable before real API adapters are added.

## Runtime Bridge
The adapter layer currently normalizes static data into snapshot objects and then converts them back into the runtime payload shape expected by:
- `RealTriageEngine`
- `RealThreatIntelEngine`
- `RealBlastRadiusEngine`

This bridge is intentional in `S4-A-2`.

Why:
- Sprint 4 needs the source boundary fixed first
- it should not also rewrite T1/T4/T5 input contracts in the same ticket

## Configuration Semantics
`backend/app/config.py` remains the authority for:
- `static_data_mode`
- `static_data_path`
- `static_data_refresh_seconds`
- `asset_source_mode`
- `baseline_source_mode`
- `intel_seed_source_mode`
- `topology_source_mode`

Compatibility rule:
- `mock_data_path` remains a legacy alias
- `get_mock_data_dir()` continues to delegate to `get_static_data_dir()`

## Diagnosable Failure Semantics
Static-data adapter failures must be diagnosable.

Current governed reasons include:
- `static_source_missing:<source_kind>:<path>`
- `static_source_invalid_json:<source_kind>:<error>`
- `static_source_read_failed:<source_kind>:<error>`
- `static_source_mode_not_implemented:<source_kind>:<mode>`

Pipeline rule:
- any non-`ok` static-data adapter result is treated as bootstrap-blocking for now
- the raised error must retain the source kind and adapter status

## Explicit Deferrals
Not in `S4-A-2`:
- real CMDB / topology / intel seed API integrations
- host identity resolver implementation
- cache invalidation beyond the frozen TTL placeholder
- rewriting T1 / T4 / T5 to consume snapshot objects directly

## Acceptance
`S4-A-2` is complete when:
- the four static bootstrap reads are routed through explicit adapters
- local and future production-shaped paths share one `AdapterResult` envelope
- configuration and source-mode failures are diagnosable
- existing T1 / T4 / T5 behavior stays compatible with the governed mock dataset
