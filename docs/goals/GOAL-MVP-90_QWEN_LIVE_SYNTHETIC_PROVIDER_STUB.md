# GOAL-MVP-90_QWEN_LIVE_SYNTHETIC_PROVIDER_STUB

## Goal ID

```text
GOAL-MVP-90_QWEN_LIVE_SYNTHETIC_PROVIDER_STUB
```

## Goal type

```text
script
interface
run-artifact
```

## Goal statement

```text
Create a deterministic no-network Qwen synthetic provider stub that consumes local synthetic fact bundles and emits metadata-only provider output compatible with the dry provider contract.
```

## Primary executable object

```text
script=scripts/qwen_live_synthetic_provider_stub.py
test=backend/tests/test_qwen_live_synthetic_provider_stub.py
artifact=artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_output.json
report=artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report.json
report=artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report_中文.md
closeout=docs/S6_FAST_MVP_MVP_90_QWEN_LIVE_SYNTHETIC_PROVIDER_STUB_CLOSEOUT_2026_05_08.md
```

## Inputs

```text
mock_data/s0_synthetic/qwen_fact_bundle
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json
scripts/validate_qwen_provider_contract.py
```

## Output paths

```text
docs/goals/GOAL-MVP-90_QWEN_LIVE_SYNTHETIC_PROVIDER_STUB.md
scripts/qwen_live_synthetic_provider_stub.py
backend/tests/test_qwen_live_synthetic_provider_stub.py
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_output.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report_中文.md
docs/S6_FAST_MVP_MVP_90_QWEN_LIVE_SYNTHETIC_PROVIDER_STUB_CLOSEOUT_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-90_QWEN_LIVE_SYNTHETIC_PROVIDER_STUB.md
scripts/qwen_live_synthetic_provider_stub.py
backend/tests/test_qwen_live_synthetic_provider_stub.py
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_output.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report.json
artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_report_中文.md
docs/S6_FAST_MVP_MVP_90_QWEN_LIVE_SYNTHETIC_PROVIDER_STUB_CLOSEOUT_2026_05_08.md
```

## Allowed scope

```text
local/offline provider stub generation only
synthetic fact bundle reads
runtime config policy report reads
metadata-only JSON/Markdown artifact generation
local unit tests
docs-only closeout evidence for this Goal
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
py -3 scripts/qwen_live_synthetic_provider_stub.py --bundle-dir mock_data/s0_synthetic/qwen_fact_bundle --runtime-config-report artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_runtime_config_report.json --output-dir artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001 --repo-root .
py -3 scripts/validate_qwen_provider_contract.py artifacts/qwen_live_go_precheck/qwen-live-synthetic-go-2026-05-08-001/qwen_live_synthetic_provider_stub_output.json
py -3 -m unittest -q backend.tests.test_qwen_live_synthetic_provider_stub
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-90_QWEN_LIVE_SYNTHETIC_PROVIDER_STUB.md
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
runtime config report is not RUNTIME_CONFIG_POLICY_READY_PROCESS_ENV_NOT_CHECKED
input bundle is not synthetic-only
input bundle contains real data, masked-real data, secret marker, or raw layer0 payload marker
stub output is not compatible with secupilot.qwen_provider_dry_response.v1
stub output emits forbidden action, autonomous decision, connector, write-back, raw payload, auth, token, or secret text
stub script performs network request, live Qwen/API call, connector call, production write-back, or customer-visible output
unit tests fail twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert files listed in Allowed files only
delete generated provider stub output and report files for this Goal
preserve failed command output in closeout if failure occurred
```

## Evidence contract

```text
provider stub output JSON
provider stub report JSON/Markdown
provider contract validator output
unit test output
goal card validator output
git diff --check output
closeout report with exact commands
```

## Safety sentinels

```text
no qwen_used=true
no live_qwen_api=true
no network_call=true
no secret_values_read=true
no live_connectors=true
no production_writeback=true
no customer_visible_output=true
no autonomous_qwen_action=true
no Authorization/Bearer/access_token/refresh_token/private_key/raw_payload/raw_evidence in generated artifacts
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-91_MODEL_PROVIDER_SWITCH_UI.
If HOLD, stop and report the failing provider stub item.
This Goal does not unlock live execution by itself.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-90 qwen live synthetic provider stub
stage and commit only Goal files
do not push
```
