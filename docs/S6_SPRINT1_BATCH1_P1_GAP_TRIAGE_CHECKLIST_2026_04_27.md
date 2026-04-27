# S6 Sprint 1 Batch-1 P1 Gap Triage Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Sprint 1 Batch-1 P1 Gap Triage Checklist 2026-04-27 |
| Status | READY_FOR_EP_T01_EXACT_LAUNCH_CHECKLIST |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Parent closeout | `docs\S6_SPRINT1_BATCH0_P1_RECONCILIATION_CLOSEOUT_2026_04_27.md` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Route | `OPEN_SPRINT1_BATCH1_P1_GAP_TRIAGE_CHECKLIST` |

This record triages remaining P1-facing `GS / IN / CD / EP` backlog tracker tasks after Batch-0 reconciliation.

It does not authorize code implementation, backend/runtime/API/schema changes, real data, secrets, deployment, public endpoint work, external pilot execution, Jira cloud mutation, or broad Sprint 1 build-start.

## 2. Decision

Decision:

```text
READY_FOR_EP_T01_EXACT_LAUNCH_CHECKLIST
```

Meaning:

- Batch-1 should not reopen the five Batch-0 reconciled tickets.
- Several remaining P1 tickets are visually dependent, P2/P3 gated, acceptance-only, or already partially covered but not ready for closeout.
- The next clean exact implementation candidate is `EP-T01 - subordinate panels framework`, because it has no visual-frame dependency, no governance dependency, no patch-gate impact, and can remain P1-local and mock-only.
- `EP-T01` still needs its own launch checklist before implementation.

## 3. Already Closed Or Reconciled

| Ticket | Status | Handling |
| --- | --- | --- |
| `GS-T01` | Reconciled in Batch-0 | Do not reopen. |
| `GS-T02` | Reconciled in Batch-0 | Do not reopen. |
| `GS-T03` | Reconciled in Batch-0 | Do not reopen. |
| `IN-T05` | Reconciled in Batch-0 | Do not reopen. |
| `CD-T03` | Reconciled in Batch-0 | Do not reopen. |
| `P1-CD-A/B/C/D` | Implemented and pushed | Treat as repo evidence for tracker reconciliation, not new backlog tickets. |

## 4. Remaining P1 Gap Triage

| Ticket | Tracker scope | Current triage | Why yes / why no |
| --- | --- | --- | --- |
| `GS-T04` | Expert mode entry and P1 restricted state | HOLD_VISUAL_FRAME | Requires `VF-03`; must not look like a permission unlock. Avoid inventing visual/interaction behavior before frame confirmation. |
| `GS-T05` | GS route/visibility smoke tests | HOLD_AFTER_GS_T04 | Acceptance tests should wait until `GS-T04` is resolved or explicitly deferred, otherwise they would freeze an incomplete GS surface. |
| `IN-T01` | Inbox list base structure and minimal fields | PARTIAL_COVERAGE_NEEDS_VISUAL_RECONCILIATION | Current Inbox card exists, but tracker requires `VF-02` alignment and exact field semantics. Do not close from current generic card alone. |
| `IN-T02` | P3 read-only inbox variant | HOLD_VISUAL_FRAME_AND_P3_BOUNDARY | Needs `VF-02` and stricter P3 no-work-queue affordance review. Do not close from current P3 navigation alone. |
| `IN-T03` | P2 quick approval/close entry and case-first return | HOLD_P2_RATIFICATION | Touches P2 approval semantics; wait for P2 v0.3 lightweight ratification and exact P2 route/authority checklist. |
| `IN-T04` | P1 upgrade/close request entry | HOLD_VISUAL_FRAME | Current P1 action request modal covers submit-to-P2 review, not close request. Requires `VF-02` and an exact authority-safe ticket. |
| `IN-T06` | Inbox role-difference and quick-entry guard tests | HOLD_AFTER_IN_T01_TO_IN_T04 | Acceptance-only ticket should wait until `IN-T01` through `IN-T04` are implemented or explicitly reconciled/deferred. |
| `CD-T01` | Case header with caseId / verdict / coverage / case_state | PARTIAL_COVERAGE_NEEDS_VISUAL_RECONCILIATION | Current case header and coverage badge exist, but coverage is topbar, not necessarily header; tracker requires `VF-03` / `VF-07` alignment. |
| `CD-T02` | `summary_layer.*` first-screen layout | PARTIAL_COVERAGE_NEEDS_VISUAL_RECONCILIATION | Current narrative summary exists, but `summary_layer.*` exact layout should wait for visual-aligned checklist. |
| `CD-T04` | Honesty layer display/fold/no silent disappearance | HOLD_VISUAL_FRAME | Current HONESTY section is visible, but fold/no-silent-disappear behavior depends on `VF-03`, `VF-09`, and `VF-10`. |
| `CD-T05` | Independent P3 executive summary component | HOLD_P3_RATIFICATION | Must wait for P3 full ratification and must not reuse P2 technical components by masking. |
| `CD-T06` | Closed / Observation Window / Approved Pending Execution state header | HOLD_PATCH_GATE_POSSIBLE | D-02/state label sensitive and `Patch Gate Impact = possible`; do not mix into Batch-1. |
| `CD-T07` | Case Detail multi-role / multi-state smoke tests | HOLD_AFTER_CD_T01_TO_CD_T06 | Acceptance-only ticket should wait until CD implementation gaps are resolved or explicitly deferred. |
| `EP-T01` | `panel=evidence/timeline/blast_radius` subordinate panel framework | READY_FOR_EXACT_LAUNCH | No visual dependency, no governance dependency, no patch-gate impact. Can be bounded to existing Case Detail and tests. |
| `EP-T02` | Inferred timeline node weakened style | HOLD_VISUAL_FRAME | Requires `VF-10`; visual treatment must not be invented. |
| `EP-T03` | `lineage_confidence @ L1 = DEGRADED` | HOLD_VISUAL_FRAME | Requires `VF-10`; resolver-degradation fixture evidence exists, but production UI treatment needs exact frame-aligned ticket. |
| `EP-T04` | `blast_radius @ L1 = OFF` | PARTIAL_COVERAGE_NEEDS_EP_T01 | E0-04C/E0-04B prove static redline behavior, but full EP closeout should follow the subordinate panel framework. |
| `EP-T05` | P3 technical panel soft fallback / summary fallback | HOLD_P3_RATIFICATION | Existing P3 raw-evidence absence tests help, but full ticket touches P3 manager semantics. |
| `EP-T06` | EP L1/L2/P3 negative tests | HOLD_AFTER_EP_T01_TO_EP_T05 | Acceptance-only ticket should wait until EP implementation gaps are resolved or explicitly deferred. |

