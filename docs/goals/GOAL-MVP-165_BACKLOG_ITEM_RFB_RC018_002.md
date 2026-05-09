# GOAL-MVP-165 Backlog Item RFB-RC018-002

## Goal ID

```text
GOAL-MVP-165_BACKLOG_ITEM_RFB_RC018_002
```

## Goal type

```text
script
```

## Goal statement

```text
Add conservative wording replacement checks to reviewer backlog closeout tooling so RC018 wording updates can be verified before the backlog item is closed.
```

## Primary executable object

```text
script=scripts/close_reviewer_backlog_items.py
closeout=docs/S6_FAST_MVP_GOAL_MVP_165_BACKLOG_ITEM_RFB_RC018_002_2026_05_09.md
```

## Inputs

```text
artifacts/product_backlog/local-offline-trial-rc-018-cn-review/reviewer_backlog.json
front-end and artifact text evidence paths passed via --text-check-file
replacement pairs passed via --require-replacement old=>new
```

## Output paths

```text
docs/goals/GOAL-MVP-165_BACKLOG_ITEM_RFB_RC018_002.md
scripts/close_reviewer_backlog_items.py
docs/S6_FAST_MVP_GOAL_MVP_165_BACKLOG_ITEM_RFB_RC018_002_2026_05_09.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-165_BACKLOG_ITEM_RFB_RC018_002.md
scripts/close_reviewer_backlog_items.py
docs/S6_FAST_MVP_GOAL_MVP_165_BACKLOG_ITEM_RFB_RC018_002_2026_05_09.md
```

## Allowed scope

```text
add optional conservative wording checks to backlog closeout script
keep backward compatibility for existing closeout commands
document verification evidence for this goal
```

## Forbidden scope

```text
real data
masked-real data
live Qwen/API calls
live connectors
production write-back
customer-visible publish/deploy/output
external pilot
production launch
secrets/tokens/auth headers/raw customer logs
autonomous remediation/action-mode choice
backend API/schema migration
push
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-165_BACKLOG_ITEM_RFB_RC018_002.md
py -3 -m unittest backend.tests.test_close_reviewer_backlog_items
py -3 scripts/close_reviewer_backlog_items.py --help
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
backlog item cannot map to a bounded execution profile
script command fails
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
leave unrelated dirty/untracked residue untouched
```

## Evidence contract

```text
goal card validator PASS output
focused unittest PASS output for backlog closeout script
real command invocation output from script help command
diff --check PASS output
closeout with command results and scope guard status
```

## Safety sentinels

```text
real_data=false
masked_real_data=false
live_qwen_api=false
live_connectors=false
production_writeback=false
customer_visible_output=false
push=false
```

## Merge rule

```text
Stage and commit only allowed files after all acceptance commands PASS and no HOLD condition triggers.
Reject unrelated changes; do not stage unrelated files.
Do not push.
```

## Next unlock

```text
PASS unlock: run one follow-up backlog closeout Goal for RFB-RC018-002 using the new conservative wording checks.
HOLD behavior: report exact script failure and stop this run.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-165 backlog item rfb rc018 002
stage only Goal files
do not push
```
