# AdsPower Profile Launch Verification

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | AdsPower Profile Launch Verification |
| Status | Docs-only automation verification draft |
| Snapshot | S5-ADSPOWER-PROFILE-LAUNCH-VERIFICATION-2026-04-19-001 |
| Stage | s5-adspower-profile-launch-verification |
| Route | OPEN_ADSPOWER_PROFILE_LAUNCH_VERIFICATION_STAGE |
| Baseline commit | `a02e53fd1a439db5b14752144074be15759cd63d` |
| Baseline snapshot | S5-VSCODE-ROLE-TOOLCHAIN-ORCHESTRATION-2026-04-19-001 |
| Baseline stage | s5-vscode-role-toolchain-orchestration |
| Baseline manifest status | PASS |
| Baseline release artifact | `releases\secupilot-S5-VSCODE-ROLE-TOOLCHAIN-ORCHESTRATION-2026-04-19-001.zip` |
| Baseline release sha256 | `0410a0e2379d15d7b5a7bd534bf619a25c938a3b884a64df2efda4d572408355` |

## 2. Purpose

This stage verifies whether AdsPower Local API can safely start or attach to the user-specified AdsPower profile and reach the Claude Web review-prompt path.

This stage verifies only a bounded browser-control capability. It does not authorize product launch, production deployment, external pilot execution, real-data handling, public endpoint work, S5-B/S5-D reopen, ORDIV work, Red-3 action, AI_COLLAB change, Claude Web login automation, profile switching, cookie/session/token/auth-header inspection, or full four-tool automation.

## 3. Startup Checks

- Branch remained `codex/s3-a-runtime`.
- Baseline commit was `a02e53fd1a439db5b14752144074be15759cd63d`.
- Baseline manifest verification was `PASS`.
- `docs\DELEGATED_APPROVER_CHARTER.md` was readable.
- Authorization window remained active at verification time.
- `delegation_expires` remained `2026-05-06 23:59 Asia/Shanghai`.
- Working tree contained only known out-of-scope untracked files before this stage edits.
- User confirmed `ADSPOWER_USER_ID` was set through local environment provisioning.

## 4. Secret Boundary

AdsPower API-key material and profile identifiers are sensitive operational material.

The verification used local environment lookups and did not print, echo, commit, store, summarize, or log the API key or profile identifier.

The API key and profile identifier must not enter:

- chat
- repo files
- prompts
- review packs
- logs
- screenshots
- release artifacts

Future runs must read AdsPower API-key material and profile identifiers only through governed non-secret references, such as user-level environment variables or Windows Credential Manager references.

## 5. Verification Steps

| Step | Result | Notes |
| --- | --- | --- |
| Check API-key presence without printing value | PASS | User-level `ADSPOWER_API_KEY` was present. The key value was not displayed. |
| Check profile identifier presence without printing value | PASS | `ADSPOWER_USER_ID` was present. The value was not displayed. |
| Select safe Local API endpoint | PASS | `127.0.0.1:50325` was used for Local API access. |
| AdsPower Local API auth | PASS | Local API accepted the user-level API key. |
| Specified profile start/attach | PASS | `browser/start` returned success for the configured profile identifier. |
| CDP endpoint discovery | PASS | CDP endpoint metadata was returned. No cookies, tokens, auth headers, storage, or profile files were inspected. |
| CDP HTTP probe | PASS | `/json/version` and target metadata were reachable through the returned endpoint. |
| Claude Web target discovery | PASS | A `claude.ai` page target was found after profile start/attach. Full URLs and titles were not recorded. `claude_target_opened=false` means the probe did not need to open a new Claude target; it used the discovered target and connected directly through CDP WebSocket. |
| CDP WebSocket connection | PASS | WebSocket CDP connection succeeded using a non-secret browser-control connection. |
| Claude Web DOM readiness probe | PASS | Probe confirmed `claude.ai`, an editable input surface, and no credential prompt. Conversation text was not read. |
| Prompt submission | NOT_RUN_BY_DESIGN | This stage did not submit a prompt. The prior AdsPower Claude Web stage already verified harmless prompt round trip. |
| Clean terminal state | PASS | `hold_reason=null` and `exception_class=null` are expected for a clean readiness probe with no HOLD or exception. Any missing key/profile identifier, Local API rejection, CDP failure, missing Claude target, credential prompt, missing editable input, or ambiguous network state must populate a HOLD reason instead. |

