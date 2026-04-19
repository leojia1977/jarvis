# AdsPower Profile Launch Runbook

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | AdsPower Profile Launch Runbook |
| Status | Docs-only automation verification draft |
| Snapshot | S5-ADSPOWER-PROFILE-LAUNCH-VERIFICATION-2026-04-19-001 |
| Stage | s5-adspower-profile-launch-verification |
| Baseline commit | `a02e53fd1a439db5b14752144074be15759cd63d` |

This runbook defines the safe operating pattern for launching or attaching to the configured AdsPower profile for Claude Web review-prompt readiness. It does not authorize launch, deployment, external pilot execution, real-data handling, credential handling, public endpoint work, parked-stream reopen, Red-3 action, AI_COLLAB change, or full four-tool automation.

## 2. Secret And Identifier Handling

AdsPower API-key material is secret. AdsPower profile identifiers are sensitive operational material.

Allowed:

- read `ADSPOWER_API_KEY` through a governed non-secret local reference
- read `ADSPOWER_USER_ID` through a governed non-secret local reference
- verify whether each value exists without printing it
- use the API key in a Local API request header without logging it
- use the profile identifier as the `browser/start` selector without logging it

Prohibited:

- paste the API key or profile identifier into chat
- write either value into repo files
- print, echo, store, or summarize either value
- include either value in prompts, review packs, release artifacts, screenshots, or logs
- commit either value

## 3. Startup Sequence

Every AdsPower profile launch run must:

1. Read `docs\DELEGATED_APPROVER_CHARTER.md`.
2. Verify `delegation_expires` has not passed.
3. Load the core governance docs and toolchain docs.
4. Confirm manifest baseline and git cleanliness.
5. Confirm the requested work is allowed by lane and stage scope.
6. Confirm `ADSPOWER_API_KEY` and `ADSPOWER_USER_ID` are available through approved non-secret references.
7. Confirm no prompt contains secrets, credentials, raw customer data, or unredacted real evidence.

If any startup check fails, HOLD.

## 4. Allowed Launch Pattern

For approved review-prompt transfer only:

1. Query AdsPower Local API through `127.0.0.1:50325` using a non-logged bearer token.
2. Call `browser/start` with the configured profile identifier from `ADSPOWER_USER_ID`.
3. Use only the returned CDP endpoint metadata needed to connect to the browser target.
4. Locate a `claude.ai` page target.
5. Connect through CDP without inspecting cookies, tokens, auth headers, browser storage, or profile files.
6. Confirm the page host is `claude.ai`.
7. Confirm an editable Claude Web input surface exists.
8. Confirm no credential or login prompt is present.
9. Only after a governed review request is in scope under the current stage, AHQ-021 review-prompt-transfer limits, and applicable policy gates, insert and submit the governed review prompt.

## 5. Prohibited Browser Actions

Do not:

- create profiles
- switch profiles
- perform bulk profile control
- automate login
- enter passwords
- read or export cookies
- read tokens or auth headers
- inspect browser storage
- inspect AdsPower profile files
- modify Claude account settings
- access billing, payment, or account-management pages
- read Claude conversation history except the bounded response text required for a governed review result
- use Claude Web automation for customer data or external pilot evidence without a separate governed route

## 6. Review Result Handling

Claude Web output is review evidence only. It does not authorize implementation, launch execution, deployment, external pilot execution, public endpoint work, parked-stream reopen, Red-3 action, or full four-tool automation.

High-risk and Red-2+ uses still require the review, delegated approval, and human GO gates defined by the autonomous authorization policy.

## 7. Failure Handling

HOLD if:

- API key is missing
- profile identifier is missing
- AdsPower Local API rejects the key
- `browser/start` rejects the profile identifier
- CDP endpoint is unavailable
- Claude Web page is missing
- the browser lands outside `claude.ai`
- credential or login prompt appears
- editable input is missing
- network status is ambiguous
- response cannot be confidently attributed to the current prompt
- any prompt would include secrets, raw customer data, or unredacted evidence

Network slowness follows the existing network slow retry rule.

## 8. Minimum Readiness Probe

The minimum readiness probe may check only:

- API-key presence as a boolean
- profile identifier presence as a boolean
- Local API success/failure
- CDP endpoint presence
- Claude Web target presence
- host equals `claude.ai`
- editable input presence
- credential prompt presence as a boolean

The readiness probe must not read conversation text, cookies, tokens, auth headers, browser storage, profile files, API-key value, or profile identifier value.
