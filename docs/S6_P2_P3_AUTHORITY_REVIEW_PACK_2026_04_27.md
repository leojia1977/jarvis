# S6 P2/P3 Authority Review Pack 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 P2/P3 Authority Review Pack 2026-04-27 |
| Status | REVIEWED_BY_CLAUDE_WEB_PASS_WITH_NOTES |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Parent authorization | `docs\S6_STAGED_ACCELERATION_AUTHORIZATION_2026_04_27.md` |
| Review targets | `AP-T10`, `AP-T01`, `CD-T05`, `MV-T01` |
| Claude Web review record | `docs\S6_P2_P3_AUTHORITY_CLAUDE_WEB_REVIEW_2026_04_27.md` |

This pack prepares the authority questions, Claude Web review focus, and possible GO conditions for the P2/P3 work that can most affect product correctness and launch quality.

It is checklist/readiness material only. It does not authorize implementation.

## 2. Common Authority Rules

These rules apply to all four target tickets:

- `ResolvedSurfaceContext` remains the rendering authority for role, coverage, surface, case state, AR status, and action mode.
- URL, localStorage, sessionStorage, route params, or query params must not become authority.
- P1 must not choose `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY`.
- P2 may expose approval controls only when AP route/state authority is explicit.
- P3 must remain read-only and must not attach host-level raw evidence.
- Coverage level remains a hard ceiling.
- Missing signals must degrade honestly.
- No backend/runtime/API/schema work is authorized by this review pack.

## 3. AP-T10 Authority Questions

Ticket:

```text
AP-T10 - ARInteractiveStatus / ActionMode badge/pill mapping layer
```

Questions to resolve before implementation GO:

1. Which enum source is the only authority for badge/pill state: D-02, Model Contract, or a derived UI mapping table?
2. Can `ARInteractiveStatus` be displayed without creating or changing `ActionMode`?
3. Which states are display-only versus actionable?
4. How are `PENDING_APPROVAL`, `OBSERVATION_WINDOW`, `APPROVED_PENDING_EXECUTION`, `CLOSED`, and unavailable/degraded states represented without implying state migration?
5. Must AP-T10 provide labels only, or may it also provide visual severity/priority?
6. Which state labels must come from `ui_messages` rather than hardcoded frontend copy?

Claude Web review focus:

- enum authority;
- ActionMode non-creation;
- P1 non-authority;
- P2 display vs action boundary;
- D-02 conflict check;
- no state migration.

Possible implementation GO conditions:

- exact mapping table source is named;
- implementation is display-only;
- no AP route, CTA, confirmation modal, observation-window migration, or backend/API/schema change;
- tests prove P1 cannot select action mode and URL/storage cannot change mapped state.

## 4. AP-T01 Authority Questions

Ticket:

```text
AP-T01 - /approval route, default landing, role guard
```

Questions to resolve before implementation GO:

1. Which roles may enter `/approval`, and what does each role see?
2. Does non-P2 access route to a read-only container, a safe unavailable state, or a redirect?
3. Does route entry require an existing Action Request, or can a blank AP shell exist?
4. Can `/approval` render without implementing CTA or state transition behavior?
5. How does AP route guard avoid treating URL params as role/action authority?
6. What is the safe fallback if AR context is missing?

Claude Web review focus:

- AP route authority boundary;
- P0/P3 read-only behavior;
- P1 non-authority;
- no approval CTA leak;
- route guard fail-closed behavior.

Possible implementation GO conditions:

- exact role guard behavior is written;
- route implementation is shell/guard only;
- no approve/reject/delay/observe controls;
- no AP state transitions;
- tests prove non-P2 cannot operate AP actions.

## 5. CD-T05 Authority Questions

Ticket:

```text
CD-T05 - P3 independent executive summary component
```

Questions to resolve before implementation GO:

