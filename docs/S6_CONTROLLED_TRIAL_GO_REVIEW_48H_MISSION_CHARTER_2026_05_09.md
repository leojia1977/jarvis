# S6 Controlled Trial GO Review 48h Mission Charter

Date: 2026-05-09

Mission ID: `GOAL-CONTROLLED-TRIAL-GO-REVIEW-48H`

Mission status: `ACTIVE_AFTER_AUTOMATION_RESUME`

Machine contract: `artifacts/product_acceleration/controlled_trial_go_review_48h_mission_charter.json`

## Mission Statement

This 48h mission prepares evidence for human controlled-trial GO review after return; it does not approve customer-visible release, external pilot, live connector, live API, production deployment, or production writeback.

The human is expected to be offline during this 48h window. Automation may prepare and commit scoped evidence, but the final GO/HOLD/NO-GO decision is delayed until the human returns.

## Mission Objective

Move SecuPilot from RC-020 private-preview healthcheck PASS to a complete human GO/NO-GO review package for a controlled trial decision.

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
APPROVED_FOR_EXTERNAL_PILOT
APPROVED_FOR_PRODUCTION
APPROVED_FOR_LIVE_CONNECTOR
APPROVED_FOR_LIVE_QWEN_OR_API
APPROVED_FOR_PRODUCTION_WRITEBACK
```

## Authorization Model

Type A process actions are preauthorized inside the active Codex Goal exact scope:

- Select a mission-allowed Codex Goal.
- Edit exact allowed files.
- Run deterministic checks.
- Generate screenshots and text sidecars.
- Build the RC-021 local/offline package.
- Run package, lint, and healthcheck commands.
- Stage and commit passing scoped work.

Type B judgment actions are conditionally delegated only under this charter:

- Classify deterministic blockers as PASS, PASS_WITH_NOTES, HOLD, or NO_GO_SECURITY_BOUNDARY.
- Merge Team1 and Team2 review gate results by the rules below.
- Continue past non-blocking notes when no blocking finding exists.

Type C actions are never authorized in this mission:

- Customer-visible release or publish.
- External pilot launch.
- Production deployment.
- Live connector enablement.
- Live Qwen/API enablement, except OpenAI API review-only Team2 with sanitized inputs.
- Production write-back.
- Autonomous containment, remediation, isolation, blocking, approval, rejection, or closure.
- Push.

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

`Codex Goal` is the only executable task contract. It is not a person, reviewer, or decision maker. No actor may execute work that is not attached to an active, mission-allowed Codex Goal.

Every Codex Goal must define exact objective, allowed files, forbidden files, behavior change, screenshots or text evidence, package or healthcheck commands, acceptance criteria, HOLD conditions, rollback, commit posture, and closeout evidence.

`Codex automation` is the primary 48h execution engine. It may edit files only inside the active Codex Goal exact scope, run checks, stage, and commit passing scoped work. It must not push.

`VS Codex / Local Codex` is the integration and recovery surface. It may unblock deterministic issues under exact scope and assemble the final return package. It must not convert readiness into authorization.

`SWE / mini-swe-agent` is not part of the 48h mainline. It is an implementation agent, not a reviewer, but it is excluded here to avoid a second implementation actor conflicting with Codex automation. It may not execute product changes unless a later human-authored exact Goal explicitly authorizes it.

`Claude Code` is optional and conditional code/diff review only. It may review scope, diff risk, test risk, script reliability, and package-builder regression risk. It is not a product language reviewer, package-governance authority, or GO/NO-GO decision maker.

`Claude Web / AdsPower Team1` is the product path review gate. It reviews customer comprehension across product home, incident workbench, AI advice source, ECI/VFE summary, missing evidence, collection window, and local feedback. It does not review code, hashes, or production authorization.

`ChatGPT Team2` is the governance, boundary, and package review gate via OpenAI API review-only. Inputs must be sanitized summaries, manifests, lint outputs, healthcheck outputs, screenshot indexes, and text sidecars only. It must not receive secrets, tokens, auth headers, raw customer logs, raw payloads, real data, masked-real data, or customer identifiers.

`Human` is the sole accountable decision maker for controlled trial GO/HOLD/NO-GO, reviewer release, customer-visible output, external pilot, live API/connector, production deployment, and write-back.

## RACI Summary

| Role | Responsible | Accountable | Consulted | Informed |
| --- | --- | --- | --- | --- |
| Codex Goal | Scope contract | None | Human-authored charter | All actors |
| Codex automation | Implementation pipeline | None | VS Codex | Human return package |
| VS Codex | Integration and unblock | None | Team1, Team2, Claude Code | Human |
| SWE / mini-swe-agent | Not in mainline | None | None | Human if later enabled |
| Claude Code | Code/diff review if applicable | None | VS Codex | Human return package |
| Claude Web Team1 | Product path review | None | VS Codex | Human return package |
| ChatGPT Team2 | Package and boundary review | None | VS Codex | Human return package |
| Human | Final decision | Human | Review gates | All artifacts |

## Workflow State Machine

```text
MISSION_CHARTER_ACTIVE
CODEX_GOAL_SELECTED
IMPLEMENTATION_COMPLETE
DETERMINISTIC_CHECKS_COMPLETE
CODE_REVIEW_COMPLETE_OR_EXPLICITLY_UNAVAILABLE
PRODUCT_PATH_REVIEW_COMPLETE
PACKAGE_BOUNDARY_REVIEW_COMPLETE
GO_REVIEW_PACKAGE_ASSEMBLED
READY_FOR_HUMAN_GO_REVIEW
```

Automation must not advance to:

```text
HUMAN_GO
CUSTOMER_READY
PILOT_APPROVED
PRODUCTION_READY
LIVE_CONNECTOR_APPROVED
```

## Review Gates

Deterministic checks are required evidence. They do not replace Claude Code, Team1, Team2, or Human decisions.

Claude Code is required when code, scripts, package builder, validation logic, or healthcheck logic changes. If unavailable, record `REVIEW_TOOL_UNAVAILABLE`. If only an already generated package is being reviewed and no code/script/check logic changed, record `NOT_APPLICABLE`.

Team1 product path review is required when UI copy, screenshots, customer path package, or reviewer-facing materials change.

Team2 package and boundary review is required when package contents, manifest, hash, screenshot index, boundary language, or GO review readiness changes.

Team1 and Team2 are independent parallel gates:

- Any `HOLD` from either gate means overall `HOLD_FOR_SPECIFIC_PRODUCT_OR_PACKAGE_FIXES`.
- Any `NO_GO_SECURITY_BOUNDARY` means overall `NO_GO_SECURITY_BOUNDARY`.
- `PASS_WITH_NOTES` from one or both gates may continue only when no blocking finding exists.
- Both raw reviewer outputs and the merged result must be included in the return package.

## Review Tool Availability

Claude Code unavailable:

- Record `REVIEW_TOOL_UNAVAILABLE`.
- Do not claim code review PASS.
- Continue implementation only if deterministic checks PASS and the active goal does not require Claude Code as a blocker.
- Final readiness must record `code_review_status`.

Claude Web Team1 unavailable:

- Record `TEAM1_PRODUCT_PATH_REVIEW_PENDING`.
- Do not mark final readiness as READY unless a later successful Team1 review exists.

ChatGPT Team2 unavailable:

- Record `TEAM2_PACKAGE_BOUNDARY_REVIEW_PENDING`.
- Do not mark final readiness as READY unless a later successful Team2 review exists.

OpenAI API is allowed only for Team2 review-only with sanitized inputs. If unavailable, no manual API setup is required during the 48h window; record the unavailable status and stop final readiness at HOLD/PENDING as applicable.

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

## Mission-Allowed Goals

Picker cannot freely consume backlog or generate arbitrary P3 work. It may execute only these mission-bounded goals or a direct sub-goal derived from them that touches no broader surface:

```text
GOAL-RC021-01_CUSTOMER_MISREAD_RISK_COPY_FIX
GOAL-RC021-02_SCREENSHOT_TEXT_EVIDENCE_REFRESH
GOAL-RC021-03_LOCAL_OFFLINE_GO_REVIEW_PACKAGE_BUILD
GOAL-RC021-04_CUSTOMER_PATH_LINT_AND_HEALTHCHECK
GOAL-RC021-05_REVIEW_GATES_AND_RETURN_PACKAGE
```

Any new goal outside this list requires a future human-authored charter update.

## Mission Phases And Exit Gates

### Phase 1: Customer Misread Risk Copy Fix

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

The handoff must define target audience and trial success criteria.

### Phase 5: Return State Package

Human return package must include:

```text
executed_goal_results
hold_reasons_and_current_status
raw_team1_product_path_review
raw_team2_package_boundary_review
code_review_status_if_applicable
wake_up_conditions_triggered
go_review_package_status
blocking_items
unexecuted_goals_and_reasons
one_line_return_decision_state
```

Allowed return decision states:

```text
READY_FOR_HUMAN_GO_REVIEW
BLOCKED_NEEDS_HUMAN_UNBLOCK
PARTIAL_COMPLETE
NO_GO_SECURITY_BOUNDARY
```

## Wake-Up Conditions

If any condition occurs, stop the mission and record a wake-up note for the human:

- Any artifact suggests live/API/connector/production authorization intent.
- Any reviewer or deterministic check returns `NO_GO_SECURITY_BOUNDARY`.
- Two consecutive mission goals HOLD for the same reason.
- Any fixture or artifact appears to contain real or masked-real data.
- Acceptance commands fail more than three times with no deterministic root cause.

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

The only authorized endpoint is a prepared package for human GO/NO-GO review after return.
