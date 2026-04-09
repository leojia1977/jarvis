# S3-D-4 Snapshot Transition Checklist

## Purpose
Define one authoritative checklist for moving from one governed snapshot to the next without reintroducing source-of-truth drift.

## Use This Checklist When
- a new stage baseline is declared
- a follow-up snapshot replaces the previous governed snapshot
- a Claude review pack is being cut for formal review
- a release zip is being prepared for sign-off

## Authoritative Rule
If this checklist conflicts with scattered prompt text, old notes, or a previous zip, this checklist wins.

## Transition Steps

### 1. Freeze the intended stage boundary
- decide the next snapshot ID and stage label
- confirm what is in scope and what is explicitly deferred
- confirm whether the change is implementation, follow-up, or governance-only

### 2. Update governed docs first
- update `docs/HANDOFF.md`
- update any stage contract or PRD/backlog doc that defines the new baseline
- if a new governed document was added, add it to the release manifest and review-pack inputs

### 3. Update the manifest
- set the new `snapshot.id`
- set the new `snapshot.stage`
- keep `source_of_truth.path` unchanged unless the repository root truly changed
- ensure new governed files appear in `key_files`
- treat prompt header values in the manifest as authoritative

### 4. Build review artifacts from the current root
- run `py -3 scripts/build_claude_review_pack.py`
- confirm the folder and zip are created for the new snapshot
- confirm any new docs, tests, and fixtures are present in the review pack

### 5. Run the governed gate
- normal iteration: `py -3 scripts/git_preflight.py --mode fast`
- formal transition or review cut: `py -3 scripts/git_preflight.py --mode all`

### 6. Review if the stage requires review
- upload only the manifest-backed review pack
- use the generated `CLAUDE_PROMPT.txt` header
- treat Claude output as review-and-decision only
- port accepted changes back through Codex into canonical repo files

### 7. Re-run the full gate after accepted changes
- rebuild review pack
- rebuild release zip
- rerun verify
- confirm `verification.overall_status = PASS`

### 8. Commit and push the governed snapshot
- commit only governed files for the stage
- do not include local-only helper files such as user-owned `CLAUDE.md`
- push the branch only after the governed gate passes

## Required Evidence For A Valid Transition
- `docs/HANDOFF.md` matches the new snapshot
- `releases/release_manifest.json` matches the new snapshot
- `releases/claude_review_pack/<snapshot>/` exists
- `releases/claude-review-pack-<snapshot>.zip` exists
- `releases/secupilot-<snapshot>.zip` exists
- `releases/verify_report.json` shows `overall_status = PASS`

## What Not To Do
- do not cut a new snapshot only in chat text
- do not reuse an old review pack with a new snapshot ID
- do not ask Claude to review files that are not in the generated review pack
- do not push a snapshot that has not passed verify
- do not let wrapper shortcuts redefine the canonical gate

## Exit Criteria
- the snapshot can be reconstructed from `HANDOFF + manifest + review pack + release zip + verify report`
- no stage-critical file is missing from the review pack
- Claude and Codex would both read the same snapshot if asked to review immediately
