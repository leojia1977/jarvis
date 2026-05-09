# GOAL-ECIVFE-32 Forecast Card UI

## Goal ID

```text
GOAL-ECIVFE-32_FORECAST_CARD_UI
```

## Goal type

```text
page
```

## Goal statement

```text
Render guard-passed VFE forecast cards as defensive summaries with urgency, collection-window guidance, and no attacker-readable attack path or topology detail.
```

## Primary executable object

```text
page=frontend/src/secupilot/eciVfe/VfeForecastCard.tsx
model=frontend/src/secupilot/eciVfe/eciVfeUiModel.ts
test=frontend/src/secupilot/eciVfe/eciVfeUi.test.tsx
route=frontend/src/App.tsx
e2e=frontend/tests/e2e/eci-vfe-forecast-card.spec.ts
artifact=artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-desktop.png
artifact=artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-mobile.png
closeout=docs/S6_FAST_MVP_GOAL_ECIVFE_32_FORECAST_CARD_UI_2026_05_09.md
```

## Inputs

```text
artifacts/product_acceleration/next_goal_candidate.json
artifacts/eci_vfe_fixture_runs/rc001/forecast_candidates.json
artifacts/eci_vfe_fixture_runs/rc001/output_guard_scan.json
frontend/src/secupilot/eciVfe/types.ts
```

## Output paths

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

## Allowed files

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

## Allowed scope

```text
guard-passed VFE forecast rendering only
route-level UI exposure for /eci-vfe-forecast only
frontend unit/build/e2e checks with screenshot evidence generation
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-ECIVFE-32_FORECAST_CARD_UI.md
Set-Location -LiteralPath frontend; npm run test -- --run eciVfe
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/eci-vfe-forecast-card.spec.ts
powershell -NoProfile -Command "$files=@('artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-desktop.png','artifacts/eci_vfe_fixture_runs/rc001/screenshots/vfe-forecast-card-mobile.png'); foreach($f in $files){ if(-not (Test-Path -LiteralPath $f)){ throw \"missing screenshot: $f\" }}"
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
VFE card renders before schema validation and output guard PASS
VFE card exposes attacker-readable attack_path, exploit steps, PoC, payload, raw logs, credentials, auth headers, or internal topology reachability
VFE forecast independently upgrades a case or authorizes containment/remediation
attack_path_defensive_summary is missing or replaced by attacker-readable wording
evidence_gaps omit urgency, collection window, deadline basis, or fallback guidance
screenshot safety scan finds forbidden content or stale wording in reviewer-facing UI
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
keep failing screenshot evidence for audit
leave unrelated historical residue untouched
```

## Evidence contract

```text
goal card validator PASS json
frontend vitest output filtered to eciVfe
frontend build output
playwright e2e output for forecast card route
two screenshot artifacts under artifacts/eci_vfe_fixture_runs/rc001/screenshots
closeout report with exact command outcomes and safety assertions
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
If PASS, unlock GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE.
If HOLD, stop and report exact failing UI/test/screenshot evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-ECIVFE-32 forecast card ui
stage and commit only Goal files
do not push
```
