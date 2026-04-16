# Sprint 5 Post-Milestone External Input Tracker

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Sprint 5 Post-Milestone External Input Tracker |
| Status | Closed as governed Sprint 5 post-milestone external input tracker baseline |
| Scope | Sprint 5 post-milestone external input tracker only |
| Baseline | S5-POST-MILESTONE-ROUTE-2026-04-16-001 |
| Predecessor artifact | docs/S5_POST_MILESTONE_ROUTE_DECISION.md |
| Route | OPEN_EXTERNAL_INPUT_TRACKER |
| primary_implementor | VS Code |
| reviewer | Claude Code |
| reviewer_when_cc_implements | not applicable |
| requires_external_review | true |

`requires_external_review` is true because this tracker concerns real external pilot input categories, ownership, channels, timeout/restart criteria, escalation, and HOLD conditions after a milestone route decision. This tracker does not authorize external pilot execution, real customer/operator sign-off, or real evidence retention. It does not replace human go/no-go. External review does not authorize implementation and does not replace human product/governance decision.

## 2. Goal

This document drafts a governed docs-only tracker for the seven external pilot input categories that remain `NOT_READY` / `UNKNOWN` after the Sprint 5 milestone review and post-milestone route decision.

The tracker defines:

- input category
- current status
- owner role / decision owner placeholder
- expected source/channel
- expected artifact or answer shape
- blocker
- timeout/restart criteria
- escalation path
- HOLD triggers
- non-authorization notes

This document must not declare any input as the forbidden status term `READY`.

## 3. Status Vocabulary

Tracker rows may use only these status values:

- `UNKNOWN`
- `NOT_READY`
- `NEEDS_OWNER`
- `NEEDS_DECISION`
- `BLOCKED`
- `NOT_APPLICABLE`

The following terms are forbidden as tracker statuses and may appear only as explicit forbidden-language examples: `READY`, `APPROVED`, `IMPLEMENTABLE`, `PILOT_READY`, `PRODUCTION_READY`, and `PROVIDED`.

## 4. Baseline Summary

- Sprint 5 milestone review pass verdict is `SPRINT5_BASELINE_REVIEW_PASS_WITH_EXTERNAL_INPUTS_PENDING`.
- Post-milestone route decision recommendation is `RECOMMEND_EXTERNAL_INPUT_TRACKER_AND_S5_C_SCOPED_IMPLEMENTATION_DECISION_PREP`.
- This ticket opens only `OPEN_EXTERNAL_INPUT_TRACKER`.
- Route B / S5-C Scoped Implementation Decision Prep remains a separate later ticket.
- S5-A inputs remain `NOT_READY` / `UNKNOWN`.
- S5-B remains `PASS_AND_PARK`.
- S5-D remains `PASS_AND_PARK`.
- S5-C remains parked unless a later scoped implementation decision is explicitly opened.
- The public close-case endpoint remains `KEEP_DEFERRED`.
- S4-A host identity resolver order remains unchanged: `asset_id -> hostname -> fqdn -> ip_address -> aliases`.
- AI_COLLAB operating model and contract are not changed by this tracker.

## 5. Fixed Post-Milestone Risk Checklist

Each item below is a HOLD risk if it becomes authorized or implied by this tracker:

- external pilot execution
- external pilot readiness misread as improved
- real customer/operator sign-off
- real SIEM/EDR/source/telemetry access
- connector credentials / tokens / API keys / auth headers / cookies
- raw telemetry/source payloads, logs, screenshots, exports, event bodies, or customer/operator evidence
- evidence retention or redaction policy freeze
- secrets handling implementation
- runtime/API/schema/test/dependency changes
- fixture file creation or modification
- public close-case endpoint work
- S5-C runtime implementation without scoped decision
- S5-B source contract or identity mapping freeze
- S5-D telemetry schema/normalization/freshness/provenance/redaction/retention freeze
- S4-A host identity handoff bypass or resolver priority change
- AI_COLLAB operating model or contract changes
- automatic next route without human product/governance decision
- reopening S5-B or S5-D without explicit reopen decision

## 6. External Input Tracker Specific Risks

The tracker has its own risk profile because it names external input categories and placeholder ownership. Each item below is a HOLD risk if it becomes authorized, implied, or treated as satisfied:

- tracker mistaken for external pilot decision package
- tracker mistaken for pilot readiness improvement
- owner placeholder mistaken for real sign-off authority
- channel placeholder mistaken for approved external communication
- expected artifact mistaken for approved evidence retention
- timeout/restart criteria mistaken for automatic escalation into pilot execution
- escalation path mistaken for go/no-go approval
- `UNKNOWN` / `NOT_READY` input silently promoted to the forbidden status term `READY`
- real evidence, credentials, screenshots, logs, exports, or raw payloads introduced as tracker evidence
- redaction/retention discussion becoming policy freeze
- new source/input coverage gap silently reopening S5-B
- new telemetry coverage/normalization gap silently reopening S5-D
- S5-C implementation prep or runtime work being bundled into this tracker
- human go/no-go being replaced by tracker completion

