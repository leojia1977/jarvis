# S3-C-2 Vendor Profile Hardening

## Goal
- close the remaining canonical alert gaps before expanding real vendor coverage
- keep `ProductionSIEMAdapter` as the only layer that knows vendor-specific request and response shapes
- improve safety for `splunk_like` and `elastic_like` query construction

## In Scope
- map `activity_name` into the canonical alert schema for production adapters
- sanitize `splunk_like` free-text query literals before building SPL search payloads
- replace risky `elastic_like query_string` usage with safer text matching
- add fixture playback tests for vendor-shaped responses
- preserve `AdapterResult` and `DEGRADED` semantics unchanged

## Out Of Scope
- replacing static bootstrap data for T1 / T4 / T5
- full native vendor API path migration beyond the current normalized edge
- EDR adapterization
- UI changes

## Hardening Decisions
1. `activity_name` is part of the canonical alert contract and must be present whenever the upstream vendor response exposes any of:
   - `activity_name`
   - `event.action`
   - `action`
   - `rule.name`
   - `alert_type`

2. `splunk_like` query construction must treat user input as data, not executable SPL syntax.

3. `elastic_like` free-text searching must prefer safe text matching over `query_string`.

4. fixture playback tests are the release gate for vendor-shaped payloads.

## Minimum Fixture Coverage
- one `splunk_like` alert fixture that proves:
  - canonical `activity_name` mapping
  - dangerous input characters are escaped
- one `elastic_like` alert fixture that proves:
  - canonical `activity_name` mapping
  - `match_phrase` is used instead of `query_string`
- one `elastic_like` timed-out fixture that proves:
  - `timed_out=true` still maps to `partial`
  - canonical fields survive partial telemetry
