# S6 R2 Low-Risk Burn Pool Heartbeat Prompt

## Document Control

- Document: `S6_R2_LOW_RISK_BURN_POOL_HEARTBEAT_PROMPT_2026_04_29`
- Date: 2026-04-29
- Purpose: copy-ready automation heartbeat for docs-only low-risk work

## Heartbeat

```xml
<heartbeat>
  <automation_id>secupilot-r2-low-risk-burn-runner</automation_id>
  <instructions>
Continue SecuPilot R2 low-risk burn pool from repo D:\产品设计\New folder on branch codex/s3-a-runtime.
First read docs/HANDOFF.md, docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md,
docs/S6_REMAINING_SCOPE_TRIAGE_BATCH_R1_CHECKLISTS_CLOSEOUT_2026_04_29.md,
and docs/S6_R2_LOW_RISK_BURN_POOL_2026_04_29.md.
Verify git status before work.

Execute only R2 docs-only queue items:
R2-01 Jira parity audit refresh;
R2-02 R1 source input packet for AP-T06 / AP-T09 / CD-T06;
R2-03 R1 authority review prompt pack for CH-T04 / IN-T03 / MV-T02;
R2-04 dependent ticket HOLD map for AP-T11 / AP-T12 / CD-T07 / IN-T06 / MV-T05 / AP-T02;
R2-05 Sprint planning candidate board;
R2-06 runner heartbeat prompt refresh if needed;
R2-07 backlog tracker parity note;
R2-08 idle fallback report.

Do not implement code.
Do not touch frontend/src, Storybook, Playwright, fixtures, adapter, validator, ResolvedSurfaceContext,
backend/runtime/API/schema, dependency files, secrets, release package contents except release_manifest via preflight,
or any real-data path.
Do not create or transition Jira cloud issues without later exact Jira sync authorization.
Stop any lane at IMPLEMENTATION_GO_REQUIRED before code changes.

Allowed docs are docs/S6_R2_*.md, docs/HANDOFF.md,
docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md,
docs/S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md,
and releases/release_manifest.json only when pilot preflight refreshes it.

Run git diff --check and py -3 scripts/git_preflight.py --mode pilot before any authorized docs-only commit.
HOLD on scope expansion, missing source evidence, implementation need, product/authority ambiguity,
backend/runtime/API/schema need, fixture/adapter/validator/ResolvedSurfaceContext change,
real data, secrets, deploy, public endpoint, external pilot, or dirty worktree not produced by this heartbeat.
  </instructions>
</heartbeat>
```

## Non-Authorization

This heartbeat is operational routing only. It does not authorize implementation, Jira Done mutation, backend/runtime/API/schema, real data, secrets, deploy, public endpoint, external pilot, or launch.
