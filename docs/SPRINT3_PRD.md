# Sprint 3 PRD

## Document Control
- Product: `SecuPilot`
- Source of truth: `D:\产品设计\New folder`
- Snapshot baseline: `S3-PLAN-2026-04-08-001`
- Primary owners:
  - Product and review decisions: `Claude`
  - Implementation and release: `Codex`

## Background
Sprint 2 delivered four core outcomes:
- T3 single-host evidence compiler
- Jarvis passive hunt planner
- orchestrator wiring for T3 plus T3 to T4 IOC enrichment
- degraded-state semantics for incomplete investigations

The codebase is now structured, but Sprint 2 is still a runnable MVP snapshot. Sprint 3 moves SecuPilot from "engine pieces that can be exercised" to "a productized investigation service and analyst-facing case workflow".

## Problem Statement
SecuPilot can already compute investigation results, but it still lacks:
- a stable runtime boundary for service startup and API delivery
- a complete analyst case experience for reading, approving, and acting on cases
- a clean adapter boundary for real SIEM and EDR telemetry
- engineering controls that keep releases, reviews, and data contracts consistent across Claude and Codex

## Sprint 3 Goal
Deliver a product-ready Sprint 3 baseline that:
- exposes the orchestrator as a stable service boundary
- turns T1, T3, T4, T5, and Jarvis outputs into a coherent analyst case experience
- supports mock and real telemetry through explicit adapters
- keeps governance, release, and cross-model collaboration deterministic

## Non-Goals
- full production deployment automation
- autonomous isolation or destructive remediation
- multi-tenant RBAC and enterprise admin console
- model retraining or self-learning pipelines
- removal of compatibility wrappers during Sprint 3

## Target Users
- `L1 analyst`: wants fast triage, clear actions, and low cognitive load
- `L2 analyst`: wants evidence chains, pivots, and degraded visibility
- `SOC manager`: wants approval workflow, case summary, and traceable reasoning
- `Security engineer`: wants deterministic integration contracts and reproducible releases

## Product Principles
1. One case, one source of truth.
2. Structured evidence before narrative.
3. Degraded means explicit limits, not silent optimism.
4. Mock and real data share orchestrator contracts.
5. Claude reviews intent and risk; Codex changes code and releases.

## Scope

### S3-A Runtime Productization
Turn the orchestrator into a stable service boundary.

In scope:
- runtime config cleanup
- standard API or service entrypoint
- health check and readiness check
- mock and production mode switching
- error envelopes and request tracing

Out of scope:
- container orchestration
- autoscaling

### S3-B Analyst Case and Jarvis Experience
Turn the current outputs into a readable, approvable case artifact.

In scope:
- final case schema freeze for Sprint 3
- case summary and evidence sections
- Jarvis `hunt_plan` rendering
- degraded-state display rules
- approval-ready action blocks

Out of scope:
- full design system overhaul
- original raw process tree explorer

### S3-C Real Telemetry Integration
Normalize external data without rewriting core algorithms.

In scope:
- SIEM adapter contract
- EDR process event contract
- time-range propagation
- path and environment config
- mock to prod adapter parity

Out of scope:
- vendor-specific deep optimization for every SIEM

### S3-D Engineering and Release Hardening
Make future reviews and releases reproducible.

In scope:
- CI-aligned test matrix
- release and verification gates
- Claude review pack generation
- wrapper deprecation plan
- docs and manifest synchronization

Out of scope:
- full monorepo migration

## Functional Requirements

### FR-1 Service Entry
- The system must expose a stable entrypoint that returns an `AgenticThreatCase` from a request payload.
- The system must support mock and production adapter modes through configuration.

### FR-2 Case Output
- Every case must include investigation status, risk score, confidence, evidence summary, and any applicable `hunt_plan`.
- Degraded cases must explicitly describe missing analysis or telemetry gaps.

### FR-3 Jarvis Output
- Jarvis must generate structured hunt plans when the investigation type requires them.
- Jarvis output must be reviewable as data, not only as prose.

### FR-4 Adapter Layer
- All external telemetry ingestion must pass through explicit adapters.
- Time range and target scope must be honored consistently across mock and real modes.

### FR-5 Governance
- Every review and release must be tied to a manifest snapshot.
- Claude Web review must be driven by generated upload packs, not manually mixed files.

## UX Requirements
- First screen must answer:
  - what happened
  - why it matters
  - what the analyst should do now
- Evidence must be grouped by chain, IOC, persistence, and blast impact.
- Degraded cases must visually indicate analysis limits and suppress unsafe action suggestions.
- Manager-facing approval text must stay non-destructive by default.

## Success Metrics
- local startup to healthy response in one documented command
- 100 percent manifest-backed review flow for Claude Web
- all governed tests pass before packaging
- no duplicate source-of-truth disputes during Sprint 3 delivery
- analysts can complete one review path using only the case view plus Jarvis plan

## Delivery Definition
Sprint 3 is complete when:
- `S3-A` runtime entry and health checks work
- `S3-B` case schema and review flow are frozen and implemented
- `S3-C` adapters support both mock and production contracts
- `S3-D` release, verify, and Claude pack workflows are operational

## Risks
- UI/schema drift between case rendering and backend payloads
- adapter shortcuts leaking vendor logic into core algorithms
- compatibility wrappers becoming permanent and hiding canonical code
- Claude reviews based on stale files if upload discipline is not enforced

## Dependencies
- current structured project layout under `backend/`, `scripts/`, `mock_data/`
- current Sprint 2 T1, T3, T4, T5 behavior as baseline
- release manifest and handoff governance already in place

## Acceptance Summary By Stream
- `S3-A`: one command to start, one endpoint to investigate, one endpoint to health-check
- `S3-B`: one frozen case schema and one analyst-ready view contract
- `S3-C`: one normalized adapter contract for SIEM and EDR
- `S3-D`: one manifest-backed release and one Claude review pack per snapshot
