# S5-C Scoped Implementation Decision

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S5-C Scoped Implementation Decision |
| Status | Closed as governed S5-C scoped implementation decision baseline |
| Scope | S5-C scoped implementation decision only |
| Baseline | S5C-SCOPED-IMPLEMENTATION-DECISION-PREP-2026-04-16-001 |
| Predecessor artifacts | docs/S5C_SCOPED_IMPLEMENTATION_DECISION_PREP.md; docs/S5_POST_MILESTONE_EXTERNAL_INPUT_TRACKER.md; docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md; docs/S5C_IMPLEMENTATION_DECISION_CHECKPOINT.md |
| Route | OPEN_S5_C_SCOPED_IMPLEMENTATION_DECISION |
| primary_implementor | VS Code |
| reviewer | Claude Code |
| reviewer_when_cc_implements | not applicable |
| requires_external_review | true |

`requires_external_review` is true because this decision chooses which governed S5-C clauses may later enter scoped implementation tickets and which areas must remain HOLD. It engages case lifecycle semantics, action-request semantics, audit/evidence behavior, redaction/secret/evidence boundaries, public endpoint deferral, and future runtime/test planning. External review does not authorize implementation and does not replace human go/no-go.

## 2. Goal

This document drafts a governed docs-only S5-C scoped implementation decision.

The goal is to decide which already-governed S5-C planning/contract areas are eligible for later separate implementation tickets, and which areas remain HOLD.

This decision must not authorize implementation.

This document answers:

- Which S5-C governed areas may be candidates for later implementation tickets?
- Which areas remain HOLD and why?
- What exact requirements must any later implementation ticket include?
- Which public endpoint, external pilot, evidence, S5-B/S5-D, S4-A, and AI_COLLAB boundaries remain unchanged?
- What is the recommended next route after this decision?

## 3. Baseline Summary

- Sprint 5 milestone verdict: `SPRINT5_BASELINE_REVIEW_PASS_WITH_EXTERNAL_INPUTS_PENDING`.
- External Input Tracker is closed as a governed tracker baseline and does not make any input `READY`.
- S5-C Scoped Implementation Decision Prep is closed as a governed prep baseline.
- This ticket opens only `OPEN_S5_C_SCOPED_IMPLEMENTATION_DECISION`.
- S5-A external pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- Real customer/operator sign-off remains unauthorized.
- S5-B remains `PASS_AND_PARK`.
- S5-D remains `PASS_AND_PARK`.
- S5-C is a governed planning/contract baseline; this decision is not implementation authorization.
- Public close-case endpoint remains `KEEP_DEFERRED`; this decision must keep it HOLD.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- AI_COLLAB operating model and contract are not changed.

## 4. S5-C-3 Status Correction

- `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md` file header may still say `Status: Draft for review`.
- `docs/HANDOFF.md`, `releases/release_manifest.json`, and later S5-C / Sprint 5 governance records are the controlling evidence that S5-C-3 is a governed contract/planning artifact.
- Treat the header mismatch as documentation hygiene only, not an unmet precondition.
- This draft does not modify S5-C-3.
- S5-C-3 alone does not authorize implementation.

## 5. Decision Vocabulary

Allowed decision outcomes:

- `ALLOW_LATER_IMPLEMENTATION_TICKET`
- `HOLD_PUBLIC_ENDPOINT`
- `HOLD_EXTERNAL_INPUT`
- `HOLD_POLICY_OR_EXTERNAL_REVIEW`
- `HOLD_OUT_OF_SCOPE`
- `HOLD_PENDING_PRODUCT_DECISION`
- `NOT_APPLICABLE`

Forbidden decision outcomes:

- `READY`
- `APPROVED`
- `IMPLEMENTABLE`
- `PILOT_READY`
- `PRODUCTION_READY`
- `AUTHORIZED_FOR_IMPLEMENTATION`
- `IMPLEMENT_NOW`

This document must not use forbidden outcomes as decision values. `ALLOW_LATER_IMPLEMENTATION_TICKET` means only that a later separate ticket may be drafted if it satisfies all requirements in this decision; it is not immediate implementation permission.

## 6. Fixed S5-C Scoped Decision Risks

