# S6 Sprint 0 Exit Review And Sprint 1 Entry Gate 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Sprint 0 Exit Review And Sprint 1 Entry Gate 2026-04-27 |
| Status | SPRINT_0_EXIT_PASS_WITH_SPRINT1_BATCH_GATE |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Current route | `WAIT_FOR_NEXT_EXACT_BOUNDED_TICKET_SELECTION` |
| Backlog SoT | `D:\产品设计\secupilot0421\SecuPilot_Engineering_Backlog_Tracker_v0.4.xlsx` |

This record closes Sprint 0 at the foundation level and opens Sprint 1 entry only through batch-level ticket launch gates.

It does not authorize full Sprint 1 implementation, broad ticket starts, backend/runtime/API/schema changes, real data, secrets, deployment, public endpoint work, external pilot execution, or parked-stream reopen.

## 2. Decision

Decision:

```text
SPRINT_0_EXIT_PASS_WITH_SPRINT1_BATCH_GATE
```

Meaning:

- Sprint 0 foundation work is sufficient to exit into Sprint 1 planning and batch launch.
- Sprint 1 implementation may start only for a selected exact batch or ticket after its launch checklist names allowed files, test command, reviewer path, rollback condition, and HOLD conditions.
- Backlog Tracker v0.4 is the current planning source of truth, but it is not itself a build-start authorization for every Sprint 1 ticket.
- Existing E0-03 and E0-04 tickets must not be reopened from older wording. Any regression or registry expansion must use explicit follow-up tickets such as E0-03B, E0-04B, E0-04C, or E0-04D.

## 3. Sprint 0 Exit Review Matrix

| Criterion | Verdict | Evidence | Remaining action |
| --- | --- | --- | --- |
| E0-02B complete or explicitly non-blocking for Sprint 1 | PASS | E0-02B closed as `IMPLEMENTED_GATE_PASS_CLAUDE_CODE_PASS_COMMITTED_PUSHED`; commit `633cc73`; Jira `SCRUM-19` done. | None for Sprint 1 entry. Future fixture QA expansion still needs exact tickets. |
| Fixture registry usable | PASS | E0-02B added phase, boundary, poison-pill, and resolver-degradation registry coverage. `validate=false` is restricted to poison-pill rejection tests. | Use default validated fixture loading in Storybook, Playwright, and production-like paths. |
| Storybook baseline can run | PASS | E0-03/E0-03B completed; Storybook build passed; registry stories expose validated phase, boundary, resolver-degradation, and non-renderable poison-pill inventory. | Do not treat poison-pill fixtures as renderable stories. |
| Playwright baseline can run | PASS_WITH_NON_BLOCKING_HOLD | E0-04/E0-04B completed; full Playwright baseline passed after static redline expansion. | E0-04D remains HOLD for material observation-window/state-sync assertions until an exact `emitStateSync` / resolved-context harness exists. |
| E0-01 through E0-04 closeout state is clear | PASS_WITH_STALE_NOTE_CLEANUP | Route and handoff lineage record E0-01, E0-02, E0-03, E0-04, E0-02B, E0-03B, E0-04B, and E0-04C as closed. | If an older handoff line still says E0-02 pending closeout, latest route lineage supersedes it. Do not reopen E0-02. |
| Backlog Tracker v0.4 is current SoT | PASS | v0.4 workbook title and overview identify it as replacing v0.2/v0.3 for backlog tracker SoT; route update keeps v0.4 current. | Continue using v0.4 for planning, not as blanket implementation GO. |
| Sprint 1 tickets have AI_COLLAB execution fields | PARTIAL_PASS | Tracker includes primary implementor, execution surface, reviewer, review surface, HOLD trigger, and review-related fields. | Broad Sprint 1 still has many `Allowed Files / File Scope` and `Test Command` entries marked TBD. These must be filled per selected ticket or batch launch. |

## 4. Route Adjustment Review

### 4.1 Sprint 0 Tail

Proposed path:

```text
E0-02B -> E0-03 Storybook regression + fixture-registry integration
       -> E0-04 Playwright regression + fixture-registry integration
       -> Sprint 0 Exit Review
```

Adjustment:

```text
YES
```

Reason:

E0-02B is already complete. E0-03 and E0-04 primary tickets are already complete and pushed, so the route must name follow-up tickets instead of reopening them.

Corrected route:

```text
E0-02B - Fixture QA Expansion: COMPLETE
E0-03B - Storybook negative/boundary registry stories: COMPLETE
E0-04C - App static redline renderability hooks: COMPLETE
E0-04B - Static Playwright LC-B / LC-N redline assertions: COMPLETE
E0-04D - Observation-window/state-sync Playwright readiness: HOLD, non-blocking for Sprint 1 entry
Sprint 0 Exit Review: THIS RECORD
```

### 4.2 Sprint 0 Exit Conditions

Adjustment:

```text
YES
```

Accepted exit conditions:

- E0-02B fixture registry supports phase, poison-pill inventory, boundary, and resolver-degradation coverage.
- Storybook has reviewable baseline and registry stories, including at least one P1 case-detail path plus the negative/boundary registry views.
- Playwright LC-N/static redline assertions are runnable.

Clarification:

Material observation-window state migration is not part of Sprint 0 exit. It remains E0-04D HOLD until an exact state-sync harness exists.

### 4.3 Sprint 1 - P1 Case Detail

Adjustment:

```text
YES
```

Reason:

P1 is still the correct Sprint 1 first product surface, but current repo work already completed P1-CD-A, P1-CD-B, P1-CD-C, and P1-CD-D. Sprint 1 planning must reconcile those completed repo tickets against Backlog Tracker v0.4 before creating duplicate implementation work.

