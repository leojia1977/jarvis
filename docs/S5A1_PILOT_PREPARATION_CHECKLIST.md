# S5-A-1 Pilot Preparation Checklist

## Goal
Define the minimum controlled pilot preparation checklist for SecuPilot after the governed Sprint 5 planning baseline.

This checklist prepares the project for pilot dry-run and later sign-off work. It does not start an external pilot, connect real external systems, or replace the governed Sprint 4 readiness, smoke-path, runbook, and validation evidence.

## Scope
- Confirm the source-of-truth repo, branch, snapshot, and governed evidence before pilot-prep work proceeds.
- Confirm the `pilot_local` readiness assumptions that must be true before dry-run evidence is collected in `S5-A-2`.
- Confirm case-store and smoke-path readiness assumptions without executing or redefining the full smoke path.
- Record the boundaries between preparation, dry-run, redaction, sign-off, and external pilot execution.
- Provide a clean handoff into `S5-A-2 Pilot Dry-Run Evidence Template`.

## Baseline
- source of truth: `D:\产品设计\New folder`
- current governed snapshot: `S5-PLAN-2026-04-13-001`
- current branch: `codex/s3-a-runtime`
- Sprint 5 planning baseline:
  - `docs/SPRINT5_DISCOVERY_BRIEF.md`
  - `docs/SPRINT5_PRD.md`
  - `docs/SPRINT5_JIRA_BACKLOG.md`
- Sprint 4 integrated pilot baseline:
  - `docs/S4_SPRINT4_PILOT_BASELINE_REVIEW_PASS.md`
  - `docs/S4D5_PILOT_READINESS_REVIEW_PASS.md`
- governed release evidence:
  - `releases/release_manifest.json`
  - `releases/verify_report.json`

## Preparation Boundaries
- `S5-A-1` is pilot preparation, not external pilot execution.
- Dry-run completion does not equal external pilot start.
- This checklist does not require a real SIEM, EDR, source system, customer environment, or external pilot participant.
- Evidence should come from governed repo artifacts or local dry-run outputs.
- Preparation evidence must not record secret values, raw credentials, bearer tokens, API keys, Authorization headers, cookies, full connection strings, or sensitive customer data.
- This checklist does not change runtime readiness semantics, the governed `POST /api/v1/pilot-smoke` path, case lifecycle contracts, adapter contracts, or release governance rules.

## Governed Evidence To Confirm
- `current snapshot`: `S5-PLAN-2026-04-13-001`
- `Sprint 4 integrated pilot baseline pass`: `docs/S4_SPRINT4_PILOT_BASELINE_REVIEW_PASS.md`
- `S4-D-1 environment / secret profile`: `docs/S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md`
- `S4-D-2 pilot smoke path`: `docs/S4D2_PILOT_SMOKE_PATH.md`
- `S4-D-3 operator runbook and failure triage`: `docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md`
- `S4-D-4 pilot validation gate`: `docs/S4D4_PILOT_VALIDATION_GATE.md`
- `canonical dry-run evidence collection gate entry`: `py -3 scripts\git_preflight.py --mode pilot`, inherited from the `S4-D-4` pilot validation gate
- `S4-D-5 pilot readiness pass`: `docs/S4D5_PILOT_READINESS_REVIEW_PASS.md`
- `release_manifest`: `releases/release_manifest.json`
- `verify_report`: `releases/verify_report.json`

Evidence confirmation should verify that these artifacts are present in the source-of-truth repo and aligned to the current governed snapshot. It should not rely on old zip files, screenshots, copied folders, or chat-only claims.

## Pilot Preparation Checklist

### 1. Source-Of-Truth Root Confirmation
- Confirm the working root is `D:\产品设计\New folder`.
- Confirm no repo-external file, old zip, screenshot, or historical directory is being treated as latest runnable truth.
- Confirm all pilot-prep references point back to governed repo files.

### 2. Branch / Snapshot Confirmation
- Confirm the active branch is `codex/s3-a-runtime`.
- Confirm the governed planning snapshot is `S5-PLAN-2026-04-13-001`.
- Confirm Sprint 5 starts from `S4-INTEGRATED-2026-04-13-001`.
- Confirm this checklist remains a draft until it is later included in a governed S5-A closeout.

### 3. Governed Evidence Confirmation
- Confirm `docs/SPRINT5_PRD.md` makes `S5-A Controlled Pilot Preparation` the first product direction.
- Confirm `docs/SPRINT5_JIRA_BACKLOG.md` records `S5-A-1 Pilot Preparation Checklist` as a `DOC` ticket.
- Confirm `docs/S4_SPRINT4_PILOT_BASELINE_REVIEW_PASS.md` accepts the integrated Sprint 4 baseline as coherent enough for controlled pilot use.
- Confirm `docs/S4D5_PILOT_READINESS_REVIEW_PASS.md` accepts the D-stream operator baseline for pilot readiness.
- Confirm `py -3 scripts\git_preflight.py --mode pilot` is the dry-run evidence collection canonical gate entry from `docs/S4D4_PILOT_VALIDATION_GATE.md`.
- Confirm `releases/release_manifest.json` and `releases/verify_report.json` identify the current governed snapshot and passing release verification evidence.

