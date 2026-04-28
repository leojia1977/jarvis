# S6 CD-T06A Existing-State Header Skeleton Checklist 2026-04-28

## 1. Decision

`CD_T06A_CHECKLIST_GO_IMPLEMENTATION_AUTHORIZED`

CD-T06A may proceed as a bounded split from full CD-T06. The current repo can render non-CLOSED Case Detail states through existing fixture phases, while full CLOSED behavior remains HOLD.

## 2. Scope

Allowed scope:

- Case Detail state header semantic skeleton for existing renderable non-CLOSED states only.
- Target states: `OBSERVATION_WINDOW` and `APPROVED_PENDING_EXECUTION`.
- Stable test anchors proving state, AR status, visual-frame reference, state-mutation boundary, and `CLOSED` non-claim.

Not authorized:

- `CLOSED` rendering or claim.
- New fixture phase, fixture registry, fixture adapter, `ContextValidator`, or `ResolvedSurfaceContext` changes.
- AP controls, action controls, state transitions, observation-window countdown/state-sync, stale approve behavior, audit summary, backend/runtime/API/schema, real data, secrets, deploy, public endpoint, or external pilot.

## 3. Source Evidence

- `docs\S6_CD_T06_CLOSED_CONTEXT_UNBLOCK_CHECKLIST_2026_04_28.md`
- `docs\S6_CD_T06_STATE_HEADER_ISOLATED_CHECKLIST_2026_04_27.md`
- `frontend\fixtures\secupilot_core_surface_fixture_v0_1.json`
- Existing Case Detail implementation in `frontend\src\App.tsx`

## 4. Allowed Files

- `frontend\src\App.tsx`
- `frontend\src\App.css`
- `frontend\src\App.test.tsx`
- `docs\S6_CD_T06A_EXISTING_STATE_HEADER_SKELETON_CHECKLIST_2026_04_28.md`
- `docs\S6_CD_T06A_EXISTING_STATE_HEADER_SKELETON_CLOSEOUT_2026_04_28.md`
- `docs\S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs\HANDOFF.md`
- `docs\S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md`
- `docs\S6_EXTENDED_BOUNDED_AUTOMATION_AUTHORIZATION_2026_04_28.md`

Gate-generated release manifest refresh is allowed only if the canonical pilot gate updates it.

## 5. Test Command

```powershell
Push-Location frontend; npm test; npm run build; Pop-Location
py -3 scripts/git_preflight.py --mode pilot
git diff --check
```

## 6. HOLD Conditions

HOLD immediately if implementation needs a CLOSED context, fixture/context/validator changes, backend/runtime/API/schema, AP mutation, action controls, state transitions, observation-window state-sync, route handoff, P2/P3 authority change, real data, secrets, deploy, public endpoint, external pilot, or any file outside the allowed set.

