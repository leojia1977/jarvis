# S6 Design Unblock Frame Priority 2026-04-27

## 1. Document Control

| Field | Value |
| --- | --- |
| Title | S6 Design Unblock Frame Priority 2026-04-27 |
| Status | ACTIVE_DESIGN_UNBLOCK_PRIORITY |
| Date | 2026-04-27 |
| Repo root | `D:\产品设计\New folder` |
| Branch | `codex/s3-a-runtime` |
| Parent board | `docs\S6_SPRINT1_4_PROGRESS_RISK_BOARD_2026_04_27.md` |

This brief tells design which frames unblock the most automation work first. It is not a visual approval record and does not authorize final visual PASS.

## 2. Priority Order

Deliver in this order:

```text
VF-03
VF-02
VF-10
HF-SH-01
VF-01
VF-06
```

## 3. Frame Details

| Priority | Frame | Primary unlock | Why it matters now |
| --- | --- | --- | --- |
| 1 | `VF-03` | `GS-T04`; visual reconciliation for already implemented `CD-T01`, `CD-T02`, `CD-T04` | Highest Sprint 1 leverage; prevents expert-mode entry from being guessed. |
| 2 | `VF-02` | `IN-T02`, `IN-T04`; later `IN-T03` | Unblocks Inbox read-only/escalation skeletons and reduces case-intake ambiguity. |
| 3 | `VF-10` | `EP-T02`, `EP-T03`; visual reconciliation for `CD-T04` | Allows evidence weakening/degradation treatment without inventing style. |
| 4 | `HF-SH-01` | `SH-T01`, later `SH-T02` | Turns the already implemented `SH-T03` route guard into useful Search/History list work. |
| 5 | `VF-01` | `CH-T01`, later `CH-T02` | Opens Sprint 4 Coverage & Health skeleton/hardening path. |
| 6 | `VF-06` | `MV-T01`, later `MV-T02` | Starts P3 Manager readiness, but remains authority-gated. |

## 4. What Design Should Deliver

For each frame, provide:

- visible frame screenshot or Figma frame;
- frame id matching tracker id;
- target role/surface;
- required visible labels;
- required hidden/absent controls;
- degraded/unavailable state if relevant;
- notes on what must not be implied.

## 5. Design Guardrails

Design must not:

- turn expert mode into a permission unlock ladder;
- show P1 approval controls or ActionMode choices;
- show P3 host-level raw evidence;
- use approval audit as a coverage unlock ladder;
- represent `OBSERVATION_WINDOW` as frontend auto-execution progress;
- replace required inline warnings with toast-only behavior;
- invent new product scope to fill visual gaps.

## 6. Automation Use

When a frame lands:

1. open a frame intake/reconciliation checklist;
2. map it to the exact tracker tickets it unblocks;
3. decide whether existing skeleton work can move to visual reconciliation;
4. run visual regression / Storybook / Playwright follow-up only inside exact files;
5. never mark final visual PASS without explicit frame evidence.

## 7. Next Safe Action

Next safe action:

```text
DESIGN_DELIVER_VF_03_FIRST
```
