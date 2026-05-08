# GOAL-MVP-123 Backlog Item RFB-RC016-001

## Goal ID

```text
GOAL-MVP-123_BACKLOG_ITEM_RFB_RC016_001
```

## Goal type

```text
package
```

## Goal statement

```text
Mirror folded-state screenshot archive-evidence requirement into package_manifest.json so archive validators can enforce the same contract without parsing package index only.
```

## Primary executable object

```text
script=scripts/build_local_offline_trial_rc.py
validator=backend/tests/test_build_local_offline_trial_rc.py
goal_card=docs/goals/GOAL-MVP-123_BACKLOG_ITEM_RFB_RC016_001.md
closeout=docs/S6_FAST_MVP_GOAL_MVP_123_BACKLOG_ITEM_RFB_RC016_001_2026_05_08.md
```

## Inputs

```text
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
GOAL-MVP-122 implementation commit b37c004
```

## Output paths

```text
docs/goals/GOAL-MVP-123_BACKLOG_ITEM_RFB_RC016_001.md
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
docs/S6_FAST_MVP_GOAL_MVP_123_BACKLOG_ITEM_RFB_RC016_001_2026_05_08.md
```

## Allowed files

```text
docs/goals/GOAL-MVP-123_BACKLOG_ITEM_RFB_RC016_001.md
scripts/build_local_offline_trial_rc.py
backend/tests/test_build_local_offline_trial_rc.py
docs/S6_FAST_MVP_GOAL_MVP_123_BACKLOG_ITEM_RFB_RC016_001_2026_05_08.md
```

## Allowed scope

```text
package manifest schema extension mirroring folded screenshot archive-evidence contract
matching unittest assertions only
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
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-123_BACKLOG_ITEM_RFB_RC016_001.md
py -3 -m unittest backend.tests.test_build_local_offline_trial_rc
py -3 scripts/build_local_offline_trial_rc.py --help
git -c core.quotepath=false diff --check
```

## HOLD conditions

```text
package builder behavior changes outside selected backlog scope
unit test fails twice in the same way
scope expands beyond listed files
```

## Rollback

```text
revert only files listed in Allowed files
preserve known residue and unrelated dirty/untracked artifacts
```

## Evidence contract

```text
goal card validator PASS output
unittest PASS output proving required_archive_evidence in package_manifest and package_index
builder help command PASS output
diff --check PASS output
closeout references to mirrored manifest contract key
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
Do not stage unrelated residue.
```

## Next unlock

```text
If PASS, unlock follow-up backlog closeout Goal for RFB-RC016-001.
If HOLD, stop and report failing command and exact boundary.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): GOAL-MVP-123 mirror folded evidence manifest contract
stage and commit only Goal files
do not push
```
