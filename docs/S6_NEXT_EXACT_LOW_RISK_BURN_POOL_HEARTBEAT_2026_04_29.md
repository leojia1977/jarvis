# S6 Next Exact Low-Risk Burn Pool Heartbeat 2026-04-29

```xml
<heartbeat>
  <automation_id>secupilot-30m-bounded-burn-runner</automation_id>
  <instructions>
Use current SecuPilot route state from repo D:\产品设计\New folder on branch codex/s3-a-runtime.
First read docs/HANDOFF.md, docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md,
docs/S6_AP_PARENT_CLOSURE_REVIEW_2026_04_29.md, and
docs/S6_NEXT_EXACT_LOW_RISK_BURN_POOL_2026_04_29.md.
Verify git status is clean before work.

Continue with LR4 exact low-risk burn pool only:
1. E0 parent closure review.
2. GS parent closure review.
3. IN parent closure review.
4. CD parent closure review.
5. MV P3-only parent closure review.
6. EP parent parity audit.
7. SH parent parity audit.
8. CH parent parity audit.
9. Sprint planning board refresh / Jira Done diff.

Parent Jira Done transition is allowed only when exact Jira read-back proves every exposed child is Done
and the closure does not imply launch, deploy, real-data, backend/runtime/API/schema, or product-scope expansion.

Do not implement code. Do not touch frontend/src, Storybook, Playwright, fixtures, adapter, validator,
ResolvedSurfaceContext, backend/runtime/API/schema, dependency files, real data, secrets, deploy, public endpoint,
external pilot, or launch. Stop at IMPLEMENTATION_GO_REQUIRED before any code.
HOLD on dirty worktree, missing evidence, non-Done child, unmapped child, authority ambiguity, source ambiguity,
scope expansion, or mandatory external review trigger.
For PASS docs/Jira governance batches, run git diff --check and py -3 scripts/git_preflight.py --mode pilot
before authorized stage/commit/push.
  </instructions>
</heartbeat>
```
