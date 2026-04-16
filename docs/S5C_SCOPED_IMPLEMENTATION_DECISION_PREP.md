# S5-C Scoped Implementation Decision Prep

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S5-C Scoped Implementation Decision Prep |
| Status | Closed as governed S5-C scoped implementation decision prep baseline |
| Scope | S5-C scoped implementation decision prep only |
| Baseline | S5-POST-MILESTONE-EXTERNAL-INPUT-TRACKER-2026-04-16-001 |
| Predecessor artifacts | docs/S5_POST_MILESTONE_ROUTE_DECISION.md; docs/S5_POST_MILESTONE_EXTERNAL_INPUT_TRACKER.md; docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md; docs/S5C_IMPLEMENTATION_DECISION_CHECKPOINT.md |
| Route | OPEN_S5_C_SCOPED_IMPLEMENTATION_DECISION_PREP |
| primary_implementor | VS Code |
| reviewer | Claude Code |
| reviewer_when_cc_implements | not applicable |
| requires_external_review | true |

`requires_external_review` is true for this draft because this route prepares a future scoped implementation decision over governed S5-C case workflow, lifecycle, and action-request contract clauses. Naming exact S5-C clauses and deciding which may later enter implementation will likely engage case lifecycle semantics, evidence/audit handling, contract clauses, runtime/API behavior planning, or other AI_COLLAB triggers. External review does not authorize implementation and does not replace human go/no-go.

## 2. Goal

This document drafts a governed docs-only S5-C scoped implementation decision prep artifact.

The goal is to map already-governed S5-C planning/contract clauses into candidate future implementation-decision buckets without authorizing implementation.

This document answers:

- Which S5-C governed areas are candidates for later scoped implementation decision?
- Which areas remain HOLD?
- What exact information must a future implementation ticket define before any code/test/runtime/API/schema/dependency change?
- Which boundaries must remain unchanged?
- What external review and human go/no-go requirements apply?

This draft must not authorize implementation.

## 3. Baseline Summary

- Sprint 5 milestone verdict: `SPRINT5_BASELINE_REVIEW_PASS_WITH_EXTERNAL_INPUTS_PENDING`.
- Post-milestone route recommendation: `RECOMMEND_EXTERNAL_INPUT_TRACKER_AND_S5_C_SCOPED_IMPLEMENTATION_DECISION_PREP`.
- External Input Tracker is closed as a governed tracker baseline and does not make any input `READY`.
- This ticket opens only `OPEN_S5_C_SCOPED_IMPLEMENTATION_DECISION_PREP`.
- S5-A external pilot inputs remain `NOT_READY` / `UNKNOWN`.
- External pilot execution remains unauthorized.
- Real customer/operator sign-off remains unauthorized.
- S5-B remains `PASS_AND_PARK`.
- S5-D remains `PASS_AND_PARK`.
- S5-C is a governed planning/contract baseline, not implementation authorization.
- Public close-case endpoint remains `KEEP_DEFERRED`.
- S4-A resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- AI_COLLAB operating model and contract are not changed.

## 4. S5-C-3 Status Correction

- `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md` file header may still say `Status: Draft for review`.
- `docs/HANDOFF.md`, `releases/release_manifest.json`, and later S5-C / Sprint 5 governance records are the controlling evidence that S5-C-3 is a governed contract/planning artifact.
- Treat the header mismatch as documentation hygiene only, not an unmet precondition.
- This draft does not modify S5-C-3.
- S5-C-3 alone does not authorize implementation.

## 5. Fixed S5-C Scoped Decision Risks

Each risk below is a HOLD trigger if it appears, becomes implied, or is treated as satisfied by this draft:

- scoped decision prep mistaken for implementation authorization
- S5-C PASS mistaken for runtime authorization
- public close-case endpoint `KEEP_DEFERRED` weakened
- exact clauses skipped or left ambiguous
- exact files skipped or left ambiguous
- exact behavior changes skipped or left ambiguous
- exact tests / test commands skipped or left ambiguous
- acceptance criteria skipped or left ambiguous
- audit/evidence behavior skipped or left ambiguous
- redaction/secret/evidence handling boundaries skipped or frozen without review
- case lifecycle semantics changed or frozen without external review
- action request approval/denial/cancellation semantics changed without external review
- new persisted lifecycle/action-request statuses introduced
- destructive response automation introduced
- RBAC / ticketing / workflow engine scope introduced
- runtime/API/schema/test/dependency changes appear in this draft
- fixture file creation or modification appears
- external pilot execution appears
- real customer/operator sign-off appears
- real SIEM/EDR/source/telemetry access appears
- credentials/tokens/API keys/auth headers/cookies appear
- raw logs/screenshots/exports/payloads/event bodies/customer evidence appear
- S5-B or S5-D reopen appears
- S4-A resolver order changes
- AI_COLLAB operating model or contract changes
- external review bypass or human go/no-go replacement