### 4. `pilot_local` Readiness Assumptions
- Confirm `pilot_local` is the intended preparation profile.
- Confirm the expected runtime mode remains `runtime_mode=production`.
- Confirm `static_data_path` is explicit and `pilot_local` does not rely on legacy `mock_data_path` fallback.
- Confirm `siem_vendor` is expected to be `splunk_like` or `elastic_like`, not `generic_http`.
- Confirm `siem_base_url` is configured when readiness is later evaluated.
- Confirm `siem_auth_token` is required by name but its value must never be recorded.
- Confirm `edr_source_mode` is explicitly set.
- Confirm `edr_auth_token` is required by name only when `edr_source_mode=api`; its value must never be recorded.
- If dry-run or later pilot preparation requires remote analyst / manager access, confirm `server_host` does not remain `127.0.0.1`.
- Treat loopback `server_host` as a readiness warning that remote pilot access is blocked, not as an ignorable detail.
- Confirm readiness interpretation remains based on governed fields including `environment_profile`, `profile_contract_ready`, `profile_contract_missing`, `state_class`, `failure_category`, `reasons`, and `operator_message`.

### 5. Case-Store Readiness Assumptions
- Confirm the expected case store backend remains `case_store_backend=sqlite_local`.
- Confirm `case_store_path` must be writable before smoke-path dry-run evidence is collected.
- Confirm `case_store_ready=true` is part of the operator-facing smoke-path prerequisite set.
- Confirm case-store failures should be triaged through the governed S4-D-3 case-store failure guidance.

### 6. Smoke-Path Readiness Assumptions
- Confirm the governed smoke endpoint remains `POST /api/v1/pilot-smoke`.
- Confirm the governed path ID remains `pilot_local_production_case_round_trip`.
- Confirm smoke-path success requires the governed order:
  - `readiness`
  - `investigate`
  - `create_case`
  - `get_case`
- Confirm the internal `create_case` step should report `http_status=201` when the smoke path succeeds.
- Confirm `smoke_path.failed_step=null` is required for success.
- Confirm failure triage must use `smoke_path.failed_step` and `smoke_path.steps` instead of relying only on the outer HTTP status.

### 7. Redaction Reminder
- Do not record secret values, raw credentials, bearer tokens, API keys, Authorization headers, cookies, full connection strings, or sensitive customer data.
- It is acceptable to record missing field names and missing secret names, such as entries from `profile_contract_missing` or `required_secret_names`.
- Pilot-prep evidence should be redacted before it is handed to review, release, or external sign-off workflows.
- The detailed pilot run log evidence redaction boundary belongs to `S5-A-3`; this checklist only records the reminder and handoff.

### 8. Dry-Run Evidence Handoff To `S5-A-2`
- Confirm the checklist is complete before `S5-A-2` defines the dry-run evidence template.
- Handoff to `S5-A-2` should include which governed artifacts are confirmed and which local dry-run outputs are expected.
- Do not use this checklist as the final evidence template; `S5-A-2` owns that template.

### 9. Sign-Off Handoff To `S5-A-4`
- Confirm this checklist does not approve external pilot execution.
- Confirm dry-run completion will not automatically start an external pilot.
- Handoff to `S5-A-4` should include the preparation checklist status, dry-run evidence status from `S5-A-2`, and redaction boundary status from `S5-A-3`.
- Do not use this checklist as the final pilot sign-off checklist; `S5-A-4` owns that checklist.

## Dry-Run Boundary
- A dry run is an internal preparation activity against governed repo evidence or local dry-run outputs.
- A dry run may confirm readiness assumptions, smoke-path evidence expectations, release verification evidence, and operator handoff clarity.
- A dry run must not be represented as real external pilot feedback.
- A dry run must not require real external SIEM, EDR, source systems, customer data, or production credentials.
- Dry-run evidence details belong to `S5-A-2`.

## External Pilot Execution Boundary
- External pilot execution is out of scope for `S5-A-1`.
- External pilot execution must not begin solely because this checklist is complete.
- External pilot execution requires later sign-off, explicit approval, and any required external inputs beyond this checklist.
- This checklist may prepare materials for future sign-off, but it does not authorize deployment, external operator onboarding, live data collection, or customer-facing activity.

## Not Required For S5-A-1
- no real SIEM connection
- no real EDR connection
- no real production source-system connection
- no external pilot participant
- no real customer data
- no secret value collection
- no new runtime API behavior
- no new case lifecycle behavior
- no full dry-run evidence template
- no final pilot run log evidence redaction boundary
- no final pilot sign-off checklist
- no governance closeout

## Handoff To S5-A-2
`S5-A-2 Pilot Dry-Run Evidence Template` should consume this checklist and define the actual dry-run evidence template.

The handoff should include:
- confirmed source-of-truth root and branch
- confirmed governed snapshot
- confirmed governed evidence set
- confirmed `pilot_local` readiness assumptions
- confirmed case-store readiness assumptions
- confirmed smoke-path readiness assumptions
- redaction reminder and the need for the separate `S5-A-3` boundary
- explicit statement that dry-run completion does not start the external pilot

## Acceptance
`S5-A-1 Pilot Preparation Checklist` is complete when:
- the checklist exists as a focused preparation document
- it clearly states that `S5-A-1` is pilot preparation, not external pilot execution
- it clearly states that dry-run completion does not equal external pilot start
- it does not require real SIEM, EDR, or source-system connectivity
- it does not request secret values, raw credentials, bearer tokens, API keys, or sensitive customer data
- it anchors preparation evidence to governed repo artifacts or local dry-run outputs
- it confirms the governed evidence set required before `S5-A-2`
- it hands off to `S5-A-2`, `S5-A-3`, and `S5-A-4` without prematurely writing those documents
