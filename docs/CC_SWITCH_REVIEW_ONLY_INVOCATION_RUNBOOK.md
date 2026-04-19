# CC Switch Review-Only Invocation Runbook

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | CC Switch Review-Only Invocation Runbook |
| Status | Docs-only invocation runbook draft |
| Snapshot | S5-CC-SWITCH-COMMAND-PATH-PROVISIONING-2026-04-19-001 |
| Stage | s5-cc-switch-command-path-provisioning |
| Baseline commit | `5c1d8c1e288c1e16f47279f147fc4a973064e874` |

This runbook governs the only currently verified Claude Code callable non-interactive review-only path.

## 2. Verified Path

Use the npm Claude Code shim:

```text
claude.cmd
```

The shim is verified only when invoked through stdin with:

```text
-p --bare --output-format json --tools "" --no-session-persistence --permission-mode plan --max-budget-usd 0.05
```

The `--tools ""` argument must be passed as an explicit empty string. It means no tools are allowed; omitting `--tools` is not equivalent because it may allow the default tool set. The provisioning probe baseline confirmed this mode with `web_search_requests=0` and `web_fetch_requests=0`.

The local environment may contain cc-switch routing variables such as `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN`, but their values must never be read, printed, logged, pasted into chat, committed to repo, or added to prompts.

Do not use:

- `claude.exe`
- a missing local `cc` command
- non-bare invocation
- command-argument multi-line prompts
- `--json-schema` until separately governed and verified

## 3. Allowed Use

Allowed use is limited to:

- review-only prompt transfer
- parseable first-line verdict capture
- finding summary capture
- non-secret token confirmation for harmless probes
- Green/docs-only stage review support where the governing stage allows Claude Code review-only evidence

Claude Code output is evidence, not authority. It does not authorize implementation, launch, deployment, external pilot execution, Red execution, public endpoint work, parked-stream reopen, staging, commit, or push.

## 4. Prompt Requirements

Every prompt must:

- be supplied through stdin
- contain no secrets
- contain no raw customer data
- contain no unredacted evidence
- contain no credential, API-key, session, cookie, token, auth-header, browser-storage, or profile-file content
- state the exact review scope
- state allowed files
- state prohibited actions
- require review-only behavior
- require no file edits
- require no file reads beyond supplied prompt material unless a later stage explicitly governs file-read review
- require no commands
- require no tests
- require no staging, commit, push, or remote action
- require the first line of `result` to be one of the verdict lines in Section 5

## 5. Required Result Contract

The first line of the `result` field from the JSON wrapper must be exactly one of:

```text
VERDICT: PASS
VERDICT: PASS_WITH_FINDINGS
VERDICT: FAIL
VERDICT: HOLD
```

All downstream parsing must use this first-line verdict contract. Free-form prose after the first line may be recorded as rationale, but it must not override a missing or invalid verdict line.

If the verdict line is missing, malformed, duplicated, or contradicted, treat the result as HOLD.

## 6. Required Checks

Before invocation:

1. Run `git status --short -b`.
2. Confirm no unexpected staged files.
3. Confirm prompt content contains no prohibited material.
4. Confirm the current stage authorizes Claude Code review-only evidence for the exact scope.

Invocation:

```text
<stdin prompt> | claude.cmd -p --bare --output-format json --tools "" --no-session-persistence --permission-mode plan --max-budget-usd 0.05
```

After invocation:

1. Confirm process exit code is `0`.
2. Parse wrapper JSON.
3. Parse the first-line verdict.
4. Confirm no web-search or web-fetch request was made.
5. Confirm no permission-denial escalation or tool-use surprise appears in the wrapper.
6. Run `git status --short -b`.
7. Confirm no files changed because of the Claude Code invocation.
8. Confirm no staged files were created.

Any failure means HOLD unless a later governed route explicitly authorizes a focused retry.

## 7. Result Handling

| Verdict | Handling |
| --- | --- |
| `PASS` | May be recorded as review evidence if scope, prompt hygiene, wrapper JSON, verdict-line parse, no-web, no-mutation, and no-staged checks pass. |
| `PASS_WITH_FINDINGS` | Triage findings by severity; apply only governed focused fixes in allowed files; HOLD for out-of-scope or ambiguous fixes. |
| `FAIL` | HOLD until a governed fix or route decision exists. |
| `HOLD` | Stop and report the blocker. |
| Missing/invalid verdict | Treat as HOLD. |

## 8. Failure And Retry Rules

- Timeout means HOLD.
- Non-zero exit means HOLD.
- Ambiguous output means HOLD.
- Missing wrapper JSON means HOLD.
- Missing first-line verdict means HOLD.
- Any credential prompt means HOLD.
- Any web request when not explicitly authorized means HOLD.
- Any file mutation, staged file, commit, push, command execution, or external action means FAIL/HOLD.
- One retry is allowed only for idempotent review-only requests when the first request clearly did not mutate state and the retry remains within the same governed prompt scope.
- Network ambiguity must not be used to claim PASS.
- `--json-schema` is rejected until a separate governed reopen. If a prohibited or future governed `--json-schema` attempt times out, immediately raise HOLD before any retry; enumerate residual child `node` processes by the timed-out invocation parent PID, terminate only those child processes, confirm no residual child process or file lock remains, and do not retry `--json-schema` without a separate governed reopen.

## 9. Independence Boundary

Claude Code review-only evidence cannot be the sole independent final reviewer when Claude Code behavior, cc-switch routing, or this invocation path is itself under verification.

For stages verifying Claude Code or cc-switch behavior, use Claude Web through the verified AdsPower path or human-supervised external review for final independent review.

## 10. Non-Authorization

This runbook does not authorize:

- file edits by Claude Code
- code generation into repo files
- file-read review beyond supplied prompt material unless separately governed
- command execution by Claude Code
- test execution by Claude Code
- dependency installation
- fixture changes
- runtime/API/schema changes
- release script changes
- contract changes
- staging
- commit
- push
- force-push or history rewrite
- secrets, credentials, API keys, cookies, tokens, auth headers, browser storage, session data, or profile files
- raw customer data
- unredacted real evidence
- external pilot execution
- launch or deployment
- public endpoint work
- S5-B/S5-D reopen
- ORDIV work
- AI_COLLAB changes
- Red execution or Red approval
- replacing required human, delegated, Claude Web, or external review
