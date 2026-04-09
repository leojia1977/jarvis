# Release Process

## Goal
Ensure every accepted release comes from one root, one snapshot, one manifest.

## Rules
1. Do not package files manually in Explorer.
2. Do not zip from any folder outside `D:\产品设计\New folder`.
3. Do not upload a zip for review unless it was created by `scripts/package_release.py`.
4. Do not sign off on a package unless `scripts/verify_release.py` passes.
5. Do not treat a Claude review pack as valid unless it contains the current snapshot's governed docs, key files, and test fixtures.

## Import Workflow
1. Put the external material under `incoming/`.
2. Compare it against the current source-of-truth root.
3. Import only the required files into the root.
4. Update the manifest.
5. Run `py -3 scripts/git_preflight.py --mode fast`.
6. Build a Claude review pack if review is needed.
7. Create a release zip.
8. Verify the zip.

## Release Gate Modes

### Fast Gate
Use this during normal iteration:

```powershell
py -3 scripts\git_preflight.py --mode fast
```

It covers:
- compat T3 tests
- compat draft regression
- governed structured backend tests
- vendor replay tests
- T1/T5 self-check

### Full Gate
Use this before formal review, release cut, or sign-off:

```powershell
py -3 scripts\git_preflight.py --mode all
```

It covers:
- fast gate
- Claude review-pack generation
- release packaging
- release verification

## Packaging Command
```powershell
py -3 scripts\package_release.py
```

## Full Preflight Command
```powershell
py -3 scripts\git_preflight.py --mode all
```

## Push Hook Behavior
Normal `git push` only runs `py -3 scripts\git_preflight.py --mode fast`.
Release packaging and verification are explicit steps and should be run before a
formal review or release cut, not hidden inside the push hook.

## Verification Command
```powershell
py -3 scripts\verify_release.py
```

## Acceptance Gate
A release is acceptable only if all of the following are true:
- key files exist
- manifest hashes match the current root
- listed tests pass
- Claude review-pack folder and zip both exist for the current snapshot
- required review-pack entries are present in both the folder and zip
- release zip exists
- release zip hash matches the manifest

## What This Prevents
- Claude reviewing an old zip as if it were latest
- Claude reviewing an incomplete pack as if it were complete
- Codex modifying a different directory than the release directory
- manual packaging drift
- untracked duplicated files
