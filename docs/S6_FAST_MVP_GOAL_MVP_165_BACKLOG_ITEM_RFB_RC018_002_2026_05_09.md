# S6 Fast MVP GOAL-MVP-165 Backlog Item RFB-RC018-002

Date: 2026-05-09

Goal: GOAL-MVP-165_BACKLOG_ITEM_RFB_RC018_002

Decision: PASS

## Scope

为 reviewer backlog closeout 脚本增加可选“保守措辞替换校验”参数，用于后续关闭 `RFB-RC018-002` 时显式校验旧文案已移除、新文案已存在。

## Commands Run

```text
py -3 scripts/validate_codex_goal_card.py docs/goals/GOAL-MVP-165_BACKLOG_ITEM_RFB_RC018_002.md
```

Result: PASS.

```text
py -3 -m unittest backend.tests.test_close_reviewer_backlog_items
```

Result: PASS, 3 tests passed.

```text
py -3 scripts/close_reviewer_backlog_items.py --help
```

Result: PASS, help 输出包含新增参数 `--text-check-file` 与 `--require-replacement`.

```text
git -c core.quotepath=false diff --check
```

Result: PASS（仅有既有非本 Goal 文件的 CRLF/LF warning）。

## Delivered Executable Object

- `scripts/close_reviewer_backlog_items.py` 新增可选校验能力：
  - `--text-check-file`：指定文本证据文件。
  - `--require-replacement old=>new`：对每个文本文件校验旧文案不存在、新文案存在。
  - 校验结果写入 closeout JSON/Markdown 的 `conservative_wording_checks`。

## Scope Guard Outcome

- 本 Goal 代码改动仅涉及：
  - `docs/goals/GOAL-MVP-165_BACKLOG_ITEM_RFB_RC018_002.md`
  - `scripts/close_reviewer_backlog_items.py`
  - `docs/S6_FAST_MVP_GOAL_MVP_165_BACKLOG_ITEM_RFB_RC018_002_2026_05_09.md`
- 未触碰已知历史残留与其他未授权路径。

## Next Suggested Goal

按 picker 规则进入该 backlog 项的一次 follow-up closeout Goal，调用 `close_reviewer_backlog_items.py` 并传入 RC018 文案替换校验参数，完成 `RFB-RC018-002` 的关闭证据。
