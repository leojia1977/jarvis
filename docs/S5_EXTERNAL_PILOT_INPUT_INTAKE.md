# S5 External Pilot Input Intake

## Document Control
- Status: `draft for review`
- Baseline: `S5-MIDPOINT-2026-04-13-001`
- Source of truth: `D:\产品设计\New folder`
- Purpose: external pilot input intake
- Non-goals:
  - not external pilot execution
  - not external pilot authorization
  - not external pilot decision package
  - not real customer/operator sign-off
  - not runtime/test changes
  - not real SIEM/EDR/source access

## Goal
Define the seven required input categories that must be completed before an external pilot decision package can be drafted.

This document is an intake and checklist artifact only. It does not authorize external pilot execution, start pilot work, collect real pilot evidence, or create the external pilot decision package.

## Current Baseline
- `S5-A Controlled Pilot Preparation` is closed as a governed preparation package.
- `S5-E AI Collaboration Operating Model` is governed as collaboration workflow guidance.
- `docs/S5_MIDPOINT_DECISION.md` selected this intake as the next safe planning step before choosing external pilot package versus S5-C versus discovery.
- External pilot execution remains unauthorized.
- Product/governance must complete or explicitly accept the required inputs before any external pilot decision package can be drafted.

## Seven Input Categories

### Pilot Scope
- Definition: the bounded purpose, duration, environment, systems, user group, success criteria, and non-goals for a future external pilot.
- Required decisions:
  - what the pilot is intended to prove
  - what user or operator activities are in scope
  - what systems or data contexts are excluded
  - what would count as pilot stop, hold, or completion
- Required evidence or artifact: a scoped pilot brief or product/governance decision note.
- Owner to be decided: product/governance owner.
- PASS condition: scope is explicit enough to determine whether a proposed activity is inside or outside the external pilot.
- HOLD condition: scope is vague, oral-only, or implies unrestricted production use.
- Notes / examples: acceptable scope may reference controlled analyst/manager review activity; it must not imply destructive response execution or live source expansion without separate approval.

### Participating Roles
- Definition: the people or role classes expected to participate in the external pilot and their decision, review, execution, or observation responsibilities.
- Required decisions:
  - which roles participate
  - who can review pilot evidence
  - who can approve go/no-go or rollback/hold decisions
  - whether any external operator or customer-like role is included
- Required evidence or artifact: role roster, role matrix, or product/governance approval note.
- Owner to be decided: product/governance owner with pilot operations input.
- PASS condition: each participating role has an explicit responsibility and authority boundary.
- HOLD condition: participants are unnamed, authority is unclear, or role design drifts into enterprise RBAC, tenancy, ticketing, or workflow-engine scope.
- Notes / examples: role labels may remain simple and pilot-local; this intake does not create enterprise access-control design.

### Environment And Access Boundary
- Definition: the approved environment, network exposure, access method, host configuration, data boundary, and real-system connection boundary for any future pilot.
- Required decisions:
  - where the pilot may run
  - whether remote analyst/manager access is expected
  - whether `server_host` must move beyond loopback for approved remote access
  - whether any real SIEM, EDR, or source-system access is allowed
  - what access is explicitly prohibited
- Required evidence or artifact: environment/access boundary note, approved access diagram, or security/governance decision record.
- Owner to be decided: product/governance owner with engineering/security input.
- PASS condition: environment and access boundaries are explicit enough to prevent accidental real system access or loopback-only remote access assumptions.
- HOLD condition: the plan requires real SIEM/EDR/source access without approval, leaves remote access ambiguous, or treats loopback-only access as acceptable for remote pilot participation.
- Notes / examples: `127.0.0.1` remains a readiness warning for remote analyst/manager access; this intake does not modify runtime configuration.

### Evidence Retention Policy
- Definition: what external pilot records may be retained, where they may be stored, who may review them, and how long they may be kept.
- Required decisions:
  - which evidence classes may be retained
  - storage location and access limits
  - retention duration
  - deletion or archive expectations
  - whether generated artifacts become governed repo inputs
- Required evidence or artifact: retention policy note or product/security approval record.
- Owner to be decided: product/governance owner with security/privacy input.
- PASS condition: retention expectations are explicit before any real pilot evidence is collected.
- HOLD condition: pilot evidence would be collected without retention limits, storage rules, or access boundaries.
- Notes / examples: dry-run evidence rules from S5-A do not automatically authorize retention of real customer/operator pilot records.

### Redaction Approval For Real Pilot Records
- Definition: approval of the redaction rules that will apply to real pilot records, distinct from dry-run evidence and operator escalation triage material.
- Required decisions:
  - which fields must be omitted
  - which fields may be recorded as names only
  - whether case identifiers are acceptable operational identifiers
  - how request/response bodies, logs, and vendor payloads are handled
  - who approves redaction sufficiency
