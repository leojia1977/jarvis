# SP3-B-4：Degraded UX Contract 冻结文档

> **状态**：FROZEN — Codex 实现必须遵守本文档  
> **Snapshot 基线**：S3-B-2026-04-08-002  
> **目标**：让前端无需读取原始 `audit_trail` 也能稳定展示降级状态、禁用不安全处置、解释缺失范围

---

## 一、设计原则

`DEGRADED UX Contract` 是 `case_view` 的补充层，不替换原始数据。

目标不是增加更多分析结论，而是冻结一组 **前端可以直接消费** 的字段，回答三个问题：

1. 当前案卷是否处于降级状态
2. 为什么降级
3. 因为降级，哪些动作现在不能做

---

## 二、冻结字段

在 `case_view.executive_summary` 与 `case_view.analysis_limits` 中新增/冻结以下字段：

```json
{
  "case_view": {
    "executive_summary": {
      "status_banner": {
        "visible": true,
        "severity": "warning",
        "title": "调查已降级",
        "message": "部分关键工具或遥测不可用，当前结论可能不完整。"
      }
    },

    "recommended_action": {
      "available": false,
      "disabled_reason": "调查降级，处置建议不可用",
      "action_state": "DISABLED_DEGRADED"
    },

    "analysis_limits": {
      "degraded": true,
      "degraded_reasons": ["tool_timeout", "blast_radius_no_target"],
      "missing_telemetry": [],
      "missing_telemetry_summary": null,
      "unavailable_tools": ["timeout"],
      "unavailable_tools_summary": "以下能力未完成：timeout",
      "unresolved_pivots": [],
      "action_disabled_reason": "调查降级，处置建议不可用"
    }
  }
}
```

---

## 三、派生规则

| 字段 | 来源 | 规则 |
|---|---|---|
| `executive_summary.status_banner.visible` | `investigation_status`, `analysis_limits` | `investigation_status == "DEGRADED"` 或存在 `missing_telemetry` / `unavailable_tools` 时为 `true` |
| `executive_summary.status_banner.severity` | `investigation_status` | `DEGRADED -> warning`，其余为空 |
| `executive_summary.status_banner.title` | `investigation_status` | `DEGRADED -> 调查已降级`，`PARTIAL -> 调查存在缺口` |
| `executive_summary.status_banner.message` | `analysis_limits` | 使用确定性模板生成 |
| `recommended_action.action_state` | `recommended_action.available`, `investigation_status` | `available=true -> AVAILABLE`；`DEGRADED -> DISABLED_DEGRADED`；无动作 -> `UNAVAILABLE` |
| `analysis_limits.missing_telemetry_summary` | `analysis_limits.missing_telemetry` | 非空时生成中文摘要 |
| `analysis_limits.unavailable_tools_summary` | `analysis_limits.unavailable_tools` | 非空时生成中文摘要 |

---

## 四、生成规则

### 4.1 Status Banner

- `DEGRADED`：
  - `visible = true`
  - `severity = "warning"`
  - `title = "调查已降级"`
  - `message = "部分关键工具或遥测不可用，当前结论可能不完整。"`

- `PARTIAL` 且存在 `missing_telemetry`：
  - `visible = true`
  - `severity = "info"`
  - `title = "调查存在缺口"`
  - `message = "存在未覆盖的遥测缺口，建议人工补充复核。"`

- `COMPLETE`：
  - `visible = false`
  - `severity = null`
  - `title = null`
  - `message = null`

### 4.2 Action State

| 条件 | `action_state` |
|---|---|
| `recommended_action.available == true` | `AVAILABLE` |
| `investigation_status == "DEGRADED"` | `DISABLED_DEGRADED` |
| 其余无可执行动作 | `UNAVAILABLE` |

### 4.3 Summary 文案

- `missing_telemetry_summary`
  - 空：`null`
  - 非空：`共 N 项遥测缺口，建议优先补齐关键主机或工具日志。`

- `unavailable_tools_summary`
  - 空：`null`
  - 非空：`以下能力未完成：tool1, tool2`

---

## 五、实现要求

1. 只允许在 `case_view` 层派生，不修改原始 `audit_trail`
2. 不允许调用 LLM
3. 不允许在 `COMPLETE` 案卷里显示可见 banner
4. 不允许在 `DEGRADED` 案卷里把 `action_state` 标成 `AVAILABLE`

---

## 六、测试要求

至少覆盖：

1. `DEGRADED` 案卷：
   - `status_banner.visible = true`
   - `recommended_action.action_state = DISABLED_DEGRADED`
   - `action_disabled_reason` 非空

2. `PARTIAL` 且有 `missing_telemetry`：
   - `status_banner.visible = true`
   - `status_banner.title = 调查存在缺口`
   - `missing_telemetry_summary` 非空

3. `COMPLETE`：
   - `status_banner.visible = false`
   - `action_state` 与 `recommended_action.available` 一致

---

> 本文档冻结。Codex 可基于此直接开始 SP3-B-4 实现。
