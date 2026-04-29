# S6 R2 R1 Authority Review Prompt Pack

## Document Control

- Document: `S6_R2_R1_AUTHORITY_REVIEW_PROMPT_PACK_2026_04_29`
- Date: 2026-04-29
- R2 item: `R2-03`
- Mode: docs-only authority prompt pack
- Implementation authorization: NO

## Decision

```text
R1_AUTHORITY_REVIEW_PROMPT_PACK_READY_NO_AUTHORITY_DECISION_FABRICATED
```

## Purpose

This pack gives governance / Claude Web a focused review prompt for the three R1 authority-blocked lanes. It does not answer the authority questions itself.

## Review Scope

```text
CH-T04 runtime/source-health scope
IN-T03 P2 shortcut approval / close-entry authority
MV-T02 P0/P2 Manager authority model
```

## Prompt

```text
Claude Web / Governance Review:

Review only authority boundaries for CH-T04, IN-T03, and MV-T02.
Do not authorize implementation, launch, deploy, real data, secrets, public endpoint, external pilot,
backend/runtime/API/schema, fixture/adapter/validator, or ResolvedSurfaceContext changes.

For CH-T04:
- Decide whether source-health scope is frontend-only semantic display or requires runtime/backend/API/schema.
- If runtime/backend/API/schema is required, mark implementation HOLD pending separate human/governed decision.
- Confirm whether ui_messages may drive degraded source-health copy.

For IN-T03:
- Decide whether Inbox may expose any P2 shortcut approval / close-entry affordance.
- Distinguish display-only, navigation-only, and action-capable behavior.
- Confirm how P1 ActionMode creation and P2 authority leakage are prevented.

For MV-T02:
- Decide whether P0/P2 may enter /manager.
- Define readonly/degraded fields for P0/P2, if any.
- Confirm whether P0/P2 require separate renderable contexts.
- Confirm no raw evidence DOM, P3-only audit leakage, or route/storage authority fallback.

Return one of:
- PASS_WITH_BOUNDED_GO_CONDITIONS
- PASS_WITH_NOTES
- HOLD
```

## Non-Authorization

This prompt pack does not authorize implementation or decide authority by itself. Any PASS must still become a future exact checklist with allowed files, tests, reviewer path, rollback/HOLD conditions, and Jarvis implementation GO.

## Next Route

```text
WAIT_FOR_CH_T04_IN_T03_MV_T02_AUTHORITY_REVIEW
```