Each item below is a HOLD trigger if it appears, becomes implied, or is treated as satisfied by this decision:

- scoped decision mistaken for implementation authorization
- `ALLOW_LATER_IMPLEMENTATION_TICKET` mistaken for direct implementation permission
- S5-C PASS mistaken for runtime authorization
- public close-case endpoint `KEEP_DEFERRED` weakened
- exact future implementation ticket requirements skipped
- case lifecycle semantics changed or frozen beyond governed baselines
- action request approval/denial/cancellation semantics changed or frozen beyond governed baselines
- audit/evidence behavior changed into evidence retention
- redaction/secret/evidence boundaries frozen without separate review
- new persisted lifecycle/action-request statuses introduced
- destructive response automation introduced
- RBAC / ticketing / workflow engine scope introduced
- runtime/API/schema/test/dependency changes appear in this decision
- fixture file creation or modification appears
- external pilot execution or readiness appears
- real customer/operator sign-off appears
- real SIEM/EDR/source/telemetry access appears
- credentials/tokens/API keys/auth headers/cookies appear
- raw logs/screenshots/exports/payloads/event bodies/customer evidence appear
- S5-B or S5-D reopen appears
- S4-A resolver order changes
- AI_COLLAB operating model or contract changes
- external review bypass or human go/no-go replacement
- automatic implementation ticket created by this decision

## 7. Decision Matrix

