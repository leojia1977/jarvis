# S6 CH-T03 Patch-Gate Isolated Checklist 2026-04-28

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `CH-T03` |
| Title | Coverage & Health `ui_messages` rendering patch-gate checklist |
| Status | CHECKLIST_ONLY_PATCH_GATE_ISOLATION_IMPLEMENTATION_NOT_AUTHORIZED |
| Date | 2026-04-28 |
| Primary implementor | Codex for checklist only |
| Execution surface | codex |
| Reviewer | Not required for docs-only checklist |
| Review surface | n/a |
| Workspace | VS Code / local repo |
| Source inputs | `docs\S6_REMAINING_BLOCKER_MAP_2026_04_27.md`, `docs\S6_DESIGN_UNBLOCK_FRAME_REQUEST_PACK_2026_04_27.md` |

This checklist isolates `CH-T03` before any `ui_messages` rendering work.

It does not authorize implementation, patching governed wording, coverage semantics changes, final visual PASS, backend/runtime/API/schema changes, fixture/adapter/validator changes, `ResolvedSurfaceContext` changes, real data, secrets, deploy, public endpoint, or external pilot.

## 2. Current Preconditions

Closed predecessor:

| Ticket | Evidence |
| --- | --- |
| `CH-T01` | Coverage & Health page skeleton implemented and gated. |

Open related blockers:

- `CH-T02` still needs `VF-01`;
- `CH-T04` depends on `CH-T01`, `CH-T02`, and `CH-T03`;
- `CH-T03` is patch-gate possible because `ui_messages` rendering can affect governed copy semantics.

## 3. Patch-Gate Questions

Before implementation GO, answer all:

1. Which existing `ui_messages` keys may render in Coverage & Health?
2. Are messages static fixture-driven, governed-copy driven, or dynamic backend-driven?
3. Does rendering require changing any frozen product wording?
4. Does rendering imply live source health or backend readiness?
5. How is missing `ui_messages` represented honestly?
6. Can implementation proceed before `VF-01`, or only as semantic skeleton?
7. Which tests prove no hardcoded misleading health copy is introduced?

## 4. Tentative GO Conditions For A Later Implementation

`CH-T03` may move to implementation GO only if a later launch checklist proves:

```text
Allowed ui_messages keys are exact: YES
No governed wording patch is required: YES
No live backend/source-health claim is introduced: YES
Missing messages degrade honestly: YES
Allowed files are exact: YES
Test command is exact: YES
Patch-gate conflict absent or resolved: YES
No backend/runtime/API/schema change required: YES
No fixture/adapter/validator/ResolvedSurfaceContext change required: YES
```

## 5. Required Tests For A Later Implementation

Future implementation tests should prove:

- known `ui_messages` render only inside the Coverage & Health skeleton;
- missing `ui_messages` render unavailable/degraded copy;
- no live backend readiness claim appears;
- no coverage escalation or OFF-field bypass occurs;
- P1/P3 role exposure remains guarded as established by `CH-T01`.

## 6. External Review

External review is conditional.

It becomes mandatory if implementation discovers:

- governed wording conflict;
- coverage semantics conflict;
- live health/readiness implication;
- backend/runtime/API/schema need;
- fixture/adapter/validator/`ResolvedSurfaceContext` need.

## 7. Decision

Decision:

```text
CHECKLIST_PASS_PATCH_GATE_ISOLATED_IMPLEMENTATION_REQUIRES_SEPARATE_GO
```

Implementation status:

```text
NOT_AUTHORIZED
```

## 8. Next Safe Action

```text
AUTHORIZE_CH_T03_IMPLEMENTATION_ONLY_AFTER_UI_MESSAGES_KEYS_AND_PATCH_GATE_CONFLICT_CHECK_ARE_EXACT
```

