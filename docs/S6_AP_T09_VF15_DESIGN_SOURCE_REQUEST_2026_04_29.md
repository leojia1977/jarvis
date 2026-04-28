# S6 AP-T09 VF-15 Design Source Request 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 AP-T09 VF-15 Design Source Request 2026-04-29 |
| Ticket | `AP-T09` |
| Status | AP_T09_VF15_DESIGN_SOURCE_REQUEST_READY_NO_IMPLEMENTATION |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Automation id | `secupilot-30m-bounded-burn-runner` |
| Trigger | Idle fallback design-frame request refresh |

## 2. Decision

```text
AP_T09_VF15_DESIGN_SOURCE_REQUEST_READY_NO_IMPLEMENTATION
```

This record converts the remaining `AP-T09` blocker into an exact design/source
request for `VF-15` or an equivalent governed audit empty/unavailable source.

It does not implement `AP-T09`, transition Jira, authorize visual PASS, or
create audit empty/unavailable copy in frontend code.

## 3. Current Blocker

`AP-T09` remains HOLD after `AP-T08` closeout because the repo has no governed
source that distinguishes:

```text
empty audit state
unavailable audit state
```

Existing `UNAVAILABLE` enum fallback is not enough. It is only a fallback
label, not a governed UX/source rule for audit-empty versus audit-unavailable
states.

## 4. Evidence

| Evidence | Result |
| --- | --- |
| `docs\S6_AP_T09_AUDIT_EMPTY_UNAVAILABLE_BLOCKER_REFRESH_2026_04_28.md` | `AP-T09` remains HOLD pending `VF-15` and exact source/copy. |
| `docs\S6_AP_T08_APPROVAL_AUDIT_SOURCE_BOUNDARY_CLOSEOUT_2026_04_28.md` | `AP-T08` is closed; approval audit source boundary exists. |
| `docs\S6_SPRINT1_RQ02_VISUAL_DEPENDENCY_UNBLOCK_QUEUE_2026_04_27.md` | `VF-15` is listed for `AP-T09` approval audit no-event / unavailable states. |
| `frontend/src/App.tsx` | Current fixed enum mapping includes missing event -> `UNAVAILABLE`, but this is not a complete AP-T09 governed empty/unavailable source. |

## 5. Required Design / Source Output

Design or product-source delivery should provide `VF-15` or an equivalent
governed source with these minimum decisions:

- visual/semantic treatment for approval audit empty state;
- visual/semantic treatment for approval audit unavailable state;
- exact distinction between empty audit and unavailable audit;
- governed copy source for each state;
- whether copy is static enum-label copy or `ui_messages`-driven copy;
- required test IDs / semantic anchors;
- whether a compact AP-surface version and a Manager/Search-History version
  share the same wording or only share state semantics;
- whether unavailable audit may appear when `activeContext.audit_trail` is
  missing, malformed, filtered, or explicitly absent;
- whether empty audit may appear when `activeContext.audit_trail` is present
  and valid but contains no renderable events.

## 6. Suggested Anchors

The source should either confirm or replace these implementation anchors:

```text
approval-audit-empty-state
approval-audit-unavailable-state
data-audit-state="empty"
data-audit-state="unavailable"
data-source="activeContext.audit_trail"
data-message-source="ui_messages" OR data-message-source="governed_enum_label"
```

If the design/source chooses different anchors, those anchors must be explicitly
listed so future tests do not invent selectors.

## 7. Future AP-T09 Implementation Eligibility

`AP-T09` can return to implementation checklist only after a later record proves:

- `VF-15` or equivalent governed source exists;
- empty and unavailable audit states are distinct;
- exact copy/source rules exist;
- renderable context can be tested without fixture/adapter/validator or
  `ResolvedSurfaceContext` expansion, or a separate governed context expansion
  ticket has been authorized;
- exact allowed files and tests are known.

## 8. Non-Authorization

This request does not authorize:

- `AP-T09` implementation;
- AP audit empty/unavailable rendering;
- frontend-authored product copy;
- AP state mutation;
- `ActionMode` creation;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext`
  changes;
- backend/runtime/API/schema work;
- Jira Done transition;
- real data;
- secrets;
- deploy;
- public endpoint;
- external pilot.

## 9. Next Route

```text
WAIT_FOR_MV_T04_IMPLEMENTATION_GO_OR_AP_T09_VF15_SOURCE_DELIVERY_OR_SH_T09_RECONCILIATION_GO_OR_JIRA_MAPPING_GO_OR_NEXT_IDLE_FALLBACK
```
