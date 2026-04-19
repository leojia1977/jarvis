# Autonomous Tool Runbook

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Tool Runbook |
| Status | Updated by AdsPower profile launch verification draft |
| Snapshot | S5-ADSPOWER-PROFILE-LAUNCH-VERIFICATION-2026-04-19-001 |
| Stage | s5-adspower-profile-launch-verification |
| Baseline commit | `a02e53fd1a439db5b14752144074be15759cd63d` |

This runbook defines toolchain operating rules. It does not authorize browser launch, Claude Web login, external review automation, full gate, release packaging, staging, commit, push, launch execution, production deployment, external pilot execution, credential handling, real-data handling, or Red-3 action.

## 2. Per-Run Startup

Every run must:

1. Read `docs\DELEGATED_APPROVER_CHARTER.md`.
2. Verify `delegation_expires` has not passed.
3. Load the eight core governance docs.
4. Confirm manifest baseline and git cleanliness.
5. Select one next allowed item.
6. Classify lane as Green, Yellow, Red-1, Red-2, Red-3, or HOLD.
7. Proceed only if lane and authorization are clear.

If the charter cannot be read, `delegation_expires` is missing, or the authorization window has expired, all Red authority is HOLD and automation must stop.

## 3. Tool Selection

Use the lowest-risk tool that can complete the allowed step:

- Use Codex workspace editing for allowed docs-only changes.
- Use VS Code CLI only as a local workspace/editing surface when needed and governed; do not treat it as product memory, review authority, or closeout authority.
- Use Claude Code through the `cc switch` API tool only after review-only command/API format and non-interactive behavior are verified.
- Use Claude Web through the verified AdsPower configured-profile path only for governed review-prompt transfer when the prompt contains no secrets, raw customer data, credentials, or unredacted real evidence.
- Use Git only for inspection unless staging/commit/push is explicitly authorized.

## 4. VS Code Workspace Usage

VS Code is a local editing/workspace surface. It is not long-term product memory, lane authority, review authority, route authority, manifest authority, or closeout authority by itself.

Allowed:

- Edit allowed docs when stage scope permits.
- Inspect local files.
- Prepare review material.
- Support human-supervised implementation edits only when a separate governed ticket defines exact files, exact behavior, exact tests, review path, rollback/HOLD criteria, and approval requirements.

Prohibited:

- Treating unsaved/editor-only state as governed truth.
- Using VS Code state to override repo-governed docs, manifest, release verification, review results, or current git status.
- Assigning lane authority, review PASS, release PASS, or closeout eligibility from VS Code context alone.
- Modifying code/tests/dependencies/fixtures/runtime/API/schema/release scripts/AI_COLLAB outside allowed scope.
- Staging, commit, or push outside the standing Green docs-only closeout rule or separate explicit authorization.

If Codex output and VS Code workspace context conflict, prefer committed repo evidence, the manifest, current git status, and governed docs. If the conflict cannot be resolved from governed sources, HOLD.

## 5. Claude Code / `cc switch` Review-Only Usage

Claude Code automation may be used only through the user-configured `cc switch` API tool after command/API format and non-interactive behavior are verified. The current verification found no local `cc` command or alias. `claude.exe` visibility is not enough and must not be treated as the governed `cc switch` automation path.

Until verified, automation should generate a Claude Code review prompt and HOLD for human/tool execution. For stages verifying `cc switch` itself, final independent review must come from Claude Web through the verified AdsPower active-profile path or from human-supervised external review.

Review-only means:

- no edits
- no staging
- no commit
- no push

API error, non-zero exit, unavailable `cc switch` path, or ambiguous output means HOLD.

If Claude Code review says `PASS_WITH_FINDINGS`, classify each finding by severity, apply only allowed focused fixes, refresh affected hashes, and return to review. If any finding requires out-of-scope files, external access, credentials, real data, Red-3, or unclear authority, HOLD.

`docs\CC_SWITCH_CLAUDE_CODE_RUNBOOK.md` governs any future retry. A future PASS may verify only non-interactive review-only prompt transfer and verdict capture; it does not authorize edits, implementation, code execution, staging, commit, push, Red execution, launch/deploy, real data, external pilot execution, or full four-tool automation.

## 6. Claude Web / Manual External Review Path

Claude Web is an external review path.

The user-confirmed Claude Web surface is an AdsPower browser/profile. The configured-profile path is verified only for safe launch/attach to review-prompt readiness and harmless review-prompt round trip. If the configured profile, CDP endpoint, Claude Web page, or input surface is missing, automation must produce a Claude Web prompt and HOLD for manual transfer.

No credentials, cookies, tokens, API keys, auth headers, or secret material may enter repo, chat, prompts, review packs, or logs.

AdsPower browser/profile/session/login issues mean HOLD.

Claude Web or external review is required for high-risk triggers already defined in governance docs.

## 7. AdsPower Browser Automation Boundary

AdsPower configured-profile launch/attach and CDP automation are verified only for governed review-prompt transfer readiness. AdsPower profile switching, profile creation, login automation, and broader session control are not authorized by this stage.

AdsPower Local API accepts a user-level environment variable API key. The API key is secret material. Do not paste it into chat, commit it to repo, add it to prompts, print it in logs, or ask the AI to read/display it. Future runs must use a human-controlled non-secret provisioning path, such as a local environment variable or Windows Credential Manager reference.

