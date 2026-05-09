# S6 Controlled Trial GO Review 48h Mission Charter

Date: 2026-05-09

Mission ID: `GOAL-CONTROLLED-TRIAL-GO-REVIEW-48H`

Machine contract: `artifacts/product_acceleration/controlled_trial_go_review_48h_mission_charter.json`

## Mission Objective

Move SecuPilot from RC-020 private-preview healthcheck PASS to a human GO/NO-GO review package for a controlled trial.

This mission does not authorize customer-visible release, external pilot launch, production deployment, live Qwen/API, live connectors, or production write-back.

Allowed final automation outcomes:

```text
READY_FOR_HUMAN_GO_REVIEW_FOR_CONTROLLED_TRIAL
HOLD_FOR_SPECIFIC_PRODUCT_OR_PACKAGE_FIXES
NO_GO_SECURITY_BOUNDARY
```

Forbidden final automation outcomes:

```text
READY_FOR_CUSTOMER
READY_TO_PUBLISH
READY_TO_DEPLOY
READY_FOR_EXTERNAL_PILOT
APPROVED_FOR_CUSTOMER_USE
APPROVED_FOR_PRODUCTION
```

## Candidate And Versioning

Target candidate:

```text
LOCAL_OFFLINE_GO_REVIEW_RC_021_CN
```

Rules:

- Do not overwrite RC-020.
- Do not reuse RC-020 zip names.
- RC-021 package, screenshot index, package manifest, healthcheck, and handoff material must refer to RC-021 as the current candidate.
- Historical RC-018/019/020 references may appear only in changelog, provenance, or closeout sections, never as the current reviewer path.

## Role Model

`Codex automation` is the primary 48h execution engine. It may edit files only inside the active Codex Goal exact scope, run checks, stage, and commit passing scoped work. It must not push.

`Codex Goal` is the executable task contract. Each run must create or update exactly one goal contract before implementation, with exact files, behavior, checks, HOLD conditions, rollback, evidence, and commit posture.

`VS Codex` is the local integration and recovery surface. It may unblock deterministic issues under exact scope, but it is not an independent release approver.

`SWE / mini-swe-agent` is not part of the 48h mainline. It may not execute product changes unless a later exact goal explicitly authorizes it with no-secret, exact-file, no-scope-expansion rules.

`Claude Code` is optional review-only evidence. It may be invoked only with non-secret prompts and no tools/write access. Timeout, auth, network, malformed verdict, or ambiguity records `CLAUDE_CODE_REVIEW_UNAVAILABLE` and does not block unless the active goal explicitly requires it.

`Claude Web / AdsPower` is optional review-only evidence. Timeout, auth, network, page/profile, or ambiguity records `CLAUDE_WEB_REVIEW_UNAVAILABLE` and does not block this 48h mission.

`ChatGPT Team2` is authorized as OpenAI API review-only evidence for package and boundary review. Inputs must be sanitized summaries, manifests, lint outputs, and text sidecars only. No secrets, auth headers, raw payloads, real data, masked-real data, or customer logs may be sent.

`Human` is the only GO/NO-GO decision-maker for controlled trial, external pilot, customer-visible output, production deployment, live Qwen/API, connectors, or write-back.

## Run Start Gate

Every run must start with:

```text
git -c core.quotepath=false status --short
git -c core.quotepath=false log --oneline -8
```

Known residue may remain unstaged:

```text
artifacts/product_acceleration/next_goal_candidate.json
artifacts/product_acceleration/next_goal_candidate.md
artifacts/local_demo_packages/local-offline-trial-rc-002-review-package-20260506.zip
artifacts/local_demo_packages/s1-closed-shadow-local-offline-trial-rc-003-review-package-20260506.zip
artifacts/local_demo_packages/s1-closed-shadow-local-offline-trial-rc-004-review-package-20260506.zip
artifacts/reviews/claude_code/mvp-69-current-diff-review-20260508.txt
```

If any other dirty or untracked path is present and not owned by the active goal, the run must stop with a read-only dirty-scope report.

## Mission Phases And Exit Gates

### Phase 1: Customer Misread Risk Copy Fix

Goal name:

```text
GOAL-RC021-01_CUSTOMER_MISREAD_RISK_COPY_FIX
```

Must reduce customer misunderstanding around deployment and remediation wording.

Required machine assertions from screenshot text sidecars:

```text
"查看部署准备" must_not_appear
"查看本地接入准备" must_appear
"隔离 finance-042 并锁定凭据" must_not_appear
"待复核：finance-042 隔离与凭据锁定建议" must_appear
```

Exit criteria:

