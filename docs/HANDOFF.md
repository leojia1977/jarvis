# SecuPilot Handoff

## Source Of Truth
- Root path: `D:\产品设计\New folder`
- Rule: only this directory may be treated as runnable truth.
- Any zip, copied folder, or loose file outside this root is input-only material until it is explicitly imported here.

## Current Snapshot
- Snapshot ID: `S4-D-2026-04-10-005`
- Stage: `Sprint 4 operator runbooks and failure triage baseline`
- Owner of code changes: `Codex`
- Owner of product/review decisions: `Claude`

## Current Scope
- Canonical application code now lives under `backend/`.
- Canonical data/build utilities now live under `scripts/`.
- Canonical generated datasets now live under `mock_data/`.
- Root-level `.py` files are compatibility wrappers so the current runnable snapshot is not broken.
- Sprint 3 planning documents now live under `docs/` and are part of the governed handoff set.
- Git workflow scaffolding now lives under `.githooks/`, `.gitignore`, `.gitattributes`, `.gitmessage.txt`, and `scripts/install_git_workflow.py`.
- Runtime productization now lives under `backend/app/main.py`, `backend/app/runtime_service.py`, and `run_runtime.py`.
- Case view contract and shaping layer now live under `docs/SP3_B1_Case_View_Contract.md` and `backend/app/agents/case_view.py`.
- Jarvis case embedding now lives under `backend/app/agents/jarvis_hunt_engine.py` and the `case_view.jarvis_plan` mapping.
- Degraded UX contract now lives under `docs/SP3_B4_Degraded_UX_Contract.md` and the `case_view.executive_summary` / `case_view.analysis_limits` mappings.
- Case contract tests now freeze summary, Jarvis, evidence refs, and degraded action semantics under `backend/tests/test_case_view.py`.
- S3-C-0 adapter contract skeleton now lives under `backend/app/tools/siem_adapter.py`, `docs/S3C0_ADAPTER_CONTRACT.md`, and the orchestrator's `TimeRangeSpec + AdapterResult` flow.
- S3-C follow-up now adds dedicated SIEM timeout handling before tool execution, plus explicit `partial / unavailable / gather timeout / scenario metadata timeout` regression coverage.
- S3-C-1 now adds the first production-facing SIEM adapter path, runtime configuration consumption, and transport-normalization tests under `docs/S3C1_SIEM_ADAPTER_BOUNDARY.md`.
- S3-C-1 follow-up now adds thin vendor field mapping profiles (`splunk_like` / `elastic_like`) and a governed `runtime_mode=production -> investigate_sync -> threat_case` smoke path.
- S3-C-1 hardening now maps non-JSON transport responses to `production_transport_bad_response:*` and exposes `adapter_type / adapter_configured` in runtime readiness.
- S3-C-2 now hardens vendor profiles by filling canonical `activity_name`, escaping `splunk_like` free text, replacing risky `elastic_like query_string` usage, and freezing fixture playback tests under `docs/S3C2_VENDOR_PROFILE_HARDENING.md`.
- S3-C-2 follow-up now proves `activity_name` flows end-to-end through the production smoke path and lowers generic `action` behind `rule.name` in canonical field selection.
- S3-C-3 now adds offline vendor replay fixtures, `ReplayTransport`, and two end-to-end replay tests under `docs/S3C3_VENDOR_REPLAY_SPEC.md` and `backend/tests/test_vendor_replay.py`.
- S3-D-1 now hardens the governed release gate by aligning fast/full gate documentation, requiring review-pack completeness, and expanding verification to review artifacts as first-class acceptance inputs.
- S3-D-2 now freezes wrapper inventory, canonical import guidance, and wrapper retirement criteria under `docs/PROJECT_STRUCTURE.md` and `docs/S3D2_WRAPPER_RETIREMENT_PLAN.md`.
- S3-D-2 follow-up now distinguishes standalone smoke scripts from compatibility test wrappers, moves canonical test commands ahead of wrapper shortcuts, and defines wrapper retirement counter start plus rollback behavior.
- S3-D-3 now freezes runtime operability semantics under `docs/S3D3_RUNTIME_OPERABILITY_CONTRACT.md` and exposes operator-facing `state_class / failure_category / operator_message` fields in runtime health and readiness.
- S3-D-3 follow-up now clarifies `DEGRADED` as a reserved future runtime state, makes `static_data_path` authoritative over the legacy `mock_data_path` alias, and adds log-backed coverage for both mock and production static-data startup failures.
- S3-D-4 now freezes snapshot transition discipline, Claude Web upload rules, and alignment rules so future stage changes are driven by generated review artifacts instead of chat-only instructions.
- S3-D-4 follow-up now adds the missing package step to the snapshot checklist, makes the generated review pack authoritative over handwritten upload lists, and forbids stale zip reuse during review-pack generation.
- SP3-D-13 now records the governance closeout decision under `docs/S3D13_GOVERNANCE_REVIEW_PASS.md`.
- Sprint 4 planning is now frozen under `docs/SPRINT4_PRD.md` and `docs/SPRINT4_JIRA_BACKLOG.md`.
- Sprint 4 planning follow-up now makes `SP4-A-3` the explicit unlock for `SP4-B-1`, requires `SP4-C-1` to freeze persistence backend selection, and clarifies that `SP4-D-1` plus `SP4-D-3` may start in parallel while downstream pilot smoke work waits for `S4-A + S4-B + S4-C`.
- S4-A-1 now freezes the static-data source contract under `docs/S4A1_STATIC_DATA_SOURCE_CONTRACT.md`, `backend/app/tools/static_data_sources.py`, and the new static-data config fields in `backend/app/config.py`.
- S4-A-2 now routes T1 / T4 / T5 bootstrap static data through `backend/app/tools/static_data_adapters.py`, replaces the four direct JSON bootstrap reads in `backend/app/agents/graph.py`, and freezes the adapter baseline under `docs/S4A2_STATIC_DATA_ADAPTER_BASELINE.md`.
- S4-A-3 now adds a canonical host identity resolver under `backend/app/tools/host_identity.py`, routes SIEM asset queries plus T3 / blast target selection through the same resolver, and freezes the behavior under `docs/S4A3_HOST_IDENTITY_RESOLVER.md`.
- S4-A-4 now adds TTL cache semantics for static-data adapters, freezes governed refresh behavior under `docs/S4A4_STATIC_DATA_CACHE_AND_TESTS.md`, and extends regression coverage for cache expiry, missing sources, and static-data readiness classification.
- S4-A-5 now records the governed source integration review closeout under `docs/S4A5_SOURCE_INTEGRATION_REVIEW_PASS.md`, accepts asset inventory as the authoritative host-identity seed for Sprint 4, and explicitly lists unsupported source fields plus deferred source-mode work before downstream pilot execution.
- S4-B-1 now freezes the production-facing EDR process-event contract under `docs/S4B1_EDR_ADAPTER_CONTRACT.md`, `backend/app/tools/edr_adapter.py`, and `backend/tests/test_edr_adapter_contract.py` without changing frozen T3 input or output semantics.
- S4-B-2 now routes T3 process-event ingestion through explicit EDR adapters, replaces the last direct `process_events` bootstrap read in `backend/app/agents/graph.py`, and freezes the baseline under `docs/S4B2_PRODUCTION_EDR_INGESTION_BASELINE.md`.
- S4-B-3 now adds offline EDR replay fixtures plus `EDRReplayTransport`, proves canonical normalization for `crowdstrike_like` and `elastic_defend_like`, and freezes replay validation under `docs/S4B3_EDR_REPLAY_FIXTURES.md`.
- S4-B-4 now proves T3 anomaly detection, persistence detection, IOC extraction, and `partial / degraded` semantics remain stable under production-shaped EDR ingestion, frozen under `docs/S4B4_T3_PRODUCTION_PARITY_TESTS.md`.
- S4-B-4 follow-up now removes machine-local mock-data assumptions from the parity tests and makes `backend/app/tools/siem_adapter.py` safe under standard-logging fallback when `structlog` is unavailable.
- S4-B-5 now closes the telemetry stream review under `docs/S4B5_TELEMETRY_REVIEW_PASS.md`, removes the remaining machine-local EDR test paths, and clarifies that `extra{}` may exist only as audit/debug baggage and must never influence T3 output or case contracts.
- S4-C-1 now freezes the durable case schema, lifecycle status model, action-request record, audit record, and pilot persistence backend choice under `docs/S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md` and `backend/app/tools/persistent_case.py`.
- S4-C-2 now adds a governed SQLite case store, `POST /api/v1/cases`, `GET /api/v1/cases/{case_id}`, immutable record helpers, and retrieval/persistence regression coverage under `docs/S4C2_CASE_STORE_AND_RETRIEVAL_API.md`, `backend/app/tools/case_store.py`, and `backend/tests/test_case_store.py`.
- S4-C-3 now freezes the action-request and approval contract under `docs/S4C3_ACTION_REQUEST_AND_APPROVAL_CONTRACT.md`, adds durable create/submit/approve/reject/cancel helpers plus runtime APIs, and folds the prior unstructured create-case exception path into governed `internal_error` handling.
- S4-C-4 now locks lifecycle regression coverage under `docs/S4C4_CASE_LIFECYCLE_REGRESSION_TESTS.md`, blocks closed-case reject/cancel updates, and proves deterministic create/retrieve/review/approve/close audit history through persisted round-trips.
- S4-C-4 follow-up now routes the lifecycle regression create step through `runtime_service.create_case_sync()` while keeping deterministic case semantics via a controlled investigation output, closing the last review gap before `SP4-C-5`.
- S4-C-5 now records the persisted case lifecycle product closeout under `docs/S4C5_PRODUCT_REVIEW_PASS.md`, accepting `S4-C` as the Sprint 4 baseline for pilot-facing analyst and manager usage.
- S4-D-1 now freezes the pilot environment and secret profile contract under `docs/S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md`, exposes profile-level missing requirements through runtime readiness, and records that `SP4-D-2` must not start until `SP4-A-5` has an explicit governed closeout record.
- S4-D-1 follow-up now treats `siem_vendor=generic_http` as invalid for `pilot_local`, exposes a loopback-host warning for remote pilot access in readiness, removes `mock_data_path` from `pilot_local` optional fields, and clarifies the deterministic lifecycle regression create path in `backend/tests/test_case_lifecycle_regression.py`.
- S4-D-2 now freezes one governed pilot smoke path under `docs/S4D2_PILOT_SMOKE_PATH.md`, exposes `POST /api/v1/pilot-smoke`, and proves `pilot_local readiness -> production-shaped investigate -> persistent create_case -> get_case` through `backend/app/runtime_service.py`, `backend/app/main.py`, and dedicated runtime regression coverage.
- S4-D-2 review follow-up now keeps `pilot_smoke_sync()` on a single readiness snapshot for downstream error payloads, documents the outer `200 OK` vs inner `create_case=201` contract, and adds regression coverage for `time_range` propagation plus investigate/get-case failure stages.
- S4-D-3 now freezes the operator runbook and failure-triage baseline under `docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md`, links governed failure-step triage back from `docs/S4D2_PILOT_SMOKE_PATH.md`, and adds a redacted operator triage artifact checklist under `docs/RELEASE_PROCESS.md`.