## 5. Recommended Next Ticket

Recommended next route:

```text
OPEN_EP_T01_SUBORDINATE_PANEL_FRAMEWORK_LAUNCH_CHECKLIST
```

Recommended ticket:

```text
EP-T01 - subordinate panels framework
```

Why this ticket:

- no visual-frame dependency;
- no P2/P3 ratification dependency;
- no patch-gate impact;
- no backend/runtime/API/schema need;
- can be bounded to existing Case Detail UI;
- can preserve current evidence panel and Dialogue Dock behavior;
- creates the structural prerequisite for later EP negative tests and L1 blast/lineage hardening.

## 6. EP-T01 Draft Launch Bounds

These bounds are not implementation authorization. They define what the next launch checklist should verify.

Candidate allowed files:

- `docs/S6_EP_T01_SUBORDINATE_PANEL_FRAMEWORK_LAUNCH_CHECKLIST_2026_04_27.md`
- `docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md`
- `docs/HANDOFF.md`
- `frontend/src/App.tsx`
- `frontend/src/App.css`
- `frontend/src/App.test.tsx`

Candidate test command:

```powershell
cd frontend
npm run test -- --run
npm run build
```

Backend guard:

```powershell
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
```

Repo hygiene:

```powershell
git diff --check
```

Candidate acceptance:

- Case Detail exposes subordinate panel choices for evidence, timeline, and blast radius without adding a new top-level page.
- Subordinate panels remain mock-only and read-only.
- Blast radius must obey `coverage_level`; L1 must not render blast-radius detail or placeholder card.
- Existing contextual evidence panel controls remain accessible.
- P1 must not gain P2 approval authority.
- P3 host raw evidence must remain absent from the DOM.

Candidate non-goals:

- no new route;
- no backend/runtime/API/schema;
- no Storybook or Playwright changes;
- no fixture registry, adapter, validator, or E0 root context changes;
- no P2 approval workflow;
- no P3 manager implementation;
- no inferred timeline visual weakening beyond what existing CSS can safely express;
- no real data, secrets, deploy, public endpoint, or external pilot.

## 7. HOLD Conditions

HOLD if:

- `EP-T01` requires new fixture semantics, backend data, route handoff, or runtime/API/schema work;
- subordinate panels cannot be implemented without inventing product behavior;
- implementation needs visual details from `VF-10` or other visual frames;
- implementation touches P2 approval or P3 manager semantics;
- implementation must change `ResolvedSurfaceContext`, `ContextValidator`, fixture registry, or mock adapter behavior;
- tests cannot be named exactly;
- allowed files cannot remain exact;
- Claude Code review is unavailable after implementation diff;
- any Go/No-Go Section 9 or AI_COLLAB external-review trigger fires.

## 8. Next Safe Action

Next safe automation action:

```text
OPEN_EP_T01_SUBORDINATE_PANEL_FRAMEWORK_LAUNCH_CHECKLIST
```

No implementation is authorized by this triage checklist.