## 6. Candidate S5-C Decision Areas

Allowed bucket values:

- `CANDIDATE_FOR_LATER_SCOPED_DECISION`
- `HOLD_PUBLIC_ENDPOINT`
- `HOLD_EXTERNAL_INPUT`
- `HOLD_POLICY_OR_EXTERNAL_REVIEW`
- `HOLD_OUT_OF_SCOPE`
- `NOT_APPLICABLE`

Forbidden bucket/status values for this matrix: `READY`, `APPROVED`, `IMPLEMENTABLE`, `PILOT_READY`, `PRODUCTION_READY`, and `AUTHORIZED_FOR_IMPLEMENTATION`.

| S5-C governed area | Governed source artifact(s) | Current governed status | Candidate implementation-decision bucket | Required future implementation-ticket details | requires_external_review implication | HOLD triggers | Non-authorization note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| durable case lifecycle baseline | `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md`; S4-C lifecycle baselines referenced by S5-C | Governed planning/contract baseline; durable lifecycle guarantees inherited | `CANDIDATE_FOR_LATER_SCOPED_DECISION` | exact lifecycle clause, exact files, exact behavior delta, closed-case safety expectations, tests, rollback/HOLD criteria | true if lifecycle semantics are frozen, changed, or mapped to runtime/API behavior | new lifecycle states, weakened closed-case safety, ambiguous files/tests, or runtime work from this draft | does not change lifecycle behavior or authorize implementation |
| case close reason / lifecycle semantics | `docs/S5C2_CLOSE_REASON_AND_LIFECYCLE_SEMANTICS.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Governed close reason/lifecycle vocabulary baseline | `CANDIDATE_FOR_LATER_SCOPED_DECISION` | exact close reason clause, exact persistence/API impact, exact tests, acceptance criteria, audit expectations | true if semantics are frozen into implementation scope or changed | new close reasons, new persisted states, ambiguous close behavior, or public endpoint scope creep | does not freeze new semantics or alter close behavior |
| action request approval semantics | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Governed contract/planning semantics; approval remains non-destructive workflow data | `CANDIDATE_FOR_LATER_SCOPED_DECISION` | exact approval clause, exact files, exact behavior under test, audit entry expectations, no destructive execution boundary | true if approval semantics are mapped into runtime/test behavior or changed | destructive execution, external action, new statuses, or approval becoming real sign-off | does not authorize approval implementation or response execution |
| action request denial / rejection semantics | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Governed contract/planning semantics; denial/rejection preserves evidence and audit | `CANDIDATE_FOR_LATER_SCOPED_DECISION` | exact denial/rejection clause, exact tests, evidence/audit preservation expectations, no deletion behavior | true if denial/rejection semantics are mapped into runtime/test behavior or changed | evidence deletion, audit erasure, new status vocabulary, or ambiguous rejection behavior | does not authorize denial/rejection implementation |
| action request cancellation / withdrawal semantics | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Governed contract/planning semantics; cancellation/withdrawal is non-destructive | `CANDIDATE_FOR_LATER_SCOPED_DECISION` | exact cancellation/withdrawal clause, exact current/proposed behavior, test command, audit preservation expectations | true if cancellation semantics are mapped into runtime/test behavior or changed | prior request history erased, evidence removed, or broader withdrawal workflow invented | does not authorize cancellation/withdrawal implementation |
| audit history / decision traceability | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Governed requirement for ordered, durable, append-safe, replayable audit/decision traces | `CANDIDATE_FOR_LATER_SCOPED_DECISION` | exact audit clauses, exact audit fields if any, retention/non-retention boundary, tests, redaction/secret check | true if audit/evidence behavior is changed, frozen, or mapped into runtime behavior | mutable audit, oral-only evidence, raw external evidence, retention approval, or ambiguous replay expectation | does not authorize audit storage changes or evidence retention |
| pending action request behavior around close-case workflows | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` | Governed as a required future decision if close-case endpoint work is ever scoped | `CANDIDATE_FOR_LATER_SCOPED_DECISION` | exact pending-request clause, exact close-case relationship, exact HOLD behavior, tests, acceptance criteria | true if pending-request behavior affects lifecycle/API semantics or endpoint planning | endpoint proceeds while pending behavior is ambiguous or S5-C-3 is bypassed | does not authorize endpoint work or pending-request runtime behavior |
| closed-case safety / immutability boundary | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Governed inherited safety boundary; closed cases must not accept unsafe mutation | `CANDIDATE_FOR_LATER_SCOPED_DECISION` | exact closed-case safety clause, exact files/tests, expected failure behavior, rollback/HOLD criteria | true if closed-case safety is frozen into new behavior or changed | closed-case protections weakened, post-close mutation allowed, or lifecycle states changed | does not authorize code/test/runtime changes |
| evidence/audit note handling | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md` | Governed as redacted, non-sensitive, append-safe decision context only | `HOLD_POLICY_OR_EXTERNAL_REVIEW` | exact evidence/audit note boundary, non-retention rule, redaction/secret handling, tests if later scoped | true if evidence retention, redaction, audit storage, or real evidence handling changes | raw evidence, logs, screenshots, exports, payloads, event bodies, customer evidence, or retention appear | does not authorize evidence retention or raw evidence handling |
| redaction / secret handling boundary | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; S5-A/S5-D redaction boundaries | Governed as no secrets or unredacted customer/operator payloads | `HOLD_POLICY_OR_EXTERNAL_REVIEW` | exact redaction/secret check, forbidden data categories, non-retention boundary, reviewer ownership | true if redaction/secret/evidence handling boundaries are frozen or changed | credentials, tokens, API keys, auth headers, cookies, raw payloads, or policy freeze appear | does not authorize redaction policy freeze or secrets handling implementation |
| public close-case HTTP endpoint | `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | `KEEP_DEFERRED`; endpoint implementation remains deferred | `HOLD_PUBLIC_ENDPOINT` | a later explicit endpoint ticket would need product need, exact method/path/request/response/error model, audit behavior, pending action behavior, tests, and review scope | true if endpoint behavior is opened, frozen, or mapped to runtime/API implementation | `KEEP_DEFERRED` weakened, endpoint implementation selected, method/path/payload frozen, or runtime/API work appears | this draft does not authorize endpoint implementation |
| destructive response automation / response execution | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Explicitly outside S5-C scope; approval is non-destructive workflow data | `HOLD_OUT_OF_SCOPE` | not applicable unless a later product/governance route explicitly opens a separate response-automation decision | true if destructive response semantics or external action behavior are proposed | destructive execution, external SIEM/EDR/source action, automated response, or ticket/action execution appears | no destructive response automation is authorized |
| RBAC / ticketing / workflow engine integration | `docs/S5C3_ACTION_REQUEST_APPROVAL_DENIAL_CONTRACT.md`; `docs/S5C4_PUBLIC_CLOSE_CASE_HTTP_ENDPOINT_DECISION.md`; `docs/S5C5_CASE_WORKFLOW_REVIEW_PASS.md` | Explicitly outside S5-C planning scope unless later governed route opens it | `HOLD_OUT_OF_SCOPE` | not applicable unless a later governed route explicitly opens RBAC, ticketing, or workflow engine scope | true if authorization, integration, multi-tenant ownership, or workflow-engine semantics are proposed | RBAC, ticketing, workflow engine, external ticket creation, or permission infrastructure appears | remains out of scope unless a later governed route explicitly opens it |
| external pilot / customer evidence behavior | `docs/S5_POST_MILESTONE_EXTERNAL_INPUT_TRACKER.md`; `docs/S5_SPRINT5_MILESTONE_REVIEW_PASS.md`; S5-A external pilot docs | External pilot inputs remain `NOT_READY` / `UNKNOWN`; real customer/operator evidence not accepted | `HOLD_EXTERNAL_INPUT` | future ticket must state external pilot execution, real sign-off, real access, and evidence retention remain unauthorized | true if real external evidence/access, pilot readiness, sign-off, or retention is implicated | external pilot readiness, customer/operator evidence, real sign-off, live access, credentials, or raw payloads appear | no real customer/operator evidence is accepted |

