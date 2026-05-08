# GOAL-ECIVFE-34 Output Guard

## Goal ID

```text
GOAL-ECIVFE-34_OUTPUT_GUARD
```

## Goal type

```text
validator
```

## Goal statement

```text
Implement the ECI/VFE output guard for schema validation, forbidden content scan, topology disclosure scan, prompt-injection propagation scan, and VFE query-control validation.
```

## Primary executable object

```text
validator=scripts/validate_eci_vfe_output.py
test=backend/tests/test_validate_eci_vfe_output.py
artifact=artifacts/eci_vfe_fixture_runs/rc001/output_guard_scan.json
closeout=docs/S6_FAST_MVP_GOAL_ECIVFE_34_OUTPUT_GUARD_2026_05_08.md
```

## Inputs

```text
artifacts/product_acceleration/next_goal_candidate.json
artifacts/eci_vfe_fixture_runs/rc001/chain_assessment.json
artifacts/eci_vfe_fixture_runs/rc001/forecast_candidates.json
artifacts/eci_vfe_fixture_runs/rc001/correlation_result.json
artifacts/eci_vfe_fixture_runs/rc001/run_record.json
```

## Output paths

```text
docs/goals/GOAL-ECIVFE-34_OUTPUT_GUARD.md
scripts/validate_eci_vfe_output.py
backend/tests/test_validate_eci_vfe_output.py
artifacts/eci_vfe_fixture_runs/rc001/output_guard_scan.json
docs/S6_FAST_MVP_GOAL_ECIVFE_34_OUTPUT_GUARD_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-ECIVFE-34_OUTPUT_GUARD.md
scripts/validate_eci_vfe_output.py
backend/tests/test_validate_eci_vfe_output.py
artifacts/eci_vfe_fixture_runs/rc001/output_guard_scan.json
docs/S6_FAST_MVP_GOAL_ECIVFE_34_OUTPUT_GUARD_2026_05_08.md
```

## Allowed scope

```text
local/offline validation of ECI/VFE analyzer outputs only
schema and safety-boundary guard checks against rc001 output artifacts
focused validator tests including explicit HOLD-path checks
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
API keys
secrets/tokens/auth headers/raw customer logs
live connectors
production write-back
customer-visible publish/deploy/output
external pilot
production launch
backend API/schema migration
push
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-ECIVFE-34_OUTPUT_GUARD.md
py -3 scripts/validate_eci_vfe_output.py --input artifacts/eci_vfe_fixture_runs/rc001
py -3 -m unittest backend.tests.test_validate_eci_vfe_output
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
output_guard_scan.json is missing or not PASS
schema-invalid output passes
forbidden content passes
private CIDR plus reachability plus port/control semantics passes
bulk_export=true passes
prompt injection text propagates into narrative, watch_for, or remediation
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
preserve failing output_guard_scan.json when HOLD is triggered
do not touch unrelated historical residue files
```

## Evidence contract

```text
goal card validator PASS json
output guard validator execution output
unittest PASS output including HOLD-path tests
output_guard_scan.json with status, finding counts, and validated file hashes
closeout report with exact command outcomes and boundary assertions
```

## Safety sentinels

```text
no real_data=true
no masked_real_data=true
no live_qwen_api=true
no production_writeback=true
no customer_visible_output=true
no Authorization header
no Bearer token
no raw_payload
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-ECIVFE-31_CHAIN_INDICATOR_UI because guard-passed outputs are available.
If HOLD, stop and report the failing guard finding before any UI/page implementation.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-ECIVFE-34 output guard
stage and commit only Goal files
do not push
```
