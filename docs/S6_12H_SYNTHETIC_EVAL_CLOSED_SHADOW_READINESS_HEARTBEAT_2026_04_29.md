# S6 12h Synthetic Evaluation And Closed-Shadow Readiness Heartbeat 2026-04-29

## Heartbeat Prompt

```text
Continue SecuPilot docs-only readiness work from repo D:\产品设计\New folder on branch codex/s3-a-runtime.

Use current route state, not the obsolete Jira burn-down queue. First read:
- docs/HANDOFF.md
- docs/S6_PRODUCT_DEVELOPMENT_ROUTE_SELECTION_2026_04_25.md
- docs/S6_12H_SYNTHETIC_EVAL_CLOSED_SHADOW_READINESS_QUEUE_2026_04_29.md
- docs/S6_S1_CLOSED_SHADOW_G01_G09_EVIDENCE_BOARD_2026_04_29.md
- docs/S6_OFFLINE_SYNTHETIC_MAPPING_TOOLING_TICKETS_2026_04_29.md
- docs/S6_CUSTOMER_UAT_DEMO_PACK_2026_04_29.md
- docs/S6_S0_QWEN_CLOUD_HANDOFF_REFRESH_PACKET_2026_04_29.md

Verify git status is clean before work.

Allowed docs-only work:
- refresh S1 G-01 through G-09 evidence status from newly supplied non-secret evidence;
- refine MAP-T01 / MAP-T02 / MAP-T03 implementation checklists, stopping at IMPLEMENTATION_GO_REQUIRED before code;
- refine Customer UAT demo scripts, keeping them internal draft only;
- update the S0 Qwen cloud handoff packet after Jarvis supplies cloud-team non-secret fields;
- update route, handoff, progress board, HOLD maps, and idle reports.

Forbidden:
- no Qwen execution;
- no real data;
- no masked real data;
- no closed-shadow execution;
- no customer-visible output;
- no production write-back;
- no autonomous action;
- no backend/runtime/API/schema;
- no connector changes;
- no secrets;
- no Jira mutation;
- no deploy;
- no external pilot;
- no launch;
- no code changes;
- no Storybook or Playwright edits;
- no fixture/adapter/validator/ResolvedSurfaceContext changes.

Run docs gates for PASS docs-only batches:
- git diff --check
- py -3 scripts/git_preflight.py --mode pilot

If preflight refreshes releases/release_manifest.json and it is not in scope, restore it before commit.

Stage/commit/push only PASS docs-only updates.
HOLD on scope expansion, dirty worktree, missing source evidence, authority ambiguity, Qwen execution need, real/masked-real data need, backend/runtime/API/schema need, connector changes, secrets, customer-visible output, deploy, external pilot, or launch.
```
