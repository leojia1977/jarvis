# S6 R3 Low-Risk Burn Pool Heartbeat Prompt 2026-04-29

```xml
<heartbeat>
  <automation_id>secupilot-r3-low-risk-burn-runner</automation_id>
  <instructions>
Use current SecuPilot route state from repo D:\产品设计\New folder on branch codex/s3-a-runtime.
First read docs/HANDOFF.md, docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md,
docs/S6_DEPENDENT_ACCEPTANCE_BURN_POOL_2026_04_29.md,
docs/S6_JIRA_MISSING_CHILD_ISSUE_CREATION_SYNC_2026_04_29.md,
docs/S6_AP_T12_ACCEPTANCE_SCOPE_DECISION_2026_04_29.md,
docs/S6_MV_T05_RESCOPE_DECISION_2026_04_29.md, and
docs/S6_R3_EXACT_LOW_RISK_BURN_POOL_2026_04_29.md.
Verify git status is clean before work.
Execute R3 docs-only queue in order:
1) AP-T12A acceptance evidence index checklist.
2) MV-T05A P3-only Manager acceptance reconciliation checklist.
3) AP-T02 blocker refresh.
4) Parent epic closure readiness board.
5) Jira stale seed cleanup proposal.
6) Next implementation candidate board.
Do not touch frontend/src, Storybook, Playwright, fixtures, adapter, validator,
ResolvedSurfaceContext, backend/runtime/API/schema, dependencies, real data,
secrets, deploy, public endpoint, external pilot, or launch.
Do not transition parent epics, HOLD rows, or non-ready Jira issues to Done.
Stop any lane at IMPLEMENTATION_GO_REQUIRED before code changes.
For PASS docs-only batches, run git diff --check and py -3 scripts/git_preflight.py --mode pilot
before authorized stage/commit/push.
HOLD on scope expansion, dirty worktree, missing evidence, authority ambiguity,
backend/runtime/API/schema need, fixture/adapter/validator/ResolvedSurfaceContext change,
real data/secrets/deploy/public endpoint/external pilot, or non-ready ticket.
  </instructions>
</heartbeat>
```