Recommended Sprint 1 entry:

```text
OPEN_SPRINT1_BATCH0_P1_LAUNCH_CHECKLIST
```

Candidate first batch remains acceptable only after per-ticket launch checklist:

```text
GS-T01 / GS-T02 / GS-T03 / IN-T05 / CD-T03
```

Each selected ticket must fill:

- primary implementor;
- execution surface;
- reviewer;
- review surface;
- allowed files;
- test command;
- rollback condition;
- HOLD conditions;
- external review trigger, if conditional.

Sprint 1 small integration should remain P1-local unless a later exact ticket authorizes cross-surface handoff:

- P1 submitted Action Request may show local `Waiting on P2` state.
- P1 must not render `IMMEDIATE`, `DELAYED`, or `OBSERVE_ONLY` choices.
- P1 must not expose P2 approval authority.
- ActionMode DOM must not mount on P1.
- Storybook and Playwright coverage may be added only through exact files and tests.

### 4.4 Sprint 2 - P2 Approval Surface

Adjustment:

```text
YES
```

Reason:

P2 remains the correct second product surface. However, first P2 implementation remains gated by P2 v0.3 lightweight ratification, and observation-window material state migration depends on the same state-sync harness currently parked by E0-04D.

Recommended additions:

- Treat `AP-T10` badge/pill mapping as a good first P2 infrastructure ticket.
- Require P2 v0.3 lightweight ratification before any `P2-AP-*` implementation.
- Require HF-01 final frame before AP-T06 observation-window timer UI.
- Do not implement material `OBSERVATION_WINDOW -> PENDING_APPROVAL` migration until an exact `emitStateSync` or equivalent resolved-context harness is available.

### 4.5 Sprint 3A - Search/History

Adjustment:

```text
MINOR_YES
```

Reason:

SH-T03 clamp-first routing is correctly placed first. The route should explicitly keep Search/History read-only and mock-only unless a later exact ticket authorizes data-source or backend changes.

Required guard:

```text
Search/History may establish manager/history source semantics, but it must not upgrade coverage, infer missing evidence, or attach P3 host raw evidence DOM.
```

### 4.6 Sprint 3B - P3 Manager View

Adjustment:

```text
YES
```

Reason:

Starting P3 after Search/History is correct because P3 approval-audit and manager/history source semantics depend on SH groundwork.

Required additions:

- P3 full ratification must complete before the first `P3-MV-*` implementation.
- P3 manager summaries must remain independent from P2 technical components.
- P3 host raw evidence must be absent from the DOM, not merely hidden.
- Unsupported claims must keep cautious manager-facing language.

### 4.7 Sprint 4 - Coverage & Health + Cross-Surface Hardening

Adjustment:

```text
YES
```

Reason:

Sprint 4 is the right place for cross-surface hardening, but it must distinguish static redline tests from material runtime/state-sync tests.

Required additions:

- E0-04D or an equivalent exact state-sync harness must be resolved before full observation-window migration E2E.
- `CH-T03` remains a good first CH ticket because `ui_messages` rendering is directly tied to LC-N hardcoded-copy detection.
- Any touch to `backend/app/runtime_service.py` or backend runtime behavior requires a separate human go/no-go before implementation.

### 4.8 Post-Sprint 4 Build-Ready Evaluation

Adjustment:

```text
NO_MAJOR_CHANGE
```

Reason:

The proposed boundary is correct. Build-ready evaluation must not imply authorization for real data, production deployment, public endpoints, external pilot, parked stream reopen, or backend/runtime/API/schema breaking changes.

Each of those remains a separate governed decision record.

## 5. Revised Timeline

```text
Sprint 0 tail
  E0-02B COMPLETE
  E0-03B COMPLETE
  E0-04C COMPLETE
  E0-04B COMPLETE
  E0-04D HOLD, non-blocking
  Sprint 0 Exit Review PASS_WITH_SPRINT1_BATCH_GATE

Sprint 1
  P1 Case Detail continuation and tracker reconciliation
  Sprint 1 Batch-0 launch checklist
  Selected P1 tickets only after allowed files and test commands are exact
  P1-local small integration

Sprint 2
  P2 Approval Surface after P2 v0.3 lightweight ratification
  AP-T10 first if still valid
  Observation-window implementation only after exact visual and state-sync harness readiness

Sprint 3A
  Search/History read-only path
  SH-T03 clamp-first route first

Sprint 3B
  P3 Manager View after P3 full ratification and SH source semantics

Sprint 4
  Coverage & Health
  Cross-surface hardening
  Full LC-P / LC-B / LC-N regression only where exact renderable/state-sync scope exists

Post-Sprint 4
  Build-Ready Evaluation
  Governed readiness planning only after PASS
```

## 6. Non-Negotiable Constraints

These constraints continue across all future tickets:

- `coverage_level` is a hard ceiling.
- Expert mode must not reveal OFF fields.
- The frontend may display, fold, weaken, or hide existing information; it must not create new product facts.
- P3 host evidence must not be attached to the DOM.
- URL, localStorage, and sessionStorage are not authority sources for role, coverage, case state, action mode, or surface.
- Fixtures must be fully artificial and marked through fixture metadata.
- Static HTML remains visual and interaction reference only, not production frontend source.
- AI_COLLAB Amendment v0.2 governs execution surface, reviewer floor, single-writer lock, and SWE HOLD-on-expansion behavior.

## 7. Next Safe Action

Next safe automation action:

```text
OPEN_SPRINT1_BATCH0_P1_LAUNCH_CHECKLIST
```

No Sprint 1 code implementation should start until the selected Batch-0 tickets have exact allowed files, test commands, review path, rollback, and HOLD conditions.
