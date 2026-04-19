# CC Switch Claude Code Runbook

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | CC Switch Claude Code Runbook |
| Status | Superseded by cc switch command-path provisioning draft |
| Snapshot | S5-CC-SWITCH-COMMAND-PATH-PROVISIONING-2026-04-19-001 |
| Stage | s5-cc-switch-command-path-provisioning |
| Baseline commit | `5c1d8c1e288c1e16f47279f147fc4a973064e874` |

This historical runbook records the earlier HOLD posture. The current governed invocation rules are now in `docs\CC_SWITCH_REVIEW_ONLY_INVOCATION_RUNBOOK.md`.

## 2. Current Status

Current status: `VERIFIED_REVIEW_ONLY_VERDICT_LINE_WITH_LIMITS`, superseding the earlier `HOLD_FOR_TOOL_VERIFICATION` posture for review-only verdict capture only.

The verified path may be used autonomously only under `docs\CC_SWITCH_REVIEW_ONLY_INVOCATION_RUNBOOK.md`.

`claude.exe` visibility is still not sufficient evidence and remains rejected. The verified callable path is stdin prompt transfer to the npm `claude.cmd` shim under cc-switch environment references, with `--bare`, JSON wrapper output, disabled tools, no session persistence, plan permission mode, budget cap, first-line verdict parsing, no web requests, and unchanged git status.

## 3. Allowed Use After Verification

Allowed use is limited to:

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

The current expected response format is governed by `docs\CC_SWITCH_REVIEW_ONLY_INVOCATION_RUNBOOK.md`: the first line of the JSON wrapper `result` must be exactly one of:

```text
VERDICT: PASS
VERDICT: PASS_WITH_FINDINGS
VERDICT: FAIL
VERDICT: HOLD
```

Any finding detail after that first line is rationale and must not override a missing or invalid verdict line.

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

Do not substitute `claude.exe`, local `cc`, non-bare invocation, command-argument multi-line prompts, or `--json-schema` for the verified invocation path.
