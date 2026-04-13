# AI Collaboration Operating Model

## Goal
Define one default operating model for human + AI collaboration in the `D:\产品设计\New folder` source-of-truth repo so planning, implementation, review, governance, and context handoff remain stable across tools and conversations.

## Scope
- applies to Codex Web, VS Code, Claude Code, Claude Web, and the human operator
- applies to planning, implementation, review, release governance, snapshot transitions, and conversation resets
- does not replace product contracts, release rules, or runtime contracts already frozen elsewhere in `docs/`
- defers to `docs/RELEASE_PROCESS.md` and existing governed release/snapshot rules for exact closeout, packaging, manifest, verification, review-pack, and full-gate requirements

## Source Of Truth
- root path: `D:\产品设计\New folder`
- only this directory may be treated as latest runnable truth
- governed truth lives in Git plus governed repo files such as `docs/HANDOFF.md`, `releases/release_manifest.json`, and `releases/verify_report.json`
- chat history is coordination context, not code truth

## Draft Governance Status
This document remains a draft until it is explicitly added through a governed snapshot path that includes:
- `docs/HANDOFF.md` update
- `releases/release_manifest.json` key_file entry
- `releases/verify_report.json` refresh
- review-pack and release artifact alignment
- full gate PASS

Before that happens, this document should not be treated as a governed contract.

## Operating Principles
1. one writer at a time
2. implementation and review stay separate by default
3. governance state must be recorded in repo artifacts, not only in chat
4. new conversations are normal and expected; continuity must come from governed handoff, not model memory
5. external review is useful, but must not become a critical-path dependency

## Role Assignment
These role labels map to the current `docs/HANDOFF.md` practice:
- VS Code: writer / execution workspace
- Claude Code: review-only by default; may write only when explicitly authorized and not concurrently with VS Code on the same files
- Codex Web: planning, governance, prompt orchestration, and closeout judgment
- Claude Web: optional external red-team reviewer, not critical path

This is a wording clarification, not a workflow redesign.

### VS Code
- primary execution workspace
- default and only file writer
- responsible for:
  - code and doc edits
  - local tests
  - `git add`, `git commit`, and `git push`
- does not decide governance closure by itself

### Codex Web
- control tower for planning and workflow coordination
- responsible for:
  - structured ticket definition
  - prompt orchestration
  - pacing and phase transitions
  - review interpretation
  - governance closure judgment
  - conversation handoff packaging
- does not write repo files under the default model

### Claude Code
- primary local review engine
- default mode is `review only`
- responsible for:
  - delta-focused code and doc review
  - bug, regression, contract, and testing-gap detection
  - bounded follow-up implementation only when explicitly authorized
- must not edit the same scoped files concurrently with VS Code

### Claude Web
- independent red-team reviewer
- used for milestone-level challenge, not routine implementation
- responsible for:
  - product-logic challenge
  - governance challenge
  - maintainability and operator-clarity challenge
- must not be treated as code truth or release truth

## Default Workflow
1. Codex Web defines the structured ticket.
2. VS Code executes the scoped implementation.
3. Codex Web prepares a delta-only review prompt.
4. Claude Code performs `review only`.
5. VS Code addresses accepted findings.
6. Codex Web decides whether the result needs:
   - normal commit/push only
   - or a governed snapshot transition
7. Claude Web may perform milestone red-team review when needed.

## Structured Ticket
Each new task should be expressed by Codex Web with these sections:
- `Goal`
- `Scope`
- `Non-goals`
- `Acceptance Criteria`
- `Files In Scope`
- `Risks`
- `Governance Checks`
- `Test Plan`
- `Review Target Delta`

Small tasks may compress the wording, but should still make goal, write scope, and acceptance explicit.

## Review Rules

### Claude Code Review
- default scope is the current delta only
- primary targets:
  - bugs
  - regressions
  - contract drift
  - missing tests
  - operator ambiguity introduced by the change
- not intended to re-audit the whole repo every round

### Claude Web Review
- trigger only for:
  - stage baseline completion
  - high-risk governance transitions
  - pilot readiness challenge
  - major architecture uncertainty
- preferred angle:
  - red-team challenge
  - long-term maintainability
  - product coherence
  - governance robustness

## Governed Snapshot Rule
Use a governed snapshot when one of these is true:
- a stage baseline changes
- a contract changes
- release or review-pack inputs change
- handoff expectations materially change
- a milestone needs independent review or delivery packaging

Do not roll a new snapshot for:
- trivial typo fixes
- isolated test-only micro-fixes
- tiny non-governance edits that do not change the accepted baseline

A governed snapshot is complete only when:
- `docs/HANDOFF.md` is aligned
- `releases/release_manifest.json` is aligned
- `releases/verify_report.json` is regenerated and passing
- release packaging and review-pack artifacts are rebuilt as required by `docs/RELEASE_PROCESS.md` and the active governed release process

Release process precedence:
- this operating model describes collaboration workflow
- `docs/RELEASE_PROCESS.md` and existing governed release/snapshot rules remain authoritative for exact release packaging, manifest, `verify_report`, review-pack, and full-gate requirements
- if this document conflicts with product contracts, release rules, or runtime contracts, the governed product, release, and runtime contracts take precedence

## Context Reset Rule

### Green Zone
Continue the current conversation when:
- one ticket is in flight
- one implementation/review loop is active
- snapshot and scope are still stable

### Yellow Zone
Prepare a handoff card when:
- the thread has crossed multiple sub-tasks
- repeated review/fix cycles have accumulated
- snapshot, branch, or current objective must be repeatedly restated
- response quality or context precision is starting to degrade

### Red Zone
Start a new conversation when:
- the stage changes
- the governed snapshot changes
- the task switches from implementation to governance closure
- the thread begins mixing multiple concerns
- tool reliability drops, including `stream disconnected` or repeated context loss

## Conversation Handoff Card
Each new conversation should carry only the minimum durable context:
- single source of truth
- current snapshot
- current branch
- current commit
- must-read files
- current task goal
- files or areas that must not be touched
- immediate next step

## Delta Discipline
- implementation prompts should define explicit write scope
- review prompts should target only the changed files and directly affected contracts
- broad repo-wide prompts should be reserved for milestone reviews, not normal iteration

## File Safety
- untracked files explicitly marked as off-limits must remain untouched
- repo-external files, zips, screenshots, and copied folders must never override in-repo truth
- generated release artifacts are delivery outputs, not alternate truth sources

## Tool Failure Resilience
- tool instability must be handled by conversation reset, not by loosening source-of-truth rules
- if Codex Web becomes unstable, the next session resumes from governed handoff plus the handoff card
- the workflow must remain operable even if Claude Web is unavailable or rate-limited

## Cost And Usage
- daily default: `VS Code + Codex Web`
- per implementation round: add `Claude Code review`
- per milestone only: optionally add `Claude Web`
- prefer low-latency local execution over repeated full-context external review

## Expected Outcome
This operating model should produce:
- stable implementation velocity
- lower context-loss risk
- less duplicate review effort
- cleaner governance closure
- more predictable snapshot transitions
- less tool contention across the same file set

## Open Follow-Ups
- whether to formalize structured tickets in a dedicated template
- whether to add an ADR section to each governed snapshot
- whether to externalize tickets into an external ticketing system, if separately approved after the in-repo workflow is fully stable
- whether to define a backup execution workspace for temporary tool instability
