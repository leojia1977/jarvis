# S4-A-5 Source Integration Review Pass

## Goal
Record the Sprint 4 A-stream source integration review before EDR and pilot-smoke work depend on these contracts.

## Baseline Reviewed
- snapshot reviewed: `S4-D-2026-04-10-002`
- review scope:
  - `S4-A-1` static-data source contract freeze
  - `S4-A-2` static-data adapter layer
  - `S4-A-3` host identity resolver
  - `S4-A-4` static-data cache and contract tests

## Review Outcome
`SP4-A-5` closes the governed source integration review with no open `P1` product ambiguity around identity authority.

This review accepts the stream because:
- `AssetInventorySnapshot` is the Sprint 4 authoritative seed for host identity.
- `InvestigationPipeline` now bootstraps T1 / T4 / T5 through explicit static-data adapters instead of direct static-file reads inside `graph.py`.
- one resolver contract now drives SIEM asset-query normalization, T3 host selection, and blast-radius target selection.
- identity ambiguity remains explicit through `AdapterResult.partial(...)` instead of silent host selection.
- unsupported source modes and missing static data surface governed `static_data` readiness failures instead of implicit fallback.

## Identity Authority Decision
- the canonical host authority for Sprint 4 is the asset-inventory contract, not SIEM alert strings, EDR vendor payloads, topology hints, or scenario keywords.
- SIEM, EDR, and scenario hints may provide lookup inputs, but downstream host decisions must resolve through one canonical resolver.
- when multiple hosts match the same identifier, runtime must report an identity gap and must not silently choose one candidate.

## Unsupported Source Fields
- asset inventory:
  - legacy `ip_address` is accepted only as a compatibility alias; the canonical contract remains `ip_addresses[]`.
  - non-canonical asset fields such as `known_behaviors`, `last_compromised_date`, `fqdn`, and `source_refs` are compatibility or enrichment inputs and are not frozen as cross-source first-class authority fields.
- baselines:
  - `activity_names[]` may be absent in local seed data; the adapter currently backfills it from `pattern_description`.
- threat-intel seed:
  - legacy `family` input is normalized into canonical `threat_type` / `actor`; it is not treated as a separate first-class contract field.
- topology:
  - topology records remain loosely typed as `nodes{}` plus `edges[]`; deeper node and edge typing is still deferred.

## Explicit Deferred Items
- `api` and `hybrid` static-data source modes are not implemented yet; they remain governed `unavailable` outcomes.
- `bundle` currently reuses the `local_files` implementation and is not yet a distinct backend.
- multi-source host-identity federation is deferred; Sprint 4 authority remains seeded only from `AssetInventorySnapshot`.
- T1 / T4 / T5 still consume bridged runtime payload shapes rather than snapshot objects directly.
- live background refresh and stale-serve-through behavior after TTL expiry remain out of scope for the Sprint 4 A-stream baseline.

## Accepted Baseline Guarantees
- one normalized static-data contract exists for asset inventory, baselines, intel seed, and topology.
- one authoritative host-identity resolver exists with frozen priority order: `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- missing or unsupported static data is diagnosable as a governed `static_data` readiness failure.
- downstream work may rely on S4-A identity authority only if it continues to route host decisions through the canonical resolver.

## Acceptance
`SP4-A-5` is complete when:
- no unresolved `P1` product ambiguity remains around identity authority.
- unsupported source fields and deferred items are explicitly listed.
- the governed snapshot remains backed by passing verification artifacts.
- this review record is accepted as the governed predecessor for `SP4-D-2`.
