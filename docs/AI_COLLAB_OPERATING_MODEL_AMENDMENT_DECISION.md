# AI Collaboration Operating Model Amendment Decision

## Document Control
- Title: AI Collaboration Operating Model Amendment Decision
- Baseline: `S5-STREAM-REVIEW-2026-04-14-001`
- Source of truth: `D:\产品设计\New folder`
- Status: Draft for review
- Scope: docs-only amendment decision; no direct model edit
- Owner: Human-governed collaboration model planning

## Goal
Evaluate whether the pending operating-model rules should be codified in a later bounded amendment to `docs/AI_COLLAB_OPERATING_MODEL.md`.

This decision document does not modify `docs/AI_COLLAB_OPERATING_MODEL.md`, does not add itself to the manifest, and does not itself create newly governed operating rules. It only decides whether the nine pending rules are safe candidates for a later separately governed amendment ticket.

## Non-Goals
- modifying `docs/AI_COLLAB_OPERATING_MODEL.md` directly
- changing code, tests, runtime/API/schema, release tooling, or dependencies
- changing S4-C or S5-C product semantics
- authorizing external pilot execution or real customer/operator sign-off
- authorizing real SIEM/EDR/source-system access
- changing release, manifest, or gate behavior
- making Claude Web or Claude Code mandatory blockers for routine tickets
- weakening human go/no-go authority

## Current Baseline And Inputs
- Current governed baseline is `S5-STREAM-REVIEW-2026-04-14-001`.
- `docs/S5_STREAM_REVIEW_CHECKPOINT.md` recommended `AI_COLLAB_OPERATING_MODEL_AMENDMENT_DECISION` as the next safe docs-only route.
- `docs/AI_COLLAB_OPERATING_MODEL.md` is already governed as collaboration workflow guidance and must not be modified without a separate amendment ticket.
- `docs/HANDOFF.md`, `releases/release_manifest.json`, and `releases/verify_report.json` record the current governed baseline and manifest state.
- `D:\产品设计\SecuPilot_Context\Codex_Operating_Context_20260414.md` and `D:\产品设计\SecuPilot_Context\SecuPilot_对话延续包_20260414.md` were readable and treated as advisory context only, not governed repo artifacts.
- This document is not yet in `releases/release_manifest.json`.

## Pending Amendment Rules
The pending amendment rules are:
- primary_implementor per ticket, not tool-bound
- single-writer lock by ticket and file scope
- Claude Code default review-only unless explicitly assigned Primary Implementor
- reviewer_when_cc_implements required if Claude Code implements
- Claude Code cannot be the sole reviewer of its own implementation
- AI provides governance recommendations; human makes go/no-go
- Claude Web is high-value external review, not default blocker for routine tickets
- requires_external_review mandatory trigger categories
- integration verifier as checklist role at stream/milestone closeout

## Rule-by-Rule Decision Matrix

| Pending rule | Proposed disposition | Reason | Intended AI_COLLAB section or placement | Risk reduced | HOLD trigger |
| --- | --- | --- | --- | --- | --- |
| primary_implementor per ticket, not tool-bound | `ACCEPT_FOR_LATER_AMENDMENT` | Recent tickets already assign implementor responsibility explicitly; making it tool-neutral avoids binding authority to a specific interface. | `Structured Ticket` and `Role Assignment` | Ambiguous ownership and accidental multi-writer work. | Rule is written as mandatory use of one tool rather than a role assignment. |
| single-writer lock by ticket and file scope | `ACCEPT_FOR_LATER_AMENDMENT` | Existing one-writer principle should be made file-scope and ticket-scope explicit. | `Operating Principles`, `Delta Discipline`, and `File Safety` | Concurrent edits, accidental overwrites, and review confusion. | Rule blocks review-only access or conflicts with emergency human correction. |
| Claude Code default review-only unless explicitly assigned Primary Implementor | `ACCEPT_FOR_LATER_AMENDMENT` | Current practice already treats Claude Code as review-only by default and allows implementation only when explicitly scoped. | `Role Assignment` and `Claude Code Review` | Silent role drift from reviewer to writer. | Wording makes Claude Code unable to implement even when explicitly authorized. |
| reviewer_when_cc_implements required if Claude Code implements | `ACCEPT_FOR_LATER_AMENDMENT` | If Claude Code writes, a separate reviewer must be named before work starts. | `Structured Ticket` and `Review Rules` | Self-review and missing independent risk check. | Wording makes every Claude Code review require extra reviewer even when Claude Code did not implement. |
| Claude Code cannot be the sole reviewer of its own implementation | `ACCEPT_FOR_LATER_AMENDMENT` | Separation of implementation and review remains the core safety model. | `Operating Principles` and `Review Rules` | Self-approval and unreviewed implementation deltas. | Rule is used to block Claude Code review of unrelated human/VS Code work. |
| AI provides governance recommendations; human makes go/no-go | `ACCEPT_FOR_LATER_AMENDMENT` | Repo practice consistently keeps final product, governance, push, and phase decisions human-governed. | `Role Assignment`, `Default Workflow`, and a governance note | AI over-authorizing snapshot, push, pilot, or product decisions. | Wording implies AI can make final go/no-go or overrides human decision. |
| Claude Web is high-value external review, not default blocker for routine tickets | `ACCEPT_FOR_LATER_AMENDMENT` | Existing model already treats Claude Web as optional red-team/milestone review, not routine critical path. | `Claude Web Review` and `Cost And Usage` | Unnecessary bottlenecks and routine ticket over-escalation. | Wording removes Claude Web from required high-risk review triggers. |
| requires_external_review mandatory trigger categories | `ACCEPT_FOR_LATER_AMENDMENT` | Trigger-based escalation preserves rigor for high-risk changes without making every ticket a blocker. | `Claude Web Review` or new `External Review Triggers` subsection | Missed external review for contracts, principles, dependencies, semantic boundaries, and milestone closeout. | Trigger list becomes so broad that routine docs/test tickets are always blocked. |
| integration verifier as checklist role at stream/milestone closeout | `ACCEPT_FOR_LATER_AMENDMENT` | Stream/milestone closeout benefits from an explicit cross-artifact consistency check without creating a new authority layer. | `Governed Snapshot Rule` or new closeout checklist note | Manifest/HANDOFF/review-pack/test evidence drift at closeout. | Role is written as replacing human go/no-go or release process authority. |

