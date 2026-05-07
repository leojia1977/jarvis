# <GOAL-ID>

## Goal ID

```text
GOAL-MVP-00_EXAMPLE
```

## Goal type

```text
page | script | interface | interface/API | package | test-report | run-artifact | validator
```

## Goal statement

```text
One sentence that names the exact product or engineering outcome.
```

## Primary executable object

```text
page=<route>
script=<path>
interface=<contract or module>
package=<artifact path>
test=<test target>
validator=<script path>
report=<report path>
```

## Inputs

```text
List exact source packages, fixtures, pages, interfaces, or artifacts.
```

## Output paths

```text
List exact repo paths or artifact directories this Goal may create or update.
```

## Allowed files

```text
List exact files, directories, or globs that may be edited.
```

## Allowed scope

```text
local/offline only
local tests
local package/artifact generation
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
push unless separately authorized
```

## Acceptance commands

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/<GOAL-ID>.md
npm run test -- src/App.test.tsx
```

## HOLD conditions

```text
Any acceptance command fails twice in the same way.
Any safety sentinel is observed.
Any file outside Allowed files requires modification.
```

## Rollback

```text
Revert changed files in Allowed files only.
Delete generated local artifacts for this Goal candidate only.
Preserve failure evidence.
```

## Evidence contract

```text
command transcript or test output
artifact manifest or package index when artifacts are generated
screenshots when UI changes
closeout note with exact commands
```

## Safety sentinels

```text
no P1/P2/P3 in reviewer-clean screenshots
no Mock Fixture in reviewer-clean screenshots
no Expert Mode in reviewer-clean screenshots
no Authorization: / Bearer / refresh_token in artifacts
no writeback_enabled=true
no customer_visible_output=true
```

## Merge rule

```text
May stage/commit only if all acceptance commands pass and no HOLD condition is observed.
Do not push.
Do not merge unrelated changes.
```

## Next unlock

```text
If PASS, unlock the exact next GOAL-*.
If PASS_WITH_NOTES, create follow-up notes without expanding current scope.
If HOLD, stop and write the HOLD reason.
```

## Commit posture

```text
one commit per passing Goal
commit message: feat(secupilot): <GOAL-ID lowercase summary>
do not push unless separately authorized
```
