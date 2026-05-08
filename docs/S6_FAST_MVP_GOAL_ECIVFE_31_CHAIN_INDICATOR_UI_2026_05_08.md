# S6 Fast MVP GOAL-ECIVFE-31 Chain Indicator UI

Date: 2026-05-08

Goal: GOAL-ECIVFE-31_CHAIN_INDICATOR_UI

Decision: PASS

## Scope

Render a guarded `/eci-vfe-chain` UI surface from rc001 ECI analyzer artifacts with stage/confidence/evidence-gap summaries and no raw evidence exposure.

## Executable Object Delivered

```text
frontend/src/secupilot/eciVfe/EciChainIndicator.tsx
frontend/src/secupilot/eciVfe/EciEvidenceGapPanel.tsx
frontend/src/secupilot/eciVfe/eciVfeUiModel.ts
frontend/src/secupilot/eciVfe/eciVfeUi.test.tsx
frontend/src/App.tsx route support for /eci-vfe-chain
frontend/tests/e2e/eci-vfe-chain-indicator.spec.ts
artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-desktop.png
artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-mobile.png
```

## Files Changed

```text
docs/goals/GOAL-ECIVFE-31_CHAIN_INDICATOR_UI.md
frontend/src/secupilot/eciVfe/EciChainIndicator.tsx
frontend/src/secupilot/eciVfe/EciEvidenceGapPanel.tsx
frontend/src/secupilot/eciVfe/eciVfeUiModel.ts
frontend/src/secupilot/eciVfe/eciVfeUi.test.tsx
frontend/src/App.tsx
frontend/tests/e2e/eci-vfe-chain-indicator.spec.ts
artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-desktop.png
artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-mobile.png
docs/S6_FAST_MVP_GOAL_ECIVFE_31_CHAIN_INDICATOR_UI_2026_05_08.md
```

## Acceptance Commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-ECIVFE-31_CHAIN_INDICATOR_UI.md
```

Result: PASS.

```text
Set-Location -LiteralPath frontend; npm run test -- --run eciVfe
```

Result: PASS, 2 files / 10 tests passed.

```text
Set-Location -LiteralPath frontend; npm run build
```

Result: PASS.

```text
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/eci-vfe-chain-indicator.spec.ts
```

Result: PASS, 2 e2e tests passed.

```text
$files=@('artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-desktop.png','artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-mobile.png'); foreach($f in $files){ if(-not (Test-Path -LiteralPath $f)){ throw "missing screenshot: $f" }}
```

Result: PASS.

```text
git -c core.quotepath=false diff --check
```

Result: PASS (line-ending warnings only on pre-existing picker files and App.tsx normalization).

## HOLD Condition Check

- `UI renders output before output_guard_scan PASS`: PASS (`eciVfeUiModel` hard-checks guard scan status).
- `UI exposes raw evidence / attacker-readable details`: PASS (component only renders summarized stage/confidence/gaps).
- `semantic similarity alone upgrades case`: PASS (display-only, no mutation path).
- `high-stage labels without downgrade`: PASS (rendered from guarded artifacts; no override logic added in UI).
- `evidence gaps omit urgency or collection window`: PASS (unit + render path include urgency/window/fallback lines).
- `screenshot safety forbidden content`: PASS (e2e assertions verify local-only boundary attributes and card visibility).
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

GOAL-ECIVFE-32_FORECAST_CARD_UI.
