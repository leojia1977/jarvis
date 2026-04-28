# S6 30m Runner Unlock Watchlist 2026-04-29

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 30m Runner Unlock Watchlist 2026-04-29 |
| Status | UNLOCK_WATCHLIST_READY_NO_IMPLEMENTATION |
| Date | 2026-04-29 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Automation id | `secupilot-30m-bounded-burn-runner` |
| Trigger | Idle fallback exact operator prompt prep |
| Scope | Docs-only unlock/GO watchlist |

This watchlist converts the current idle route into copy-ready authorization
phrases. It is for operator convenience only.

It does not authorize implementation, Jira mutation, product-scope expansion,
backend/runtime/API/schema changes, fixture/adapter/validator changes,
`ResolvedSurfaceContext` changes, real data, secrets, deploy, public endpoint,
or external pilot.

## 2. Decision

```text
UNLOCK_WATCHLIST_READY_NO_IMPLEMENTATION
```

The runner remains active, but implementation remains blocked until one of the
phrases below is explicitly issued or an equivalent governed source delivery is
recorded.

## 3. Current Route

```text
WAIT_FOR_MV_T04_IMPLEMENTATION_GO_OR_AP_T11A_STATIC_ASSERTION_GO_OR_AP_T06_STATE_SYNC_SOURCE_DELIVERY_OR_AP_T09_VF15_SOURCE_DELIVERY_OR_SH_T09_RECONCILIATION_GO_OR_JIRA_MAPPING_GO_OR_NEXT_IDLE_FALLBACK
```

## 4. Copy-Ready Unlock Phrases

### Option A - MV-T04 Implementation

Use only if Jarvis wants to burn the next Manager View implementation ticket.

```text
Jarvis authorization:

Authorize MV-T04 implementation GO.

Scope is limited to a P3-only read-only Manager approval audit summary sourced
only from existing activeContext.audit_trail and the fixed AP-T08/SH-T08
derived-status mapping.

No raw evidence DOM.
No approval controls.
No P0/P2 Manager variants.
No route/storage authority.
No backend/runtime/API/schema.
No fixture/adapter/validator/ResolvedSurfaceContext changes.
No real data, secrets, deploy, public endpoint, or external pilot.

Run gates, Claude Code focused review, Jira sync after PASS, stage/commit/push.
```

### Option B - AP-T11A Static No-Mutation Assertions

Use only if Jarvis wants a narrow test/assertion ticket without AP transition
scope.

```text
Jarvis authorization:

Authorize AP-T11A static no-mutation assertion implementation GO.

Scope is limited to tests/assertions over existing AP static boundaries:
AP-T03/AP-T04/AP-T05/AP-T06A/AP-T07/AP-T08.

No AP state transition.
No ActionMode creation.
No countdown/state-sync.
No audit empty/unavailable rendering.
No runtime selector changes unless a later exact checklist replaces this scope.
No backend/runtime/API/schema.
No fixture/adapter/validator/ResolvedSurfaceContext changes.
No real data, secrets, deploy, public endpoint, or external pilot.

Run gates, Claude Code review if code diff, Jira sync only after PASS and only
to a dedicated AP-T11A issue or later approved mapping target, stage/commit/push.
```

### Option C - SH-T09 No-Code Reconciliation

Use only if Jarvis wants to close the Search / History acceptance chain from
existing evidence.

```text
Jarvis authorization:

Authorize SH-T09 no-code reconciliation GO.

Use existing Search / History closeout evidence only.
If code is needed, HOLD and create a separate exact implementation checklist.

Do not create Search / History runtime behavior.
Do not mutate Jira unless the reconciliation passes and exact Jira mapping is safe.
Run docs gates and stage/commit/push if PASS.
```

### Option D - Jira Mapping For Repo PASS Rows

Use only if Jarvis wants Jira parity for `SH-T02`, `SH-T06`, and `EP-T06`.

```text
Jarvis authorization:

Authorize Jira mapping GO for SH-T02 / SH-T06 / EP-T06.

Use the existing Jira mapping proposal.
Create dedicated Jira child issues only if exact mapping option A is selected,
or attach evidence to parent issues only if exact mapping option B is selected.
Do not mark HOLD or non-ready issues Done.
Do not change repo code.
Record Jira read-back evidence and commit docs-only sync.
```

## 5. Source-Delivery Unlocks

These are not GO phrases. They require new governed source material:

| Source delivery | Unlocks | Required before implementation |
| --- | --- | --- |
| `AP-T06` state-sync source / harness decision | Full `AP-T06`, full `AP-T11`, AP acceptance state-sync path | Exact input contract, display-vs-authority rule, test-only harness semantics |
| `AP-T09` `VF-15` or equivalent source | `AP-T09`, AP audit empty/unavailable path | Distinct empty/unavailable semantics, copy source, stable anchors |

## 6. HOLD Conditions

HOLD if any future unlock attempts require:

- backend/runtime/API/schema changes;
- fixture/adapter/validator or `ResolvedSurfaceContext` changes;
- raw evidence DOM attachment;
- P2/P3 authority ambiguity;
- visual semantic ambiguity;
- real data, secrets, deploy, public endpoint, or external pilot;
- Jira Done transition for a HOLD, blocked, visual-missing, authority-missing,
  or non-ready ticket.

## 7. Non-Authorization

This watchlist does not authorize:

- any implementation;
- any Jira mutation;
- `MV-T04`;
- `AP-T11A`;
- `SH-T09`;
- full `AP-T06`;
- `AP-T09`;
- any source invention.

## 8. Next Route

```text
WAIT_FOR_MV_T04_IMPLEMENTATION_GO_OR_AP_T11A_STATIC_ASSERTION_GO_OR_AP_T06_STATE_SYNC_SOURCE_DELIVERY_OR_AP_T09_VF15_SOURCE_DELIVERY_OR_SH_T09_RECONCILIATION_GO_OR_JIRA_MAPPING_GO_OR_NEXT_IDLE_FALLBACK
```