## 7. Seven-Input Tracker Matrix

| Input category | Current status | Owner role placeholder | Expected source/channel | Expected artifact / answer shape | Current blocker | Timeout / restart criteria | Escalation path | HOLD triggers | Non-authorization notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pilot scope | `UNKNOWN` | product/governance decision owner placeholder | governed planning discussion or non-sensitive decision record | future decision record describing bounded pilot scope questions and exclusions | no governed external pilot scope answer exists | if no answer is recorded by the next review window, restart as human product/governance route review | human product/governance decision, not pilot start | any scope text implies external pilot execution, real access, real sign-off, or forbidden status promotion | does not define pilot scope, start a pilot, or improve external pilot readiness |
| participating roles | `NEEDS_OWNER` | product/governance decision owner placeholder | governed planning discussion or non-sensitive role decision record | future answer naming role categories only, without real sign-off authority | no governed participant role answer exists | if no owner is assigned by the next review window, restart as ownership decision checkpoint | human product/governance decision, not operational approval | owner placeholder becomes real customer/operator sign-off authority or pilot go/no-go authority | does not name real participants, approve sign-off, or authorize communication channels |
| environment boundary/access | `NOT_READY` | product/governance decision owner placeholder | governed planning discussion or non-sensitive environment boundary answer | future boundary decision record describing access constraints without credentials or system details | no governed access boundary answer exists and real access is unauthorized | if environment boundary remains undefined, continue HOLD and restart route review before any external input use | human product/governance decision, not external-system access | live SIEM/EDR/source/telemetry access, credentials, tokens, API keys, auth headers, cookies, screenshots, logs, exports, event bodies, or customer data appear | does not authorize live access, connector setup, external-system testing, or real evidence collection |
| evidence retention policy | `NEEDS_DECISION` | product/governance decision owner placeholder | governed planning discussion or non-sensitive retention boundary decision record | future decision record describing whether a later policy path is needed, without retaining evidence | no governed evidence retention approval exists | if retention boundary remains unresolved, keep external inputs blocked and escalate for product/governance decision | human product/governance decision with external-review implications, not evidence storage | retention, storage, replay, deletion, expiry, evidence-pack behavior, raw evidence, logs, screenshots, exports, event bodies, or payloads are approved or frozen | does not authorize evidence retention, evidence-pack behavior, storage, replay, deletion, or expiry policy |
| redaction approval | `NEEDS_DECISION` | product/governance decision owner placeholder | governed planning discussion or non-sensitive redaction boundary decision record | future decision record describing redaction questions and review needs, without redaction policy freeze | no governed redaction approval exists | if redaction remains unresolved, keep external evidence use blocked and restart as product/governance route review | human product/governance decision with external-review implications, not evidence handling | redaction wording becomes policy freeze or allows raw payload, log, screenshot, export, event body, or customer/operator evidence retention | does not approve redaction policy, secrets handling, raw evidence handling, or real evidence retention |
| go/no-go authority | `NEEDS_OWNER` | product/governance decision owner placeholder | governed planning discussion or non-sensitive authority decision record | future answer identifying decision authority process without real sign-off | no governed go/no-go authority answer exists | if authority is not assigned by the next review window, keep pilot execution blocked and restart ownership decision | human product/governance decision, not automatic approval | tracker completion is treated as go/no-go, real customer/operator sign-off, or external pilot authorization | does not grant go/no-go authority, replace human decision, or authorize pilot execution |
| rollback/hold authority | `NEEDS_OWNER` | product/governance decision owner placeholder | governed planning discussion or non-sensitive rollback/HOLD decision record | future answer describing decision path for HOLD/rollback authority without operational execution | no governed rollback/HOLD authority answer exists | if authority is not assigned by the next review window, keep external pilot path blocked and restart authority review | human product/governance decision, not operational rollback execution | rollback/HOLD language becomes operational runbook, runtime change, public close-case endpoint work, or pilot execution control | does not create rollback implementation, runtime behavior, endpoint behavior, or automatic HOLD/rollback authority |

## 8. Relationship To Route B

S5-C Scoped Implementation Decision Prep remains a separate later route. This External Input Tracker does not open Route B.

This tracker may inform Route B only through governed, non-sensitive, non-evidence decision records. Route B must have its own sanity check, human confirmation, draft, Claude Code review, and closeout. Route B must re-evaluate `requires_external_review` in its own ticket. The practical expectation is that Route B will likely require external review once exact S5-C clauses are named, but that is not decided by this tracker.

