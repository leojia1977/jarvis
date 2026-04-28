# S6 SH-T09 Search / History Acceptance Checklist 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `SH-T09` |
| Title | Search / History acceptance reconciliation checklist |
| Status | `SH_T09_ACCEPTANCE_CHECKLIST_READY_RECONCILIATION_REQUIRES_SEPARATE_GO` |
| Date | 2026-04-29 |
| Automation | `secupilot-30m-bounded-burn-runner` |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Execution surface | `codex` |
| Implementation authorization | `not authorized by this checklist` |

This checklist prepares `SH-T09` for a later no-code reconciliation or exact
implementation decision. It does not close `SH-T09`, transition Jira, or
authorize new frontend/backend work.

## 2. Decision

```text
SH_T09_ACCEPTANCE_CHAIN_EVIDENCE_READY
SH_T09_RECONCILIATION_REQUIRES_SEPARATE_GO
```

The Search / History dependency chain is now sufficiently documented for an
acceptance reconciliation pass, but this checklist does not perform that pass.

## 3. Dependency Evidence

| Dependency | Evidence | Current status |
| --- | --- | --- |
| `SH-T01` | `docs\S6_SH_T01_HISTORICAL_LIST_ITEM_SKELETON_CLOSEOUT_2026_04_27.md` | Closed as historical list item skeleton. |
| `SH-T02` | `docs\S6_SH_T02_DUAL_COVERAGE_CLAMP_CLOSEOUT_2026_04_28.md` | Closed as dual coverage / clamp semantics; Jira parity pending env visibility. |
| `SH-T03` | `docs\S6_SH_T03_PATCH_GATE_ISOLATED_LAUNCH_CHECKLIST_2026_04_27.md` | Closed as clamp-first history route implementation and Jira-synced. |
| `SH-T04` | `docs\S6_SH_T04_SEARCH_HISTORY_SCOPE_RECONCILIATION_CLOSEOUT_2026_04_28.md` | Closed as no-code scope reconciliation. |
| `SH-T05` | `docs\S6_SH_T05_READONLY_FOCUS_SCOPE_CLOSEOUT_2026_04_27.md` | Closed as readonly focus scopes and Jira-synced. |
| `SH-T06` | `docs\S6_SH_T06_STRUCTURAL_DEGRADED_EMPTY_STATE_CLOSEOUT_2026_04_28.md` | Closed as structural/degraded empty-state split; Jira parity pending env visibility. |
| `SH-T07` | `docs\S6_SH_T07_WRITE_CTA_ABSENCE_RECONCILIATION_CLOSEOUT_2026_04_27.md` | Closed as no-code write CTA absence reconciliation and Jira-synced. |
| `SH-T08` | `docs\S6_SH_T08_APPROVAL_AUDIT_SOURCE_BOUNDARY_CLOSEOUT_2026_04_28.md` | Closed as P3 approval-audit source boundary; Jira parity pending env visibility. |
| Visual baseline | `docs\S6_VISUAL_BASELINE_HF_SH_01_02_VF14_RECONCILIATION_2026_04_28.md` | `HF-SH-01`, `HF-SH-02`, and `VF-14` v0.2 accepted for Search / History clamp/list behavior. |

## 4. Acceptance Scope For Later Reconciliation

A later `SH-T09` reconciliation pass may verify these acceptance points:

- history route resolves through clamp-first guard before rendering;
- recorded coverage and current visible coverage are both displayed;
- current visible coverage never exceeds recorded coverage;
- historical upgrade attempts are blocked;
- read-only focus scopes remain hints only and do not create write authority;
- structural empty and degraded empty states remain distinct;
- missing-signal / degraded notices are sourced from `ui_messages`;
- P3 approval-audit source boundary is present only for P3 and remains read-only;
- P1/P2 audit focus requests downgrade safely;
- approve, reject, delay, observe, close, and ActionMode controls are absent;
- no P3 host raw evidence DOM is attached;
- URL, localStorage, and sessionStorage remain non-authoritative for role,
  coverage, case state, audit source, and write authority.

## 5. Required Gate For Later Closeout

Minimum gate for a later `SH-T09` closeout:

```powershell
Push-Location frontend
npm run test -- --run
npm run build
Pop-Location
py -3 scripts/git_preflight.py --mode pilot
git diff --check
```

Claude Code focused review is required only if the later pass introduces a code
diff. For no-code reconciliation, local evidence plus the gate is sufficient.

## 6. Allowed Files For Later Reconciliation

Docs-only reconciliation may update only:

```text
docs/S6_SH_T09_ACCEPTANCE_CHECKLIST_2026_04_29.md
docs/S6_SH_T09_ACCEPTANCE_RECONCILIATION_CLOSEOUT_<date>.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
releases/release_manifest.json
```

Any code implementation would require a separate exact implementation GO and a
new allowed-files list.

## 7. HOLD Conditions

HOLD the later closeout if:

- any dependency above is missing or later invalidated;
- gate or build fails;
- acceptance requires files outside the docs-only reconciliation list;
- acceptance requires new Search / History implementation;
- acceptance requires route handoff behavior beyond existing governed scope;
- acceptance requires P2/P3 authority changes;
- acceptance requires backend/runtime/API/schema changes;
- acceptance requires fixture registry, fixture adapter, `ContextValidator`, or
  `ResolvedSurfaceContext` changes;
- raw evidence DOM would attach;
- real data, secrets, deploy, public endpoint, or external pilot scope appears;
- a mandatory external review trigger fires.

## 8. Jira Handling

Do not mark `SH-T09` Done from this checklist.

Allowed Jira action, if credentials are visible:

```text
Add non-transition checklist comment:
SH-T09 acceptance checklist prepared; reconciliation closeout requires separate GO and gate evidence.
```

## 9. Next Route

```text
WAIT_FOR_SH_T09_RECONCILIATION_GO_OR_SAFE_JIRA_PARITY_SYNC
```

## 10. Non-Authorization

This checklist does not authorize:

- `SH-T09` closeout;
- frontend implementation;
- backend/runtime/API/schema changes;
- fixture registry, fixture adapter, `ContextValidator`, or `ResolvedSurfaceContext` changes;
- Jira Done transition;
- real data, secrets, deploy, public endpoint, or external pilot.
