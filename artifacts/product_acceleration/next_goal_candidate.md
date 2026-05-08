# SecuPilot Next MVP Goal Candidate

Generated at: 2026-05-08T16:51:44

Selection mode: QUEUE_FALLBACK

## Candidate Goal

- queue_key: GOAL-ECIVFE-33_LOCAL_RULE_ENGINE
- goal_id: GOAL-ECIVFE-33_LOCAL_RULE_ENGINE
- goal_type: script
- statement: Implement the local/offline deterministic ECI/VFE fixture analyzer that consumes metadata-only fixtures and emits structured chain, forecast, and correlation artifacts.

## Exact Files

- docs/goals/GOAL-ECIVFE-33_LOCAL_RULE_ENGINE.md
- scripts/eci_vfe_fixture_analyze.py
- backend/tests/test_eci_vfe_fixture_analyze.py
- artifacts/eci_vfe_fixture_runs/rc001/chain_assessment.json
- artifacts/eci_vfe_fixture_runs/rc001/forecast_candidates.json
- artifacts/eci_vfe_fixture_runs/rc001/correlation_result.json
- artifacts/eci_vfe_fixture_runs/rc001/run_record.json
- docs/S6_FAST_MVP_GOAL_ECIVFE_33_LOCAL_RULE_ENGINE_2026_05_08.md

## Acceptance Commands

- py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-ECIVFE-33_LOCAL_RULE_ENGINE.md
- py -3 scripts/eci_vfe_fixture_analyze.py --fixture-dir mock_data\eci_vfe --output artifacts/eci_vfe_fixture_runs/rc001
- py -3 -m pytest backend\tests\test_eci_vfe_fixture_analyze.py
- git -c core.quotepath=false diff --check

## HOLD Conditions

- semantic similarity alone upgrades a case
- high-stage label is emitted below the required threshold without suspected-state downgrade
- evidence_gaps omit urgency, window_closes_in, deadline_basis, or fallback_if_missed
- output contains raw prompt-injection text
- VFE query_context is missing or loses audit-required non-bulk controls
- script requires live Qwen/API/connectors, network access, secret, or API key
- scope expands beyond listed files