## Working Rules
1. Claude and Codex must both read `releases/release_manifest.json` before reviewing or changing anything.
2. Claude must not treat any file outside `D:\产品设计\New folder` as latest code.
3. Codex must make all runnable code changes inside `D:\产品设计\New folder`.
4. Any external zip must first be unpacked under `incoming/<name>_<date>/`.
5. External material becomes valid code only after it is copied into the source-of-truth root and the manifest is updated.
6. A release is valid only if it is created from `scripts/package_release.py`.
7. A release is accepted only if `scripts/verify_release.py` passes.
8. Git hooks and commit template must be installed with `py -3 scripts/install_git_workflow.py`.

## Claude Web Workflow
Because Claude Web cannot directly browse your local filesystem like Codex:

1. Run `py -3 scripts/build_claude_review_pack.py`.
2. Upload the generated review pack or its copied files from `releases/claude_review_pack/<snapshot>/`.
3. Always include:
   - `docs/HANDOFF.md`
   - `contracts/AI_COLLAB_CONTRACT.md`
   - `releases/release_manifest.json`
   - `docs/SPRINT3_PRD.md`
   - `docs/SPRINT3_JIRA_BACKLOG.md`
   - `docs/SP3_B1_Case_View_Contract.md`
   - `docs/SP3_B4_Degraded_UX_Contract.md`
   - `docs/S3C0_ADAPTER_CONTRACT.md`
   - `docs/S3C1_SIEM_ADAPTER_BOUNDARY.md`
   - `docs/S3C2_VENDOR_PROFILE_HARDENING.md`
   - `docs/S3C3_VENDOR_REPLAY_SPEC.md`
   - `docs/S3D_ENGINEERING_HARDENING_PRD.md`
   - `docs/S3D2_WRAPPER_RETIREMENT_PLAN.md`
   - `docs/S3D3_RUNTIME_OPERABILITY_CONTRACT.md`
   - `docs/S3D4_SNAPSHOT_TRANSITION_CHECKLIST.md`
   - `docs/S3D13_GOVERNANCE_REVIEW_PASS.md`
   - `docs/S3D_JIRA_BACKLOG.md`
   - `docs/SPRINT4_PRD.md`
   - `docs/SPRINT4_JIRA_BACKLOG.md`
   - `docs/S4A1_STATIC_DATA_SOURCE_CONTRACT.md`
   - `docs/S4A2_STATIC_DATA_ADAPTER_BASELINE.md`
   - `docs/S4A3_HOST_IDENTITY_RESOLVER.md`
   - `docs/S4A4_STATIC_DATA_CACHE_AND_TESTS.md`
   - `docs/S4B1_EDR_ADAPTER_CONTRACT.md`
   - `docs/S4B2_PRODUCTION_EDR_INGESTION_BASELINE.md`
   - `docs/S4B3_EDR_REPLAY_FIXTURES.md`
   - `docs/S4B4_T3_PRODUCTION_PARITY_TESTS.md`
   - `docs/S4B5_TELEMETRY_REVIEW_PASS.md`
   - `docs/S4C1_PERSISTENT_CASE_SCHEMA_FREEZE.md`
   - `docs/S4C2_CASE_STORE_AND_RETRIEVAL_API.md`
   - `docs/S4C3_ACTION_REQUEST_AND_APPROVAL_CONTRACT.md`
   - `docs/S4C4_CASE_LIFECYCLE_REGRESSION_TESTS.md`
   - `docs/S4C5_PRODUCT_REVIEW_PASS.md`
   - `docs/S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md`
   - `docs/S4A5_SOURCE_INTEGRATION_REVIEW_PASS.md`
   - `docs/S4D2_PILOT_SMOKE_PATH.md`
   - `docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md`
   - the exact code files under review