## 5.1 Manifest Draft State

The release manifest remains in draft state for this stage:

- `current_release_sha256` is intentionally `null` until the full gate, release package, and release verification pass.
- `last_verified_at` is intentionally `null` until the full gate and release verification pass.
- Verification fields remain `PENDING_FULL_GATE_AFTER_REVIEW`.

No PASS state or release SHA may be recorded before the governed full closeout gate and release verification succeed.

## 6. Verified Capability

The AdsPower profile launch path is verified only for:

- reading `ADSPOWER_API_KEY` and `ADSPOWER_USER_ID` through local non-secret references without printing values
- calling AdsPower Local API `browser/start` for the configured profile identifier
- receiving a CDP endpoint from AdsPower
- locating a Claude Web page target after profile start/attach
- connecting through CDP without inspecting cookies, tokens, auth headers, browser storage, or profile files
- confirming Claude Web review-prompt readiness by checking host, editable input presence, and absence of credential prompt

Verified status: `VERIFIED_PROFILE_LAUNCH_TO_REVIEW_PROMPT_READY_WITH_LIMITS`.

## 7. Not Verified

This stage does not verify:

- profile creation
- profile switching
- bulk profile control
- login automation
- password entry
- cookie, token, auth header, browser storage, or profile-file inspection
- Claude account settings access
- billing, payment, or account-page access
- reading Claude conversation content
- submitting a new prompt in this stage
- high-risk Claude Web review workflows
- Red-2 or Red-3 review substitution
- external pilot readiness or execution
- production deployment
- full four-tool automation

## 8. Operating Limits

AdsPower profile launch may be used only for governed Claude Web review-prompt readiness when:

- the configured profile identifier is supplied through a non-secret local reference
- the API key is supplied through a non-secret local reference
- the launched or attached profile reaches `claude.ai`
- no credential prompt appears
- an editable Claude Web input surface is present
- the prompt contains no secrets, credentials, raw customer data, cookies, tokens, auth headers, or unredacted real evidence
- no unresolved HOLD blocks the action
- the readiness probe ends with `hold_reason=null` and no exception; otherwise the action remains HOLD

If any check fails, HOLD and fall back to manual Claude Web prompt transfer.

## 9. HOLD Queue Impact

- AHQ-022 may advance from `PARTIAL_VERIFIED_ACTIVE_PROFILE_ONLY` to `VERIFIED_PROFILE_LAUNCH_TO_REVIEW_PROMPT_READY_WITH_LIMITS`.
- AHQ-021 remains `VERIFIED_FOR_REVIEW_PROMPT_TEST_ONLY`; Claude Web output remains review evidence only.
- AHQ-020 remains `HOLD_FOR_TOOL_VERIFICATION` because Claude Code `cc switch` non-interactive review behavior is still not verified.
- AHQ-023 remains `CLOSED_BY_USER_ENV_AUTH_OK`.
- AHQ-003 through AHQ-014 remain HOLD.
- AHQ-017 remains `HOLD_IF_AMBIGUOUS`.

## 10. Non-Authorization

This stage does not authorize:

- API-key disclosure
- profile identifier disclosure
- AdsPower API-key or profile identifier printing, storing, echoing, logging, or committing
- cookie, token, auth header, browser storage, or session inspection
- AdsPower profile export
- AdsPower profile creation
- AdsPower profile switching
- login automation
- Claude account settings changes
- billing or payment access
- reading Claude conversation text beyond the future governed review response needed for a review result
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
- full four-tool automation
- full gate or release packaging without explicit authorization
- staging, commit, or push without explicit authorization
