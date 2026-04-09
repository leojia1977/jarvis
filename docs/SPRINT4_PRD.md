# Sprint 4 PRD

## Document Control
- Product: `SecuPilot`
- Source of truth: `D:\产品设计\New folder`
- Snapshot baseline: `S4-PLAN-2026-04-09-001`
- Primary owners:
  - Product and review decisions: `Claude`
  - Implementation and release: `Codex`

## Background
Sprint 3 delivered four major outcomes:
- `S3-A` turned the orchestrator into a stable runtime boundary
- `S3-B` froze the analyst case contract and Jarvis case embedding
- `S3-C` completed SIEM adapterization, vendor hardening, and replay validation
- `S3-D` closed the release, review-pack, wrapper, runtime operability, and governance loops

SecuPilot is now a governed, reproducible investigation service with a stable case contract. The biggest remaining gaps are not release discipline or case formatting anymore. They are:
- static data for T1/T4/T5 still comes from local governed files instead of explicit source adapters
- T3 still lacks a production EDR ingestion path equal to the SIEM path
- investigations are still request-time outputs rather than durable analyst work objects
- pilot deployment and operator runbooks are not yet frozen for a real field trial

## Problem Statement
SecuPilot can now produce governed investigation cases, but it still lacks the next layer required for a pilot:
- a normalized source layer for asset inventory, baselines, topology, and intel-seed data
- a production-grade EDR contract for process-event ingestion
- a persistent case lifecycle that analysts and managers can retrieve, review, approve, and audit
- a pilot-readiness package for staging environments, secrets, health semantics, and operator procedures

## Sprint 4 Goal
Deliver a pilot-ready Sprint 4 baseline that:
- replaces remaining local-static-data shortcuts with explicit source contracts
- productionizes EDR ingestion with the same contract discipline already achieved for SIEM
- turns one-shot runtime investigation output into a persistent analyst case lifecycle
- freezes pilot deployment, operator, and release-readiness expectations for a first controlled field trial

## Non-Goals
- autonomous containment or destructive response execution
- enterprise RBAC, tenancy, or organization management
- full frontend or design-system rebuild
- deep vendor optimization for every EDR and SIEM variant
- container orchestration, autoscaling, or multi-region deployment
- replacing the governed release and review workflow built in Sprint 3

## Target Users
- `L1 analyst`: wants retrievable cases, clear current status, and safe action guidance
- `L2 analyst`: wants durable evidence, replayable telemetry contracts, and source-gap visibility
- `SOC manager`: wants approval history, action requests, and auditable case status transitions
- `Security engineer`: wants explicit data-source contracts, deterministic staging validation, and pilot-safe runtime behavior

## Product Principles
1. One case, one durable record.
2. External data must enter through explicit contracts, never hidden file reads.
3. Runtime, case, and source semantics must degrade explicitly, never silently.
4. Pilot readiness means repeatable operator behavior, not just passing developer tests.
5. Claude reviews product risk and scope; Codex changes canonical files and releases.

## Scope

### S4-A Static Data and Identity Source Integration
Replace remaining local-static-data shortcuts with governed source contracts.

In scope:
- asset inventory source contract
- baseline source contract
- threat-intel seed source contract
- topology or knowledge-graph source contract
- canonical host-identity resolution across SIEM, EDR, and blast-radius logic
- cache and refresh semantics for static data adapters

Out of scope:
- bidirectional CMDB synchronization
- autonomous baseline writing or learning
- replacing current algorithms for T1, T4, or T5

Execution note:
- `S4-A-3 Host Identity Resolver` is a hard prerequisite for `S4-B-1 EDR Adapter Contract`.
- Sprint 4 must not freeze production EDR host-identity semantics against legacy string matching before the authoritative resolver is accepted.

### S4-B EDR Telemetry Productionization
Bring T3 onto the same production contract footing that SIEM already has.

In scope:
- `EDRAdapterProtocol`
- production process-event ingestion path
- `TimeRangeSpec` parity between SIEM and EDR
- EDR replay fixtures and replay transport
- T3 degraded and partial-telemetry parity under production-style ingestion

Out of scope:
- raw memory acquisition
- file download or forensic artifact collection
- original full process-tree explorer UX

### S4-C Persistent Case Lifecycle
Turn the runtime case output into a durable analyst work object.

