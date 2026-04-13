# Sprint 5 Jira Backlog

## Usage
- Use this backlog with `docs/SPRINT5_PRD.md` and `docs/SPRINT5_DISCOVERY_BRIEF.md`.
- Sprint 5 starts from governed snapshot `S4-INTEGRATED-2026-04-13-001`.
- Treat S5-A as the first product direction, S5-E as a lightweight parallel governance decision, S5-C as conditional, and S5-B / S5-D as discovery-limited until external inputs exist.
- Claude review should focus on scope boundaries, dry-run versus external pilot execution, redaction boundaries, governance wording, and hold triggers.
- Codex implementation should stay within the named ticket scope and canonical repo files only.
- `docs/AI_COLLAB_OPERATING_MODEL.md` remains an ungoverned local draft until Sprint 5 explicitly decides whether to govern it through the normal snapshot path.

## Epic S5-A Controlled Pilot Preparation

### S5-A-1 Pilot Preparation Checklist
- Type: `DOC`
- Goal: define the minimum checklist for controlled pilot preparation before any external pilot execution.
- Files:
  - `docs/SPRINT5_PRD.md`
  - new pilot-preparation document under `docs/`
- Acceptance:
  - checklist starts from governed snapshot `S4-INTEGRATED-2026-04-13-001`
  - dry-run preparation is explicitly separate from external pilot execution
  - checklist references governed repo evidence instead of chat-only instructions
  - no real external SIEM / EDR / source system connection is required
  - operator steps remain consistent with S4-D readiness, smoke path, runbook, and validation gate evidence

### S5-A-2 Pilot Dry-Run Evidence Template
- Type: `DOC`
- Goal: define the evidence template for an internal pilot-prep dry run.
- Files:
  - S5-A pilot-preparation document
  - `docs/S4D2_PILOT_SMOKE_PATH.md`
  - `docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md`
  - `docs/S4D4_PILOT_VALIDATION_GATE.md`
  - `docs/S4D5_PILOT_READINESS_REVIEW_PASS.md`
- Acceptance:
  - template captures readiness evidence, `POST /api/v1/pilot-smoke` evidence, pilot gate evidence, release manifest evidence, verify report evidence, and review-pack evidence
  - dry-run evidence is explicitly not a real external pilot result
  - evidence can be collected from governed repo outputs or local dry-run outputs without external systems
  - template does not request secret values, raw credentials, or sensitive customer data
  - failure evidence maps back to governed D-stream runbook categories and fields

### S5-A-3 Pilot Run Log Redaction Boundary
- Type: `DOC`
- Goal: define the pilot run log evidence redaction boundary for dry-run and future controlled pilot preparation.
- Files:
  - S5-A pilot-preparation document
  - `docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md`
  - `docs/RELEASE_PROCESS.md`
- Acceptance:
  - pilot run log evidence redaction boundary is documented separately from operator escalation triage redaction
  - boundary is compatible with S4D3 / RELEASE_PROCESS escalation redaction but does not replace it
  - log evidence must exclude secret values, raw credentials, bearer tokens, API keys, customer-identifying payloads, and unnecessary raw event bodies
  - template distinguishes evidence needed for pilot readiness from material needed for escalation
  - ambiguity between dry-run log evidence and escalation artifacts is resolved before S5-A closeout

### S5-A-4 Pilot Sign-Off Checklist
- Type: `DOC`
- Goal: define the sign-off checklist for pilot preparation readiness.
- Files:
  - S5-A pilot-preparation document
  - S5-A dry-run evidence template
- Acceptance:
  - checklist distinguishes ready for external pilot consideration from starting external pilot execution
  - checklist requires dry-run evidence, redaction boundary acceptance, and governed snapshot alignment
  - checklist states that external pilot execution still needs explicit sign-off outside this backlog item
  - checklist does not depend on real external pilot feedback
  - checklist identifies who must review evidence without introducing enterprise RBAC, tenancy, or workflow-engine scope

### S5-A-5 Pilot Prep Review Pass
- Type: `INT`
- Goal: close S5-A pilot preparation review after checklist, evidence template, redaction boundary, and sign-off checklist are accepted.
- Files:
  - S5-A pilot-preparation documents
  - `docs/SPRINT5_PRD.md`
  - `docs/SPRINT5_JIRA_BACKLOG.md`