## requires_external_review Trigger List
The later amendment should define `requires_external_review=true` for these mandatory trigger categories:
- new contract freeze or modification to frozen contract
- AP-01 to AP-06 architecture principle changes
- new runtime/build dependency
- source identity authority / telemetry normalization / case lifecycle / pilot readiness semantic changes
- stream or milestone closeout
- real external pilot/customer/operator evidence/access decisions
- redaction/secret/evidence retention boundary changes

Routine docs/test tickets do not require external review unless they hit one of these triggers.

## Implementation Boundary
A later amendment ticket, if opened, must:
- name exact file: `docs/AI_COLLAB_OPERATING_MODEL.md`
- identify exact sections to edit
- preserve existing source-of-truth and governance principles
- avoid creating duplicate or conflicting contracts
- include acceptance criteria and validation command if relevant
- preserve human go/no-go authority
- not require external tools as default dependencies

The later amendment ticket must not change release tooling, manifest format, full-gate behavior, product semantics, runtime behavior, tests, schema, or dependencies.

## Candidate Decisions

| Candidate decision | Meaning | When to use | Non-meaning | Next step |
| --- | --- | --- | --- | --- |
| `ACCEPT_AMENDMENT_PLAN` | The nine pending rules are accepted as candidates for a later bounded amendment ticket. | Use when rules are consistent with current governed practice and reduce collaboration risk. | Does not modify AI_COLLAB now and does not make the rules newly governed. | Draft a scoped docs-only amendment ticket for `docs/AI_COLLAB_OPERATING_MODEL.md`. |
| `NEEDS_REWRITE` | The rule set is directionally useful but needs restructuring before amendment. | Use if rules duplicate existing sections, conflict with source-of-truth discipline, or over-constrain routine work. | Does not reject collaboration governance improvements. | Rewrite the amendment proposal as a new decision draft. |
| `KEEP_AS_CONTEXT_ONLY` | The rules remain advisory context and should not enter the governed operating model yet. | Use if the repo evidence is insufficient or the rules are too situational. | Does not allow teams to treat context packages as governed rules. | Keep using governed AI_COLLAB as-is and revisit later. |
| `HOLD` | A blocking ambiguity prevents even planning a later amendment. | Use if human authority, source-of-truth discipline, review separation, or product/runtime boundaries would be weakened. | Does not authorize partial amendment. | Resolve blocker before any amendment ticket. |

## Preliminary Decision
Decision: `ACCEPT_AMENDMENT_PLAN`.

Meaning:
- The nine pending rules are accepted as candidates for a later bounded amendment ticket.
- The later ticket may propose exact wording changes to `docs/AI_COLLAB_OPERATING_MODEL.md`.
- The amendment should remain docs-only and preserve the existing human-governed source-of-truth model.

Non-meaning:
- does not modify AI_COLLAB now
- does not make the rules newly governed until the amendment is completed
- does not authorize code, test, runtime, API, schema, dependency, release tooling, or product-semantics changes
- does not make Claude Web or Claude Code mandatory blockers beyond the accepted trigger rules
- does not change S5 product semantics

## HOLD Conditions

| HOLD condition | Reason |
| --- | --- |
| This document is treated as directly modifying AI_COLLAB. | It is a decision/planning artifact only. |
| Pending rules are treated as already governed without amendment closeout. | Governance requires a separate bounded amendment ticket and snapshot path. |
| Human go/no-go is weakened. | Final product, governance, push, and phase decisions remain human-owned. |
| Claude Code reviews its own implementation as sole reviewer. | Implementation and independent review must stay separated. |
| Single-writer lock is bypassed. | Ticket/file-scope ownership prevents conflicting writes. |
| External review is required for all routine tickets rather than trigger-based tickets. | Routine docs/test work should not become blocked by default. |
| External tools are introduced as default dependencies. | The current operating model avoids external tool dependency. |
| S4-C or S5-C product semantics are changed. | This decision is collaboration-process only. |
| Code/test/runtime/API/schema/dependency changes appear. | This task authorizes no implementation change. |

## Future Amendment Ticket Requirements
Any later AI_COLLAB amendment ticket must include:
- `primary_implementor`
- `reviewer`
- `reviewer_when_cc_implements` if relevant
- exact file and sections
- exact wording changes or patch scope
- acceptance criteria
- validation command if relevant
- conflict check against existing AI_COLLAB principles
- rollback/hold criteria
- external review requirement decision

## Acceptance Criteria
This decision draft is acceptable when:
- all nine pending rules are evaluated
- `requires_external_review` trigger list is complete
- direct `docs/AI_COLLAB_OPERATING_MODEL.md` modification is excluded
- future amendment ticket is separately required
- human go/no-go remains final
- no product/runtime/test/dependency changes are authorized
- preliminary decision is one of `ACCEPT_AMENDMENT_PLAN`, `NEEDS_REWRITE`, `KEEP_AS_CONTEXT_ONLY`, or `HOLD`
