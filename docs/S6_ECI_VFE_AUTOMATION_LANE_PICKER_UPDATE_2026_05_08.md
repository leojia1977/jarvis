# S6 ECI/VFE Automation Lane Picker Update

Date: 2026-05-08

Status:

```text
PASS
```

## Purpose

After `GOAL-ECIVFE-30_FIXTURE_MODEL` passed, the automation picker needed an explicit low-conflict ECI/VFE lane so recurring automation can consume the next schema/engine/guard work instead of continuing only through the private-preview pool.

## Change

Updated `scripts/pick_next_mvp_goal.py` to recognize:

- `GOAL-ECIVFE-33_LOCAL_RULE_ENGINE`
- `GOAL-ECIVFE-34_OUTPUT_GUARD`

The picker now selects `GOAL-ECIVFE-33_LOCAL_RULE_ENGINE` only after `GOAL-ECIVFE-30_FIXTURE_MODEL` exists.

The picker selects `GOAL-ECIVFE-34_OUTPUT_GUARD` only after both:

- `GOAL-ECIVFE-30_FIXTURE_MODEL`
- `GOAL-ECIVFE-33_LOCAL_RULE_ENGINE`

This preserves the required order:

```text
schema/fixture -> local rule engine -> output guard -> UI
```

## Current Candidate

The refreshed candidate is:

```text
GOAL-ECIVFE-33_LOCAL_RULE_ENGINE
```

Output files:

- `artifacts/product_acceleration/next_goal_candidate.json`
- `artifacts/product_acceleration/next_goal_candidate.md`

## Verification

Commands run:

```powershell
py -3 -m unittest backend.tests.test_pick_next_mvp_goal
py -3 scripts\pick_next_mvp_goal.py --repo-root . --output-json artifacts\product_acceleration\next_goal_candidate.json --output-md artifacts\product_acceleration\next_goal_candidate.md
git -c core.quotepath=false diff --check
```

Results:

- Picker unit tests: PASS, 12 passed.
- Picker refresh: PASS, selected `GOAL-ECIVFE-33_LOCAL_RULE_ENGINE`.
- Diff check: PASS.

## Boundary

This update does not authorize:

- real data
- masked-real data
- live Qwen/API/connectors
- production write-back
- customer-visible publish, deploy, or output
- external pilot
- production launch
- secrets, tokens, auth headers, raw logs, raw payloads, or host raw evidence
- PoC, exploit steps, payload, attacker-readable topology detail, or autonomous action

## Next Automation Step

Recurring automation can now implement:

```text
GOAL-ECIVFE-33_LOCAL_RULE_ENGINE
```

If `GOAL-ECIVFE-33` passes, the picker will advance to:

```text
GOAL-ECIVFE-34_OUTPUT_GUARD
```