| S5-C governed area | Governed source artifact(s) | Decision outcome | Decision rationale | Future implementation ticket may include | Future implementation ticket must not include | requires_external_review implication | HOLD triggers | Non-authorization note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| durable case lifecycle baseline | `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`; S4-C lifecycle baselines referenced by S5-C | `ALLOW_LATER_IMPLEMENTATION_TICKET` | Durable case lifecycle is already governed and may be considered only through a later exact scoped ticket. | exact lifecycle clause, exact file paths, current/proposed behavior, tests, closed-case safety checks, rollback/HOLD criteria | new lifecycle states, weakened closed-case safety, broad runtime rewrite, or endpoint scope | true if lifecycle semantics are mapped into runtime/API/test behavior or changed | lifecycle state expansion, unsafe post-close mutation, ambiguous files/tests | does not authorize implementation now |
| case close reason / lifecycle semantics | `docs/S5C2_CLOSE_REASON_AND_LIFECYCLE_SEMANTICS.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | `ALLOW_LATER_IMPLEMENTATION_TICKET` | Close reason/lifecycle semantics are governed enough for later exact scoping, but not for endpoint work or semantic expansion. | exact close reason/lifecycle clause, exact behavior delta, exact tests, audit expectations | public endpoint opening, new semantics beyond governed baselines, new persisted states | true if close semantics are frozen into implementation scope or changed | endpoint creep, new close reason behavior, ambiguous acceptance criteria | does not open public endpoint or add new semantics |
| action request approval semantics | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | `ALLOW_LATER_IMPLEMENTATION_TICKET` | Approval semantics are governed as non-destructive workflow data and may be considered only in a later scoped ticket. | exact approval clause, exact files, exact tests, audit traceability, non-destructive boundary | destructive execution, real sign-off, external action, RBAC/ticketing integration | true if approval semantics are mapped into runtime/test behavior or changed | approval triggers response action, real customer/operator sign-off, new status behavior | does not authorize approval implementation now |
| action request denial / rejection semantics | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | `ALLOW_LATER_IMPLEMENTATION_TICKET` | Denial/rejection semantics are governed as evidence-preserving and may be considered only through exact later scope. | exact denial/rejection clause, tests, audit preservation, expected user-facing wording if relevant | evidence deletion, audit erasure, new status vocabulary, destructive behavior | true if denial/rejection semantics are mapped into runtime/test behavior or changed | evidence deletion, new persisted vocabulary, ambiguous rejection behavior | does not authorize denial/rejection implementation now |
| action request cancellation / withdrawal semantics | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | `ALLOW_LATER_IMPLEMENTATION_TICKET` | Cancellation/withdrawal semantics are governed as non-destructive and may be scoped later if history preservation is exact. | exact cancellation/withdrawal clause, existing behavior comparison, tests, audit preservation | erased request history, removed evidence, broader workflow invention, endpoint coupling | true if cancellation semantics are mapped into runtime/test behavior or changed | request history erasure, evidence removal, new workflow implied | does not authorize cancellation/withdrawal implementation now |
| audit history / decision traceability | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | `ALLOW_LATER_IMPLEMENTATION_TICKET` | Append-safe, replayable audit/decision traceability is governed enough for later exact implementation-ticket scoping. | exact audit clause, exact audit behavior, non-sensitive decision references, tests, replay expectations | raw evidence retention, customer/operator evidence, mutable audit, oral-only evidence | true if audit/evidence behavior is mapped into runtime behavior or changed | raw evidence appears, retention is implied, audit mutability appears | does not authorize raw evidence retention |
| pending action request behavior around close-case workflows | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` | `HOLD_PUBLIC_ENDPOINT` | Pending-close behavior is tied to the deferred public close-case endpoint and should not be implemented until endpoint scope is explicitly opened. | future endpoint-specific decision questions only if a later explicit endpoint ticket opens the endpoint | endpoint behavior, close API implementation, runtime/API payloads, method/path/response freeze | true if endpoint behavior or lifecycle/API semantics are opened later | `KEEP_DEFERRED` weakened, endpoint proceeds while pending behavior is ambiguous | does not authorize endpoint or pending-close runtime behavior |
| closed-case safety / immutability boundary | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | `ALLOW_LATER_IMPLEMENTATION_TICKET` | Closed-case safety is a governed boundary and may be considered for later exact hardening scope only. | exact closed-case safety clause, exact files/tests, expected failure behavior, rollback/HOLD criteria | weakened closed-case protections, post-close unsafe mutation, endpoint implementation | true if closed-case behavior is mapped into runtime/test behavior or changed | unsafe mutation, lifecycle state changes, endpoint coupling | does not authorize code/test/runtime changes now |
| evidence/audit note handling | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5_POST_MILESTONE_EXTERNAL_INPUT_TRACKER.md` | `HOLD_POLICY_OR_EXTERNAL_REVIEW` | Evidence/audit notes touch evidence handling and must not become retention or raw evidence handling through this decision. | future non-sensitive note boundary questions only if separately scoped | evidence retention, raw logs, screenshots, exports, payloads, event bodies, customer/operator evidence | true for any evidence retention, redaction, real evidence, or storage behavior change | raw evidence appears, retention/storage/replay is implied, policy freeze appears | does not authorize evidence retention or raw evidence handling |
| redaction / secret handling boundary | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5_POST_MILESTONE_EXTERNAL_INPUT_TRACKER.md`; S5-A/S5-D redaction boundaries | `HOLD_POLICY_OR_EXTERNAL_REVIEW` | Redaction and secret handling are high-risk boundaries and must remain separate unless externally reviewed in a later policy/boundary route. | future redaction/secret checklist questions only if separately scoped | redaction policy freeze, secrets handling implementation, credentials, tokens, API keys, auth headers, cookies | true for any redaction/secret/evidence-retention boundary change | secrets appear, raw payloads appear, policy freeze appears | does not authorize redaction policy or secrets handling implementation |
| public close-case HTTP endpoint | `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | `HOLD_PUBLIC_ENDPOINT` | S5-C-4 selected `KEEP_DEFERRED`; this decision preserves that endpoint hold. | no endpoint implementation; only a future explicit endpoint ticket could reopen endpoint eligibility | endpoint implementation, method/path/request/response/error model freeze, public API changes | true if endpoint behavior is later opened or mapped to runtime/API implementation | `KEEP_DEFERRED` weakened, endpoint scope appears, runtime/API endpoint work appears | does not authorize endpoint implementation |
| destructive response automation / response execution | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | `HOLD_OUT_OF_SCOPE` | S5-C approval semantics are non-destructive and do not create response execution authority. | `NOT_APPLICABLE` unless a later separate product/governance route explicitly opens response automation | destructive response, external SIEM/EDR/source action, automated execution, ticket/action execution | true if destructive response or external action behavior is proposed | response execution appears, external action appears, approval becomes execution | no destructive response automation is authorized |
| RBAC / ticketing / workflow engine integration | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | `HOLD_OUT_OF_SCOPE` | RBAC, ticketing, and workflow engine integration remain outside S5-C scoped implementation decision unless separately opened. | `NOT_APPLICABLE` unless a later governed route explicitly opens integration scope | RBAC, ticketing, workflow engine, permission infrastructure, external ticket creation | true if authorization, integration, multi-tenant ownership, or workflow-engine semantics are proposed | integration scope appears, actor wording becomes permission model | no RBAC/ticketing/workflow integration is authorized |
| external pilot / customer evidence behavior | `docs/S5_POST_MILESTONE_EXTERNAL_INPUT_TRACKER.md`; `docs/S5_SPRINT5_MILESTONE_REVIEW_PASS.md`; S5-A external pilot docs | `HOLD_EXTERNAL_INPUT` | External pilot inputs remain `NOT_READY` / `UNKNOWN`, and real customer/operator evidence remains outside S5-C decision scope. | future non-sensitive governance decision records only | external pilot execution, real sign-off, real access, customer/operator evidence, credentials, raw payloads | true if real external evidence/access, pilot readiness, sign-off, or retention is implicated | external input status promoted, real evidence appears, live access appears | no real customer/operator evidence is accepted |

## 8. Future Implementation Ticket Requirements

Any later implementation ticket allowed by this decision must define the following before code/test/runtime/API/schema/dependency work can begin:

- exact governed S5-C clause(s)
- exact implementation ticket scope
- exact file paths
- exact behavior changes
- exact tests to add or modify
- exact test command(s)
- acceptance criteria
- audit history expectations
- evidence handling / non-retention boundary
- redaction / secret handling check
- pending action request behavior if relevant
- closed-case safety behavior if relevant
- rollback / hold criteria
- public close-case endpoint status, preserving `KEEP_DEFERRED`
- external pilot execution remains unauthorized
- real customer/operator sign-off remains unauthorized
- real external-system access remains unauthorized
- `requires_external_review` decision and rationale
- human go/no-go requirement
- `primary_implementor` / `reviewer` / `reviewer_when_cc_implements` assignment

If a later ticket cannot make these details exact, that later ticket must HOLD rather than infer implementation scope.

## 9. Relationship To Prior Baselines

- `docs/S5C_SCOPED_IMPLEMENTATION_DECISION_PREP.md` remains the governed prep baseline.
- `docs/S5_POST_MILESTONE_EXTERNAL_INPUT_TRACKER.md` remains the governed tracker baseline.
- The tracker does not make any external input `READY`.
- This decision may not consume real evidence, raw payloads, logs, screenshots, exports, credentials, tokens, or external-system access.
- If later external inputs reveal a source/input gap, S5-B reopen requires explicit reopen decision.
- If later external inputs reveal a telemetry gap, S5-D reopen requires explicit reopen decision.
- This decision does not reopen S5-B or S5-D.

## 10. Non-Authorization

This decision does not authorize:

- implementation
- immediate code/test/runtime/API/schema/dependency changes
- fixture file creation or modification
- S5-C runtime work by itself
- public close-case endpoint work
- weakening `KEEP_DEFERRED`
- destructive response automation
- RBAC / ticketing / workflow engine integration
- new persisted lifecycle or action-request statuses
- case lifecycle semantic freeze beyond already governed baselines
- action request semantic freeze beyond already governed baselines
- evidence retention, storage, replay, deletion, expiry, or evidence-pack behavior
- redaction policy freeze
- secrets handling implementation
- external pilot execution
- external pilot readiness
- real customer/operator sign-off
- real SIEM/EDR/source/telemetry access
- credentials/tokens/API keys/auth headers/cookies/secret material
- raw logs/screenshots/exports/payloads/event bodies/customer/operator evidence
- S5-B reopen
- S5-D reopen
- S4-A resolver priority or authority changes
- AI_COLLAB operating model or contract changes
- external review bypass
- human go/no-go replacement
- automatic implementation ticket

## 11. HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| any implementation instruction appears | this decision is docs-only and non-implementing |
| runtime/API/schema/test/dependency or fixture changes appear | changes require a later governed implementation ticket |
| any decision row uses forbidden outcome vocabulary | this decision may use only the allowed outcomes listed above |
| `ALLOW_LATER_IMPLEMENTATION_TICKET` is treated as immediate implementation permission | allowed rows permit only later separate ticket drafting |
| future implementation ticket requirements are skipped | exact clauses, files, behavior, tests, acceptance, evidence boundaries, review, and go/no-go are mandatory |
| public close-case endpoint `KEEP_DEFERRED` is weakened | public endpoint remains held |
| destructive response automation appears | destructive response remains out of scope |
| RBAC / ticketing / workflow engine integration appears | integration remains out of scope |
| new persisted lifecycle/action-request statuses appear | status changes require separate governed decision and implementation scope |
| external pilot execution/readiness/sign-off appears | external pilot path remains unauthorized and inputs remain non-ready |
| real external-system access appears | live SIEM/EDR/source/telemetry access is outside scope |
| credentials/tokens/API keys/auth headers/cookies/secret material appear | secrets are prohibited in this draft |
| raw evidence, logs, screenshots, exports, payloads, event bodies, or customer/operator evidence appear | this decision may not consume real evidence |
| evidence retention/redaction/secrets boundary is frozen without external review | boundary freeze is an external-review trigger and is not authorized here |
| S5-B or S5-D reopen appears without explicit reopen decision | both streams remain `PASS_AND_PARK` |
| S4-A resolver priority changes | resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases` |
| AI_COLLAB operating model or contract changes appear | AI_COLLAB files are not part of this task |
| external review is skipped or treated as replacing human go/no-go | external review is required and human go/no-go remains required |
| HANDOFF or manifest is modified during draft-only stage | this draft may create only this new docs file |
| protected untracked files are touched | protected untracked files must remain untouched |

