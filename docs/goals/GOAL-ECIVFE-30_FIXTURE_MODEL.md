# GOAL-ECIVFE-30 Fixture Model

## Goal ID

GOAL-ECIVFE-30_FIXTURE_MODEL

Human-readable lane alias:

```text
GOAL-ECI-VFE-30_FIXTURE_MODEL
```

External baseline alias:

```text
GOAL-MVP-30_ECI_VFE_FIXTURE_MODEL
```

## Goal Type

interface

## Goal Statement

Establish the ECI/VFE TypeScript data model, JSON schemas, and metadata-only synthetic fixture set for normal, malicious, false-positive, and prompt-injection cases.

## Primary Executable Object

interface=frontend/src/secupilot/eciVfe/types.ts
schema=schemas/eci_chain_assessment.schema.json
schema=schemas/vfe_forecast_candidate.schema.json
schema=schemas/eci_vfe_correlation.schema.json

- `frontend/src/secupilot/eciVfe/types.ts`
- `schemas/eci_chain_assessment.schema.json`
- `schemas/vfe_forecast_candidate.schema.json`
- `schemas/eci_vfe_correlation.schema.json`

fixture set:

- `mock_data/eci_vfe/eci_cases/*.json`
- `mock_data/eci_vfe/vfe_cases/*.json`

test:

- `frontend/src/secupilot/eciVfe/types.test.ts`

closeout:

- `docs/S6_ECI_VFE_GOAL_30_FIXTURE_MODEL_CLOSEOUT_2026_05_08.md`

## Inputs

- `D:/downloads/ECI_VFE_V0_2_BASELINE_AND_GOAL_QUEUE_2026_05_08.md`
- `docs/S6_ECI_VFE_V0_2_BASELINE_INTAKE_AND_GOAL_MAPPING_2026_05_08.md`
- metadata-only synthetic security event concepts

## Output Paths

- `docs/goals/GOAL-ECIVFE-30_FIXTURE_MODEL.md`
- `frontend/src/secupilot/eciVfe/types.ts`
- `frontend/src/secupilot/eciVfe/types.test.ts`
- `schemas/eci_chain_assessment.schema.json`
- `schemas/vfe_forecast_candidate.schema.json`
- `schemas/eci_vfe_correlation.schema.json`
- `mock_data/eci_vfe/eci_cases/eci_case_001_early_stage_recon.json`
- `mock_data/eci_vfe/eci_cases/eci_case_002_initial_access_to_persistence.json`
- `mock_data/eci_vfe/eci_cases/eci_case_003_lateral_movement_suspected.json`
- `mock_data/eci_vfe/eci_cases/eci_case_004_prompt_injection_process_name.json`
- `mock_data/eci_vfe/eci_cases/eci_case_005_prompt_injection_user_agent.json`
- `mock_data/eci_vfe/eci_cases/eci_case_006_prompt_injection_code_comment.json`
- `mock_data/eci_vfe/vfe_cases/vfe_case_001_config_risk_candidate.json`
- `mock_data/eci_vfe/vfe_cases/vfe_case_002_privilege_boundary_candidate.json`
- `mock_data/eci_vfe/vfe_cases/vfe_case_003_false_positive_candidate.json`
- `mock_data/eci_vfe/vfe_cases/vfe_case_004_malicious_banner_injection.json`
- `mock_data/eci_vfe/vfe_cases/vfe_case_005_malicious_config_comment_injection.json`
- `docs/S6_ECI_VFE_GOAL_30_FIXTURE_MODEL_CLOSEOUT_2026_05_08.md`

## Allowed Files

- `docs/goals/GOAL-ECIVFE-30_FIXTURE_MODEL.md`
- `docs/S6_ECI_VFE_V0_2_BASELINE_INTAKE_AND_GOAL_MAPPING_2026_05_08.md`
- `docs/S6_RC017_UX03_INCIDENT_EVIDENCE_TIMELINE_REVIEW_DECISION_2026_05_08.md`
- `docs/S6_ECI_VFE_GOAL_30_FIXTURE_MODEL_CLOSEOUT_2026_05_08.md`
- `frontend/src/secupilot/eciVfe/types.ts`
- `frontend/src/secupilot/eciVfe/types.test.ts`
- `schemas/eci_chain_assessment.schema.json`
- `schemas/vfe_forecast_candidate.schema.json`
- `schemas/eci_vfe_correlation.schema.json`
- `mock_data/eci_vfe/eci_cases/*.json`
- `mock_data/eci_vfe/vfe_cases/*.json`

## Allowed Scope

- local/offline only
- metadata-only synthetic fixtures
- schema/type changes
- local TypeScript tests
- local build verification

## Forbidden Scope

- real data
- masked-real data
- raw logs
- raw payloads
- host raw evidence
- secrets, tokens, auth headers, cookies, private keys, or API keys
- live Qwen/API/connectors
- PoC, exploit steps, payload, or attacker-readable attack path
- internal topology reachability detail
- production write-back
- autonomous containment, remediation, isolation, blocking, approval, rejection, or action-mode choice
- customer-visible publish, deploy, output, external pilot, or production launch
- push

## Acceptance Commands

```powershell
Set-Location -LiteralPath frontend; npm run test -- --run eciVfe
Set-Location -LiteralPath frontend; npm run build
git -c core.quotepath=false diff --check
```

## HOLD Conditions

- fixture contains real or masked-real data
- fixture contains raw log, raw payload, host raw evidence, secret, token, auth header, or credential
- fixture contains PoC, exploit step, payload, attacker-readable attack path, or internal topology reachability detail
- schema allows LLM output to be authoritative by default
- schema lacks `source_type`, `trust_level`, `is_authoritative`, or `evidence_refs`
- schema lacks VFE `query_context`
- prompt injection fixtures are missing
- TypeScript tests or build fail twice in the same way
- scope expands beyond listed files

## Rollback

- Revert the listed types, schemas, fixtures, tests, and closeout docs.
- Preserve failing test output under a closeout note if failure occurs.
- Leave unrelated untracked artifacts untouched.

## Evidence Contract

- TypeScript fixture/model test output
- frontend build output
- closeout with exact command results
- explicit statement that fixtures are metadata-only and synthetic

## Safety Sentinels

- no `real_data=true`
- no `masked_real_data=true`
- no `raw_log`
- no `raw_payload`
- no `host_raw_evidence`
- no `Authorization`
- no `Bearer`
- no `api_key`
- no `access_token`
- no `private_key`
- no `PoC`
- no `payload`
- no `exploit steps`
- no `attack_path`
- no autonomous action instruction

## Merge Rule

May stage and commit only if all acceptance commands pass and no HOLD condition is observed. Do not push. Do not merge unrelated changes.

## Next Unlock

If PASS, unlock:

```text
GOAL-ECIVFE-33_LOCAL_RULE_ENGINE
```

Human-readable lane alias: `GOAL-ECI-VFE-33_LOCAL_RULE_ENGINE`.

If HOLD, stop and report the exact schema, fixture, or test blocker.

## Commit Posture

One commit for `GOAL-ECIVFE-30`. Stage and commit only listed files. Do not push.
