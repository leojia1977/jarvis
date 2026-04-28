# S6 SH-T04 Search/History Scope Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `SH-T04` |
| Title | Search/History filter and scope reconciliation checklist |
| Status | CHECKLIST_ONLY_RECONCILIATION_CANDIDATE_IMPLEMENTATION_NOT_AUTHORIZED |
| Date | 2026-04-28 |
| Primary implementor | Codex for checklist only |
| Execution surface | codex |
| Reviewer | Not required for docs-only checklist |
| Review surface | n/a |
| Workspace | VS Code / local repo |
| Source inputs | `docs\S6_REMAINING_BLOCKER_MAP_2026_04_27.md`, `docs\S6_MV_SH_AUDIT_AUTHORITY_MAP_2026_04_27.md` |

This checklist determines whether `SH-T04` can close as no-code reconciliation or needs a later bounded implementation.

It does not authorize implementation, route handoff, approval controls, write actions, host raw evidence, backend/runtime/API/schema changes, fixture/adapter/validator changes, `ResolvedSurfaceContext` changes, real data, secrets, deploy, public endpoint, or external pilot.

## 2. Current Preconditions

Closed related tickets:

| Ticket | Evidence |
| --- | --- |
| `SH-T01` | Historical list item skeleton implemented. |
| `SH-T03` | Clamp-first route behavior implemented. |
| `SH-T05` | Readonly focus scopes implemented. |
| `SH-T07` | Write CTA absence reconciled. |

Open related blockers:

- `SH-T02` needs visual frames;
- `SH-T06` needs visual frame;
- `SH-T08` depends on AP audit source;
- `SH-T09` remains acceptance-only later.

## 3. Scope Questions

Before closeout or implementation GO, answer all:

1. What exactly is `SH-T04` expected to cover: filters, tabs, focus scopes, source labels, or empty/degraded states?
2. Is current repo behavior already sufficient after `SH-T01`, `SH-T03`, `SH-T05`, and `SH-T07`?
3. Does `SH-T04` require new visual frame interpretation?
4. Does it require route handoff to Case Detail or Manager?
5. Does it require P3 approval-audit source behavior owned by `SH-T08`?
6. Can it close as no-code reconciliation with existing tests?

## 4. No-Code Reconciliation Conditions

`SH-T04` may close as no-code only if a later reconciliation record proves:

```text
Ticket scope is fully covered by existing SH behavior: YES
No visual-frame interpretation is needed: YES
No route handoff is needed: YES
No P3 approval-audit source is needed: YES
Existing tests cover the acceptance surface: YES
Jira issue can be safely synced as Done: YES
```

## 5. Implementation Conditions If No-Code Is Insufficient

If implementation is needed, it requires separate GO and must prove:

```text
Allowed files are exact: YES
Test command is exact: YES
No route handoff beyond SH-T04: YES
No approval/write control: YES
No backend/runtime/API/schema: YES
No fixture/adapter/validator/ResolvedSurfaceContext change: YES
```

## 6. Decision

Decision:

```text
CHECKLIST_PASS_RECONCILIATION_OR_IMPLEMENTATION_REQUIRES_SEPARATE_CLOSEOUT_DECISION
```

Implementation status:

```text
NOT_AUTHORIZED
```

## 7. Next Safe Action

```text
OPEN_SH_T04_NO_CODE_RECONCILIATION_REVIEW_OR_REQUEST_EXACT_IMPLEMENTATION_GO_IF_GAP_EXISTS
```

