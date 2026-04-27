# S6 CD-T05 Source Field Map Checklist 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Ticket | `CD-T05` |
| Title | P3 independent executive summary source-field map |
| Decision | `SOURCE_FIELD_MAP_CHECKLIST_PASS_IMPLEMENTATION_REQUIRES_SEPARATE_GO` |
| Primary implementor | Codex for checklist only |
| Execution surface | codex |
| Reviewer | Claude Code required if later implementation diff exists |
| Review surface | claude-cmd |
| Workspace | VS Code / local repo |
| G0-05 signoff | `YES` |
| Implementation status | `NOT_STARTED` |
| Jira issue | `SCRUM-51` |
| Jira parent | `SCRUM-8 [CD] Case Detail、summary、honesty、状态 header、P3 executive summary` |

This checklist is source-field mapping only. It does not implement `CD-T05`, does not mark `CD-T05` Done, and does not authorize P3 executive summary implementation.

## 2. Checklist Decision

Decision:

```text
SOURCE_FIELD_MAP_CHECKLIST_PASS_IMPLEMENTATION_REQUIRES_SEPARATE_GO
```

Interpretation:

- Claude Web authority review returned `PASS_WITH_NOTE` for `CD-T05`.
- The G0-05 signoff note is now repo-locally closed.
- The allowed source-field map is now explicit enough for a later bounded implementation ticket.
- A separate `CD-T05 implementation GO` is still required before any code change.
- Jira cloud sync completed only for this checklist issue; the `CD-T05` implementation remains `NOT_STARTED`.

## 3. Allowed Source-Field Map

Later implementation may read only these source categories:

| Allowed field category | Current repo / fixture projection | Use limit |
| --- | --- | --- |
| `summary_layer.verdict` | existing case verdict projection | Management summary wording only. |
| `summary_layer.summary` | existing case summary projection | WHAT/brief narrative only. |
| `summary_layer.coverage_level` | existing effective visible coverage label | Boundary label only; never unlock hidden fields. |
| `honesty_layer.unsupported_claims[]` | existing redline unsupported-claims projection | Caution language and forbidden over-certainty guard only. |
| `honesty_layer.what_would_raise_confidence[]` | existing honesty layer projection if surfaced | Confidence-raising language only; no KPI inference. |
| `honesty_layer.what_would_disprove_current_verdict[]` | existing honesty layer projection if surfaced | Disproof/caution language only; no evidence expansion. |

If a listed projection is absent in the current mock fixture, later implementation must render data-unavailable or omit the section honestly. It must not create substitute product facts.

## 4. Forbidden Source Categories

Later implementation must not read, derive from, or mount:

- `evidence_layer.*`;
- `blast_radius`;
- `lineage_confidence`;
- host raw evidence;
- process raw evidence;
- technical panels;
- approval controls;
- action controls;
- approval audit summary;
- Manager View handoff/output;
- frontend-inferred KPI, ROI, MTTA, MTTR, queue count, or trend metrics;
- over-certain management copy such as `完全受控` or `已彻底消除`.

## 5. Later Implementation Guardrails

If separately authorized, `CD-T05` may do only:

- render a P3-only independent executive summary inside Case Detail;
- use only the allowed field map above;
- prove forbidden source categories are not attached to the DOM;
- apply G0-05 translation-matrix caution language for unsupported claims;
- add stable test ids and regression assertions for source boundaries and over-certainty exclusions.

## 6. Non-Authorization

This checklist does not authorize:

- Manager View page content;
- approval audit summary;
- P0/P2 Manager variants;
- P2 approval controls;
- route handoff or cross-surface data flow;
- fixture registry, fixture adapter, validator, or `ResolvedSurfaceContext` changes;
- backend/runtime/API/schema changes;
- Storybook, Playwright, real data, anonymized real data, secrets, deploy, public endpoint, or external pilot.

## 7. Next Route

```text
WAIT_FOR_CD_T05_IMPLEMENTATION_GO_OR_CONTINUE_NEXT_EXACT_BOUNDED_TICKET
```
