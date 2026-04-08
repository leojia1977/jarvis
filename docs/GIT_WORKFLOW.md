# Git Workflow

## Purpose
This repository uses Git as the code-truth layer for `D:\产品设计\New folder`.
Claude review packs and release zips are generated from the Git working tree, not from ad hoc copied folders.

## Branch Model
- default branch: `main`
- implementation branches: `codex/<scope>`
- documentation or review branches if ever needed: `docs/<scope>`

## Rules
1. Only `D:\产品设计\New folder` may be treated as runnable truth.
2. All code changes must land in canonical files under `backend/`, `scripts/`, `mock_data/`, and governed docs.
3. Root-level compatibility wrappers may be edited only when needed to preserve the runnable snapshot.
4. Any external zip must first be placed under `incoming/`.
5. A release is valid only if it is produced by `scripts/package_release.py`.
6. A release is accepted only if `scripts/verify_release.py` passes.

## Daily Workflow
1. `git status`
2. create or switch to a branch such as `codex/s3-a-runtime`
3. make changes in canonical files
4. run `py -3 scripts/git_preflight.py --mode fast`
5. review diffs with `git diff`
6. commit with the template from `.gitmessage.txt`

## Release Workflow
1. run `py -3 scripts/build_claude_review_pack.py`
2. run `py -3 scripts/package_release.py`
3. run `py -3 scripts/verify_release.py`
4. tag the accepted snapshot with the manifest snapshot ID

## Private Remote Setup
1. create your private GitHub repository
2. run `py -3 scripts/setup_github_remote.py --url <YOUR_REPO_URL>`
3. verify with `git remote -v`
4. push with `git push -u origin main`

## Hooks
- `pre-commit` runs fast local checks
- `pre-push` runs release-grade packaging and verification

Install them once with:

```powershell
py -3 scripts/install_git_workflow.py
```

## Commit Guidance
- use small, reviewable commits
- keep snapshot and manifest updates together with the code they describe
- do not commit external zips as source code truth

## Claude And Codex
- Claude reviews design, risk, UX, and schema semantics
- Codex implements code, tests, release, and manifest updates
- Claude must review only files from the current manifest-backed review pack