- Acceptance:
  - no unresolved P1/P2 pilot-prep ambiguity remains
  - dry-run versus external pilot execution boundary is explicitly accepted
  - pilot run log evidence redaction is accepted as compatible with but distinct from S4D3 / RELEASE_PROCESS escalation redaction
  - governed evidence is sufficient for pilot-prep sign-off
  - closeout does not start external pilot execution

## Epic S5-E Governance And Collaboration Operating Model

### S5-E-1 AI Collaboration Operating Model Review
- Type: `INT`
- Goal: review the existing `docs/AI_COLLAB_OPERATING_MODEL.md` draft and decide whether it is suitable for light governance preparation.
- Files:
  - `docs/AI_COLLAB_OPERATING_MODEL.md`
  - `docs/SPRINT5_DISCOVERY_BRIEF.md`
  - `docs/SPRINT5_PRD.md`
- Acceptance:
  - review confirms this is not a from-scratch collaboration rule design
  - light revision is limited to clarifying existing role assignment, one-writer discipline, review-only mode, handoff cards, snapshot discipline, and tool-failure resilience
  - substantial rewrite, new tool policy, or product-scope change requires a separate ticket before governance
  - review does not govern `docs/AI_COLLAB_OPERATING_MODEL.md` by itself
  - S5-E remains a lightweight parallel governance decision and does not displace S5-A as the product mainline

### S5-E-2 Structured Ticket Template Decision
- Type: `DOC`
- Goal: decide whether Sprint 5 should formalize structured tickets as a governed template.
- Files:
  - `docs/AI_COLLAB_OPERATING_MODEL.md`
  - optional new ticket-template document under `docs/`
- Acceptance:
  - decision states whether a dedicated structured-ticket template is needed now
  - if created, template captures goal, scope, non-goals, acceptance criteria, files in scope, risks, governance checks, test plan, and review target delta
  - decision does not introduce Linear, Notion, or any external tool dependency
  - decision does not block S5-A unless execution clarity requires it
  - any governed template change follows normal snapshot discipline

### S5-E-3 Governance Workflow Review Pass
- Type: `INT`
- Goal: close the Sprint 5 governance workflow review decision.
- Files:
  - S5-E review and decision documents
  - `docs/AI_COLLAB_OPERATING_MODEL.md` if explicitly accepted for governance
- Acceptance:
  - records whether `docs/AI_COLLAB_OPERATING_MODEL.md` should remain an ungoverned local draft or enter the governed baseline
  - if governed, HANDOFF, manifest, verify report, and review-pack expectations are updated through the normal snapshot path
  - if deferred, the reason and next review trigger are documented
  - no product contract or Sprint 5 product scope is changed by governance workflow closure alone

## Epic S5-C Analyst / Manager Case Workflow Hardening

Trigger:
- Start only after pilot-prep dry-run feedback or explicit product decision.
- Hold if approval role design exceeds the `pilot_local` analyst/manager distinction or touches enterprise RBAC, ticketing, or workflow-engine scope.

### S5-C-1 Analyst / Manager Journey Decision
- Type: `INT`
- Goal: define the minimum analyst / manager journey hardening target for Sprint 5.
- Files:
  - `docs/SPRINT5_PRD.md`
  - S4-C case lifecycle documents
- Acceptance:
  - journey and approval roles may come from internal product decision and do not require real pilot user feedback
  - role language stays within `pilot_local` analyst/manager distinction
  - non-destructive case lifecycle semantics remain intact
  - hold trigger is applied before introducing RBAC, ticketing, or workflow-engine design

### S5-C-2 Case Review And Action Request Surface Hardening
- Type: `FE/BE/DOC`
- Goal: tighten the pilot-local analyst / manager review surface without expanding into enterprise workflow.
- Files:
  - case view and case service files as scoped by implementation ticket
  - relevant S4-C governed docs
- Acceptance:
  - analyst and manager actions remain understandable in pilot-local terms
  - action request state transitions remain consistent with S4-C case lifecycle semantics
  - no destructive response execution is introduced
  - no enterprise RBAC, org management, tenancy, ticketing, or workflow engine is introduced
  - changes include targeted regression coverage if runtime or UI behavior changes

