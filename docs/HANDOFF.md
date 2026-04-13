# SecuPilot Handoff

## Source Of Truth
- Root path: `D:\产品设计\New folder`
- Rule: only this directory may be treated as runnable truth.
- Any zip, copied folder, or loose file outside this root is input-only material until it is explicitly imported here.

## Current Snapshot
- Snapshot ID: `S5-PILOT-INPUT-2026-04-13-002`
- Stage: `external-pilot-input-assessment`
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
- S4-D-4 now freezes the pilot validation gate baseline under `docs/S4D4_PILOT_VALIDATION_GATE.md`, exposes `py -3 scripts/git_preflight.py --mode pilot` as the deterministic gate entry, and extends `scripts/verify_release.py` to prove `S4D2 / S4D3 / S4D4` pilot-governed artifacts are present in the manifest, review pack, and release zip.
- S4-D-5 now records the readiness review record under `docs/S4D5_PILOT_READINESS_REVIEW.md`, the review closeout under `docs/S4D5_PILOT_READINESS_REVIEW_PASS.md`, and accepts the current D-stream baseline as the pilot-ready operator baseline for Sprint 4.
- Sprint 4 integrated closeout now records `docs/S4_SPRINT4_PILOT_BASELINE_REVIEW.md` as the integrated review record and `docs/S4_SPRINT4_PILOT_BASELINE_REVIEW_PASS.md` as the integrated PASS closeout; `S4-A / S4-B / S4-C / S4-D` jointly satisfy the Sprint 4 Delivery Definition, and the current governed baseline is accepted as the Sprint 4 integrated pilot baseline for controlled pilot use.
- Sprint 5 planning now records `docs/SPRINT5_DISCOVERY_BRIEF.md` as the Sprint 5 discovery record, `docs/SPRINT5_PRD.md` as the Sprint 5 PRD draft baseline, and `docs/SPRINT5_JIRA_BACKLOG.md` as the Sprint 5 backlog baseline. Sprint 5 starts from `S4-INTEGRATED-2026-04-13-001`; `S5-A` is the first product direction, `S5-E` is a lightweight parallel governance decision, `S5-C` is conditional, and `S5-B / S5-D` remain discovery-limited until external inputs exist.
- S5-A-1 now records `docs/S5A1_PILOT_PREPARATION_CHECKLIST.md` as the controlled pilot preparation checklist. It separates preparation, dry-run, redaction, sign-off, and external pilot execution boundaries, and confirms S4/S5 governed evidence without starting external pilot execution.
- S5-A-2 now records `docs/S5A2_DRY_RUN_EVIDENCE_TEMPLATE.md` as the dry-run evidence template baseline. It converts the S5-A-1 preparation checklist into fillable evidence capture for the pilot validation gate and `POST /api/v1/pilot-smoke` path while preserving the dry-run-only boundary.
- S5-A-3 now records `docs/S5A3_PILOT_RUN_LOG_REDACTION_BOUNDARY.md` as the pilot run log evidence redaction boundary baseline. It defines what dry-run, pilot-prep, and future sign-off evidence may retain without replacing S4-D-3 / `RELEASE_PROCESS` operator escalation triage redaction rules.
- S5-A-4 now records `docs/S5A4_PILOT_SIGN_OFF_CHECKLIST.md` as the pilot sign-off checklist baseline. It defines `PASS` / `HOLD` / `NEEDS_DECISION` judgment for controlled dry-run sign-off without creating a real customer/operator sign-off record or authorizing external pilot execution.
- S5-A-5 now records `docs/S5A5_DRY_RUN_EXTERNAL_PILOT_BOUNDARY_CLOSEOUT.md` as the dry-run versus external pilot boundary closeout. It closes the dry-run/external-pilot boundary for the S5-A preparation package, but it is not the S5-A stream review pass.
- S5-A Controlled Pilot Preparation now records `docs/S5A_REVIEW_PASS.md` as the stream-level review pass. S5-A is closed as a governed controlled pilot preparation baseline. This does not authorize external pilot execution. External pilot execution, S5-C triggering, S5-E governance, and S5-B/S5-D scope expansion remain gated on separate product/governance decisions.
- Post-S5-A decision checkpoint now records `docs/S5_EXTERNAL_PILOT_DECISION_CHECKPOINT.md` as the governed post-S5-A decision record. S5-A is closed as a governed controlled pilot preparation baseline. This checkpoint does not authorize external pilot execution. The recommended immediate next step is `S5-E-1` lightweight governance review while external pilot inputs are gathered, unless product/governance can immediately provide all required pilot scope, role, access, evidence retention, redaction, go/no-go, and rollback/hold authority inputs.
- S5-E-1 now records `docs/S5E1_AI_COLLAB_OPERATING_MODEL_REVIEW.md` as the AI collaboration operating model review closeout. S5-E-1 reviews `docs/AI_COLLAB_OPERATING_MODEL.md` and records `NEEDS_LIGHT_REVISION`. `docs/AI_COLLAB_OPERATING_MODEL.md` remains ungoverned and must not be treated as a governed contract. Future governance of `docs/AI_COLLAB_OPERATING_MODEL.md` requires a separate light-revision task, snapshot transition, manifest update, verification refresh, and review-pack alignment.
- S5-E-2 now records `docs/S5E2_AI_COLLAB_LIGHT_REVISION_CLOSEOUT.md` as the AI collaboration operating model light revision closeout. `docs/AI_COLLAB_OPERATING_MODEL.md` was lightly revised but remains ungoverned. `docs/S5E2_AI_COLLAB_LIGHT_REVISION_CLOSEOUT.md` is the governed closeout record. Future governance of `docs/AI_COLLAB_OPERATING_MODEL.md` requires a separate snapshot path and manifest entry.
- S5-E-3 now records `docs/S5E3_AI_COLLAB_GOVERNANCE_DECISION.md` as the AI collaboration operating model governance decision closeout. S5-E-3 records `APPROVE_GOVERNANCE` for `docs/AI_COLLAB_OPERATING_MODEL.md` as a future governed artifact. This does not itself govern `docs/AI_COLLAB_OPERATING_MODEL.md`; it must remain outside manifest key_files until a separate governance snapshot explicitly adds it.
- S5-E-4 now governs `docs/AI_COLLAB_OPERATING_MODEL.md` as the team collaboration operating model. The document governs collaboration workflow only; it does not override product PRDs, runtime contracts, `docs/RELEASE_PROCESS.md`, manifest, `verify_report`, review pack, release zip, or full gate requirements, and it does not introduce external tool dependencies.
- Sprint 5 midpoint decision now records `docs/S5_MIDPOINT_DECISION.md` as the governed planning decision record. S5-A Controlled Pilot Preparation is closed, S5-E AI Collaboration Operating Model is governed as collaboration workflow guidance, external pilot execution remains unauthorized, and the next product path requires product/governance confirmation before implementation begins. The midpoint recommendation is conditional: external pilot decision package only if all required pilot inputs are available; S5-C only with dry-run feedback or explicit product decision; S5-B/S5-D discovery only if external inputs are available.
- External pilot input intake now records `docs/S5_EXTERNAL_PILOT_INPUT_INTAKE.md` as the governed intake checklist. The intake defines the seven required input categories for any later external pilot decision package, does not authorize external pilot execution, and records that all seven categories currently require explicit product/governance confirmation before a decision package can proceed.
- External pilot input assessment now records `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md` as the initial governed assessment state for the seven external pilot input categories. All seven categories are currently `UNKNOWN` in governed repo evidence, the project cannot draft an external pilot decision package yet, and external pilot execution remains unauthorized.

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
   - `docs/S4D4_PILOT_VALIDATION_GATE.md`
   - `docs/S4D5_PILOT_READINESS_REVIEW.md`
   - `docs/S4D5_PILOT_READINESS_REVIEW_PASS.md`
   - `docs/S4_SPRINT4_PILOT_BASELINE_REVIEW.md`
   - `docs/S4_SPRINT4_PILOT_BASELINE_REVIEW_PASS.md`
   - `docs/SPRINT5_DISCOVERY_BRIEF.md`
   - `docs/SPRINT5_PRD.md`
   - `docs/SPRINT5_JIRA_BACKLOG.md`
   - `docs/S5A1_PILOT_PREPARATION_CHECKLIST.md`
   - `docs/S5A2_DRY_RUN_EVIDENCE_TEMPLATE.md`
   - `docs/S5A3_PILOT_RUN_LOG_REDACTION_BOUNDARY.md`
   - `docs/S5A4_PILOT_SIGN_OFF_CHECKLIST.md`
   - `docs/S5A5_DRY_RUN_EXTERNAL_PILOT_BOUNDARY_CLOSEOUT.md`
   - `docs/S5A_REVIEW_PASS.md`
   - `docs/S5_EXTERNAL_PILOT_DECISION_CHECKPOINT.md`
   - `docs/S5E1_AI_COLLAB_OPERATING_MODEL_REVIEW.md`
   - `docs/S5E2_AI_COLLAB_LIGHT_REVISION_CLOSEOUT.md`
   - `docs/S5E3_AI_COLLAB_GOVERNANCE_DECISION.md`
   - `docs/AI_COLLAB_OPERATING_MODEL.md`
   - `docs/S5_MIDPOINT_DECISION.md`
   - `docs/S5_EXTERNAL_PILOT_INPUT_INTAKE.md`
   - `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md`
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
- Treat `docs/S4D1_ENVIRONMENT_AND_SECRET_PROFILE_FREEZE.md` plus `docs/S4D2_PILOT_SMOKE_PATH.md` plus `docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md` plus `docs/S4D4_PILOT_VALIDATION_GATE.md` plus `docs/S4D5_PILOT_READINESS_REVIEW.md` plus `docs/S4D5_PILOT_READINESS_REVIEW_PASS.md` as the governed pilot-readiness baseline before any pilot execution or sign-off activity.
- Treat `S4-INTEGRATED-2026-04-13-001` as the governed Sprint 4 integrated pilot baseline before Sprint 5 planning, external pilot preparation, or pilot sign-off activity.
- Treat `S5-PLAN-2026-04-13-001` as the governed Sprint 5 planning baseline before starting `S5-A` or `S5-E` work.
- Treat `docs/S5A1_PILOT_PREPARATION_CHECKLIST.md` as the governed upstream checklist before `S5-A-2` dry-run evidence template work.
- Use `docs/S5_EXTERNAL_PILOT_DECISION_CHECKPOINT.md` to choose the next path: `S5-E-1` lightweight governance review as the default immediate next step while pilot inputs are gathered; external pilot decision package only if all required pilot decision inputs are available; `S5-C` only with dry-run feedback or explicit product decision; `S5-B / S5-D` discovery only if external inputs are available.
- Use `docs/AI_COLLAB_OPERATING_MODEL.md` as governed collaboration workflow guidance for future multi-tool work.
- Product/runtime decisions remain governed by their own PRDs, contracts, tests, and release process.
- Use `docs/S5_MIDPOINT_DECISION.md` to choose the next mainline. No implementation stream should start from chat-only context without a structured ticket and governed baseline check.
- Use `docs/S5_EXTERNAL_PILOT_INPUT_INTAKE.md` to collect or confirm the seven external pilot inputs. If all seven are provided or explicitly accepted, the next step may be an external pilot decision package; if not, continue collecting inputs or choose `S5-C` / `S5-B` / `S5-D` according to governed midpoint criteria.
- Use `docs/S5_EXTERNAL_PILOT_INPUT_ASSESSMENT.md` to collect or explicitly accept the seven external pilot inputs. If all seven become `PROVIDED` or explicitly accepted by product/governance, an external pilot decision package may be drafted; if inputs remain `UNKNOWN` and product explicitly chooses case workflow hardening, proceed to S5-C planning. `S5-B / S5-D` remain discovery-only unless source/telemetry inputs are available.
- Use `py -3 scripts/git_preflight.py --mode pilot` as the canonical deterministic gate entry for pilot validation evidence refresh.
- Make code changes only in `D:\产品设计\New folder`.
- Package from this root only.
- Keep Git as the only code-truth layer and use release artifacts only for delivery.
