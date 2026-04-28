# S6 SH-T08 Approval Audit Source Order Checklist 2026-04-28

## 1. Decision

`SH_T08_CHECKLIST_GO_IMPLEMENTATION_AUTHORIZED`

SH-T08 may proceed as a narrow Search / History approval-audit source-boundary implementation because AP-T08, SH-T02, and SH-T06 are closed, and the existing repo exposes governed `activeContext.audit_trail` without fixture/context changes.

## 2. Source Order

Required source order:

```text
AP-T08 display-only audit mapping
-> SH-T02 Search / History clamp-first guard
-> SH-T06 structural/degraded empty-state split
-> SH-T08 P3 read-only approval-audit source boundary
```

All prior steps are closed with gate and Claude Code PASS.

## 3. Allowed Scope

- P3-only Search / History read-only approval-audit boundary.
- P1/P2 audit-focus requests must downgrade to summary.
- Use existing `activeContext.audit_trail` only.
- Fixed enum derived-status mapping only.
- Render minimal summary fields only: latest audit id, event, actor role, derived status, case state after event, observation presence, and honest terminal-close unavailable state.

## 4. Non-Goals

- No write CTA.
- No full audit chain rendering in `/search`.
- No Manager View approval-audit summary.
- No route handoff implementation beyond the already closed MV-T03 route-only handoff.
- No AP mutation, `ActionMode`, state transition, backend/runtime/API/schema, fixture registry, fixture adapter, `ContextValidator`, `ResolvedSurfaceContext`, raw evidence DOM, real data, secrets, deploy, public endpoint, or external pilot.

## 5. Allowed Files

- `frontend\src\App.tsx`
- `frontend\src\App.css`
- `frontend\src\App.test.tsx`
- `docs\S6_SH_T08_APPROVAL_AUDIT_SOURCE_ORDER_CHECKLIST_2026_04_28.md`
- `docs\S6_SH_T08_APPROVAL_AUDIT_SOURCE_BOUNDARY_CLOSEOUT_2026_04_28.md`
- `docs\S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs\HANDOFF.md`
- `docs\S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md`
- `docs\S6_EXTENDED_BOUNDED_AUTOMATION_AUTHORIZATION_2026_04_28.md`

Gate-generated release manifest refresh is allowed only if the canonical pilot gate updates it.

## 6. Test Command

```powershell
Push-Location frontend; npm test; npm run build; Pop-Location
py -3 scripts/git_preflight.py --mode pilot
git diff --check
```

## 7. HOLD Conditions

HOLD immediately if implementation needs source invention, full audit-chain rendering, write controls, Manager summary output, route payload, fixture/context/validator changes, backend/runtime/API/schema, raw evidence DOM, real data, secrets, deploy, public endpoint, external pilot, or a mandatory external review trigger.

