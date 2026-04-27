# S6 Sprint 1 RQ-04 Exact Bounded Runner Queue 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Sprint 1 RQ-04 Exact Bounded Runner Queue 2026-04-27 |
| Queue item | `RQ-04` |
| Status | BOUNDED_RUNNER_QUEUE_OPEN_EP_T05_CLOSED |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |
| Predecessor | `docs\S6_SPRINT1_RQ03_PATCH_GATE_BATCH_ISOLATION_CHECKLIST_2026_04_27.md` |
| Route | `OPEN_RQ04_EXACT_BOUNDED_RUNNER_QUEUE` |

This queue gives the background runner several exact, bounded next actions without reopening general scope.

It does not authorize P2 Approval Surface, P3 Manager View, backend/runtime/API/schema changes, fixture registry or adapter changes, validator or `ResolvedSurfaceContext` changes, real data, secrets, deployment, public endpoint work, or external pilot execution.

## 2. Decision

Decision:

```text
BOUNDED_RUNNER_QUEUE_OPEN_EP_T05_SH_T05_THEN_SH_T07
```

Meaning:

- `EP-T05` and `SH-T05` are the only immediate code-ticket candidates in this queue.
- `SH-T07` is a follow-on candidate only after `SH-T05` closes as `GATE_PASS`.
- If a ticket-local HOLD occurs, the runner must record the HOLD and may continue only to a later ticket whose dependency chain is still satisfied.
- No patch-gate possible row other than the already closed `SH-T03` is reopened by this queue.

## 3. Candidate Selection Evidence

Strict tracker filter used:

```text
Ready State = ready
Design Dependency = none
Patch Gate Impact = none
Automation Eligible = yes
Dependencies already closed in repo evidence
Primary Implementor = codex
```

Immediate strict candidates:

| Ticket | Why safe enough for bounded runner |
| --- | --- |
| `EP-T05` | Depends only on `EP-T01`, which is implemented and pushed. No visual dependency, no patch-gate impact, no external review required by tracker. |
| `SH-T05` | Depends only on `SH-T03`, which is implemented, gated, reviewed, Jira-synced, and pushed. No visual dependency, no patch-gate impact, no external review required by tracker. |

Follow-on candidate:

| Ticket | Unlock condition |
| --- | --- |
| `SH-T07` | May start only after `SH-T05` closes with `IMPLEMENTED_GATE_PASS` or `RECONCILED_GATE_PASS_NO_CODE`. |

## 4. Authorized Queue

Run in this order:

1. `EP-T05-LAUNCH`
   - Use `docs\S6_EP_T05_P3_TECHNICAL_PANEL_FALLBACK_LAUNCH_CHECKLIST_2026_04_27.md`.
   - First determine whether current repo evidence already satisfies the ticket.
   - If no-code coverage is sufficient, close out as reconciliation and sync Jira.
   - If implementation is needed, proceed only if the checklist remains `GO` and exact allowed files are sufficient.

   Status: `IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_JIRA_DONE_SYNCED`.
   Closeout: `docs\S6_EP_T05_P3_TECHNICAL_PANEL_FALLBACK_CLOSEOUT_2026_04_27.md`.

2. `EP-T05-IMPLEMENT`
   - Allowed only if `EP-T05-LAUNCH` returns `GO`.
   - Must stay inside the checklist's allowed files.

   Status: complete. Do not reopen duplicate EP-T05 implementation.

3. `SH-T05-LAUNCH`
   - Use `docs\S6_SH_T05_READONLY_FOCUS_SCOPE_LAUNCH_CHECKLIST_2026_04_27.md`.
   - First determine whether current `/search?tab=history` behavior already satisfies the ticket.
   - If no-code coverage is sufficient, close out as reconciliation and sync Jira.
   - If implementation is needed, proceed only if the checklist remains `GO` and exact allowed files are sufficient.

4. `SH-T05-IMPLEMENT`
   - Allowed only if `SH-T05-LAUNCH` returns `GO`.
   - Must stay inside the checklist's allowed files.

5. `SH-T07-LAUNCH`
   - Create a new exact launch checklist only after `SH-T05` closeout.
   - Scope must be limited to history-page write CTA absence/disablement.
   - No implementation is authorized until that checklist gives `GO`.

6. `JIRA-PARITY-SAFE-SYNC`
   - If no code ticket is safe, sync only already repo-closed rows identified by RQ-01 as optional Jira parity candidates.
   - Do not mark any non-ready or visually blocked ticket Done.

## 5. Shared Allowed Files

For code implementation tickets in this queue, allowed files must be one of these exact sets:

```text
frontend/src/App.tsx
frontend/src/App.css
frontend/src/App.test.tsx
docs/S6_EP_T05_P3_TECHNICAL_PANEL_FALLBACK_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_SH_T05_READONLY_FOCUS_SCOPE_LAUNCH_CHECKLIST_2026_04_27.md
docs/S6_SPRINT1_RQ04_EXACT_BOUNDED_RUNNER_QUEUE_2026_04_27.md
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
docs/HANDOFF.md
```

No code ticket may change files outside the relevant ticket checklist plus route/handoff records.

## 6. Required Gates

Each implemented or reconciled ticket must run the smallest applicable gate:

```powershell
cd frontend
npm run test -- --run
npm run build
cd ..
py -3 -m unittest -q backend.tests.test_runtime_service backend.tests.test_case_view
git diff --check
```

Claude Code focused review is required for implementation diffs. It is not required for no-code reconciliation unless the runner modifies behavior.

## 7. Jira Rules

Jira cloud sync is allowed for PASS closeout only.

Allowed Jira behavior:

- create missing parent epic only if exact parent is absent and safe;
- create/update the exact ticket issue;
- transition the exact ticket to Done only after repo gate PASS;
- add labels that identify automation sync and ticket id.

Forbidden Jira behavior:

- bulk transition;
- marking visually blocked or dependency-blocked rows Done;
- marking `AP`, `MV`, `CH`, `CD-T06`, `SH-T08`, `SH-T09`, or any non-ready row Done from this queue.

## 8. HOLD Conditions

HOLD immediately if:

- implementation needs files outside the exact allowed list;
- implementation needs visual-frame interpretation not already available in repo evidence;
- implementation touches P2/P3 authority, P2 approval, P3 manager view, approval audit, state sync, observation-window migration, route handoff beyond the ticket surface, fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext`;
- implementation needs backend/runtime/API/schema changes;
- implementation uses real data, anonymized real data, secrets, deploy, public endpoint, or external pilot behavior;
- tests/build fail and cannot be corrected inside the ticket;
- Claude Code raises a blocking finding;
- any GoNoGo Section 9 mandatory external-review trigger fires.

## 9. Next Safe Action

Next safe automation action:

```text
OPEN_SH_T05_READONLY_FOCUS_SCOPE_LAUNCH_CHECKLIST
```
