# S6 GS-T05 Expert Mode Regression Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `GS-T05` |
| Title | Global Shell expert-mode regression / acceptance lane |
| Decision | `REGRESSION_CHECKLIST_PASS_READY_FOR_NO_CODE_REGRESSION_CLOSEOUT` |
| Primary implementor | Codex |
| Execution surface | codex |
| Reviewer | Claude Code not mandatory until closeout evidence is claimed |
| Review surface | local evidence / gate |
| Workspace | VS Code / local repo |

## 2. Checklist Result

`GS-T05` is ready for a later no-code regression closeout or regression-lane evidence refresh. It does not require new implementation before that closeout because `GS-T04` and the `VF-03 v0.2` reconciliation already established the required anchors:

- `vf-03-expert-mode-frame`;
- `expert-mode-entry`;
- `expert-mode-toggle`;
- expert-mode ON example selectors;
- `DEGRADED` lineage-confidence selector;
- forbidden OFF-field absence assertions.

## 3. Regression Scope

The later `GS-T05` closeout may only verify existing behavior:

- P1 expert mode remains restricted to current field set.
- P0/P2 expert mode remains skeleton-only.
- P3 does not receive the expert-mode entry.
- No route, permission upgrade, coverage bypass, OFF-field DOM mount, or action binding exists.
- Static VF-03 HTML is not copied into production code.

## 4. Non-Authorization

This checklist does not authorize:

- final VF-03 visual PASS;
- interactive expert-mode switching;
- coverage escalation;
- new information creation;
- route changes;
- backend/runtime/API/schema changes;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes.

## 5. Next Route

```text
WAIT_FOR_GS_T05_NO_CODE_REGRESSION_CLOSEOUT_OR_CONTINUE_AP_IMPLEMENTATION_BATCH
```