4. In the prompt, state the snapshot ID and tell Claude not to use any other zip or folder as truth.
5. Ask Claude to review or design, not to become the source of code truth.
6. If Claude proposes code changes, apply them back into `D:\产品设计\New folder` and update the manifest.

## Baseline Test Commands

### Canonical Authoritative Gate
- `py -3 -m unittest -q backend.tests.test_t3_hunt backend.tests.test_secupilot_drafts backend.tests.test_runtime_service backend.tests.test_case_view backend.tests.test_siem_adapter_contract backend.tests.test_vendor_replay backend.tests.test_static_data_contracts backend.tests.test_static_data_adapters backend.tests.test_host_identity_resolver backend.tests.test_edr_adapter_contract backend.tests.test_edr_replay backend.tests.test_t3_production_parity backend.tests.test_persistent_case_contract backend.tests.test_case_action_request_contract backend.tests.test_case_store backend.tests.test_case_lifecycle_regression`
- `py -3 -m unittest -q backend.tests.test_environment_profile`
- `py -3 -m unittest -q backend.tests.test_persistent_case_contract`
- `py -3 -m unittest -q backend.tests.test_case_action_request_contract`
- `py -3 -m unittest -q backend.tests.test_case_store`
- `py -3 -m unittest -q backend.tests.test_case_lifecycle_regression`
- `py -3 -m unittest -q backend.tests.test_vendor_replay`

### Legacy / Compat Shortcuts
- `py -3 test_t3_hunt.py`
- `py -3 test_secupilot_drafts.py`
- `py -3 selfcheck_t1_t5.py`

The canonical suite above is the authoritative gate. Wrapper commands remain only for compatibility until retirement criteria are met.

## Release Outputs
- Manifest: `releases/release_manifest.json`
- Packages: `releases/*.zip`
- Verification report: `releases/verify_report.json`

## Next Expected Use
- Build a Claude review pack from the current snapshot.
- Review current snapshot with Claude using the manifest and the generated review pack.
- Treat `docs/S4A5_SOURCE_INTEGRATION_REVIEW_PASS.md` plus `docs/S4D2_PILOT_SMOKE_PATH.md` as the governed baseline for any `SP4-D-2` review.
- Treat `docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md` plus `docs/RELEASE_PROCESS.md` as the governed operator baseline before extending validation-gate work.
- Use `POST /api/v1/pilot-smoke` as the canonical pilot round-trip proof when connecting `S4-D-3` operator runbooks to `SP4-D-4` validation-gate coverage.
- Make code changes only in `D:\产品设计\New folder`.
- Package from this root only.
- Keep Git as the only code-truth layer and use release artifacts only for delivery.