Do not:

- launch or attach to any AdsPower profile other than the configured governed profile identifier
- switch AdsPower profiles
- create AdsPower profiles
- log into Claude Web
- inspect cookies, sessions, credentials, tokens, auth headers, AdsPower profiles, or browser profile state
- print, store, or echo AdsPower API keys
- claim blanket Claude Web automation is verified beyond the governed review-prompt path

AdsPower/browser capability may be documented as candidate-only until a later governed safe verification route exists.

## 8. Closeout Gate Behavior

Fast/full gate and release packaging may run only when the current stage prompt or later closeout instruction explicitly authorizes them.

This stage does not run full gate and does not create release artifacts.

If a gate is authorized later:

- run the exact governed command
- stop on failure unless the fix is Green/Yellow, scoped, and authorized
- do not fabricate PASS, release sha, verification metadata, or review status

## 9. Day-1 Commit/Push Rule

During day 1, staging, commit, and push require explicit human confirmation.

Automation may prepare:

- changed-file list
- diff summary
- review prompt
- gate plan
- staging proposal

Automation may not stage, commit, or push until explicit human confirmation is given.

## 10. Network Slow Retry

If network access, remote review, GitHub, Claude Web, external reviewer, or remote status check is slow or unresponsive for more than 5 minutes:

- retry idempotent/read-only requests once
- check prior status before retrying non-idempotent actions
- do not resend approval, push, deploy, launch, upload, or external access actions unless prior status is known safe
- if ambiguity remains, update HOLD context and stop

Network slowness never permits bypassing review, gate, delegated approval, external review, or HOLD conditions.

## 11. HOLD And Escalation

HOLD if:

- tool command is unavailable
- command returns non-zero or ambiguous output
- AdsPower/browser/session/login state is unknown
- credential prompt appears
- external access is requested
- real data is requested
- lane is ambiguous
- required approval is missing or expired
- unexpected file scope appears
- review requires prohibited work

Escalate to human or jarvis only within policy limits. Red-3 remains outside normal delegation.

## 12. Per-Run Inbox Output Format

Each run should report:

```text
AUTONOMOUS_RUN_REPORT
Baseline:
Selected task:
Lane:
Files proposed/touched:
Tools used:
Checks run:
Review status:
Gate status:
HOLDs encountered:
Next requested human/jarvis action:
```

## 13. Tool Result Conflicts

If tool results conflict:

- prefer repo-governed docs, manifest, and current git state over chat memory
- do not merge conflicting claims
- document the conflict
- HOLD until a governed source resolves it

## 14. Human Or Jarvis Approval Needed

When approval is needed, produce a concise request containing:

- stage/ticket
- lane
- exact action
- allowed files/systems
- external access yes/no
- real data yes/no
- evidence retention yes/no
- redaction reference
- rollback/HOLD criteria
- expiration
- required review

Do not proceed on incomplete, ambiguous, or expired approval.

## 15. VS Code Role Orchestration Note

`docs\VSCODE_ROLE_AND_TOOLCHAIN_ORCHESTRATION.md` governs the VS Code role in the autonomous workflow.

Required split:

- Codex owns orchestration, governance doc loading, lane classification, tool routing, gate/package/release verification when authorized, manifest updates, and closeout under policy limits.
- VS Code owns only the local workspace/editing execution surface for exact allowed files.
- Claude Web in AdsPower remains the verified review-prompt transfer path only.
- Claude Code through `cc switch` remains HOLD until a callable non-interactive review-only path is governed and verified.

This clarification does not authorize implementation, code/test changes, browser login/session access, AdsPower profile launch/switch, Red execution, launch, deployment, real-data handling, public endpoint work, staging, commit, or push.

## 16. Ops Loop Refresh Note

The active autonomous ops loop must include toolchain and AdsPower Claude Web verification/runbook context before using Claude Web review-prompt transfer. The loop may not use Claude Web for prompts containing secrets, raw customer data, credentials, or unredacted real evidence.

Standing Green docs-only closeout is governed by `docs\AUTONOMOUS_OPS_LOOP_REFRESH_AND_DAY1_CLOSEOUT.md` after that stage closes with review PASS, full gate PASS, release verification PASS, closeout commit, and push. This runbook does not authorize Yellow implementation, Red execution, profile launch/switch, Claude Web login, or full four-tool automation.

## 17. AdsPower Profile Launch Verification Note

`docs\ADSPOWER_PROFILE_LAUNCH_VERIFICATION.md` and `docs\ADSPOWER_PROFILE_LAUNCH_RUNBOOK.md` govern the configured AdsPower profile launch/attach path.

Allowed only when governed stage scope permits:

- read `ADSPOWER_API_KEY` and `ADSPOWER_USER_ID` through local non-secret references without printing values
- call AdsPower Local API `browser/start` for the configured profile identifier
- use the returned CDP endpoint to confirm Claude Web review-prompt readiness
- stop before prompt submission unless a separate governed review prompt is authorized

This note does not authorize profile switching, login automation, cookie/session/token/auth-header inspection, reading Claude conversation history, Red execution, launch, deployment, external pilot execution, real-data handling, public endpoint work, or full four-tool automation.
