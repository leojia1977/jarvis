# AdsPower Claude Web Automation Verification

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | AdsPower Claude Web Automation Verification |
| Status | Docs-only automation verification draft |
| Snapshot | S5-ADSPOWER-CLAUDE-WEB-AUTOMATION-VERIFICATION-2026-04-18-001 |
| Stage | s5-adspower-claude-web-automation-verification |
| Route | OPEN_ADSPOWER_CLAUDE_WEB_AUTOMATION_VERIFICATION_STAGE |
| Baseline commit | `bfd0920050d4780866dfdaba88fd3c7afece4e0c` |
| Baseline snapshot | S5-AUTONOMOUS-TOOLCHAIN-INTEGRATION-2026-04-18-001 |
| Baseline stage | s5-autonomous-toolchain-integration |
| Baseline manifest status | PASS |
| Baseline release artifact | `releases\secupilot-S5-AUTONOMOUS-TOOLCHAIN-INTEGRATION-2026-04-18-001.zip` |
| Baseline release sha256 | `46bd62aff5ac78315750e241fe2c790ddb1937f38702c571a0011b8211db7655` |

## 2. Purpose

This stage verifies whether Codex can operate Claude Web through the user's AdsPower browser/profile for a harmless review-prompt round trip.

This stage verifies only the automation path. It does not authorize product launch, production deployment, external pilot execution, real-data handling, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, or AI_COLLAB change.

## 3. Startup Checks

- Branch remained `codex/s3-a-runtime`.
- Baseline commit was `bfd0920050d4780866dfdaba88fd3c7afece4e0c`.
- Baseline manifest verification was `PASS`.
- `docs\DELEGATED_APPROVER_CHARTER.md` was readable.
- Authorization window remained active at verification time.
- `delegation_expires` remained `2026-05-06 23:59 Asia/Shanghai`.
- Working tree contained only known out-of-scope untracked files before this stage edits.

## 4. Secret Boundary

AdsPower API-key material is secret.

The verification used a user-level environment variable lookup and did not print, echo, commit, store, summarize, or log the API key.

The API key must not enter:

- chat
- repo files
- prompts
- review packs
- logs
- screenshots
- release artifacts

Future runs must read AdsPower API-key material only through a governed non-secret provisioning path, such as a user-level environment variable or Windows Credential Manager reference.

## 5. Verification Steps

| Step | Result | Notes |
| --- | --- | --- |
| Check key presence without printing value | PASS | `ADSPOWER_API_KEY` was available through user-level environment variable lookup. |
| AdsPower Local API auth | PASS | Local API accepted the user-level API key. |
| Active profile discovery | PASS | One active AdsPower profile was detected. The profile ID is not recorded in this document. |
| CDP target discovery | PASS | Five page targets were visible; one `claude.ai` page was present. Full URLs and titles were not recorded. |
| Claude Web DOM probe | PASS | One editable Claude input surface was detected. No conversation text was read. |
| Harmless prompt round trip | PASS | Codex inserted a harmless test prompt and observed the expected response token occurrence count increase. |

## 6. Verified Capability

The AdsPower / Claude Web path is verified only for:

- connecting to an already-active AdsPower profile through Local API and CDP
- finding an already-open Claude Web page
- focusing the Claude Web input surface
- sending a harmless text prompt
- observing that Claude Web produced the expected response token

Verified status: `VERIFIED_FOR_REVIEW_PROMPT_TEST_ONLY`.

## 7. Not Verified

This stage does not verify:

- AdsPower profile launch
- AdsPower profile creation
- AdsPower profile switching
- login automation
- cookie, token, auth header, browser storage, or profile inspection
- Claude account settings access
- billing, payment, or account-page access
- high-risk Claude Web review workflows
- Red-2 or Red-3 review substitution
- external pilot readiness or execution
- production deployment

## 8. Operating Limits

Claude Web automation may be used only for governed review-prompt transfer when:

- the prompt contains no secrets, credentials, raw customer data, cookies, tokens, auth headers, or unredacted real evidence
- the stage or policy authorizes Claude Web review prompt transfer
- no unresolved HOLD blocks the action
- the response is treated as review output only, not as implementation or launch authorization

Any high-risk or Red-2+ use still requires the review and approval gates defined in the autonomous authorization policy.

## 9. HOLD Queue Impact

- AHQ-021 may advance from `HOLD_FOR_TOOL_VERIFICATION` to `VERIFIED_FOR_REVIEW_PROMPT_TEST_ONLY`.
- AHQ-022 remains partially blocked for AdsPower profile launch, profile switching, and broader session control.
- AHQ-023 records AdsPower API-key non-secret provisioning as verified through user-level environment variable auth.
- AHQ-020 remains `HOLD_FOR_TOOL_VERIFICATION` because Claude Code `cc switch` non-interactive review behavior is still not verified.

## 10. Non-Authorization

This stage does not authorize:

- API-key disclosure
- AdsPower API-key printing, storing, echoing, logging, or committing
- cookie, token, auth header, browser storage, or session inspection
- AdsPower profile export
- login automation
- Claude account settings changes
- billing or payment access
- launch execution
- production deployment
- external pilot execution
- credential handling by AI
- real-data handling
- public endpoint work
- S5-B/S5-D reopen
- ORDIV reopen/report/CSV/L1B work
- Red-3 action
- S4-A resolver order change
- AI_COLLAB change
- full gate or release packaging without explicit authorization
- staging, commit, or push without explicit authorization
