# Merge Strategy

## Current Recommendation
Use a standard GitHub pull request from `codex/s3-a-runtime` into `main`.

## Recommended Merge Method
`Squash and merge`

## Why
- the branch is feature-scoped, not a long-lived integration branch
- review feedback may add small fixup commits before merge
- `main` stays easier to read with one merged feature commit per feature line
- the accepted release is tracked by manifest snapshot and release artifacts, so preserving every fixup commit on `main` is less important than keeping `main` clean

## Pre-Merge Gate
Before merge, confirm all of the following:
1. `git status` is clean on `codex/s3-a-runtime`
2. `py -3 scripts/git_preflight.py --mode all` passes
3. `releases/release_manifest.json` shows the intended snapshot
4. `releases/verify_report.json` is `PASS`
5. Claude review, if requested, is based on the generated review pack for the same snapshot

## Merge Sequence
1. Open PR from `codex/s3-a-runtime` to `main`
2. Review with manifest-backed artifacts
3. Resolve any requested fixes on the feature branch
4. Re-run `py -3 scripts/git_preflight.py --mode all`
5. `Squash and merge`
6. On `main`, tag the accepted snapshot ID
7. Generate a fresh release from `main`

## After Merge
- keep the feature branch until post-merge smoke is complete
- only delete the branch after:
  - `main` release verification passes
  - no rollback concerns remain

## What Not To Do
- do not merge from any folder other than `D:\产品设计\New folder`
- do not merge based on stale zips or screenshots
- do not bypass manifest and verification
