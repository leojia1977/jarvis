# GOAL-SYS-01_CODEX_GOAL_CONTRACT_LINTER

## Goal ID

```text
GOAL-SYS-01_CODEX_GOAL_CONTRACT_LINTER
```

## Goal type

```text
validator
```

## Goal statement

```text
Turn SecuPilot Codex Goal cards into executable engineering contracts that can be linted before work starts.
```

## Primary executable object

```text
validator=scripts/validate_codex_goal_card.py
test=backend/tests/test_validate_codex_goal_card.py
closeout=docs/S6_FAST_MVP_GOAL_SYS_01_CODEX_GOAL_CONTRACT_LINTER_CLOSEOUT_2026_05_07.md
```

## Inputs

```text
docs/goals/GOAL_TEMPLATE.md
docs/goals/GOAL-MVP-22_RESULT_PAGE.md
```

## Output paths

```text
docs/goals/GOAL_TEMPLATE.md
docs/goals/GOAL-SYS-01_CODEX_GOAL_CONTRACT_LINTER.md
docs/goals/GOAL-MVP-22_RESULT_PAGE.md
scripts/validate_codex_goal_card.py
backend/tests/test_validate_codex_goal_card.py
docs/S6_FAST_MVP_GOAL_SYS_01_CODEX_GOAL_CONTRACT_LINTER_CLOSEOUT_2026_05_07.md
```

## Allowed files

```text
docs/goals/**
scripts/validate_codex_goal_card.py
backend/tests/test_validate_codex_goal_card.py
docs/S6_FAST_MVP_GOAL_SYS_01_CODEX_GOAL_CONTRACT_LINTER_CLOSEOUT_2026_05_07.md
```

## Allowed scope

```text
local/offline only
docs/goals contract cards
local validator script
local unittest coverage
local command output
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
production write-back
customer-visible publish/deploy/output
secrets/tokens/auth headers/raw customer logs
backend API/schema migration
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-SYS-01_CODEX_GOAL_CONTRACT_LINTER.md docs/goals/GOAL-MVP-22_RESULT_PAGE.md
py -3 -m unittest backend.tests.test_validate_codex_goal_card
```

## HOLD conditions

```text
validator accepts a card with no executable object
validator accepts a card with no acceptance command
validator accepts a card with no evidence contract
validator accepts a card with no safety sentinels
validator accepts a broad planning-only goal
tests fail twice in the same way
```

## Rollback

```text
revert docs/goals/**
revert scripts/validate_codex_goal_card.py
revert backend/tests/test_validate_codex_goal_card.py
preserve failing command output in the closeout note
```

## Evidence contract

```text
validator PASS output for GOAL-SYS-01 and GOAL-MVP-22
unittest output for backend.tests.test_validate_codex_goal_card
closeout note with exact commands
```

## Safety sentinels

```text
no live Qwen/API requirement in validator tests
no connector call in validator tests
no production write-back in validator tests
no customer_visible_output=true in example Goal cards
no secrets/tokens/auth headers/raw customer logs in Goal cards
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock GOAL-MVP-22_RESULT_PAGE.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-SYS-01 codex goal contract linter
do not push unless separately authorized
```
