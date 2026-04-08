from __future__ import annotations

from typing import Any, Optional


def _safe_list(value: Any) -> list:
    return value if isinstance(value, list) else []


def _primary_chain(forensic_result: Optional[dict]) -> Optional[dict]:
    forensic = forensic_result or {}
    chains = _safe_list(forensic.get("top_chains"))
    if not chains:
        return None

    chain = chains[0]
    path = _safe_list(chain.get("path"))
    process_path = [node.get("process_name", "") for node in path if node.get("process_name")]

    highlight_node = None
    highlight_reason = None
    best_risk = -1
    for node in path:
        anomalies = _safe_list(node.get("anomalies"))
        if not anomalies:
            continue
        top_anomaly = max(anomalies, key=lambda item: item.get("risk", 0))
        risk = top_anomaly.get("risk", 0)
        if risk >= best_risk:
            best_risk = risk
            highlight_node = node.get("node_id")
            process_name = node.get("process_name", "")
            anomaly_type = top_anomaly.get("type", "")
            mitre = top_anomaly.get("mitre", "")
            if anomaly_type == "known_attack_tool" and process_name:
                highlight_reason = f"已知攻击工具 {process_name} ({mitre})" if mitre else f"已知攻击工具 {process_name}"
            else:
                desc = top_anomaly.get("desc", "")
                highlight_reason = f"{desc} ({mitre})" if desc and mitre else (desc or mitre or None)

    if not highlight_node and path:
        highlight_node = path[-1].get("node_id")

    return {
        "chain_id": chain.get("chain_id"),
        "anomaly_score": chain.get("anomaly_score"),
        "process_path": process_path,
        "highlight_node_id": highlight_node,
        "highlight_reason": highlight_reason,
    }


def generate_one_liner(case: dict) -> str:
    forensic = case.get("forensic_result") or {}
    stages = _safe_list(forensic.get("attack_stages_observed"))
    hosts = _safe_list(forensic.get("hosts_analyzed"))
    chains = _safe_list(forensic.get("top_chains"))
    scenario = case.get("scenario_name", "")
    verdict = case.get("verdict_status", "")
    confidence = case.get("confidence_label", "")

    if not chains:
        if verdict == "DEGRADED":
            line = "调查数据不完整，无法给出确定性结论。"
        else:
            line = f"已分析 {len(hosts)} 台主机，未发现高危攻击链。"
        if confidence == "LOW":
            line += "（置信度低，需人工确认）"
        return line

    top = chains[0]
    process_names = [
        node.get("process_name", "")
        for node in _safe_list(top.get("path"))
        if node.get("process_name")
    ]
    chain_str = " → ".join(process_names[-3:] if len(process_names) > 3 else process_names)
    stage_str = " → ".join(stages) if stages else "未知阶段"
    line = f"{scenario or '安全事件'}：检测到 {chain_str} 攻击链，阶段覆盖 {stage_str}。"
    if confidence == "LOW":
        line += "（置信度低，需人工确认）"
    return line


def _ioc_hits(intel_summary: Optional[dict]) -> list[dict]:
    summary = intel_summary or {}
    hits = []
    for match in _safe_list(summary.get("matches")):
        if match.get("match_type") != "exact":
            continue
        hits.append(
            {
                "type": match.get("ioc_type"),
                "value": match.get("indicator"),
                "actor": match.get("actor"),
                "match_type": match.get("match_type"),
            }
        )
    return hits


def _persistence_summary(forensic_result: Optional[dict]) -> tuple[int, Optional[str]]:
    mechanisms = _safe_list((forensic_result or {}).get("persistence_mechanisms"))
    count = len(mechanisms)
    if not mechanisms:
        return 0, None

    first = mechanisms[0]
    kind = first.get("type", "")
    if kind == "service_registration":
        key_path = first.get("key_path") or first.get("value_name") or ""
        summary = "检测到服务注册持久化"
        if key_path:
            summary = f"检测到服务注册持久化（{key_path}）"
        return count, summary
    if kind == "registry_run_key":
        value_name = first.get("value_name") or first.get("key_path") or ""
        summary = "检测到 Run 键持久化"
        if value_name:
            summary = f"检测到 Run 键持久化（{value_name}）"
        return count, summary
    return count, f"检测到 {kind or '持久化'} 机制"


def _business_risk(case: dict) -> str:
    risk = float(case.get("risk_score", 0) or 0)
    intel_threat = (case.get("intel_summary") or {}).get("threat_level") or (case.get("intel_summary") or {}).get("overall_threat_level")
    if risk >= 6 or intel_threat in {"CRITICAL", "HIGH"}:
        return "HIGH"
    if risk >= 3 or intel_threat == "MEDIUM":
        return "MEDIUM"
    return "LOW"


def _jarvis_next_suggested(case: dict) -> Optional[str]:
    if case.get("investigation_status") == "DEGRADED":
        return "补齐缺失遥测后重新运行调查"
    if case.get("suggested_action"):
        return "复核影响面后提交人工审批"
    forensic = case.get("forensic_result") or {}
    if _safe_list(forensic.get("top_chains")):
        return "围绕首条可疑链继续人工复核关键证据"
    return "继续监控并等待新的可疑线索"


