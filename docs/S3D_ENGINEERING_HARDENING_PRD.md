# S3-D Engineering Hardening PRD

## Document Control
- Product: `SecuPilot`
- Source of truth: `D:\产品设计\New folder`
- Planning baseline: `S3-C-2026-04-09-006`
- Stream owner:
  - Product and review decisions: `Claude`
  - Implementation and release: `Codex`

## Background
Sprint 3 `S3-A` to `S3-C` have now delivered:
- a runnable runtime boundary
- a frozen case view contract
- governed degraded semantics
- a normalized SIEM adapter contract
- hardened vendor profiles
- offline vendor replay fixtures

The remaining gap is no longer core investigation logic. The gap is engineering hardening: repeatable release gates, cleaner repo boundaries, safer operability, and lower handoff friction between runtime, tests, release artifacts, Claude, and Codex.

## Problem Statement
SecuPilot now works as a governed investigation service, but it still carries engineering debt that will slow down future delivery if left untreated:
- release gates still rely on a partially manual workflow
- compatibility wrappers and dual entry paths still increase maintenance cost
- runtime observability is not yet strong enough for production-like troubleshooting
- adapter and release governance exist, but are not yet reduced to a minimal, repeatable operating model

## Goal
Deliver an `S3-D` hardening baseline that makes SecuPilot easier to ship, review, operate, and evolve without reopening source-of-truth drift.

## Non-Goals
- no new investigation algorithms
- no vendor auth flows beyond current adapter scope
- no full container platform or cloud deployment stack
- no frontend design overhaul
- no multi-tenant admin or RBAC work

## Users
- `Security engineer`: wants deterministic setup, release, and rollback
- `SOC platform engineer`: wants runtime visibility and explicit dependency health
- `Reviewer (Claude)`: wants a stable, complete review package
- `Implementation owner (Codex)`: wants one canonical repo path, one release path, one test gate

## Engineering Principles
1. One runnable truth, one release path.
2. A release gate must be scriptable before it is considered real.
3. Compatibility is temporary and must have retirement criteria.
4. Operational states must be observable, not inferred.
5. Review artifacts must be complete enough to reproduce decisions.

## Scope

### S3-D-1 CI and Release Gate Hardening
Turn the current local release flow into a deterministic engineering gate.

In scope:
- governed test matrix cleanup
- release gate checklist alignment
- manifest and verify consistency checks
- review-pack completeness checks
- branch and release hygiene docs

Out of scope:
- hosted CI vendor setup
- organization-wide policy automation outside the repo

### S3-D-2 Wrapper and Path Cleanup
Reduce ambiguity between canonical code and compatibility wrappers.

In scope:
- inventory of wrapper files and compatibility entrypoints
- explicit wrapper retirement criteria
- canonical import-path guidance
- cleanup plan for duplicate access paths

Out of scope:
- immediate deletion of all wrappers
- any change that would break the current runnable snapshot

### S3-D-3 Runtime Operability
Make runtime diagnosis practical in production-like environments.

In scope:
- structured service logging plan
- runtime stats and adapter status review
- readiness and degraded-state observability improvements
- failure mode inventory for adapter, replay, and release flows

Out of scope:
- full metrics platform integration
- distributed tracing infrastructure

### S3-D-4 Collaboration and Review Governance
Reduce review drift between human operators, Claude, and Codex.

In scope:
- review-pack completeness rules
- Claude review handoff rules
- release artifact naming and lifecycle rules
- snapshot transition checklist

Out of scope:
- replacing Git as the code-truth layer

## Functional Requirements

### FR-1 Release Gate
- The repository must have one documented and repeatable gate for `test -> review-pack -> package -> verify`.
- The gate must fail when manifest-backed review artifacts are incomplete.

### FR-2 Review Completeness
- Claude review packs must include all fixture files and governed docs needed to review the current stage.
- Missing review artifacts must be detectable before a pack is accepted.

### FR-3 Wrapper Governance
- Compatibility wrappers must be explicitly documented as temporary.
- The repo must define removal criteria before wrappers are deleted.

### FR-4 Runtime Operability
- Readiness output must expose meaningful adapter state.
- Runtime failures must map to diagnosable categories rather than generic startup confusion.

### FR-5 Path and Ownership Clarity
- Canonical code, tests, scripts, docs, and artifacts must have stable locations.
- Any non-canonical path must be documented as legacy or generated output.

## UX and Operability Requirements
- An operator must be able to answer these questions quickly:
  - what snapshot is currently valid
  - what branch and release produced it
  - whether the runtime is healthy, ready, degraded, or misconfigured
  - what files Claude must review for the current stage
- Error wording must prefer actionable operational language over internal implementation detail.

## Success Metrics
- one governed fast-path command for local release validation
- zero known missing-file incidents in Claude review packs after `S3-D`
- one explicit wrapper retirement plan approved before wrapper deletion
- readiness output distinguishes `not configured`, `degraded`, and `ready`
- all future stage plans can be packaged for Claude without manual file hunting

## Acceptance Criteria by Workstream

### S3-D-1
- release and verify scripts cover review-pack completeness
- test matrix is documented and aligned with handoff docs
- release gate failure reasons are explicit

### S3-D-2
- wrapper inventory exists
- wrapper retirement criteria are frozen
- import path guidance is documented for future work

### S3-D-3
- runtime observability gaps are enumerated and partially closed
- adapter readiness wording is operationally understandable
- degraded-state diagnostics are easier to interpret

### S3-D-4
- Claude upload and review discipline is updated to match current repo reality
- snapshot transition steps are documented once, not in scattered prompts

## Risks
- over-hardening the release process and slowing normal iteration
- deleting wrappers too early and breaking downstream entrypoints
- treating observability as a logging-only problem instead of an operational contract problem
- letting review governance drift again when new docs are added but not packed

## Dependencies
- current canonical repo structure under `backend/`, `docs/`, `scripts/`, `releases/`
- current release and verify workflow
- current Claude review-pack generation workflow
- current `S3-C-2026-04-09-006` baseline as the last verified telemetry integration stage

## Delivery Definition
`S3-D` is complete when:
- release and review-pack gates are deterministic
- wrapper retirement is planned and bounded
- runtime operability has a documented contract
- future Claude reviews no longer miss stage-critical files by default
