# S4-A-3 Host Identity Resolver

## Goal
- create one authoritative host-identity resolver shared by SIEM asset queries, T3 host selection, and blast-radius targeting
- turn asset inventory into canonical host identity records without leaking source-specific lookup rules into the orchestrator
- make identity ambiguity explicit instead of silently guessing a host

## Canonical Resolver
- module: `backend/app/tools/host_identity.py`
- baseline implementation: `AssetInventoryHostIdentityResolver`
- frozen contract source: `backend/app/tools/static_data_sources.py`

## Resolution Order
`resolve_any(identifier)` must try matches in this order:
1. `asset_id`
2. `hostname`
3. `fqdn`
4. `ip_address`
5. `aliases`

The first successful stage must resolve to exactly one `canonical_asset_id`.

## Ambiguity Semantics
- no match: `AdapterResult.ok(None)` with metadata describing the attempted lookup
- ambiguous match: `AdapterResult.partial(None)` with `gap_reason=identity_ambiguous:<match_kind>:<value>`
- resolvers must not silently pick one host when multiple candidates remain

## Integration Points
- `SaiLouOrchestrator._gather_alerts()` uses the resolver to normalize explicit asset-query targets before calling `query_asset_alerts()`
- `SaiLouOrchestrator._determine_t3_hosts()` uses the same resolver for explicit targets, alert-derived internal IPs, and scenario-to-host hints
- `SaiLouOrchestrator._pick_blast_target()` uses the same resolver before choosing a blast-radius target
- `InvestigationPipeline` builds the resolver from `AssetInventorySnapshot` and injects it into the orchestrator

## Out of Scope
- `process_events` loading remains under `S4-B` because it is EDR telemetry, not static data
- multi-source identity federation is deferred; Sprint 4 A-3 uses `AssetInventorySnapshot` as the authoritative seed
- no changes to production EDR contract yet; `SP4-B-1` must consume this resolver contract as a prerequisite

## Acceptance Summary
- one normalized host identity structure exists
- SIEM and T3 host selection use the same resolver
- identity ambiguity is explicit, not silently guessed
- `SP4-B-1` may not freeze host-identity expectations until this resolver contract is accepted
