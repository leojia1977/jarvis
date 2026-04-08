# SP3-B-1：Case View Contract 冻结文档

> **状态**：FROZEN — Codex 实现必须遵守本文档  
> **Snapshot 基线**：S3-A-2026-04-08-001  
> **决策方**：Claude（review-and-decision）  
> **实现方**：Codex（implementation-and-release）

---

## 一、设计原则

Case View 是**一层视图模型**，叠加在 `_assemble_case()` 的原始 payload 之上。它不替换原始字段，而是从中派生出分析员可直接消费的 7 个面板。

原始字段（`tool_results`、`forensic_result`、`triage_summary`、`intel_summary`、`audit_trail`）仍然保留，供 L2 下钻和 API 消费者使用。Case View 的面板是**只读派生**，不引入新的数据源。

---

## 二、Case View 7 面板 Schema

在案卷 payload 的顶层新增一个 `case_view` 对象。以下是冻结的字段定义。

```json
{
  "...原有 V3.1 字段不变...": "...",

  "case_view": {

    "executive_summary": {
      "verdict": "CRITICAL_ACTION_REQUIRED | HIGH_RISK | MEDIUM_RISK | LOW_RISK | DEGRADED",
      "investigation_status": "COMPLETE | PARTIAL | DEGRADED",
      "risk_score": 9.2,
      "confidence_label": "HIGH | MEDIUM | LOW",
      "one_liner": "开发机到域控的完整横向移动攻击链，已到凭证窃取阶段。"
    },

    "what_happened": {
      "scenario_name": "Lateral Movement + Credential Theft",
      "attack_stages": ["Execution", "Lateral Movement", "Credential Access"],
      "affected_hosts": ["DEV-WS-01", "WKST-047"],
      "primary_chain": {
        "chain_id": "WKST-047:chain-000",
        "anomaly_score": 10.0,
        "process_path": ["services.exe", "PSEXESVC.exe", "cmd.exe", "mimikatz.exe"],
        "highlight_node_id": "WKST-047:chain-000:node-003",
        "highlight_reason": "已知攻击工具 mimikatz.exe (T1003.001)"
      },
      "source": "forensic_result"
    },

    "why_it_matters": {
      "ioc_hits": [
        {"type": "ip", "value": "185.220.101.45", "actor": "RANSOMWARE-X", "match_type": "exact"}
      ],
      "persistence_count": 1,
      "persistence_summary": "检测到 PSEXESVC 服务注册（持久化）",
      "blast_impact_summary": "隔离影响 12 个级联资产，预估损失 ¥2,310,000",
      "business_risk": "HIGH",
      "source": "intel_summary + forensic_result + tool_results.blast_radius"
    },

    "jarvis_plan": {
      "hypothesis": "内网可能存在横向移动行为",
      "status": "executed",
      "steps_total": 4,
      "steps_completed": 4,
      "steps_degraded": 0,
      "next_suggested": null,
      "source": "hunt_plan"
    },

    "recommended_action": {
      "available": true,
      "action_type": "EMERGENCY_ISOLATE",
      "targets": ["DEV-WS-01", "WKST-047"],
      "blast_summary": "直接影响 1 资产，级联 12 资产，¥2,310,000",
      "approval_required": true,
      "disabled_reason": null,
      "source": "suggested_action"
    },

    "evidence_panels": {
      "top_chains": "→ forensic_result.top_chains（已有，直接引用）",
      "ioc_table": "→ intel_summary.matches（已有，直接引用）",
      "persistence": "→ forensic_result.persistence_mechanisms（已有，直接引用）",
      "evidence_gaps": "→ forensic_result.evidence_gaps（已有，直接引用）"
    },

    "analysis_limits": {
      "degraded": false,
      "degraded_reasons": [],
      "missing_telemetry": [],
      "unavailable_tools": [],
      "unresolved_pivots": [],
      "action_disabled_reason": null
    }
  }
}
```

---

## 三、字段来源映射规则

每个 case_view 面板的字段必须从已有的原始字段派生。以下是严格的映射关系，Codex 实现时不得引入原始 payload 中不存在的数据。

| case_view 字段 | 数据来源 | 派生规则 |
|---|---|---|
| `executive_summary.verdict` | `verdict_status` | 直接复制 |
| `executive_summary.investigation_status` | `investigation_status` | 直接复制 |
| `executive_summary.risk_score` | `risk_score` | 直接复制 |
| `executive_summary.confidence_label` | `confidence_label` | 直接复制 |
| `executive_summary.one_liner` | **需要生成** | 从 `scenario_name` + `forensic_result.attack_stages_observed` + `forensic_result.top_chains[0]` 拼接，模板化，不调 LLM |
| `what_happened.scenario_name` | `scenario_name` | 直接复制 |
| `what_happened.attack_stages` | `forensic_result.attack_stages_observed` | 直接复制 |
| `what_happened.affected_hosts` | `forensic_result.hosts_analyzed` | 直接复制 |
| `what_happened.primary_chain` | `forensic_result.top_chains[0]` | 提取第一条链的摘要 |
| `why_it_matters.ioc_hits` | `intel_summary.matches` | 过滤 match_type=exact 的条目 |
| `why_it_matters.persistence_count` | `forensic_result.persistence_mechanisms` | len() |
| `why_it_matters.blast_impact_summary` | `suggested_action.blast_radius_desc` | 直接复制 |
| `jarvis_plan.*` | `hunt_plan` | 直接映射 |
| `recommended_action.available` | `suggested_action is not None` | 布尔判断 |
| `recommended_action.disabled_reason` | 当 `investigation_status == DEGRADED` 时 | 设为 `"调查降级，处置建议不可用"` |
| `analysis_limits.degraded` | `audit_trail.degraded` | 直接复制 |
| `analysis_limits.degraded_reasons` | `audit_trail.degraded_reasons` | 直接复制 |
| `analysis_limits.missing_telemetry` | `forensic_result.evidence_gaps` | 直接引用 |
| `analysis_limits.action_disabled_reason` | 同 `recommended_action.disabled_reason` | 一致 |

