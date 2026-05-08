# GOAL-ECIVFE-31 Chain Indicator UI

## Goal ID

```text
GOAL-ECIVFE-31_CHAIN_INDICATOR_UI
```

## Goal type

```text
page
```

## Goal statement

```text
Render guard-passed ECI chain indicators in the incident workbench as operator-readable stage, confidence, and evidence-gap summaries without exposing raw evidence or attacker-readable details.
```

## Primary executable object

```text
page=frontend/src/secupilot/eciVfe/EciChainIndicator.tsx
page=frontend/src/secupilot/eciVfe/EciEvidenceGapPanel.tsx
model=frontend/src/secupilot/eciVfe/eciVfeUiModel.ts
test=frontend/src/secupilot/eciVfe/eciVfeUi.test.tsx
route=frontend/src/App.tsx
e2e=frontend/tests/e2e/eci-vfe-chain-indicator.spec.ts
artifact=artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-desktop.png
artifact=artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-mobile.png
closeout=docs/S6_FAST_MVP_GOAL_ECIVFE_31_CHAIN_INDICATOR_UI_2026_05_08.md
```

## Inputs

```text
artifacts/product_acceleration/next_goal_candidate.json
artifacts/eci_vfe_fixture_runs/rc001/chain_assessment.json
artifacts/eci_vfe_fixture_runs/rc001/output_guard_scan.json
frontend/src/secupilot/eciVfe/types.ts
```

## Output paths

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

## Allowed files

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

## Allowed scope

```text
guard-passed ECI chain indicator rendering only
route-level UI exposure for /eci-vfe-chain only
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-ECIVFE-31_CHAIN_INDICATOR_UI.md
Set-Location -LiteralPath frontend; npm run test -- --run eciVfe
Set-Location -LiteralPath frontend; npm run build
Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/eci-vfe-chain-indicator.spec.ts
powershell -NoProfile -Command "$files=@('artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-desktop.png','artifacts/eci_vfe_fixture_runs/rc001/screenshots/eci-chain-indicator-mobile.png'); foreach($f in $files){ if(-not (Test-Path -LiteralPath $f)){ throw \"missing screenshot: $f\" }}"
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
UI renders ECI output before output_guard_scan.json is PASS
UI exposes raw evidence, raw logs, PoC, exploit steps, payload, credentials, token, auth header, or attacker-readable topology
semantic similarity alone upgrades a case or changes the recommended action
high-stage ECI labels appear without stricter confidence or suspected-state downgrade
evidence gaps omit urgency or collection-window guidance
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
playwright e2e output for chain indicator route
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
If PASS, unlock GOAL-ECIVFE-32_FORECAST_CARD_UI.
If HOLD, stop and report exact failing UI/test/screenshot evidence.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-ECIVFE-31 chain indicator ui
stage and commit only Goal files
do not push
```