## 12. Preliminary Recommendation

`PRELIMINARY_RECOMMENDATION_OPEN_FIRST_ALLOWED_S5_C_IMPLEMENTATION_TICKET_FOR_CASE_LIFECYCLE_AND_ACTION_REQUEST_SEMANTICS`

Meaning:

- this decision may be reviewed and, if accepted, closed as a governed S5-C scoped implementation decision baseline
- it permits a later separate implementation ticket to be drafted for a tightly scoped subset of allowed areas, preferably case lifecycle and action-request semantics that do not touch public close-case endpoint, external pilot, evidence retention, destructive response automation, RBAC/ticketing/workflow integration, S5-B/S5-D reopen, S4-A resolver behavior, or AI_COLLAB
- the later implementation ticket must still define exact clauses, files, behavior changes, tests, acceptance criteria, evidence/redaction/secret boundaries, rollback/HOLD criteria, external review decision, and human go/no-go
- the later implementation ticket may still HOLD if exact scope is not clean enough

Non-meaning:

- does not authorize implementation now
- does not authorize code/test/runtime/API/schema/dependency changes in this draft
- does not authorize public close-case endpoint work
- does not authorize external pilot execution or readiness
- does not authorize real customer/operator sign-off or real external-system access
- does not authorize evidence retention or redaction policy freeze
- does not reopen S5-B or S5-D
- does not change S4-A resolver order
- does not change AI_COLLAB
- does not create an automatic implementation ticket

## 13. Acceptance Criteria

This draft is acceptable if:

- exactly one new docs-only file is created
- `requires_external_review` is true with rationale
- baseline summary is accurate
- S5-C-3 status correction is included and does not modify S5-C-3
- decision matrix includes all required rows
- allowed / HOLD outcomes are assigned as required
- public close-case endpoint remains `KEEP_DEFERRED`
- no row uses forbidden outcome vocabulary
- `ALLOW_LATER_IMPLEMENTATION_TICKET` is defined as later ticket permission only, not immediate implementation permission
- future implementation ticket requirements are listed
- External Input Tracker remains non-ready and is not treated as evidence source
- no implementation, runtime/API/schema/test/dependency, or fixture changes are authorized in this draft
- no external pilot execution, sign-off, real access, credentials, raw evidence, or evidence retention is authorized
- S5-B and S5-D remain `PASS_AND_PARK` unless later explicit reopen decision
- S4-A resolver order remains unchanged
- AI_COLLAB files are not modified
- HANDOFF and manifest are not modified in this draft stage
- full gate is not run
- no staging, commit, or push is performed