## 7. Future Implementation Ticket Requirements

Any future implementation ticket must define the following before code/test/runtime/API/schema/dependency work can begin:

- exact governed S5-C clause(s)
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
- public close-case endpoint status, preserving `KEEP_DEFERRED` unless a later explicit endpoint ticket opens it
- external pilot execution remains unauthorized
- real customer/operator sign-off remains unauthorized
- real external-system access remains unauthorized
- `requires_external_review` decision and rationale
- human go/no-go requirement
- reviewer / `reviewer_when_cc_implements` assignment

If any of these requirements are missing, the future implementation ticket must HOLD.

## 8. Relationship To External Input Tracker

- `docs/S5_POST_MILESTONE_EXTERNAL_INPUT_TRACKER.md` remains the governed tracker baseline.
- That tracker does not make any external input `READY`.
- This S5-C prep may not consume real customer/operator evidence, raw payloads, logs, screenshots, exports, credentials, tokens, or external-system access.
- If later external inputs reveal a source/input gap, S5-B reopen requires an explicit reopen decision.
- If later external inputs reveal a telemetry gap, S5-D reopen requires an explicit reopen decision.
- This draft does not reopen S5-B or S5-D.

## 9. Non-Authorization

This draft does not authorize:

- implementation
- runtime/API/schema/test/dependency changes
- fixture file creation or modification
- S5-C runtime work
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

