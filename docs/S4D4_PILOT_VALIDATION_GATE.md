# S4-D-4 Pilot Validation Gate

## Goal
Define one deterministic validation gate that proves the governed Sprint 4 pilot artifacts, release inputs, and verification outputs are present together before operator-facing readiness review expands further.

## Scope
- define one canonical pilot validation gate entry
- reuse existing governed tests, review-pack generation, packaging, and release verification steps
- prove the governed pilot artifacts are included in both review and release outputs
- connect `SP4-D-2`, `SP4-D-3`, and `SP4-D-5` without changing runtime behavior

## Non-Goals
- no new runtime API behavior
- no replacement of the governed `POST /api/v1/pilot-smoke` path
- no manual operator exercise checklist beyond the artifacts already frozen in `S4-D-2` and `S4-D-3`
- no full pilot-readiness sign-off; that belongs to `SP4-D-5`

## Deterministic Gate Entry
Canonical command:

```powershell
py -3 scripts\git_preflight.py --mode pilot
```

Intent:
- run one repeatable pilot validation gate from the source-of-truth root
- keep the entry stable even if the underlying command list evolves later
- avoid requiring operators or reviewers to reconstruct the right sequence from chat or memory

Implementation note:
- `--mode all` remains the governed full-gate closeout path
- for the `S4-D-4` baseline, `--mode pilot` is the named pilot-validation entry and currently reuses the same underlying governed checks as the full release path

## Governed Pilot Inputs
The pilot validation gate depends on these governed inputs being aligned to the same snapshot:
- `docs/HANDOFF.md`
- `releases/release_manifest.json`
- `docs/S4D2_PILOT_SMOKE_PATH.md`
- `docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md`
- `docs/S4D4_PILOT_VALIDATION_GATE.md`
- the governed backend test inventory already listed in the manifest
- the governed release-pack and review-pack scripts

## What The Gate Must Prove
The pilot validation gate is acceptable only when it proves all of the following:
- the governed backend test suite still passes
- the snapshot can generate a Claude review pack from the current source-of-truth root
- the snapshot can generate a release zip from the current source-of-truth root
- release verification can prove the pilot-governed docs exist and are present in:
  - manifest-declared key files
  - the Claude review pack
  - the release zip
- release verification remains PASS only when those pilot artifacts and the existing governed checks all pass together

## Review Pack And Release Verification Expectations
Review-pack generation should make the pilot-governed docs reviewable in one uploadable set.

Release verification should explicitly prove the presence of:
- `docs/S4D2_PILOT_SMOKE_PATH.md`
- `docs/S4D3_OPERATOR_RUNBOOKS_AND_FAILURE_TRIAGE.md`
- `docs/S4D4_PILOT_VALIDATION_GATE.md`

The verification output should stay clear and restrained:
- one named pilot-validation result
- one deterministic gate entry reference
- one per-artifact breakdown that shows manifest, review-pack, and release-zip inclusion

## Relationship To Other D-Stream Items

### `SP4-D-2`
- provides the governed pilot round-trip baseline
- defines what the pilot smoke path must prove

### `SP4-D-3`
- provides the operator runbook and failure-triage baseline
- defines how operators interpret readiness and pilot-smoke failures

### `SP4-D-4`
- proves those governed pilot artifacts are actually packaged, reviewable, and verifiable through one deterministic gate

### `SP4-D-5`
- consumes the `S4-D-2` path baseline, the `S4-D-3` operator baseline, and the `S4-D-4` validation gate as readiness-review inputs

## Acceptance
- pilot path has a deterministic gate entry
- the gate entry is documented once under governed docs
- release verification can prove pilot artifacts and checks are present
- the result is suitable as the minimum governed validation baseline before `SP4-D-5`