### S5-C-3 Approval Role And Denial Reason Clarification
- Type: `DOC/BE`
- Goal: clarify approval role boundaries and denial reason expectations for pilot-local use.
- Files:
  - case lifecycle docs or runtime files as scoped by implementation ticket
- Acceptance:
  - approval role language stays within analyst/manager pilot-local semantics
  - denial reason expectations are clear enough for pilot dry-run review
  - hold trigger is applied before role design exceeds pilot-local scope
  - no external ticketing or workflow-system dependency is introduced

### S5-C-4 Case Workflow Regression Tests
- Type: `TEST`
- Goal: protect any accepted S5-C case workflow hardening with targeted regression tests.
- Files:
  - case workflow tests as scoped by implementation ticket
- Acceptance:
  - tests cover changed analyst/manager workflow behavior
  - tests preserve S4-C durable case lifecycle and audit semantics
  - tests do not require real external systems
  - tests do not encode enterprise RBAC or ticketing assumptions

### S5-C-5 Case Workflow Review Pass
- Type: `INT`
- Goal: close S5-C only if triggered and completed within pilot-local scope.
- Files:
  - S5-C implementation and docs
  - S5-C targeted tests
- Acceptance:
  - no unresolved P1/P2 case workflow ambiguity remains
  - approval role scope remains within pilot-local analyst/manager distinction
  - no enterprise RBAC, tenancy, ticketing, workflow-engine, or destructive response scope has been added
  - closeout records whether S5-C was completed, partially deferred, or not triggered

## Epic S5-B Production Source Mode Expansion

Scope guard:
- Keep S5-B at discovery / contract depth until external source inputs exist.
- Do not connect real external source systems.
- Source-mode discovery must not replace or bypass the accepted S4-A asset-inventory identity authority.
- Hold for independent product decision if work reaches live refresh design, external authentication, multi-tenant data ownership, or CMDB sync.

### S5-B-1 Source Mode Discovery
- Type: `DOC`
- Goal: describe candidate production source modes without implementing external connections.
- Files:
  - new S5-B discovery document under `docs/`
- Acceptance:
  - source modes are described at contract depth only
  - no real external source connection is introduced
  - required external inputs are listed explicitly
  - hold trigger covers live refresh, external auth, multi-tenant data ownership, and CMDB sync

### S5-B-2 Source Contract Sketches
- Type: `DOC`
- Goal: sketch source contract options for future product decision.
- Files:
  - S5-B discovery / contract document
- Acceptance:
  - sketches do not change frozen runtime contracts
  - sketches identify unresolved product questions
  - sketches avoid committing to refresh cadence, external auth model, tenancy ownership, or CMDB sync behavior
  - sketches remain traceable to Sprint 5 PRD non-goals

### S5-B-3 Fixture-Only Source Validation
- Type: `TEST/DOC`
- Goal: explore source-mode implications using fixtures only, if useful.
- Files:
  - fixture files and tests as scoped by implementation ticket
- Acceptance:
  - validation uses static fixtures only
  - no external network connection or credential is required
  - results are documented as discovery evidence, not production readiness
  - hold trigger is applied if validation implies live refresh, external auth, multi-tenant data ownership, or CMDB sync

### S5-B-4 Source Mode Hold Review
- Type: `INT`
- Goal: decide whether S5-B remains discovery-only or needs a later product decision.
- Files:
  - S5-B discovery artifacts
- Acceptance:
  - review records which external inputs are still missing
  - review does not declare production source readiness
  - any live integration direction is deferred to a future governed planning cycle
  - no Sprint 5 baseline is blocked by missing external source inputs

## Epic S5-D Telemetry Breadth And Host Selection Scale

Scope guard:
- Keep S5-D at discovery / fixture depth until external telemetry breadth inputs exist.
- Queue-readiness and fan-out discovery may be documented or explored with fixtures only.
- Do not implement async queueing or fan-out.
- Do not make performance commitments without external telemetry breadth inputs.
- Any host-selection policy suggestion must remain routed through the accepted S4-A identity authority; no policy may bypass or replace S4-A identity authority.

### S5-D-1 Telemetry Breadth Discovery
- Type: `DOC`
- Goal: identify future telemetry breadth questions without expanding production behavior.
- Files:
  - new S5-D discovery document under `docs/`