In scope:
- persistent case record schema
- case retrieval and lookup APIs
- status transitions such as `open / in_review / approved / closed`
- non-destructive action-request contract
- audit trail persistence for review, approval, and action-request decisions

Out of scope:
- auto-executed remediation
- ticketing-system bi-directional sync
- enterprise workflow engine

Execution note:
- persistent case work must freeze the storage backend choice before implementation begins
- the chosen backend must be justified against SecuPilot's existing data-sovereignty and audit requirements

### S4-D Pilot Deployment and Operability
Freeze what is needed to run a controlled pilot without inventing full enterprise ops.

In scope:
- environment and secret profile guidance
- staging or pilot deployment checklist
- operator runbooks for common readiness and misconfiguration states
- production smoke checklist using governed adapters and persistent case flow
- release-readiness review for pilot handoff

Out of scope:
- Kubernetes templates
- autoscaling
- on-call platform integrations

Execution note:
- `S4-D-1` and `S4-D-3` may start in parallel with late `S4-A` work because they are documentation and operator-contract heavy
- `S4-D-2`, `S4-D-4`, and `S4-D-5` remain downstream of `S4-A + S4-B + S4-C`

## Functional Requirements

### FR-1 Source Contracts
- All remaining non-telemetry source reads used by T1, T4, and T5 must move behind explicit contracts.
- Host identity resolution must return one normalized structure that can be reused by SIEM, EDR, and blast-radius logic.

### FR-2 EDR Ingestion
- The system must support a production-facing EDR adapter with canonical process-event outputs.
- Production-like EDR fixtures must be replayable without real network access.

### FR-3 Persistent Case Lifecycle
- Every investigation case must be retrievable by `case_id`.
- Case status transitions and action requests must be stored as data, not only implied in runtime output.
- Audit records must preserve who changed status, why, and when.

### FR-4 Pilot Operability
- Operators must be able to tell whether a pilot environment is ready, misconfigured, bootstrapped but degraded, or blocked by missing dependencies.
- The project must define one pilot smoke path that proves source contracts, runtime investigation, and case persistence work together.

### FR-5 Governance Continuity
- Sprint 4 planning and execution must continue to use manifest-backed review packs and governed release gates.
- New Sprint 4 source contracts and case lifecycle docs must be included in governed review artifacts.

## UX Requirements
- A persisted case must preserve the same analyst-first reading order established in Sprint 3.
- Approval and action-request surfaces must remain non-destructive by default.
- Source gaps must distinguish `missing telemetry`, `missing static data`, and `identity ambiguity`.
- Operator docs must explain what action to take for each runtime status without assuming code familiarity.

## Success Metrics
- one governed source contract exists for each static-data domain used by T1/T4/T5
- one governed EDR replay path proves T3 can ingest production-shaped events
- one persisted case can be created, retrieved, reviewed, and closed using only governed APIs
- one pilot checklist can be executed end-to-end without undocumented manual steps
- no Sprint 4 review depends on handwritten file sets outside the generated review pack

## Delivery Definition
Sprint 4 is complete when:
- `S4-A` freezes and implements static-data source contracts plus identity resolution
- `S4-B` delivers a production-facing EDR contract with replay validation
- `S4-C` delivers durable case lifecycle and audit semantics
- `S4-D` delivers pilot-ready operator guidance, release checks, and staging validation

## Risks
- scope creep from “pilot-ready” into full enterprise deployment
- source-contract work expanding into full data-platform redesign
- case persistence introducing schema drift between runtime and stored records
- EDR vendor differences leaking raw fields back into core T3 logic
- operator docs falling out of sync with runtime behavior if not governed like code

## Dependencies
- Sprint 3 governed runtime, case, adapter, and governance baseline
- current `TimeRangeSpec`, `AdapterResult`, and case schema contracts
- current release-manifest and review-pack workflow
- current SIEM replay fixtures as the contract model for EDR replay

## Acceptance Summary By Stream
- `S4-A`: one normalized static-data source layer and one canonical identity resolver
- `S4-B`: one production-grade EDR adapter contract plus replay validation
- `S4-C`: one durable case lifecycle with audit and approval-safe action requests
- `S4-D`: one pilot deployment and operator readiness baseline
