# SecuPilot Next MVP Goal Candidate

Generated at: 2026-05-09T09:17:11

Selection mode: QUEUE_FALLBACK

## Candidate Goal

- queue_key: GOAL-ECIVFE-32_FORECAST_CARD_UI
- goal_id: GOAL-ECIVFE-32_FORECAST_CARD_UI
- goal_type: page
- statement: Render guard-passed VFE forecast cards as defensive summaries with urgency, collection-window guidance, and no attacker-readable attack path or topology detail.

## Exact Files

- docs/goals/GOAL-ECIVFE-32_FORECAST_CARD_UI.md
- frontend/src/secupilot/eciVfe/VfeForecastCard.tsx
- frontend/src/secupilot/eciVfe/eciVfeUiModel.ts
- frontend/src/secupilot/eciVfe/eciVfeUi.test.tsx
- frontend/src/App.tsx
- frontend/tests/e2e/eci-vfe-forecast-card.spec.ts
- artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-desktop.png
- artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-mobile.png
- docs/S6_FAST_MVP_GOAL_ECIVFE_32_FORECAST_CARD_UI_2026_05_09.md

## Acceptance Commands

- py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-ECIVFE-32_FORECAST_CARD_UI.md
- Set-Location -LiteralPath frontend; npm run test -- --run eciVfe
- Set-Location -LiteralPath frontend; npm run build
- Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/eci-vfe-forecast-card.spec.ts
- py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/eci_vfe_fixture_runs/rc001/screenshots
- git -c core.quotepath=false diff --check

## HOLD Conditions

- VFE card renders before schema validation and output guard PASS
- VFE card exposes attacker-readable attack_path, exploit steps, PoC, payload, raw logs, credentials, auth headers, or internal topology reachability
- VFE forecast independently upgrades a case or authorizes containment/remediation
- attack_path_defensive_summary is missing or replaced by attacker-readable wording
- evidence_gaps omit urgency, collection window, deadline basis, or fallback guidance
- screenshot safety scan finds P1/P2/P3, Mock Fixture, Expert Mode, stale RC wording, or forbidden content
- scope expands beyond listed files