- Required evidence or artifact: redaction approval note that references, but does not replace, S5-A-3 and S4-D-3 / `RELEASE_PROCESS` boundaries.
- Owner to be decided: product/governance owner with security/privacy review.
- PASS condition: real pilot record redaction rules are explicitly approved and compatible with existing S5-A-3 and S4-D-3 / `RELEASE_PROCESS` boundaries.
- HOLD condition: the plan would retain secret values, auth material, raw credentials, unredacted sensitive payloads, or real customer-identifying data without approval.
- Notes / examples: acceptable intake evidence may record missing secret names or field names, never secret values.

### Go/No-Go Authority
- Definition: the authority that can approve or reject starting an external pilot after reviewing the decision package.
- Required decisions:
  - who has final go/no-go authority
  - what evidence they must review
  - whether approval must be written in a governed artifact
  - what conditions force `NO-GO`
- Required evidence or artifact: go/no-go authority assignment or approval-path decision record.
- Owner to be decided: product/governance owner.
- PASS condition: final pilot-start authority is named by role or person and can make an explicit written decision.
- HOLD condition: pilot start could be inferred from S5-A PASS, oral approval, chat-only context, or incomplete authority assignment.
- Notes / examples: S5-A sign-off readiness supports decision-making; it does not grant go authority.

### Rollback/Hold Authority
- Definition: the authority and criteria for pausing, holding, rolling back, or stopping an external pilot once issues appear.
- Required decisions:
  - who can invoke hold or rollback
  - what findings trigger hold
  - what evidence is needed to resume
  - how redaction or access violations are handled
  - how unresolved P1/P2 ambiguity is escalated
- Required evidence or artifact: rollback/hold authority record or pilot stop/hold criteria note.
- Owner to be decided: product/governance owner with operator/security input.
- PASS condition: hold and rollback authority exists before any external pilot start is considered.
- HOLD condition: no one can clearly stop the pilot, or stop conditions depend on oral knowledge or post-hoc interpretation.
- Notes / examples: hold triggers should include unapproved real system access, ungoverned evidence collection, secret exposure, S4-A identity authority drift, and S4-D operator boundary drift.

## Intake Matrix

| Category | Required input | Current status | In-repo evidence allowed | External decision required | HOLD trigger |
| --- | --- | --- | --- | --- | --- |
| Pilot scope | scoped pilot brief or product/governance decision note | `UNKNOWN` | draft scope checklist, non-goal list, links to S5-A / midpoint records | Yes | scope is oral-only, vague, or implies unrestricted production use |
| Participating roles | role roster, role matrix, or role approval note | `UNKNOWN` | role responsibility checklist with non-sensitive names or role labels | Yes | roles or authority are unclear, or role design drifts into RBAC/ticketing/workflow-engine scope |
| Environment and access boundary | approved environment/access boundary note | `UNKNOWN` | environment boundary checklist, loopback warning, prohibited access list | Yes | real SIEM/EDR/source access or remote access assumptions are ambiguous |
| Evidence retention policy | retention policy note or security/privacy approval | `UNKNOWN` | retention decision checklist without real pilot records | Yes | evidence would be collected without retention, storage, or access limits |
| Redaction approval for real pilot records | redaction approval note | `UNKNOWN` | redaction checklist referencing S5-A-3 and S4-D-3 / `RELEASE_PROCESS` | Yes | secret values, auth material, raw credentials, or unredacted sensitive payloads would be retained |
| Go/no-go authority | written authority assignment or approval path | `UNKNOWN` | authority checklist or decision-record placeholder | Yes | pilot start could be inferred from S5-A PASS, oral approval, or chat-only context |
| Rollback/hold authority | rollback/hold authority record or stop criteria | `UNKNOWN` | stop/hold criteria checklist and owner placeholder | Yes | no clear stop authority or hold criteria exist before pilot start |

## External Pilot Package Readiness
- `READY`: all seven categories are `PROVIDED` or explicitly accepted by product/governance.
- `HOLD`: any category is `UNKNOWN` or `MISSING` and the plan tries to proceed to an external pilot decision package anyway.
- `NEEDS_DECISION`: a category needs owner, product, governance, security, privacy, or operator confirmation before it can be marked complete.

The project should not draft an external pilot decision package until this intake can show that every category is either complete or explicitly accepted by product/governance.

## Boundary Rules
- This intake does not authorize external pilot execution.
- No real SIEM/EDR/source connection is allowed by this intake.
- No real customer/operator sign-off is created by this intake.
- No secret values or raw sensitive evidence should be recorded.
- Any later real pilot evidence must follow separately approved redaction rules.
- This intake does not change S5-A, S5-E, S4-A identity authority, S4-D operator readiness, runtime behavior, tests, release process, manifest, review pack, or full gate requirements.

## Next Step Logic
- If all seven inputs are complete: proceed to draft an external pilot decision package.
- If inputs are incomplete but product explicitly wants case workflow hardening: proceed to S5-C planning.
- If source or telemetry samples become available: proceed to S5-B/S5-D discovery.
- If inputs are incomplete and no alternate product decision exists: keep collecting inputs.

## Acceptance
This intake draft is complete when:
- all seven external pilot input categories are defined
- each category has a PASS and HOLD condition
- current status is explicit and does not imply provided input where none exists
- external pilot execution remains unauthorized
- no runtime, test, external system, or real pilot evidence work is started
