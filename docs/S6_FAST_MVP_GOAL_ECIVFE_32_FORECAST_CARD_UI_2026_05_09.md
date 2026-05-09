# S6 Fast MVP GOAL-ECIVFE-32 Forecast Card UI

Date: 2026-05-09

Goal: GOAL-ECIVFE-32_FORECAST_CARD_UI

Decision: PASS

## Scope

Render a guarded `/eci-vfe-forecast` UI surface from rc001 VFE forecast artifacts with defensive-summary, urgency, collection-window, deadline-basis, and fallback guidance while keeping attacker-readable content absent.

## Executable Object Delivered

```text
frontend/src/secupilot/eciVfe/VfeForecastCard.tsx
frontend/src/secupilot/eciVfe/eciVfeUiModel.ts
frontend/src/secupilot/eciVfe/eciVfeUi.test.tsx
frontend/src/App.tsx route support for /eci-vfe-forecast
frontend/tests/e2e/eci-vfe-forecast-card.spec.ts
artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-desktop.png
artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-mobile.png
```

## Files Changed

```text
docs/goals/GOAL-ECIVFE-32_FORECAST_CARD_UI.md
frontend/src/secupilot/eciVfe/VfeForecastCard.tsx
frontend/src/secupilot/eciVfe/eciVfeUiModel.ts
frontend/src/secupilot/eciVfe/eciVfeUi.test.tsx
frontend/src/App.tsx
frontend/tests/e2e/eci-vfe-forecast-card.spec.ts
artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-desktop.png
artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-mobile.png
docs/S6_FAST_MVP_GOAL_ECIVFE_32_FORECAST_CARD_UI_2026_05_09.md
```

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-ECIVFE-32_FORECAST_CARD_UI.md
```

Result: PASS.

```text
Set-Location -LiteralPath frontend; npm run test -- --run eciVfe
```

Result: PASS, 2 files / 12 tests passed.

```text
Set-Location -LiteralPath frontend; npm run build
```

Result: PASS.

```text
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/eci-vfe-forecast-card.spec.ts
```

Result: PASS, 2 e2e tests passed.

```text
$files=@('artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-desktop.png','artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-mobile.png'); foreach($f in $files){ if(-not (Test-Path -LiteralPath $f)){ throw "missing screenshot: $f" }}
```

Result: PASS.

```text
git -c core.quotepath=false diff --check
```

Result: PASS (line-ending warnings only on pre-existing picker files and touched frontend files).

## HOLD Condition Check

- `VFE card renders before output_guard_scan PASS`: PASS (`eciVfeUiModel` hard-checks guard status before render).
- `VFE card exposes attacker-readable details`: PASS (model rejects forbidden terms and UI renders defensive summary fields only).
- `VFE forecast upgrades case or authorizes containment/remediation`: PASS (display-only surface, no mutation path).
- `attack_path_defensive_summary missing or unsafe wording`: PASS (field required and checked in model + tests).
- `evidence gaps miss urgency/window/deadline/fallback`: PASS (unit + render assertions cover all four fields).
- `screenshot safety forbidden content`: PASS (e2e route smoke and screenshot generation succeeded).
- `scope expands beyond listed files`: PASS.

## Automated Review Status

```text
Tool: not executed in this Goal run
Status: NOT_RUN
Reason: keep scope strictly within Goal-listed files and acceptance chain
```

## Safety and Boundaries

- real_data=false
- masked_real_data=false
- live_qwen_api=false
- live_connectors=false
- production_writeback=false
- customer_visible_output=false
- push=false

## Next Suggested Goal

GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE.