---

## 四、DEGRADED 状态的 case_view 行为规则

这是 Sprint 2 冻结协议的延续，在 case_view 层面的具体约束：

| 条件 | case_view 行为 |
|---|---|
| `investigation_status == DEGRADED` | `recommended_action.available = false`，`recommended_action.disabled_reason = "调查降级，处置建议不可用"` |
| `investigation_status == DEGRADED` | `analysis_limits.degraded = true` |
| `investigation_status == PARTIAL` 且 `forensic_result.evidence_gaps` 非空 | `analysis_limits.missing_telemetry` 列出具体缺失 |
| `confidence_label == LOW` | `executive_summary.one_liner` 末尾追加 `"（置信度低，需人工确认）"` |

---

## 五、`one_liner` 模板化生成规则

**不调 LLM**。使用确定性模板从已有字段生成。

```python
def generate_one_liner(case: dict) -> str:
    fr = case.get("forensic_result") or {}
    stages = fr.get("attack_stages_observed", [])
    hosts = fr.get("hosts_analyzed", [])
    chains = fr.get("top_chains", [])
    scenario = case.get("scenario_name", "")
    verdict = case.get("verdict_status", "")
    confidence = case.get("confidence_label", "")

    if not chains:
        if verdict == "DEGRADED":
            return "调查数据不完整，无法给出确定性结论。"
        return f"已分析 {len(hosts)} 台主机，未发现高危攻击链。"

    top = chains[0]
    procs = [n["process_name"] for n in top.get("path", [])]
    chain_str = " → ".join(procs[-3:]) if len(procs) > 3 else " → ".join(procs)
    stage_str = " → ".join(stages) if stages else "未知阶段"

    line = f"{scenario or '安全事件'}：检测到 {chain_str} 攻击链，阶段覆盖 {stage_str}。"

    if confidence == "LOW":
        line += "（置信度低，需人工确认）"

    return line
```

---

## 六、`evidence_panels` 的引用规则

`evidence_panels` 不存储数据副本，只存储引用路径。前端通过路径从原始 payload 中读取。

```json
{
  "evidence_panels": {
    "top_chains": {"ref": "forensic_result.top_chains", "count": 3},
    "ioc_table": {"ref": "intel_summary.matches", "count": null},
    "persistence": {"ref": "forensic_result.persistence_mechanisms", "count": null},
    "evidence_gaps": {"ref": "forensic_result.evidence_gaps", "count": null}
  }
}
```

这样做的原因：避免数据在案卷中重复存储，减少 schema 漂移风险。前端拿到 `ref` 后从同一个 payload 中取值，保证一致性。

---

## 七、实现指引（给 Codex）

### 7.1 实现位置

在 `_assemble_case()` 末尾、`return` 之前，调用一个新函数：

```python
case_view = build_case_view(case_payload)
case_payload["case_view"] = case_view
```

`build_case_view()` 应作为独立函数（不是类方法），放在 `graph.py` 同文件或新建 `backend/app/agents/case_view.py`。建议后者，保持 graph.py 不再膨胀。

### 7.2 测试要求

在 `backend/tests/` 下新建 `test_case_view.py`，至少覆盖：

1. 正常案卷（有 forensic_result + intel + blast）→ 7 个面板全部存在
2. 无 T3 的案卷（summarize_recent）→ `what_happened.primary_chain` 为 null，不报错
3. DEGRADED 案卷 → `recommended_action.available = false`，`disabled_reason` 非空
4. 无 hunt_plan 的案卷 → `jarvis_plan` 为 null
5. `one_liner` 生成：有链条时含进程名，无链条时含主机数，DEGRADED 时明确说不确定

### 7.3 不允许做的事

- 不允许在 `build_case_view` 中调用任何工具链或 LLM
- 不允许修改原始 `forensic_result` / `intel_summary` / `suggested_action` 的结构
- 不允许在 `case_view` 中引入原始 payload 中不存在的数据
- 不允许在 DEGRADED 状态下让 `recommended_action.available = true`

---

## 八、与 S3-B 后续 ticket 的关系

| ticket | 依赖本文档 | 说明 |
|---|---|---|
| SP3-B-2 Add Backend Case Shaping Layer | 直接实现 | `build_case_view()` 函数 |
| SP3-B-3 Jarvis Embedding | 消费 `jarvis_plan` 面板 | 已在本 contract 中定义 |
| SP3-B-4 Degraded UX Contract | 消费 `analysis_limits` + `recommended_action.disabled_reason` | 已在本 contract 中定义 |
| SP3-B-5 Case Contract Tests | 验证本 contract | 测试要求见 7.2 |
| SP3-B-6 Product Review With Claude | 基于实现后的 review pack 审查 | — |

---

## 九、上一轮审查遗留项闭环

| 遗留项 | 闭环方式 |
|---|---|
| `forensic_result` 如何映射到 case view（上轮 P2 gap） | `what_happened.primary_chain` 从 `forensic_result.top_chains[0]` 派生，`what_happened.attack_stages` 从 `forensic_result.attack_stages_observed` 派生 |
| `infer_intent` 与 `intent_router` 重复（上轮 F-02） | 不在本 contract 范围内，建议 Codex 在 SP3-B-2 实现时顺手统一 |

---

> 本文档冻结。Codex 可基于此直接开始 SP3-B-2 实现。
