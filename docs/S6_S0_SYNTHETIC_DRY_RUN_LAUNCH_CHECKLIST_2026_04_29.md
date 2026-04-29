# S6 S0 Synthetic Dry Run Launch Checklist 2026-04-29

## 1. Document Control

- Date: 2026-04-29
- Record type: S0 synthetic-only launch checklist
- Source intake: `docs/S6_REAL_DATA_RUNTIME_UAT_SOURCE_INTAKE_2026_04_29.md`

## 2. Checklist Decision

```text
S0_LAUNCH_CHECKLIST_PASS_FOR_SYNTHETIC_ONLY_EXECUTION_ATTEMPT
REAL_DATA_AND_MASKED_REAL_DATA_FORBIDDEN
S0_MUST_RETURN_EXPLICIT_S0_DECISION
```

This checklist authorizes an S0 synthetic dry-run execution attempt only. It does not authorize real data, masked real data, customer-visible output, production write-back, autonomous action, backend/runtime/API/schema, connector changes, secrets, deploy, external pilot, or launch.

## 3. Allowed Scope

Allowed:

```text
synthetic fixtures only
UAT-01 through UAT-20
Qwen offline evaluation
prompt injection tests
action-command keyword scan
GPU runtime metrics
S0 evaluation report completion
```

## 4. Forbidden Scope

Forbidden:

```text
real data
masked real data
customer-visible output
production write-back
autonomous action
backend/runtime/API/schema
connector changes
secrets
deploy
external pilot
launch
```

## 5. Required Inputs Before S0 Can Pass

S0 must produce or identify:

- synthetic fixture manifest for UAT-01 through UAT-20;
- synthetic CaseView inputs;
- synthetic `QwenFactBundle` inputs;
- local Qwen model id / runtime;
- prompt injection cases;
- action-command keyword scan list;
- GPU runtime metric capture;
- S0 report with per-scenario decisions;
- final `S0_DECISION`.

## 6. HOLD Conditions

S0 must HOLD if:

- no local Qwen model is available;
- UAT-01 through UAT-20 synthetic fixtures cannot be resolved;
- Qwen output records cannot be produced;
- prompt injection tests cannot run;
- action-command scan cannot run;
- GPU metrics cannot be captured for model execution;
- any real or masked-real data is requested;
- backend/runtime/API/schema or connector changes become necessary;
- secrets are required;
- deploy, external pilot, launch, or customer-visible output is requested.

## 7. Required S0 Decision Enum

S0 must end with one of:

```text
S0_DECISION =
  PASS_FOR_SYNTHETIC_ONLY
  | CONDITIONAL_PASS_WITH_FIXES
  | HOLD_WITH_FAILURES
  | NO_GO
```

## 8. Launch Checklist Result

```text
CHECKLIST_RESULT: PASS_TO_EXECUTE_S0_SYNTHETIC_DRY_RUN_ATTEMPT
```

The execution attempt may start. If required runtime or fixture inputs are absent, the attempt must stop with `HOLD_WITH_FAILURES`.