- UI source and tests updated.
- Key screenshots and `.text.json` sidecars regenerated.
- Text sidecar assertions PASS.
- Screenshot safety scan PASS.
- No autonomous remediation, deployment, connector, write-back, or customer-visible output claim is introduced.

If any item fails, HOLD and do not package.

### Phase 2: RC-021 GO Review Package

Generate a unique RC-021 GO review package.

Exit criteria:

- Package manifest hashes match package contents.
- Screenshot index points only to current RC-021 screenshots.
- Zip and outer zip manifest are generated with unique RC-021 names.
- No stale RC-020-as-current path or candidate appears.
- Private-preview healthcheck PASS.

If any item fails, HOLD and do not enter reviewer material preparation.

### Phase 3: Customer Path Lint

Run product comprehension, boundary, and security exposure lint on text sidecars and package material.

Blocking findings:

- AI advice source is not default folded on first-load incident screenshots.
- ECI/VFE contains exploit, PoC, payload, attacker-readable attack path detail, or topology reachability.
- Local feedback claims backend write, artifact write, connector call, model call, production write-back, or customer-visible output.
- Any claim suggests actual deployment, live connector, live API, automatic isolation, blocking, approval, rejection, closure, or remediation.
- Any real data, masked-real data, secret, token, auth header, raw customer log, raw payload, or customer identifier appears.

Non-blocking notes:

- Visual density is high.
- A single phrase could be more product-friendly but does not imply capability or authorization.
- Expanded annex language is mildly technical but not in the customer first path.

Any blocking finding means HOLD or NO_GO_SECURITY_BOUNDARY.

### Phase 4: GO Review Materials

Prepare controlled-trial decision materials, not launch materials.

Required material:

```text
REVIEWER_START_HERE_中文.md
GO_REVIEW_HANDOFF_中文.md
TRIAL_SUCCESS_CRITERIA_中文.md
NO_GO_BOUNDARY_CHECKLIST_中文.md
KNOWN_NOTES_NOT_BLOCKERS_中文.md
STOP_CONDITIONS_中文.md
PACKAGE_MANIFEST.json
SCREENSHOT_INDEX_中文.json
SCREENSHOT_SAFETY_SCAN.json
PRIVATE_PREVIEW_HEALTHCHECK.json
```

The handoff may say:

```text
建议进入人工 GO/NO-GO 评审
```

It must not say:

```text
建议发布
建议试点
建议客户使用
```

The handoff must define the target audience and trial success criteria.

### Phase 5: Final Readiness Record

The final automation record must include:

```text
changed_customer_path
screenshots_updated
package_path
zip_sha256
healthcheck_status
team1_product_path_status
team2_package_boundary_status
boundary_status
known_notes
remaining_human_decisions
automation_final_outcome
```

Automation may only produce `READY_FOR_HUMAN_GO_REVIEW_FOR_CONTROLLED_TRIAL` if deterministic checks pass and no blocking Team1/Team2 finding exists.

## Picker Policy

The 48h mission overrides free backlog consumption. Picker output may be used only when it advances this mission.

Priority order:

1. Security or boundary blocker.
2. Customer path comprehension blocker.
3. Misleading deployment, capability, or remediation wording blocker.
4. Package integrity, manifest, hash, or screenshot index blocker.
5. Private-preview healthcheck blocker.
6. Reviewer decision-quality blocker.
7. One small product-path implementation with screenshots and closeout.
8. P3 only if it closes an existing item in the same run and touches no new surface.
9. Everything else PARK.

Anti-script-work rule:

If a run only edits scripts, helpers, or metadata, it must also fix a package blocker, healthcheck blocker, screenshot/text evidence blocker, reviewer handoff blocker, or explicit HOLD reason in the same run. Otherwise it is `NON_PRODUCTIVE_RUN` and must not commit.

## Productivity Gate

Each run must answer YES to at least one:

- advanced customer usability
- reduced reviewer blocker
- updated customer path screenshot or package
- passed or repaired healthcheck
- closed a specific blocker

If all are NO, stop without commit.

## Hard Boundaries

Always false:

```text
real_data
masked_real_data
live_qwen_api
live_connectors
production_writeback
customer_visible_output
external_pilot
production_launch
autonomous_containment
autonomous_remediation
autonomous_approval_or_rejection
push
```

Never expose attacker-readable attack path, PoC, exploit steps, payload, raw logs, credentials, auth headers, secrets, or topology reachability.

## Human-Only Decision Lock

Automation must not assert approval for:

```text
customer_visible_release
external_pilot
production_deployment
live_connector_enablement
live_qwen_or_api_enablement
production_writeback
```

The only authorized endpoint is a prepared package for human GO/NO-GO review.
