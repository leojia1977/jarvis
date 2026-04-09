# S3-C-3 Vendor Replay Spec

## Goal
- use vendor-shaped request/response fixtures to validate the end-to-end path from adapter normalization to final case output
- keep replay testing offline and deterministic
- prove that `ProductionSIEMAdapter` can consume realistic `splunk_like` and `elastic_like` payloads without leaking vendor logic into the orchestrator

## Fixture Format
Each replay fixture is a single JSON file describing one API call:

```json
{
  "vendor": "splunk_like",
  "endpoint_key": "intent_alerts",
  "scenario": "lateral",
  "request": {
    "intent": "threat_hunt",
    "user_input": "请检查横向移动"
  },
  "response": {
    "status": "ok",
    "results": []
  }
}
```

## Path And Naming
- directory: `backend/tests/fixtures/vendor_replay/`
- naming rule: `{vendor}_{endpoint_key}_{scenario}.json`

## Minimum Required Endpoints
Per vendor replay set, the minimum path is:
- `intent_alerts`
- `scenario_metadata`

This is the smallest path that can drive:
- vendor response normalization
- scenario metadata lookup
- final `threat_case` generation

## Replay Rules
1. replay tests must not make real network calls
2. replay tests must use a transport replacement, not patch orchestrator logic
3. fixtures may be hand-crafted, but field names and nesting must stay faithful to vendor documentation
4. tests must validate final case-facing outputs, not only adapter-local payloads

## Minimum Assertions
Each end-to-end replay test must prove:
- `activity_name` is non-empty after normalization
- `severity` is uppercased in the final case output
- `event_time` survives normalization in the adapter result
- `scenario_id` reaches the final case payload

## Explicitly Out Of Scope
- real vendor authentication
- live network calls
- refreshing tokens
- changing `graph.py`
- changing `case_view.py`
