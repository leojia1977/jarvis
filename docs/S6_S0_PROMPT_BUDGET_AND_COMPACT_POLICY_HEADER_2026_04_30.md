# S6 S0 Prompt Budget And Compact Policy Header 2026-04-30

## 1. Document Control

| Field | Value |
| --- | --- |
| Record type | S0 prompt budget and compact policy header implementation record |
| Date | 2026-04-30 |
| Route | `OPEN_S0_PROMPT_BUDGET_AND_COMPACT_POLICY_HEADER` |
| Implementation file | `scripts\s0_qwen_synthetic_run.py` |
| Related rerun gate | `docs\S6_QWEN_RUNTIME_STABILITY_FIX_AND_S0_RERUN_2026_04_30.md` |

## 2. Decision

```text
S0_PROMPT_BUDGET_AND_COMPACT_POLICY_HEADER_IMPLEMENTED
S0_RERUN_STILL_WAITING_FOR_QWEN_72B_ENGINECORE_RECOVERY
```

This record implements a small S0 stability guard. It does not run Qwen and does not change product behavior.

## 3. Implemented Scope

Implemented:

- compact policy header for the S0 runner;
- compact JSON user payload using JSON separators instead of pretty-printed prompt payloads;
- per-scenario prompt budget guard before model invocation;
- CLI options:
  - `--max-input-chars`, default `12000`;
  - `--max-input-tokens-estimate`, default `3000`;
- per-scenario `HOLD_PROMPT_TOO_LARGE` evidence if a synthetic input exceeds the budget;
- manifest/request-parameter recording for the prompt budget values;
- rerun checklist update to require compact prompt mode for `S0-QWEN-2026-04-30-002`.

## 4. Why This Exists

The prior S0 run confirmed two runtime risks:

1. `max_tokens=8192` is unsafe as a static direct vLLM value for an 8192 context window.
2. qwen-72b / vLLM EngineCore became unavailable after partial S0 success.

Compact prompts and a pre-call budget guard reduce avoidable pressure on the Qwen runtime. They do not replace the required cloud runtime stability fix.

## 5. Boundaries

This implementation does not:

- alter product semantics;
- alter UAT scenario content;
- alter Qwen prompt policy beyond compacting the S0 header;
- touch frontend, Storybook, Playwright, fixtures, adapters, validators, or `ResolvedSurfaceContext`;
- touch backend runtime/API/schema;
- connect to real or masked-real data;
- use secrets;
- deploy;
- authorize external pilot or launch.

## 6. Next Route

```text
WAIT_FOR_QWEN_72B_ENGINECORE_RECOVERY_EVIDENCE_OR_AUTHORIZE_S0_RERUN_002
```
