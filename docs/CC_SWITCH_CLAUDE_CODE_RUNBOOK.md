# CC Switch Claude Code Runbook

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | CC Switch Claude Code Runbook |
| Status | Docs-only runbook draft |
| Snapshot | S5-CC-SWITCH-CLAUDE-CODE-REVIEW-AUTOMATION-VERIFICATION-2026-04-19-001 |
| Stage | s5-cc-switch-claude-code-review-automation-verification |
| Baseline commit | `73be4bc2669545be5b4357058fcf446eb461787c` |

This runbook defines the safe operating pattern for a future governed `cc switch` Claude Code review-only path. The current stage did not verify the path because no local `cc` command/API invocation was discoverable in the VS Code workspace.

## 2. Current Status

Current status: `HOLD_FOR_TOOL_VERIFICATION`.

The `cc switch` path may not be used autonomously until a later governed verification proves non-interactive review-only prompt transfer, parseable verdict capture, and no file/status mutation.

`claude.exe` visibility is not sufficient evidence for this runbook because the governed path is the user-configured `cc switch` API tool.

## 3. Allowed Use After Verification

After a separate governed PASS, allowed use is limited to:

- review-only prompt transfer
- verdict capture
- finding-count capture
- non-secret token confirmation for test prompts
- recording PASS, PASS_WITH_FINDINGS, FAIL, or HOLD as review evidence

Claude Code output is review evidence only. It does not authorize implementation, launch, deployment, external pilot execution, Red execution, public endpoint work, parked-stream reopen, staging, commit, or push.

## 4. Prohibited Use

Do not use `cc switch` for:

- edits
- code generation into repo files
- command execution claims
- test execution claims
- dependency installation
- fixture creation or modification
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

## 5. Prompt Requirements

Every prompt must:

- contain no secrets
- contain no raw customer data
- contain no unredacted evidence
- contain no credential, session, cookie, token, auth-header, browser-storage, or profile-file content
- state exact review scope
- state allowed files
- state prohibited actions
- require review-only behavior
- require no edits
- require no commands
- require no staging, commit, or push
- require the output format in Section 6
- include a unique non-secret token for harmless verification prompts

## 6. Required Output Format

The expected response format is:

```text
Verdict: PASS | PASS_WITH_FINDINGS | FAIL | HOLD
Finding count: <integer>
Findings:
- Severity: HIGH | MEDIUM | LOW | INFO
  File: <path or N/A>
  Summary: <brief finding>
  Required action: <brief action or N/A>
Token: <expected token when a token is requested>
```

If there are no findings, `Finding count` must be `0` and `Findings` may be `N/A`.

## 7. Result Handling

| Result | Handling |
| --- | --- |
| PASS | May be recorded as review evidence if scope, token, and no-mutation checks pass. |
| PASS_WITH_FINDINGS | Triage findings by severity; apply only governed focused fixes in allowed files; HOLD for out-of-scope or ambiguous fixes. |
| FAIL | HOLD until a governed fix or route decision exists. |
| HOLD / ambiguous | Treat as HOLD; do not infer PASS. |

`cc switch` review evidence cannot be the sole independent final reviewer when `cc switch` behavior is itself under verification. Use Claude Web through the verified AdsPower active-profile path or human-supervised external review for final review of the verification stage.

## 8. Before And After Checks

Before any future `cc switch` review-only request:

1. Run `git status --short -b`.
2. Confirm no unexpected staged files.
3. Confirm the prompt contains no prohibited data.
4. Confirm the stage authorizes the exact review scope.

After the request:

1. Run `git status --short -b`.
2. Confirm no files changed because of `cc switch`.
3. Confirm no staged files were created.
4. Confirm verdict is parseable.
5. Confirm expected token is present when a token was requested.

Any unexpected status change means FAIL/HOLD.

## 9. Retry And Timeout Rules

- Timeout means HOLD unless a governed retry is explicitly safe.
- Only one retry is allowed for an idempotent review-only request.
- Do not retry if prior request may have mutated files, staged changes, committed, pushed, or performed an external action.
- Non-zero exit means HOLD.
- Ambiguous output means HOLD.
- Credential prompts mean HOLD.
- Network ambiguity must not be used to claim PASS.

## 10. Fallback

If the `cc switch` path is unavailable, incomplete, ambiguous, or fails:

- generate a manual Claude Code review prompt
- HOLD for human/tool execution
- use Claude Web through the verified AdsPower active-profile review-prompt path if final external review is required and available
- otherwise use human-supervised external review

Do not substitute `claude.exe` for `cc switch` unless a later governed route explicitly changes the verification target.
