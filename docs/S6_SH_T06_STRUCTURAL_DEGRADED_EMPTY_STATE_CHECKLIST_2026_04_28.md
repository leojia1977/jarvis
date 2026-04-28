# S6 SH-T06 Structural / Degraded Empty State Checklist 2026-04-28

## 1. Decision

`SH_T06_CHECKLIST_GO_IMPLEMENTATION_AUTHORIZED`

SH-T06 may proceed as a bounded Search / History implementation because the visual blocker is closed by `HF-SH-02` v0.2 and the required scope can be implemented with exact existing frontend files and tests.

## 2. Source Inputs

- `docs\S6_VISUAL_BASELINE_HF_SH_01_02_VF14_RECONCILIATION_2026_04_28.md`
- `D:\产品设计\secupilot0421\visual negative\SecuPilot_HF-SH-01_HF-SH-02_Search_History_List_Frames_v0.2.md`
- `docs\S6_SH_T02_DUAL_COVERAGE_CLAMP_CLOSEOUT_2026_04_28.md`
- `docs\S6_EXTENDED_BOUNDED_AUTOMATION_AUTHORIZATION_2026_04_28.md`

## 3. Allowed Files

- `frontend\src\App.tsx`
- `frontend\src\App.css`
- `frontend\src\App.test.tsx`
- `docs\S6_SH_T06_STRUCTURAL_DEGRADED_EMPTY_STATE_CHECKLIST_2026_04_28.md`
- `docs\S6_SH_T06_STRUCTURAL_DEGRADED_EMPTY_STATE_CLOSEOUT_2026_04_28.md`
- `docs\S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs\HANDOFF.md`
- `docs\S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md`
- `docs\S6_EXTENDED_BOUNDED_AUTOMATION_AUTHORIZATION_2026_04_28.md`

Gate-generated release manifest refresh is allowed only if the canonical pilot gate updates it.

## 4. Required Implementation

- Add a distinct `structural-empty-state` anchor for "no matching historical case under the current visibility scope".
- Add a distinct `degraded-empty-state` anchor for "case exists, but fields are unavailable after coverage clamp / downgrade".
- Keep both states sourced from existing Search / History route context and `ui_messages` semantics.
- Preserve `missing-signal-notice[data-message-source="ui_messages"]`.
- Keep Search / History read-only.

## 5. Non-Goals

- No query engine or real search implementation.
- No AP mutation, approval controls, `ActionMode`, or P2/P3 authority change.
- No Manager View approval-audit summary.
- No route handoff payload or storage/URL authority.
- No fixture registry, fixture adapter, ContextValidator, or ResolvedSurfaceContext change.
- No backend/runtime/API/schema.
- No real data, secrets, deploy, public endpoint, or external pilot.

## 6. Test Command

```powershell
Push-Location frontend; npm test; npm run build; Pop-Location
py -3 scripts/git_preflight.py --mode pilot
git diff --check
```

## 7. HOLD Conditions

HOLD if implementation requires any non-allowed file, new fixture/context source, route authority change, backend/runtime/API/schema, failed gate, visual ambiguity, raw evidence DOM attachment, real-data/secrets/deploy/public endpoint/external pilot, or mandatory external review trigger.
