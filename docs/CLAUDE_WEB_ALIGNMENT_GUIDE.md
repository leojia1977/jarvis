# Claude Web Alignment Guide

## Purpose
Claude Web cannot directly browse `D:\产品设计\New folder` the way Codex can. To keep both models aligned, Claude must review a governed upload set generated from the current manifest.

## One Rule
Claude must only review files that are:
- inside `D:\产品设计\New folder`, and
- included in the current manifest-backed review pack

Anything else is input-only material, not latest code truth.

## Standard Workflow
1. Open the Git working tree at `D:\产品设计\New folder`.
2. Run `py -3 scripts/build_claude_review_pack.py`.
3. Prefer uploading `releases/claude-review-pack-<snapshot>.zip`.
4. If needed, use `releases/claude_review_pack/<snapshot>/` only as the unpacked source.
5. Paste the generated prompt header from `CLAUDE_PROMPT.txt`.
6. Ask Claude to review, design, or challenge assumptions.
7. Apply any approved changes back through Codex in `D:\产品设计\New folder`.

## Authoritative Upload Set
- treat the generated review pack zip as the minimum and authoritative upload set
- do not maintain a separate manual file list here
- if you need a human-readable cross-check, use the `Claude Web Workflow` section in `docs/HANDOFF.md`
- if the generated review pack and any handwritten list disagree, the generated review pack wins

## Never Do These
- do not upload stale zip files from other folders as current truth
- do not mix duplicate copies of the same file from different roots
- do not ask Claude to become the code-edit source of truth
- do not review screenshots alone without the manifest and source files

## Review Roles
- Claude:
  - PRD review
  - risk review
  - schema review
  - UX and narrative review
- Codex:
  - code changes
  - tests
  - packaging
  - manifest updates

## Output Discipline
When Claude proposes changes:
- treat them as review or decision output
- do not treat them as accepted implementation
- port the accepted change into canonical files with Codex

## Snapshot Transition Discipline
- use [S3D4_SNAPSHOT_TRANSITION_CHECKLIST.md](/D:/产品设计/New%20folder/docs/S3D4_SNAPSHOT_TRANSITION_CHECKLIST.md) as the single transition checklist
- do not advance a snapshot only in chat text
- do not review a snapshot whose `HANDOFF`, `manifest`, and generated prompt header disagree

## Consistency Check
If Claude's prompt header, the handoff file, and the release manifest do not show the same snapshot ID, stop and fix the docs before continuing.
