# Autonomous Delivery Pipeline

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | Autonomous Delivery Pipeline |
| Status | Docs-only draft for autonomous delivery pipeline review |
| Snapshot | S5-AUTONOMOUS-VACATION-OPERATING-MODEL-2026-04-17-001 |
| Stage | s5-autonomous-vacation-operating-model |
| Baseline commit | `da15c383e14bc4cae6c97017f91549194c37487d` |

This pipeline defines how autonomous work should move from backlog item to governed closeout. It does not authorize implementation or launch execution.

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

## 9. Failure Handling

- Fix failures if Green/Yellow and scoped.
- HOLD if Red, ambiguous, or external input is missing.
- HOLD if the gate failure points outside the allowed file set.
- HOLD if external access, real data, secrets, launch execution, or public endpoint work becomes necessary.