1. What exact source fields may P3 executive summary use?
2. Must P3 summary be generated from existing summary/honesty/unsupported-claims fields only?
3. What text is forbidden because it overstates certainty?
4. Does CD-T05 render inside Case Detail only, or also feed Manager View?
5. What must be absent from DOM under P3: host raw evidence, technical panels, action controls, approval controls?
6. Which visual frame or contract confirms the component boundary?

Claude Web review focus:

- P3 read-only authority;
- host raw evidence DOM absence;
- no unsupported certainty;
- no manager/audit scope creep;
- no approval/control leak.

Possible implementation GO conditions:

- P3 summary source fields are explicit and existing;
- cautious language tests exist;
- host raw evidence `not.toBeAttached()` equivalent is proven in component tests;
- no Manager View, approval audit, route handoff, backend/API/schema, or fixture/validator changes.

## 6. MV-T01 Authority Questions

Ticket:

```text
MV-T01 - /manager page structure and KPI cards
```

Questions to resolve before implementation GO:

1. Is `/manager` a P3 primary surface only, or may P0/P2 enter a degraded/read-only variant later?
2. Which KPI cards are allowed from current mock-only fields?
3. Can KPI cards exist without approval audit summary?
4. How does Manager View avoid host raw evidence DOM attachment?
5. Does MV-T01 create any deep-link handoff, or is deep-link deferred to `MV-T03`?
6. What is the fail-closed state if P3 context is missing?

Claude Web review focus:

- P3 manager surface authority;
- KPI source boundaries;
- no approval audit summary in MV-T01;
- no deep-link handoff;
- no host raw evidence;
- no certainty overclaim.

Possible implementation GO conditions:

- exact KPI source fields are named;
- route/surface shell is read-only and P3-bounded;
- no `MV-T03` deep-link, `MV-T04` approval audit summary, backend/API/schema, fixture/validator, or P2/P3 authority mutation;
- tests prove P3 read-only rendering and raw-evidence absence.

## 7. Review Pack Prompt

Use this prompt for Claude Web or equivalent architecture/governance review when a checklist needs external review:

```text
Review the P2/P3 authority boundaries for the specified ticket only.

Source of truth:
- PRD / Model Contract
- D-02 status/action enum constraints
- AI_COLLAB execution/review rules
- S6 staged acceleration authorization
- current repo route/handoff/checklist for the ticket

Review focus:
- role / surface / coverage authority
- P1/P2/P3 permission boundary
- ActionMode and AR status authority
- URL/storage non-authority
- P3 raw evidence DOM absence
- no product scope expansion
- no backend/runtime/API/schema

Decision needed:
- PASS
- PASS_WITH_NOTES
- HOLD

This review is not a launch/deploy/real-data authorization.
```

## 8. Next Safe Action

Next safe action:

```text
USE_THIS_PACK_WHEN_AP_T10_AP_T01_CD_T05_MV_T01_CHECKLISTS_RUN
```

## 9. Claude Web Review Evidence

Claude Web architecture/governance review completed on 2026-04-27 and returned:

```text
PASS_WITH_2_NON_BLOCKING_NOTES
```

Ticket verdicts:

| Ticket | Verdict | Launch-checklist implication |
| --- | --- | --- |
| `AP-T10` | `PASS` | May proceed to exact patch-isolated launch checklist; implementation still requires exact files/tests and no product/contract conflict. |
| `AP-T01` | `PASS` | May proceed to exact patch-isolated launch checklist; implementation must remain shell/guard only. |
| `CD-T05` | `PASS_WITH_NOTE` | Launch checklist must confirm `G0-05 signed-off confirmed: YES` and no later P3 summary field-set revision. |
| `MV-T01` | `PASS_WITH_NOTE` | Launch checklist must forbid P0/P2 placeholders or conditional branches; P0/P2 variants remain `MV-T02` scope. |

Review record:

```text
docs/S6_P2_P3_AUTHORITY_CLAUDE_WEB_REVIEW_2026_04_27.md
```

This review evidence does not authorize broad P2/P3 implementation, backend/runtime/API/schema changes, real data, secrets, deploy/public endpoint, external pilot, or any implementation outside a later exact bounded ticket.
