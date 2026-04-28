# S6 MV-T03 Deep-Link Relaunch Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `MV-T03` |
| Title | Manager deep-link handoff relaunch checklist |
| Status | `RELAUNCH_CHECKLIST_PASS_IMPLEMENTATION_REQUIRES_SEPARATE_GO` |
| Date | 2026-04-28 |
| Primary implementor | Codex for checklist only |
| Execution surface | codex |
| Workspace | VS Code / local repo |
| Prior HOLD | `docs/S6_MV_T03_DEEP_LINK_AUTHORITY_IMPLEMENTATION_HOLD_2026_04_28.md` |
| Dependency proof | `docs/S6_AP_T08_SH_T08_AUTHORITY_SOURCE_PROOF_2026_04_28.md` |

This checklist relaunches `MV-T03` after the missing `AP-T08` / `SH-T08` source-proof
blocker was resolved.

It does not authorize implementation. A later implementation still requires explicit
Jarvis GO.

## 2. Relaunch Decision

Decision:

```text
MV_T03_RELAUNCH_CHECKLIST_PASS
AP_T08_SH_T08_DEPENDENCY_PROOF_RESOLVED
NARROW_ROUTE_ONLY_IMPLEMENTATION_CANDIDATE_READY_FOR_SEPARATE_GO
```

The previous HOLD reason is closed only for source-proof absence. It is not a broad
approval-audit, manager-summary, or cross-surface workflow authorization.

## 3. Closed Preconditions

| Precondition | Evidence |
| --- | --- |
| P3 Manager shell exists | `MV-T01` closeout implements `/manager` as P3-only structure. |
| Search / History route exists | `SH-T03` implements clamp-first `/search?tab=history`. |
| Search focus scopes exist | `SH-T05` implements readonly `summary`, `approval_audit`, `history_audit` hints. |
| Search write CTA absence reconciled | `SH-T07` no-code closeout proves no write CTA on history surface. |
| Audit source proof exists | `AP-T08` / `SH-T08` source proof records existing governed `audit_trail` source path. |
| P3 raw-evidence guard exists | `CD-T05`, `MV-T01`, and E0 redline tests keep host raw evidence absent from P3 surfaces. |

## 4. Exact Narrow Scope For Later Implementation

Allowed source surface:

```text
P3 Search / History readonly surface only.
```

Allowed source condition:

```text
activeContext.session.role === "P3"
effectiveFocus in {"approval_audit", "history_audit"}
```

Allowed target:

```text
/manager existing P3 Manager View route.
```

Allowed payload:

```text
No serialized handoff payload.
No URL query payload.
No localStorage / sessionStorage payload.
The target continues to use the current resolved P3 context and current active case already held by the app.
```

Allowed behavior:

- add a bounded P3-only readonly control or link from Search / History to existing Manager View;
- call existing route navigation only;
- expose test anchors proving source, target, and non-authority boundaries;
- leave `manager-audit-boundary` as `data-approval-audit-summary="not-implemented"`;
- keep P3 host raw evidence absent from DOM.

## 5. Explicit Non-Goals

MV-T03 must not implement:

- approval audit summary rendering;
- `MV-T04` P3 approval-audit component;
- P0/P2 Manager variants;
- full audit trail DOM;
- host raw evidence, process-tree raw data, or technical panels;
- AP state transition, approval CTA, decision composer, or ActionMode behavior;
- URL / route param / browser storage authority;
- backend/runtime/API/schema changes;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- real data, secrets, deploy, public endpoint, or external pilot.

## 6. Allowed Files For Later Implementation

A later implementation GO may touch only:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_MV_T03_DEEP_LINK_HANDOFF_CLOSEOUT_2026_04_28.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md
```

Any need to touch fixtures, adapter, validator, context types, backend, runtime, API,
schema, Storybook, or Playwright config is a HOLD.

## 7. Required Tests For Later Implementation

Minimum unit/component test expectations:

```text
P3 Search / History approval-audit or history-audit focus can navigate to /manager.
URL/storage cannot create P3 Manager authority.
P1/P2/P0 do not receive MV-T03 handoff controls from this ticket.
Manager target continues to use ResolvedSurfaceContext as authority.
No approval controls attach after handoff.
No host raw evidence or full audit trail attaches after handoff.
manager-audit-boundary remains not implemented.
```

Minimum command:

```text
npm --prefix frontend test -- src/App.test.tsx
```

Closeout gate should also run:

```text
npm --prefix frontend test
npm --prefix frontend run build
npm --prefix frontend run test:e2e
py -3 scripts/git_preflight.py --mode pilot
git diff --check
```

## 8. External Review Rule

Claude Web / external architecture review is not mandatory for the narrow route-only
implementation if all of these remain true:

- no audit summary rendering;
- no new authority model;
- no URL/storage/route-param authority;
- no P0/P2 Manager branch or placeholder;
- no fixture/adapter/validator/context change;
- no backend/runtime/API/schema change.

External review becomes mandatory if implementation tries to add any handoff payload,
approval-audit rendering, P3 summary field expansion, source/target authority change,
or cross-surface state propagation.

## 9. Final Relaunch Result

Implementation status:

```text
NOT_STARTED
IMPLEMENTATION_GO_REQUIRED
```

Next safe route:

```text
WAIT_FOR_MV_T03_IMPLEMENTATION_GO_OR_OPEN_AP_T08_SH_T08_NARROW_IMPLEMENTATION_CHECKLIST
```
