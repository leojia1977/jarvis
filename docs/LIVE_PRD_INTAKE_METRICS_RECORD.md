# Live PRD Intake Metrics Record

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Live PRD Intake Metrics Record |
| Status | Green docs-only metrics template baseline |
| Scope | Provide the fillable timing and evidence ledger for the first live PRD intake loop |
| Snapshot | S5-LIVE-PRD-INTAKE-RUNBOOK-METRICS-2026-04-22-001 |
| Stage | s5-live-prd-intake-runbook-metrics |
| Baseline commit | `6eb2cd809c89d989b1c8f91d2b5328212b1ea18d` |
| Baseline snapshot | S5-AUTONOMOUS-DELIVERY-DRY-RUN-REHEARSAL-2026-04-22-001 |
| Baseline manifest status | PASS |
| Route | `OPEN_LIVE_PRD_INTAKE_RUNBOOK_METRICS_STAGE` |
| Lane | Green docs-only |

This file is a fillable metrics template. It is not a completed live PRD intake record until a real PRD or explicit product direction is supplied.

It does not authorize implementation, code/test changes, SWE product execution, launch, deployment, external pilot execution, real-data handling, credential handling, public endpoint work, parked-stream reopen, Red execution, AI_COLLAB changes, staging, commit, or push outside governed closeout rules.

## 2. Record Status

Current status:

```text
TEMPLATE_READY_WAITING_FOR_LIVE_PRD
```

Allowed statuses:

- `TEMPLATE_READY_WAITING_FOR_LIVE_PRD`
- `INTAKE_IN_PROGRESS`
- `READY_FOR_ROUTE_SELECTION`
- `NEEDS_CLAUDE_WEB_REVIEW`
- `NEEDS_HUMAN_OR_JARVIS_GO`
- `NEEDS_GREEN_DOCS_ONLY_INTAKE_PREP`
- `HOLD`
- `CLOSED_BY_ROUTE_SELECTION`

## 3. Fillable Intake Record

```text
LIVE_PRD_INTAKE_METRICS_RECORD
Snapshot:
Baseline commit:
PRD/source id:
PRD/source date:
PRD/source owner:
Intake owner:
Source root:
Manifest path:
Intake status:

Timestamps:
- prd_received_at:
- intake_started_at:
- baseline_loaded_at:
- safety_screen_completed_at:
- goals_drafted_at:
- route_candidates_drafted_at:
- review_path_drafted_at:
- ticket_readiness_precheck_at:
- route_recommendation_at:
- intake_completed_at:

Elapsed minutes:
- prd_to_intake_start:
- baseline_load:
- safety_screen:
- goal_non_goal_summary:
- route_candidate_drafting:
- review_path_drafting:
- ticket_readiness_precheck:
- intake_total:

Product summary:
- goals:
- non_goals:
- changed_assumptions:
- affected_product_areas:
- parked_boundary_impact:

Risk and lane:
- candidate_routes:
- lane_by_route:
- red_hold_triggers:
- data_mode:
- external_access:
- real_data:
- credentials_or_secret_material:
- public_endpoint:
- launch_or_deployment:

Review routing:
- Claude Web state:
- Claude Web queued_at:
- Claude Web submitted_at:
- Claude Web verdict_at:
- Claude Web verdict:
- Claude Code state:
- Human/Jarvis state:
- External/security/privacy review state:

Prompt routing:
- prompts_copied_count:
- prompts_sent_count:
- prompt_targets:
- prompt_outputs_received:
- prompt_outputs_pending:
- prompt_holds:

Ticket readiness:
- checklist_outcome:
- exact_behavior_named:
- exact_non_goals_named:
- exact_files_named:
- exact_tests_named:
- review_path_named:
- full_gate_named:
- release_verification_named:
- commit_push_rule_named:
- hold_conditions_named:

SWE eligibility:
- SWE agent use:
- SWE mode:
- SWE output location:
- SWE command path/version:
- SWE independent review:
- SWE HOLD triggers:

Acceleration metrics:
- estimated_intake_time_saved:
- estimated_review_time_saved:
- estimated_swe_time_saved:
- scope_creep_findings:
- overgeneralization_findings:
- hold_count:
- route_reset_count:
- changed_files_count:

Decision:
- intake_decision:
- next_governed_artifact:
- required_approvals:
- unresolved_holds:
- notes:
```

## 4. Timing Rules

Record timestamps in:

```text
YYYY-MM-DD HH:MM Asia/Shanghai
```

Record elapsed time in whole minutes. Use `unknown` only when the timestamp was not captured, and explain why in `notes`.

If a review is queued due Claude Web usage limit, record:

```text
Claude Web state: REVIEW_QUEUED
Claude Web queued_at: <timestamp>
Claude Web verdict: pending
```

Do not record a Claude Web `PASS` unless an actual verdict exists.

## 5. Quality Thresholds

Preferred first-pass targets:

| Metric | Target |
| --- | --- |
| Baseline load | <= 10 minutes |
| Safety screen | <= 10 minutes |
| Goals and non-goals | <= 15 minutes |
| Route candidate drafting | <= 15 minutes |
| Review path drafting | <= 15 minutes |
| Ticket-readiness precheck | <= 15 minutes |
| Total intake to route recommendation | <= 90 minutes |
| Scope creep findings | 0 |
| Over-generalization findings | 0 |
| Unresolved HOLDs before implementation | 0 |

Targets are not authorization. A missed target is a measurement, not permission to skip review, ticket readiness, gate, or HOLD handling.

## 6. Review State Vocabulary

Use only these review states:

- `NOT_REQUIRED`
- `REQUIRED_NOT_READY`
- `REVIEW_QUEUED`
- `REVIEW_SUBMITTED`
- `PASS`
- `PASS_WITH_FINDINGS`
- `HOLD`
- `BLOCKED_BY_USAGE_LIMIT`
- `BLOCKED_BY_MISSING_INPUT`

Claude Code review state is `NOT_REQUIRED` during intake unless a bounded diff exists.

SWE state is `NOT_AUTHORIZED` during intake unless a later exact Yellow item explicitly authorizes it as `bounded implementation accelerator`.

## 7. Non-Authorization

This metrics template does not authorize:

- implementation
- code changes
- test changes
- dependency changes
- fixture creation or modification
- runtime/API/schema behavior changes
- release script changes
- contract changes
- AI_COLLAB changes
- Yellow implementation
- SWE product execution
- direct SWE repo writes
- Red execution
- launch execution
- production deployment
- external pilot execution or readiness claims
- credential handling
- real-data handling
- evidence retention or redaction policy freeze
- public endpoint work
- S5-B/S5-D reopen
- ORDIV work
- S4-A resolver change
- Red-3 action
- AdsPower profile creation/switching
- Claude Web login automation
- cookie/session/token/auth-header/browser-storage/profile-file inspection
- staging, commit, or push outside governed closeout rules

## 8. Next Use

Copy the fillable record into a live intake artifact or update this file only when a real PRD or explicit product direction arrives through a governed input path.

If no PRD or explicit product direction exists, keep the record at:

```text
TEMPLATE_READY_WAITING_FOR_LIVE_PRD
```