def _jarvis_scope(hunt_plan: dict, steps: list[dict]) -> dict:
    scope = hunt_plan.get("scope")
    if isinstance(scope, dict) and scope:
        return scope

    targets = []
    tools = []
    focus = []
    for step in steps:
        tool = step.get("tool")
        target = step.get("target")
        step_focus = step.get("focus")
        if tool and tool not in tools:
            tools.append(tool)
        if target and target not in targets and not str(target).startswith("from_"):
            targets.append(target)
        if step_focus and step_focus not in focus:
            focus.append(step_focus)

    return {
        "trigger_type": hunt_plan.get("trigger_type"),
        "targets": targets,
        "tools": tools,
        "focus": focus,
    }


def _jarvis_stop_conditions(hunt_plan: dict, steps: list[dict]) -> list[str]:
    stop_conditions = _safe_list(hunt_plan.get("stop_conditions"))
    if stop_conditions:
        return stop_conditions

    tools = {step.get("tool") for step in steps if step.get("tool")}
    generated = [
        "完成计划步骤并形成结构化调查结论",
        "若关键遥测缺失，则以降级结果结束并停止不安全处置建议",
    ]
    if "T5" in tools:
        generated.append("若影响评估不可接受，则停止直接处置并转人工审批")
    return generated


def _jarvis_plan(hunt_plan: Optional[dict], case: dict) -> Optional[dict]:
    if not hunt_plan:
        return None
    steps = _safe_list(hunt_plan.get("planned_steps"))
    next_steps = [
        {
            "seq": step.get("seq"),
            "tool": step.get("tool"),
            "action": step.get("action"),
            "purpose": step.get("purpose"),
            "target": step.get("target"),
            "focus": step.get("focus"),
        }
        for step in steps[:3]
    ]
    return {
        "hypothesis": hunt_plan.get("hypothesis"),
        "status": "executed",
        "steps_total": len(steps),
        "steps_completed": len(steps),
        "steps_degraded": 0,
        "next_steps": next_steps,
        "scope": _jarvis_scope(hunt_plan, steps),
        "stop_conditions": _jarvis_stop_conditions(hunt_plan, steps),
        "next_suggested": _jarvis_next_suggested(case),
        "source": "hunt_plan",
    }


def _normalize_targets(suggested_action: Optional[dict]) -> list[str]:
    action = suggested_action or {}
    targets = _safe_list(action.get("targets"))
    if targets:
        return targets

    target = action.get("target")
    if target:
        return [target]
    return []


def _recommended_action(case: dict) -> dict:
    suggested_action = case.get("suggested_action")
    investigation_status = case.get("investigation_status")
    disabled_reason = None

    available = suggested_action is not None
    if investigation_status == "DEGRADED":
        available = False
        disabled_reason = "调查降级，处置建议不可用"

    action = suggested_action or {}
    return {
        "available": available,
        "action_type": action.get("type"),
        "targets": _normalize_targets(suggested_action),
        "blast_summary": action.get("blast_radius_desc"),
        "approval_required": bool(suggested_action),
        "disabled_reason": disabled_reason,
        "source": "suggested_action",
    }


def _analysis_limits(case: dict, recommended_action: dict) -> dict:
    audit = case.get("audit_trail") or {}
    forensic = case.get("forensic_result") or {}
    degraded_reasons = _safe_list(audit.get("degraded_reasons"))

    unavailable_tools = []
    for reason in degraded_reasons:
        if not isinstance(reason, str):
            continue
        if reason.endswith("_failed"):
            unavailable_tools.append(reason.removesuffix("_failed"))
        elif reason == "tool_timeout":
            unavailable_tools.append("timeout")

    return {
        "degraded": bool(audit.get("degraded")),
        "degraded_reasons": degraded_reasons,
        "missing_telemetry": _safe_list(forensic.get("evidence_gaps")),
        "unavailable_tools": unavailable_tools,
        "unresolved_pivots": [],
        "action_disabled_reason": recommended_action.get("disabled_reason"),
    }


def build_case_view(case: dict) -> dict:
    forensic = case.get("forensic_result") or {}
    intel = case.get("intel_summary") or {}
    primary_chain = _primary_chain(forensic)
    persistence_count, persistence_summary = _persistence_summary(forensic)
    recommended_action = _recommended_action(case)
    analysis_limits = _analysis_limits(case, recommended_action)

    return {
        "executive_summary": {
            "verdict": case.get("verdict_status"),
            "investigation_status": case.get("investigation_status"),
            "risk_score": case.get("risk_score"),
            "confidence_label": case.get("confidence_label"),
            "one_liner": generate_one_liner(case),
        },
        "what_happened": {
            "scenario_name": case.get("scenario_name"),
            "attack_stages": _safe_list(forensic.get("attack_stages_observed")),
            "affected_hosts": _safe_list(forensic.get("hosts_analyzed")),
            "primary_chain": primary_chain,
            "source": "forensic_result",
        },
        "why_it_matters": {
            "ioc_hits": _ioc_hits(intel),
            "persistence_count": persistence_count,
            "persistence_summary": persistence_summary,
            "blast_impact_summary": (case.get("suggested_action") or {}).get("blast_radius_desc"),
            "business_risk": _business_risk(case),
            "source": "intel_summary + forensic_result + tool_results.blast_radius",
        },
        "jarvis_plan": _jarvis_plan(case.get("hunt_plan"), case),
        "recommended_action": recommended_action,
        "evidence_panels": {
            "top_chains": {"ref": "forensic_result.top_chains", "count": len(_safe_list(forensic.get("top_chains")))},
            "ioc_table": {"ref": "intel_summary.matches", "count": None},
            "persistence": {"ref": "forensic_result.persistence_mechanisms", "count": None},
            "evidence_gaps": {"ref": "forensic_result.evidence_gaps", "count": None},
        },
        "analysis_limits": analysis_limits,
    }
