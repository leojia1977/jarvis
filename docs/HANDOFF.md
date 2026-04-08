# SecuPilot Handoff

## Source Of Truth
- Root path: `D:\产品设计\New folder`
- Rule: only this directory may be treated as runnable truth.
- Any zip, copied folder, or loose file outside this root is input-only material until it is explicitly imported here.

## Current Snapshot
- Snapshot ID: `S3-A-2026-04-08-001`
- Stage: `Sprint 3 runtime productization baseline`
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
   - the exact code files under review
4. In the prompt, state the snapshot ID and tell Claude not to use any other zip or folder as truth.
5. Ask Claude to review or design, not to become the source of code truth.
6. If Claude proposes code changes, apply them back into `D:\产品设计\New folder` and update the manifest.

## Baseline Test Commands
- `py -3 test_t3_hunt.py`
- `py -3 test_secupilot_drafts.py`
- `py -3 -m unittest -q backend.tests.test_t3_hunt backend.tests.test_secupilot_drafts`
- `py -3 selfcheck_t1_t5.py`

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
