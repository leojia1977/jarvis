# AdsPower Claude Web Runbook

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | AdsPower Claude Web Runbook |
| Status | Updated by AdsPower profile launch verification draft |
| Snapshot | S5-ADSPOWER-PROFILE-LAUNCH-VERIFICATION-2026-04-19-001 |
| Stage | s5-adspower-profile-launch-verification |
| Baseline commit | `a02e53fd1a439db5b14752144074be15759cd63d` |

This runbook defines the safe operating pattern for Claude Web automation through AdsPower. It does not authorize launch, deployment, external pilot execution, real-data handling, credential handling, public endpoint work, parked-stream reopen, Red-3 action, or AI_COLLAB change.

## 2. Secret Handling

AdsPower API-key material must be treated as secret.

Allowed:

- read a key through a governed non-secret reference, such as a user-level environment variable
- verify whether a key exists without printing it
- use the key in an HTTPS/local API request header without logging it

Prohibited:

- paste the key into chat
- write the key into repo files
- print, echo, store, or summarize the key
- include the key in prompts, review packs, release artifacts, screenshots, or logs
- commit the key

## 3. Startup Sequence

Every AdsPower Claude Web automation run must:

1. Read `docs\DELEGATED_APPROVER_CHARTER.md`.
2. Verify `delegation_expires` has not passed.
3. Load the core governance docs.
4. Confirm manifest baseline and git cleanliness.
5. Confirm the requested work is allowed by lane and stage scope.
6. Confirm AdsPower API-key material is available through an approved non-secret path.
7. Confirm no prompt contains secrets, credentials, raw customer data, or unredacted real evidence.

If any startup check fails, HOLD.

## 4. Allowed Automation Pattern

For approved review-prompt transfer only:

1. Query AdsPower Local API using a non-logged bearer token.
2. Start or attach to the configured AdsPower profile only when `docs\ADSPOWER_PROFILE_LAUNCH_RUNBOOK.md` permits it.
3. Locate a Claude Web page.
4. Connect through CDP without inspecting cookies, tokens, auth headers, browser storage, or profile files.
5. Focus the Claude Web input surface.
6. Insert the governed review prompt.
7. Submit the prompt.
8. Read only the response text needed for the governed review result.
9. Record review result as PASS, PASS_WITH_FINDINGS, FAIL, or HOLD.

## 5. Prohibited Browser Actions

Do not:

- create or switch profiles
- launch or attach to any AdsPower profile other than the configured governed profile identifier
- automate login
- enter passwords
- read or export cookies
- read tokens or auth headers
- inspect browser storage
- inspect AdsPower profile files
- modify Claude account settings
- access billing, payment, or account-management pages
- use Claude Web automation for customer data or external pilot evidence without a separate governed route

## 6. Review Result Handling

Claude Web output is review evidence only. It does not authorize implementation, launch execution, deployment, external pilot execution, public endpoint work, parked-stream reopen, or Red-3 action.

High-risk and Red-2+ uses still require the review, delegated approval, and human GO gates defined by the autonomous authorization policy.

## 7. Failure Handling

HOLD if:

- API key is missing
- AdsPower Local API rejects the key
- active profile is missing
- Claude Web page is missing
- CDP endpoint is unavailable
- credential or login prompt appears
- network status is ambiguous
- response cannot be confidently attributed to the current prompt
- any prompt would include secrets, raw customer data, or unredacted evidence

Network slowness follows the existing network slow retry rule.

## 8. Minimum Test Prompt

The minimum harmless test prompt is:

```text
Reply exactly with this token and no other text: <unique non-secret test token>
```

The test passes only if the expected token appears as a response after submission. The test token is non-secret and may be recorded as test evidence.
