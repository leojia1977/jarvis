# SecuPilot Handoff

## Source Of Truth
- Root path: `D:\产品设计\New folder`
- Rule: only this directory may be treated as runnable truth.
- Any zip, copied folder, or loose file outside this root is input-only material until it is explicitly imported here.

## Current Snapshot
- Snapshot ID: `S4-A-2026-04-09-001`
- Stage: `Sprint 4 static data source contract freeze`
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
   - the exact code files under review
4. In the prompt, state the snapshot ID and tell Claude not to use any other zip or folder as truth.
5. Ask Claude to review or design, not to become the source of code truth.
6. If Claude proposes code changes, apply them back into `D:\产品设计\New folder` and update the manifest.

## Baseline Test Commands

### Canonical Authoritative Gate
- `py -3 -m unittest -q backend.tests.test_t3_hunt backend.tests.test_secupilot_drafts backend.tests.test_runtime_service backend.tests.test_case_view backend.tests.test_siem_adapter_contract backend.tests.test_vendor_replay backend.tests.test_static_data_contracts`
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
- Make code changes only in `D:\产品设计\New folder`.
- Package from this root only.
- Keep Git as the only code-truth layer and use release artifacts only for delivery.