## 10. HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| any implementation instruction appears | this document is decision prep only |
| runtime/API/schema/test/dependency or fixture changes appear | changes require a later governed implementation ticket |
| exact future implementation ticket requirements are skipped | future scope must name exact clauses, files, behavior, tests, acceptance, evidence/redaction boundaries, review, and go/no-go |
| any area is marked `READY`, `APPROVED`, `IMPLEMENTABLE`, or `AUTHORIZED_FOR_IMPLEMENTATION` | this prep artifact only maps candidate decision buckets |
| public close-case endpoint `KEEP_DEFERRED` is weakened | endpoint work remains deferred |
| destructive response automation appears | destructive response remains outside S5-C scoped prep |
| RBAC / ticketing / workflow engine integration appears | these are out of scope unless a later governed route explicitly opens them |
| new persisted lifecycle/action-request statuses appear | status changes require separate governed decision and implementation scope |
| external pilot execution/readiness/sign-off appears | external pilot path remains unauthorized and inputs remain non-ready |
| real external-system access appears | live SIEM/EDR/source/telemetry access is outside scope |
| credentials/tokens/API keys/auth headers/cookies/secret material appear | secrets are prohibited in this draft |
| raw evidence, logs, screenshots, exports, payloads, event bodies, or customer/operator evidence appear | this prep may not consume real evidence |
| evidence retention/redaction/secrets boundary is frozen without external review | boundary freeze is an external-review trigger and is not authorized here |
| S5-B or S5-D reopen appears without explicit reopen decision | both streams remain `PASS_AND_PARK` |
| S4-A resolver priority changes | resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases` |
| AI_COLLAB operating model or contract changes appear | AI_COLLAB files are not part of this task |
| external review is skipped or treated as replacing human go/no-go | external review is required and human go/no-go remains required |
| HANDOFF or manifest is modified during draft-only stage | this draft may create only this new docs file |
| protected untracked files are touched | protected untracked files must remain untouched |

## 11. Preliminary Recommendation

`PRELIMINARY_RECOMMENDATION_READY_FOR_S5_C_SCOPED_IMPLEMENTATION_DECISION`

Meaning:

- this prep artifact may be reviewed and, if accepted, closed as a governed decision-prep baseline
- it permits a later separate S5-C Scoped Implementation Decision ticket to be drafted
- that later ticket must decide exact implementation scope and may still HOLD all implementation
- that later ticket must define exact clauses, files, behavior changes, tests, acceptance criteria, evidence/redaction/secret boundaries, rollback/HOLD criteria, external review decision, and human go/no-go

Non-meaning:

- does not authorize implementation
- does not authorize code/test/runtime/API/schema/dependency changes
- does not authorize public close-case endpoint work
- does not authorize external pilot execution or readiness
- does not authorize real customer/operator sign-off or real external-system access
- does not reopen S5-B or S5-D
- does not change S4-A resolver order
- does not change AI_COLLAB
- does not create an automatic implementation ticket

## 12. Acceptance Criteria

This draft is acceptable if:

- exactly one new docs-only file is created
- `requires_external_review` is true with rationale
- baseline summary is accurate
- S5-C-3 status correction is included and does not modify S5-C-3
- candidate S5-C decision area matrix includes all required rows
- public close-case endpoint remains `KEEP_DEFERRED`
- no area is marked `READY` / `APPROVED` / `IMPLEMENTABLE` / `AUTHORIZED_FOR_IMPLEMENTATION`
- future implementation ticket requirements are listed
- External Input Tracker remains non-ready and is not treated as evidence source
- no implementation, runtime/API/schema/test/dependency, or fixture changes are authorized
- no external pilot execution, sign-off, real access, credentials, raw evidence, or evidence retention is authorized
- S5-B and S5-D remain `PASS_AND_PARK` unless later explicit reopen decision
- S4-A resolver order remains unchanged
- AI_COLLAB files are not modified
- HANDOFF and manifest are not modified in this draft stage
- full gate is not run
- no staging, commit, or push is performed
