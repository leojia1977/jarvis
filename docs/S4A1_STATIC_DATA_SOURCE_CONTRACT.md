# S4-A-1 Static Data Source Contract

## Purpose
Freeze the source contracts for the four remaining static-data domains still loaded directly during runtime bootstrap:
- asset inventory
- false-positive baselines
- threat-intel seed data
- topology or knowledge-graph data

This contract also freezes the authoritative `host identity` shape that later Sprint 4 work must use across SIEM, EDR, and blast-radius logic.

## Current Direct Reads To Be Eliminated In S4-A-2
`backend/app/agents/graph.py` currently loads the following files directly inside `InvestigationPipeline.__init__()`:
- `mock_data/assets/asset_dictionary.json`
- `mock_data/baselines/false_positive_baseline.json`
- `mock_data/threat_intel/mock_ioc_database.json`
- `mock_data/knowledge_graph/entity_relationships.json`

`S4-A-1` does not remove those reads yet. It freezes the contracts they must be replaced with in `S4-A-2`.

## Common Contract Rules
1. Every static-data source returns one governed snapshot object, not raw file blobs.
2. Every snapshot carries `StaticSourceMetadata`.
3. Every source declares:
   - `source_kind`
   - `source_name`
   - `source_mode`
   - `ownership`
   - `record_count`
   - `refresh_policy`
4. `local_files` remains the Sprint 4 bootstrap mode, but it is now an explicit source mode, not an implicit implementation detail.
5. Missing or stale static data must be diagnosable through governed runtime categories, not silent fallback.
6. `host identity` must become authoritative before any production EDR identity mapping is frozen.

## Source Modes
Allowed `source_mode` values:
- `local_files`
- `api`
- `bundle`
- `hybrid`

Sprint 4 baseline defaults:
- asset inventory: `local_files`
- baselines: `local_files`
- intel seed: `local_files`
- topology: `local_files`

## Refresh Policy
Allowed `refresh_strategy` values:
- `startup`
- `ttl`
- `manual`

Sprint 4 default:
- `startup`
- `ttl_seconds = 300` remains the default configuration placeholder for later adapter caching

## Canonical Domain Contracts

### 1. Asset Inventory
Contract object:
- `AssetInventorySnapshot`

Canonical record:
- `asset_id`
- `hostname`
- `ip_addresses[]`
- `business_unit`
- `owner`
- `network_segment`
- `role`
- `os`
- `criticality_weight`
- `aliases[]`
- `extra{}`

Current owner:
- T1 scoring context
- T5 blast-radius graph identity base
- later S4-A host-identity resolver seed

Current local source:
- `mock_data/assets/asset_dictionary.json`

### 2. False-Positive Baselines
Contract object:
- `BaselineSnapshot`

Canonical record:
- `baseline_id`
- `category`
- `pattern_description`
- `confidence`
- `scope_asset_ids[]`
- `activity_names[]`
- `extra{}`

Current owner:
- T1 baseline dampening and noise suppression

Current local source:
- `mock_data/baselines/false_positive_baseline.json`

### 3. Threat-Intel Seed
Contract object:
- `ThreatIntelSeedSnapshot`

Canonical record:
- `indicator`
- `indicator_type` in `ip | domain | hash`
- `threat_type`
- `actor`
- `confidence`
- `country`
- `tags[]`
- `extra{}`

Current owner:
- T4 initial enrichment seed

Current local source:
- `mock_data/threat_intel/mock_ioc_database.json`

### 4. Topology / Knowledge Graph
Contract object:
- `TopologySnapshot`

Canonical shape:
- `nodes{}`
- `edges[]`
- `metadata`

Current owner:
- T5 blast-radius engine

Current local source:
- `mock_data/knowledge_graph/entity_relationships.json`

## Host Identity Contract
Authoritative object:
- `HostIdentityRecord`

Canonical fields:
- `canonical_asset_id`
- `hostname`
- `fqdn`
- `ip_addresses[]`
- `aliases[]`
- `source_refs[]`
- `confidence`
- `extra{}`

Resolution contract:
- `resolve_any(identifier)`
- `resolve_asset_id(asset_id)`
- `resolve_ip(ip_address)`
- `resolve_hostname(hostname)`

Sprint 4 rule:
- `SP4-A-3` must freeze and review this contract before `SP4-B-1` freezes any production EDR host-identity expectations.

## Ownership Boundaries
- `S4-A-1` freezes contracts and configuration semantics
- `S4-A-2` implements static-data adapter replacement
- `S4-A-3` freezes the host-identity resolver
- `S4-B-1` may consume host-identity semantics only after `S4-A-3` is accepted

## Config Freeze For Sprint 4
`backend/app/config.py` must expose:
- `static_data_mode`
- `static_data_path`
- `static_data_refresh_seconds`
- `asset_source_mode`
- `baseline_source_mode`
- `intel_seed_source_mode`
- `topology_source_mode`

`mock_data_path` remains a legacy alias during Sprint 4 and must resolve to the same canonical static-data root until wrappers and bootstrap aliases are retired.

## Explicit Deferrals
Not in `S4-A-1`:
- real CMDB or knowledge-graph API implementation
- removal of current bootstrap file reads
- cache invalidation policy beyond the frozen placeholder fields
- EDR identity mapping logic
- persistence backend decisions for stored cases

## Acceptance
`S4-A-1` is complete when:
- all four static-data domains have one frozen contract object
- `host identity` has one frozen authoritative shape
- source ownership and refresh expectations are documented
- no hidden file-read dependency used by T1 / T4 / T5 remains undocumented