- Acceptance:
  - discovery lists telemetry breadth assumptions and missing external inputs
  - no production telemetry expansion is implemented
  - no performance commitment is made
  - discovery remains compatible with S4-B telemetry and T3 parity guarantees

### S5-D-2 Host Selection Policy Discovery
- Type: `DOC`
- Goal: document candidate host selection scale questions for future pilot planning.
- Files:
  - S5-D discovery document
- Acceptance:
  - host selection questions are framed as policy discovery, not production selection logic
  - any host-selection policy suggestion must remain routed through the accepted S4-A identity authority
  - no policy may bypass or replace S4-A identity authority
  - no external telemetry breadth input is assumed
  - no async fan-out or queue behavior is implemented
  - any product-impacting policy decision is deferred unless explicitly approved

### S5-D-3 Queue Readiness And Fan-Out Discovery
- Type: `DOC/FIXTURE`
- Goal: explore queue-readiness and fan-out implications through documentation or fixture-only discovery.
- Files:
  - S5-D discovery document
  - optional fixture-only artifacts
- Acceptance:
  - work remains documentation or fixture-only
  - no async queueing or fan-out implementation is introduced
  - no performance target or throughput commitment is declared
  - risks and missing external telemetry inputs are documented

### S5-D-4 Fixture Replay Expansion
- Type: `TEST`
- Goal: optionally add fixture-only replay coverage for telemetry breadth questions.
- Files:
  - replay fixture and test files as scoped by implementation ticket
- Acceptance:
  - fixtures do not imply production telemetry breadth support
  - tests do not require external telemetry sources
  - any new fixture remains mapped to existing S4-B / S4-C contracts
  - no queueing, fan-out, or performance implementation is introduced

### S5-D-5 Telemetry Breadth Review Pass
- Type: `INT`
- Goal: close S5-D discovery / fixture work without overstating production readiness.
- Files:
  - S5-D discovery and fixture artifacts
- Acceptance:
  - review records that S5-D remains discovery / fixture depth unless external inputs arrive
  - no unresolved P1/P2 telemetry contract ambiguity remains within the scoped discovery
  - no async queueing, fan-out, or performance commitment has been introduced
  - missing external telemetry inputs are clearly deferred

## Recommended Sprint 5 Sequence
- First: complete S5-A-1 through S5-A-5 to establish controlled pilot preparation materials and dry-run evidence boundaries.
- Parallel / lightweight: run S5-E-1 through S5-E-3 only as a governance decision path, without displacing S5-A.
- Conditional second stream: start S5-C only after pilot-prep dry-run feedback or explicit product decision.
- Discovery only: keep S5-B limited to source-mode discovery / contract depth until external source inputs exist.
- Discovery / fixture only: keep S5-D limited to telemetry breadth and host-selection discovery until external telemetry inputs exist.
- Governance closeout should occur only after accepted Sprint 5 scope has targeted review evidence and a clean governed snapshot path.

## Claude Review Focus
- Verify S5-A does not blur dry-run preparation with external pilot execution.
- Verify pilot run log evidence redaction is compatible with but distinct from S4D3 / RELEASE_PROCESS escalation redaction.
- Verify S5-E reviews and lightly revises the existing `docs/AI_COLLAB_OPERATING_MODEL.md` draft rather than redesigning collaboration rules from scratch.
- Verify S5-C trigger and approval role / RBAC hold trigger are explicit and enforceable.
- Verify S5-B stays discovery / contract depth and holds for live refresh, external auth, multi-tenant data ownership, or CMDB sync.
- Verify S5-D stays discovery / fixture depth and does not introduce async queueing, fan-out implementation, or performance commitments.

## Codex Implementation Focus
- Create or modify only the files named by each active ticket.
- Preserve governed Sprint 4 baseline guarantees unless a Sprint 5 ticket explicitly opens a governed change.
- Keep S5-A evidence, checklist, sign-off, and redaction documents operator-facing and minimal.
- Treat `docs/AI_COLLAB_OPERATING_MODEL.md` as read-only until an explicit S5-E task authorizes governance work.
- Prefer targeted tests for behavior changes and avoid full-gate or snapshot updates unless the active ticket requests governance closure.
- Do not touch untracked off-limits files or repo-external artifacts.
