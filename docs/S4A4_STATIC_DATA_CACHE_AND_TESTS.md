# S4-A-4 Static Data Cache and Contract Tests

## Goal
- add governed regression coverage for static-data source contracts
- freeze TTL cache and refresh semantics for static-data adapters
- confirm identity-resolution edge cases stay explicit before `SP4-B-1`

## Cache Baseline
- cache wrapper: `with_static_data_cache(...)`
- default behavior: every source built by `build_static_data_source_adapters(...)` is wrapped with the configured TTL cache
- cache stores only successful `ok` results
- failed refreshes are never silently cached as success
- once the TTL expires, the next load must call the inner source again

## Governed Outcomes
- missing static-data root remains a runtime `MISCONFIGURED / static_data` outcome
- unsupported or failed static-data source loads are surfaced as `static_data_unavailable:*` readiness reasons
- bootstrap must not silently continue with stale or missing static snapshots after TTL expiry

## Regression Coverage
- `backend/tests/test_static_data_adapters.py`
  - cache hit before expiry
  - cache refresh after expiry
  - cache expiry followed by source disappearance returns governed `unavailable`
  - bundle and api-shaped source modes remain covered
- `backend/tests/test_runtime_service.py`
  - missing static root stays `MISCONFIGURED / static_data`
  - unsupported static source mode is classified as `MISCONFIGURED / static_data`
- `backend/tests/test_host_identity_resolver.py`
  - frozen resolution priority
  - ambiguous alias handling

## Out of Scope
- live background refresh threads
- partial-stale runtime serve-through after bootstrap
- EDR `process_events` adapter work; that remains `S4-B`

## Acceptance Summary
- mock and production-shaped adapter results are covered
- stale or missing static data produces governed outcomes instead of implicit fallback
- identity-resolution edge cases are tested before EDR contract freeze
