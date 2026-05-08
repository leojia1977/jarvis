# GOAL-ECIVFE-33 Local Rule Engine

## Goal ID

```text
GOAL-ECIVFE-33_LOCAL_RULE_ENGINE
```

## Goal type

```text
script
```

## Goal statement

```text
Implement the local/offline deterministic ECI/VFE fixture analyzer that consumes metadata-only fixtures and emits structured chain, forecast, and correlation artifacts.
```

## Primary executable object

```text
script=scripts/eci_vfe_fixture_analyze.py
test=backend/tests/test_eci_vfe_fixture_analyze.py
artifact=artifacts/eci_vfe_fixture_runs/rc001/chain_assessment.json
artifact=artifacts/eci_vfe_fixture_runs/rc001/forecast_candidates.json
artifact=artifacts/eci_vfe_fixture_runs/rc001/correlation_result.json
artifact=artifacts/eci_vfe_fixture_runs/rc001/run_record.json
closeout=docs/S6_FAST_MVP_GOAL_ECIVFE_33_LOCAL_RULE_ENGINE_2026_05_08.md
```

## Inputs

```text
artifacts/product_acceleration/next_goal_candidate.json
mock_data/eci_vfe/eci_cases/*.json
mock_data/eci_vfe/vfe_cases/*.json
schemas/eci_chain_assessment.schema.json
schemas/vfe_forecast_candidate.schema.json
schemas/eci_vfe_correlation.schema.json
```

## Output paths

```text
docs/goals/GOAL-ECIVFE-33_LOCAL_RULE_ENGINE.md
scripts/eci_vfe_fixture_analyze.py
backend/tests/test_eci_vfe_fixture_analyze.py
artifacts/eci_vfe_fixture_runs/rc001/chain_assessment.json
artifacts/eci_vfe_fixture_runs/rc001/forecast_candidates.json
artifacts/eci_vfe_fixture_runs/rc001/correlation_result.json
artifacts/eci_vfe_fixture_runs/rc001/run_record.json
docs/S6_FAST_MVP_GOAL_ECIVFE_33_LOCAL_RULE_ENGINE_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-ECIVFE-33_LOCAL_RULE_ENGINE.md
scripts/eci_vfe_fixture_analyze.py
backend/tests/test_eci_vfe_fixture_analyze.py
artifacts/eci_vfe_fixture_runs/rc001/chain_assessment.json
artifacts/eci_vfe_fixture_runs/rc001/forecast_candidates.json
artifacts/eci_vfe_fixture_runs/rc001/correlation_result.json
artifacts/eci_vfe_fixture_runs/rc001/run_record.json
docs/S6_FAST_MVP_GOAL_ECIVFE_33_LOCAL_RULE_ENGINE_2026_05_08.md
```

## Allowed scope

```text
local/offline deterministic rule processing only
metadata-only synthetic fixture parsing and validation
structured chain/forecast/correlation artifact generation
focused automated tests for HOLD/PASS behavior
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
API keys
secrets/tokens/auth headers/raw customer logs
live connectors
production write-back
customer-visible publish/deploy/output
external pilot
production launch
backend API/schema migration
push
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-ECIVFE-33_LOCAL_RULE_ENGINE.md
py -3 scripts/eci_vfe_fixture_analyze.py --fixture-dir mock_data\eci_vfe --output artifacts/eci_vfe_fixture_runs/rc001
py -3 -m unittest backend.tests.test_eci_vfe_fixture_analyze
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
semantic similarity alone upgrades a case
high-stage label is emitted below the required threshold without suspected-state downgrade
evidence_gaps omit urgency, window_closes_in, deadline_basis, or fallback_if_missed
output contains raw prompt-injection text
VFE query_context is missing or loses audit-required non-bulk controls
script requires live Qwen/API/connectors, network access, secret, or API key
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
preserve generated HOLD evidence JSON and failing command output
do not delete unrelated residue files
```

## Evidence contract

```text
goal card validator PASS json
analyzer command transcript with assessment/forecast/correlation counts
unittest output for pass and hold-path tests
artifact manifests in chain_assessment/forecast_candidates/correlation_result/run_record
closeout report with exact command results and safety boundaries
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no production_writeback=true
no customer_visible_output=true
no Authorization header
no Bearer token
no api_key
no raw_payload
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-ECIVFE-34_OUTPUT_GUARD with the generated rc001 artifacts.
If HOLD, stop and report exact failing command plus blocker before any UI work.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-ECIVFE-33 local rule engine
stage and commit only Goal files
do not push
```
