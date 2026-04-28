# S6 AP-T08 / SH-T08 Authority Source Proof 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 AP-T08 / SH-T08 Authority Source Proof 2026-04-28 |
| Status | `AUTHORITY_SOURCE_PROOF_RECORDED_IMPLEMENTATION_NOT_AUTHORIZED` |
| Date | 2026-04-28 |
| Tickets | `AP-T08`, `SH-T08` |
| Jira | `SCRUM-62` and `SCRUM-63` remain `待办` with source-proof comments. |

This proof answers whether the approval-audit source path exists in governed product and fixture evidence. It does not implement approval audit rendering.

## 2. Source Evidence

| Source | Evidence | Authority consequence |
| --- | --- | --- |
| PRD v1.0 §5.8 / §5.9 | `MV-04` defines P3 `approval_audit` as an independent summary component with latest decision, timestamp, actor role, observation window presence, and terminal close status. `SH-08` says P3 approval-audit visibility is governed by role + source + data availability, not coverage unlock. | `approval_audit` is real governed scope, but only as read-only summary for P3. |
| Search/History Interaction Spec §6.1 / §6.2 | `approval_audit` focus is read-only; P1 redirects to summary; P3 is allowed only through `source=history|manager`. Minimal P3 fields are `latest_decision_status`, `latest_decision_timestamp`, `decision_actor_role_badge`, `observation_window_present`, `terminal_close_status`. | SH-T08 may define a read-only source boundary; it must not create audit data or write controls. |
| HF UI Spec §5.2 | `HF-AU-02` is an independent P3 summary component. It must not show approval CTA, host-level evidence links, or a coverage unlock ladder. Missing states are limited to no approval event record or audit data unavailable. | Visual boundary is known, but final visual PASS still needs the HF frame. |
| Core Surface Walkthrough v0.2 §4.6 / §5 | P3 Manager View may show `AUD-003 / AUD-004 / AUD-005`, must show `AUD-004` as `RETURN_TO_PENDING_APPROVAL`, and must not show approval queue, P2 strong confirm, host raw evidence, or raw payload. | Audit chain object continuity is defined across `CASE-2847`, `AR-2847-001`, and `AUD-*`. |
| Repo fixture `frontend\fixtures\secupilot_core_surface_fixture_v0_1.json` | The governed mock fixture already contains `audit_trail` entries `AUD-001` through `AUD-005`, including observation-window and approved-pending events. | A future narrow implementation can derive from existing mock context without changing fixture schema. |
| Repo context layer | `ResolvedSurfaceContext` already includes `audit_trail`, and the validator requires it as an array of records. | No `ResolvedSurfaceContext`, validator, registry, or adapter change is needed for source existence. |

## 3. AP-T08 Result

```text
AP_T08_AUTHORITY_SOURCE_PROOF_PASS_NARROW_IMPLEMENTATION_CHECKLIST_REQUIRED
```

AP-T08 source legality is proven for a future narrow checklist. That future checklist must still define:

- exact allowed fields derived from existing `audit_trail`;
- exact display-only AP boundary;
- exact test command;
- no state mutation, no AP transition, no backend/API/schema, no fixture/adapter/validator changes;
- no P3 output implementation inside AP scope.

Implementation is not authorized by this proof.

## 4. SH-T08 Result

```text
SH_T08_AUTHORITY_SOURCE_PROOF_PASS_NARROW_IMPLEMENTATION_CHECKLIST_REQUIRED
```

SH-T08 source legality is proven for a future narrow checklist. That future checklist must still define:

- P3 source guard: `source=history|manager` only;
- P1 downgrade to summary;
- read-only summary display or honest unavailable state;
- no write CTA and no full technical audit chain in `/search`;
- no route handoff implementation unless separately scoped.

Implementation is not authorized by this proof.

## 5. MV-T03 / MV-T04 Unlock Impact

This proof removes the specific `AP-T08 / SH-T08 source proof missing` blocker for:

- `MV-T03` deep-link authority relaunch checklist;
- `MV-T04` P3 approval-audit summary readiness checklist.

It does not authorize either implementation. Both still need exact per-ticket launch checklists and explicit implementation GO.

## 6. Non-Authorization

This proof does not authorize:

- approval audit UI implementation;
- Manager View deep-link implementation;
- P3 approval audit summary implementation;
- backend/runtime/API/schema changes;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- real data, secrets, deploy, public endpoint, or external pilot.