## 9. Non-Authorization

This tracker does not authorize:

- external pilot execution
- external pilot readiness
- real customer/operator sign-off
- live SIEM/EDR/source/telemetry access
- connector credentials, tokens, API keys, auth headers, cookies, or secret material
- raw telemetry/source payloads, logs, screenshots, exports, event bodies, or customer/operator evidence
- evidence retention, storage, replay, deletion, expiry, or evidence-pack behavior
- redaction policy freeze
- secrets handling implementation
- runtime/API/schema/test/dependency changes
- fixture file creation or modification
- S5-C runtime implementation
- public close-case endpoint work
- S5-B reopen
- S5-D reopen
- S5-B source contract or identity mapping freeze
- S5-D telemetry normalization/freshness/provenance/redaction/retention freeze
- S4-A host identity authority or resolver order changes
- AI_COLLAB operating model or contract changes
- external review bypass
- human go/no-go replacement
- automatic next route

## 10. HOLD Conditions

| HOLD condition | Why it holds |
| --- | --- |
| any input is declared `READY`, `APPROVED`, `PROVIDED`, `PILOT_READY`, or complete | the tracker is allowed to record only non-ready external input states |
| tracker becomes external pilot decision package | this file is a tracker only and must not decide pilot launch |
| tracker starts, schedules, or implies external pilot execution | external pilot execution remains unauthorized |
| real customer/operator sign-off appears | real sign-off remains unauthorized |
| live external-system access appears | live SIEM/EDR/source/telemetry access remains unauthorized |
| credentials, tokens, API keys, auth headers, cookies, or secret material appear | secret material is outside tracker scope |
| raw evidence, payloads, logs, screenshots, exports, or event bodies appear | real evidence collection and retention are not authorized |
| evidence retention, redaction, deletion, expiry, storage, replay, or evidence-pack behavior is approved or frozen | this tracker must not become a policy or evidence-retention decision |
| runtime/API/schema/test/dependency or fixture changes appear | this is docs-only and must not alter implementation surfaces |
| public close-case endpoint work appears or `KEEP_DEFERRED` is weakened | public close-case endpoint remains deferred |
| S5-C implementation prep or runtime implementation is bundled into this tracker | Route B must remain a separate later ticket |
| S5-B or S5-D is reopened without explicit reopen decision | both streams remain `PASS_AND_PARK` unless separately governed |
| S4-A resolver priority changes | resolver order remains `asset_id -> hostname -> fqdn -> ip_address -> aliases` |
| AI_COLLAB operating model or contract changes appear | AI_COLLAB files are not part of this task |
| external review is skipped or treated as replacing human go/no-go | external review is required and does not replace human product/governance decision |
| HANDOFF or manifest is modified during draft-only stage | this draft may create only this new tracker file |
| protected untracked files are touched | protected untracked files must remain untouched |

## 11. Preliminary Recommendation

`PRELIMINARY_RECOMMENDATION_KEEP_TRACKER_OPEN_AND_PREPARE_SEPARATE_S5_C_SCOPED_IMPLEMENTATION_DECISION_PREP`

Meaning:

- the tracker can be reviewed and, if accepted, closed as a governed tracking baseline
- Route B remains separately recommended by the prior post-milestone route decision
- Route B must be opened in a separate later ticket
- this tracker does not itself start Route B

Non-meaning:

- does not declare external inputs ready
- does not open an external pilot decision package
- does not authorize pilot execution
- does not authorize implementation
- does not authorize external evidence retention
- does not reopen S5-B or S5-D
- does not change S5-C runtime scope
- does not change public close-case endpoint status
- does not change S4-A resolver order
- does not change AI_COLLAB

## 12. Acceptance Criteria

This draft is acceptable if:

- exactly one new docs-only file is created
- `requires_external_review` is true with rationale
- all seven external input categories are present
- all seven inputs remain `NOT_READY` / `UNKNOWN` or equivalent non-ready statuses
- no input is declared `READY` / `APPROVED` / `PROVIDED` / `PILOT_READY`
- tracker is not an external pilot decision package
- tracker does not authorize pilot execution or sign-off
- tracker does not request or retain credentials, raw evidence, logs, screenshots, exports, payloads, event bodies, or customer/operator evidence
- tracker does not freeze evidence retention, redaction, secrets handling, S5-B source contracts, S5-D telemetry semantics, or S5-C runtime behavior
- S5-C Route B is kept as a separate later ticket
- public close-case endpoint remains `KEEP_DEFERRED`
- S4-A resolver order remains unchanged
- AI_COLLAB files are not modified
- HANDOFF and manifest are not modified in this draft stage
- full gate is not run
- no staging, commit, or push is performed
