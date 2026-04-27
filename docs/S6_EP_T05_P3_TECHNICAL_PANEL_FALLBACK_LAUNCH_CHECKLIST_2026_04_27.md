# S6 EP-T05 P3 Technical Panel Fallback Launch Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 EP-T05 P3 Technical Panel Fallback Launch Checklist 2026-04-27 |
| Ticket | `EP-T05` |
| Scope | `P3 technical panels soft fallback / summary fallback` |
| Status | READY_FOR_RECONCILIATION_OR_BOUNDED_IMPLEMENTATION_GO |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Parent queue | `docs\S6_SPRINT1_RQ04_EXACT_BOUNDED_RUNNER_QUEUE_2026_04_27.md` |
| Depends on | `EP-T01` |
| Primary implementor | Codex |
| Execution surface | codex |
| Reviewer | Claude Code focused review if implementation diff exists |
| Review surface | claude-cmd |
| External review | not required unless HOLD trigger fires |
| SWE | disabled |

This checklist opens `EP-T05` for reconciliation first, then bounded implementation only if needed.

## 2. Launch Decision

Decision:

```text
GO_FOR_RECONCILIATION_THEN_BOUNDED_IMPLEMENTATION_IF_NEEDED
```

Meaning:

- The runner must first check whether existing EP-T01/P3 redline behavior already satisfies EP-T05.
- If current repo evidence is sufficient, close out as `RECONCILED_GATE_PASS_NO_CODE`.
- If code is needed, implementation may proceed only inside the allowed files and acceptance criteria below.

## 3. Exact Scope

Implement or reconcile only:

- P3 does not enter host-level technical panels;
- P3 sees a soft fallback or summary fallback for technical panel content;
- fallback stays cautious and read-only;
- host raw evidence remains absent from the DOM;
- no P3 Manager View, approval audit summary, or new route is introduced.

## 4. Exact Non-Goals

Do not implement:

- `EP-T02` inferred-node weakening;
- `EP-T03` lineage confidence degradation;
- `EP-T06` acceptance suite;
- new top-level pages or routes;
- Search/History behavior;
- P2 Approval Surface;
- P3 Manager View;
- approval audit source/data rules;
- backend/runtime/API/schema;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- Storybook, Playwright, real data, secrets, deploy, public endpoint, or external pilot.

## 5. Allowed Files

Allowed files:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_EP_T05_P3_TECHNICAL_PANEL_FALLBACK_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_SPRINT1_RQ04_EXACT_BOUNDED_RUNNER_QUEUE_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
```

No other files are authorized.

## 6. Required Tests

Minimum gate:

```powershell
cd frontend
npm run test -- --run
npm run build
cd ..
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
git diff --check
```

## 7. Acceptance Criteria

Closeout must prove:

- P3 context does not attach host-level raw evidence.
- P3 technical evidence content is summarized or softened, not shown as host-level detail.
- fallback text remains cautious and avoids over-certainty claims.
- no approve/reject/delay/observe/close CTA appears from this ticket.
- implementation does not create a P3 Manager View or approval audit summary.
- URL/localStorage/sessionStorage do not become authority for role or coverage.

## 8. HOLD Conditions

HOLD if:

- implementation requires new fixture content, registry changes, adapter changes, validator changes, or `ResolvedSurfaceContext` changes;
- implementation needs P3 Manager View or approval audit semantics;
- implementation needs visual-frame interpretation;
- implementation needs backend/runtime/API/schema work;
- implementation attaches host raw evidence under P3;
- implementation adds write controls or ActionMode choices;
- tests/build fail;
- Claude Code review raises a blocking finding;
- any GoNoGo Section 9 mandatory external-review trigger fires.

## 9. Next Safe Action

Next safe automation action:

```text
EP_T05_RECONCILE_OR_IMPLEMENT
```
