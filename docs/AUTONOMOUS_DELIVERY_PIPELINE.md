# Autonomous Delivery Pipeline

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Delivery Pipeline |
| Status | Docs-only autonomous operation startup draft for autonomous delivery pipeline |
| Snapshot | S5-AUTONOMOUS-OPERATION-STARTUP-2026-04-18-001 |
| Stage | s5-autonomous-operation-startup |
| Baseline commit | `ab8f022604c86fa6ed6edeb87435ca4f2f49c4b8` |

This pipeline defines how autonomous work should move from backlog item to governed closeout. It does not authorize implementation or launch execution.

## 1.1 Autonomous Session Startup Requirements

Before autonomous action, the activation prompt must require loading the core governance docs:

- `docs\AUTONOMOUS_AUTHORIZATION_POLICY.md`
- `docs\DELEGATED_APPROVER_CHARTER.md`
- `docs\AUTONOMOUS_DELIVERY_PIPELINE.md`
- `docs\AUTONOMOUS_HOLD_QUEUE.md`
- `docs\L3_CUSTOMER_TRIAL_LAUNCH_CRITICAL_PATH.md`
- `docs\PRODUCT_STATE.md`
- `docs\ROADMAP_AND_PARKED_ITEMS.md`
- `docs\GOVERNANCE_DECISION_LOG.md`

At the start of every autonomous session, Codex must re-read `docs\DELEGATED_APPROVER_CHARTER.md` and verify that `delegation_expires` has not passed. If the charter cannot be read, the timestamp is missing, or the authorization window has expired, all Red authority is HOLD and AI must not proceed with any Red-lane action.

Lane ambiguity defaults to the higher-restriction lane. If still unclear, HOLD.

The policy is `ACTIVE` only during the authorization window and only after the charter reread and expiry check pass. `ACTIVE` does not create blanket Red execution; Red-1/Red-2 still require exact per-action `DELEGATED_APPROVER_GO` where policy requires it, and any unresolved HOLD blocks the action.

## 1.2 Autonomous Operation Cadence

Default autonomous operation cadence is every 2 hours.

Each run should select one next allowed item, classify the lane, and report baseline read, selected task, files proposed or touched, checks run, HOLDs encountered, and any requested human or jarvis action.

Work selection priority is:

1. Green docs-only route judgment and planning artifacts.
2. Yellow docs-only or test-plan-only tasks when exact scope exists.
3. Red-1/Red-2 preparation packages only as drafts or `DELEGATED_APPROVER_GO` requests.
4. L3 critical path blocker reduction by drafting templates, checklists, or question sets.
5. HOLD queue maintenance.

During day 1, automation may draft Green/Yellow docs-only stages and prepare closeout gate material where authorized, but staging, commit, and push require explicit human confirmation.

## 2. Pipeline Stages

| Stage | Required input | Output |
| --- | --- | --- |
| Backlog item | Human/delegated/governed source need | Candidate work item |
| Route judgment | Baseline, boundaries, risk lane | Route decision or HOLD |
| Scoped ticket | Exact files, behavior, tests, lane, HOLD rules | Implementation or docs ticket |
| Draft/implement | Authorized file set | Draft or patch |
| Review | Claude Code review-only, and Claude Web/external when triggered | PASS, findings, or HOLD |
| Full gate | `py -3 scripts\git_preflight.py --mode all` | PASS or FAIL |
| Package | Release process and manifest | Review pack, release zip, verification |
| Commit/push | PASS, clean scope, lane permission | Governed commit |
| Product map update | Accepted closeout | Updated rolling maps |
| Next/HOLD | Remaining inputs and risks | Next route or HOLD queue entry |

## 3. Review Gates

- Claude Code review-only is required for governed drafts and implementations unless a stage explicitly says otherwise.
- Claude Web or a designated external reviewer is required when high-risk triggers apply.
- Review does not replace human or delegated GO where GO is required.

## 4. Gate Commands

Fast gate:

```text
py -3 scripts\git_preflight.py --mode fast
```

Full gate:

```text
py -3 scripts\git_preflight.py --mode all
```

Full gate is required before governed closeout commit/push when release/manifest verification must be refreshed.

## 5. Release Package And Manifest Rules

- Release artifacts may be generated only through the repo release process.
- Manifest snapshot/stage must match the governed stage.
- Manifest hashes must match tracked key files.
- Do not fabricate PASS, release SHA, or verification metadata.
- Release artifacts may be generated through the release process, but only tracked files may be staged for commit.

## 6. Product Map Updates

After closeout, update rolling maps when the governed state changes:

- `docs\PRODUCT_STATE.md`
- `docs\GOVERNANCE_DECISION_LOG.md`
- `docs\ROADMAP_AND_PARKED_ITEMS.md`

These maps summarize truth and do not authorize implementation.

`docs\PRODUCT_STATE.md` and `docs\ROADMAP_AND_PARKED_ITEMS.md` are passive governed context. They are not active authorization.

## 7. Commit Message Conventions

Use scoped messages such as:

- `docs: close <stage>`
- `test: <bounded test change>`
- `feat: <bounded implementation>`

The message must not imply readiness, customer launch, or implementation authorization beyond the governed scope.

## 8. Branch Rules

- Work from the governed branch named in the prompt.
- Confirm branch and HEAD before starting high-risk or closeout work.
- Do not include unrelated untracked files.
- Do not rewrite pushed history unless explicitly instructed by the human.

## 9. Network Slow Retry Rule

If network access, remote review, GitHub, Claude Web, external reviewer, or remote status check is slow/unresponsive for more than 5 minutes:

- For idempotent/read-only requests, AI may retry once.
- For non-idempotent requests, AI must first check whether the prior request succeeded before retrying.
- For git push, deployment, launch, external access, approval submission, package upload, or any customer/production-affecting action, AI must verify status before resending.
- Maximum automatic retry count: 1.
- If the second attempt exceeds 5 minutes or remains ambiguous, create/update HOLD queue and stop.
- Network slowness never permits bypassing review, gate, release verification, delegated approval, Claude Web/external review, or HOLD conditions.
- Do not duplicate approval requests unless the first request is confirmed not delivered or marked expired/void.
- If delivery status cannot be confirmed due to network conditions, treat the request as ambiguous and apply HOLD.
- Do not repeat non-idempotent launch/deploy/access actions without explicit delegated/human GO.

## 10. Failure Handling

- Fix failures if Green/Yellow and scoped.
- HOLD if Red, ambiguous, or external input is missing.
- HOLD if the gate failure points outside the allowed file set.
- HOLD if external access, real data, secrets, launch execution, or public endpoint work becomes necessary.
