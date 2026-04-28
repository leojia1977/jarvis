# S6 MV-T03 Deep-Link Authority Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `MV-T03` |
| Title | Manager deep-link handoff authority checklist |
| Status | CHECKLIST_ONLY_AUTHORITY_IMPLEMENTATION_NOT_AUTHORIZED |
| Date | 2026-04-28 |
| Primary implementor | Codex for checklist only |
| Execution surface | codex |
| Reviewer | Not required for docs-only checklist |
| Review surface | n/a |
| Workspace | VS Code / local repo |
| Source inputs | `docs\S6_MV_SH_AUDIT_AUTHORITY_MAP_2026_04_27.md`, `docs\S6_P2_P3_AUTHORITY_REVIEW_PACK_2026_04_27.md` |

This checklist defines the authority questions for `MV-T03` Manager deep-link handoff.

It does not authorize implementation, route handoff, approval audit summary, raw host evidence, backend/runtime/API/schema changes, fixture/adapter/validator changes, `ResolvedSurfaceContext` changes, real data, secrets, deploy, public endpoint, or external pilot.

## 2. Current Preconditions

Closed related tickets:

| Ticket | Evidence |
| --- | --- |
| `MV-T01` | P3-only Manager structure implemented; no P0/P2 placeholders. |
| `SH-T05` | Readonly focus scopes implemented. |
| `SH-T07` | Write CTA absence reconciled. |

Open related dependencies:

- `AP-T08` approval audit source legality is not implemented;
- `SH-T08` P3 approval-audit source availability is not resolved;
- `MV-T04` P3 approval audit summary is not implemented.

## 3. Authority Questions

Before implementation GO, answer all:

1. What source may initiate a Manager deep-link: Search/History, Case Detail, approval audit, or only explicit P3 navigation?
2. What payload may be passed without URL/storage becoming authority?
3. Does the deep-link require AP audit source legality from `AP-T08`?
4. Does the deep-link require SH P3 approval-audit source behavior from `SH-T08`?
5. What happens when target case/audit context is missing?
6. What must remain absent from DOM after handoff?
7. Can implementation avoid backend/runtime/API/schema and fixture/validator changes?

## 4. Tentative GO Conditions For A Later Implementation

`MV-T03` may move to implementation GO only if a later launch checklist proves:

```text
Source surface is exact: YES
Payload fields are exact: YES
URL/storage are non-authority: YES
Missing target context fail-closes: YES
No raw host evidence attaches: YES
Allowed files are exact: YES
Test command is exact: YES
AP-T08/SH-T08 dependency either not needed or already resolved: YES
No backend/runtime/API/schema required: YES
No fixture/adapter/validator/ResolvedSurfaceContext change required: YES
```

## 5. Required Tests For A Later Implementation

Future implementation tests should prove:

- allowed source can navigate to Manager without authority leakage;
- URL/query cannot upgrade role, coverage, or manager authority;
- missing handoff context renders safe guard/unavailable state;
- P3 raw host evidence is not attached;
- P0/P2 Manager variants are not introduced by this ticket.

## 6. External Review

External architecture/governance review is recommended if the checklist determines that `MV-T03` creates any new cross-surface authority path.

Review focus:

- source/target authority;
- URL/storage non-authority;
- dependency on `AP-T08` and `SH-T08`;
- P3 raw-evidence absence;
- no P0/P2 Manager variant leakage.

## 7. Decision

Decision:

```text
CHECKLIST_PASS_IMPLEMENTATION_REQUIRES_DEPENDENCY_PROOF_AND_SEPARATE_GO
```

Implementation status:

```text
NOT_AUTHORIZED
```

## 8. Next Safe Action

```text
DEFER_MV_T03_IMPLEMENTATION_UNTIL_AP_T08_SH_T08_DEPENDENCY_PROOF_OR_EXPLICIT_AUTHORITY_REVIEW_PASS
```

