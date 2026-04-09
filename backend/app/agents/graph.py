"""
SecuPilot 细佬（Sai Lou）调查编排器 V3

从 V2 Mock 版全面升级：
- 集成 T1/T4/T5 真实算法引擎
- 调查策略引擎（根据线索类型自动选择工具链组合）
- asyncio.gather 并行执行多工具链
- AgenticThreatCase V3 输出（含多工具链结论汇总）
- 熔断/超时保护

架构：
  老贾下达调查指令 → 细佬制定计划 → 并行调用 T1/T4/T5 → 汇总 → 返回案卷
"""

import time
import asyncio
import copy
import ipaddress
from typing import TypedDict, Optional

try:
    import structlog
    logger = structlog.get_logger()
except ImportError:
    import logging
    logger = logging.getLogger("secupilot.graph")

from app.tools.triage_engine import RealTriageEngine
from app.tools.threat_intel import RealThreatIntelEngine
from app.tools.blast_radius import RealBlastRadiusEngine
from app.tools.process_tree_t3 import ProcessTreeCompiler
from app.tools.siem_adapter import (
    AdapterResult,
    SIEMAdapterProtocol,
    TimeRangeSpec,
)
from app.tools.static_data_adapters import (
    StaticDataSourceAdapters,
    build_static_data_source_adapters,
    load_static_data_runtime_payloads_sync,
)
from app.tools.static_data_sources import HostIdentityResolverProtocol
from app.tools.host_identity import build_asset_inventory_host_identity_resolver
from app.agents.jarvis_hunt_engine import JarvisHuntEngine
from app.agents.case_view import build_case_view
from app.config import settings


# ============================================================
# 调查状态
# ============================================================

class InvestigationState(TypedDict):
    """调查管线的共享状态"""
    # 输入
    intent: str
    user_input: str
    target_asset_id: Optional[str]
    target_ip: Optional[str]
    time_range: str

    # 工具链结果
    triage_result: Optional[dict]
    intel_result: Optional[dict]
    blast_result: Optional[dict]

    # 汇总
    threat_case: Optional[dict]
    tools_used: list
    execution_time_ms: float
    error: Optional[str]


# ============================================================
# 调查策略引擎
# ============================================================

SEVERITY_ORDER = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1,
    "INFO": 0,
}

RFC1918_NETWORKS = (
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
)


def _is_public_ip(value: str) -> bool:
    """只按 RFC1918 私网判断，避免把 172.217.* 或 TEST-NET 地址误过滤。"""
    if not value:
        return False
    try:
        addr = ipaddress.ip_address(value)
        return not any(addr in network for network in RFC1918_NETWORKS)
    except ValueError:
        return False


def _is_internal_ip(value: str) -> bool:
    if not value:
        return False
    try:
        addr = ipaddress.ip_address(value)
        return any(addr in network for network in RFC1918_NETWORKS)
    except ValueError:
        return False


def _append_unique(values: list[str], value: Optional[str]) -> None:
    if value and value not in values:
        values.append(value)

def plan_investigation(intent: str, user_input: str,
                       target_asset_id: str = None,
                       target_ip: str = None,
                       initial_alerts: list = None) -> list[str]:
    """
    细佬的调查策略：根据意图和初步线索决定启用哪些工具链。

    不是固定全调，而是按需编排——这才是"专家"的核心。
    """
    tools = []
    u = user_input.lower() if user_input else ""

    # 规则 1：所有调查都先过 T1 Triage
    tools.append("triage")

    # 规则 2：如果涉及外部 IP 或提及 IOC 关键词，必查情报
    has_external_ip = _is_public_ip(target_ip)
    has_intel_keyword = any(kw in u for kw in ["apt", "c2", "情报", "组织", "归因", "ioc", "恶意", "黑客"])

    if has_external_ip or has_intel_keyword or intent == "data_exfil_check":
        tools.append("threat_intel")

    # 规则 3：如果有处置意图或高危场景，必算爆炸半径
    has_action_keyword = any(kw in u for kw in ["隔离", "断开", "封禁", "block", "isolate"])
    if has_action_keyword or intent in ("threat_hunt", "data_exfil_check"):
        tools.append("blast_radius")

    # 规则 4：如果初步告警含高危告警，追加情报查询（从告警中提取 IP）
    if initial_alerts:
        critical_count = sum(1 for a in initial_alerts if a.get("severity") in ("CRITICAL", "HIGH"))
        if critical_count > 0 and "threat_intel" not in tools:
            tools.append("threat_intel")
        if critical_count >= 3 and "blast_radius" not in tools:
            tools.append("blast_radius")

    # 规则 5：态势总结只需要 Triage（轻量快速）
    if intent == "summarize_recent" and len(tools) == 1:
        pass  # 只有 triage，足够了

    # 规则 6：威胁狩猎和资产查询需要 T3 进程树分析
    if intent in ("threat_hunt", "asset_query", "data_exfil_check"):
        tools.append("process_tree")

    return tools


# ============================================================
# 细佬编排器
# ============================================================

class SaiLouOrchestrator:
    """
    细佬：调查编排器

    不亲自做分析，而是：
    1. 制定调查计划（选择工具链）
    2. 并行执行选中的工具链
    3. 汇总结论为 AgenticThreatCase V3
    """

    def __init__(self, siem: SIEMAdapterProtocol,
                 triage: RealTriageEngine,
                 intel: RealThreatIntelEngine,
                 blast: RealBlastRadiusEngine,
                 t3: ProcessTreeCompiler = None,
                 jarvis: JarvisHuntEngine = None,
                 process_events_cache: dict = None,
                 host_identity_resolver: HostIdentityResolverProtocol = None):
        self.siem = siem
        self.triage = triage
        self.intel = intel
        self.blast = blast
        self.t3 = t3 or ProcessTreeCompiler(top_k=3)
        self.jarvis = jarvis or JarvisHuntEngine()
        self._process_events = process_events_cache or {}  # host_id → [events]
        self.host_identity_resolver = host_identity_resolver

    async def investigate(
        self,
        intent: str,
        user_input: str,
        target_asset_id: str = None,
        target_ip: str = None,
        time_range: str = "24h",
        timeout: float = 10.0,
    ) -> dict:
        """
        执行完整调查

        Returns: AgenticThreatCase V3 dict
        """
        start = time.monotonic()
        tools_used = []
        tool_results = {}
        hunt_plan = None
        degraded_reasons: list[str] = []
        time_spec = TimeRangeSpec.from_value(time_range, settings.business_timezone)
        siem_timeout_budget = max(timeout * 0.25, 0.1)
        scenario_meta_timeout_budget = max(timeout * 0.05, 0.05)

        try:
            # ---- Step 1: 收集原始告警 ----
            try:
                siem_alerts = await asyncio.wait_for(
                    self._gather_alerts(
                        intent=intent,
                        user_input=user_input,
                        asset_id=target_asset_id,
                        ip=target_ip,
                        time_range=time_spec,
                    ),
                    timeout=siem_timeout_budget,
                )
            except asyncio.TimeoutError:
                siem_alerts = AdapterResult.timeout([], gap_reason="siem_gather_timeout")
            raw_alerts = siem_alerts.data or []
            tool_results["siem_adapter"] = {
                "status": siem_alerts.status,
                "latency_ms": round(siem_alerts.latency_ms, 2),
                "gap_reason": siem_alerts.gap_reason,
                "result_count": len(raw_alerts),
                "time_range": {
                    "start_utc": time_spec.start_utc.isoformat(),
                    "end_utc": time_spec.end_utc.isoformat(),
                    "tz_label": time_spec.tz_label,
                },
            }
            if siem_alerts.status != "ok":
                _append_unique(degraded_reasons, f"siem_adapter_{siem_alerts.status}")
            if siem_alerts.gap_reason:
                _append_unique(degraded_reasons, f"siem_adapter_{siem_alerts.gap_reason}")
            if siem_alerts.metadata.get("scenario_id"):
                tool_results["_siem_scenario_id"] = siem_alerts.metadata["scenario_id"]

            # ---- Step 2: 制定调查计划 ----
            plan = plan_investigation(
                intent=intent,
                user_input=user_input,
                target_asset_id=target_asset_id,
                target_ip=target_ip,
                initial_alerts=raw_alerts[:20],
            )
            logger.info("Investigation plan", tools=plan, alert_count=len(raw_alerts))

            # ---- Step 2.5: Jarvis 被动巡猎规划 ----
            if "process_tree" in plan:
                try:
                    plan_obj = self.jarvis.create_hunt_plan(
                        trigger_type="user_query",
                        user_input=user_input,
                        intent=intent,
                        target_asset_id=target_asset_id,
                        target_ip=target_ip,
                        context={
                            "initial_alert_count": len(raw_alerts),
                            "planned_tools": list(plan),
                        },
                    )
                    hunt_plan = self.jarvis.plan_to_dict(plan_obj)
                except Exception as exc:
                    logger.error("Jarvis hunt planning failed", error=str(exc))
                    tool_results["_jarvis_error"] = str(exc)

            # ---- Step 3: 并行执行工具链（带超时保护）----
            tasks = {}

            if "triage" in plan:
                tasks["triage"] = self._run_triage(raw_alerts)

            if "threat_intel" in plan:
                # 从告警中提取所有 IP 用于情报查询
                ips_to_check = self._extract_ips(raw_alerts, target_ip)
                tasks["threat_intel"] = self._run_intel(ips_to_check)

            if "blast_radius" in plan:
                tasks["blast_radius"] = self._run_blast(
                    raw_alerts, target_asset_id, target_ip, user_input
                )

            if "process_tree" in plan:
                # 确定 T3 分析目标主机
                t3_selection = await self._determine_t3_hosts(
                    raw_alerts, target_asset_id, target_ip, user_input
                )
                if t3_selection["identity_gaps"]:
                    tool_results["_identity_resolution"] = {
                        "t3_host_selection": copy.deepcopy(t3_selection["identity_gaps"]),
                    }
                    for gap in t3_selection["identity_gaps"]:
                        _append_unique(degraded_reasons, gap.get("reason", "identity_unresolved"))
                tasks["process_tree"] = self._run_t3(
                    t3_selection["host_ids"],
                    identity_gaps=t3_selection["identity_gaps"],
                )

            # asyncio.gather 并行执行
            if tasks:
                task_names = list(tasks.keys())
                task_coros = list(tasks.values())

                try:
                    results = await asyncio.wait_for(
                        asyncio.gather(*task_coros, return_exceptions=True),
                        timeout=timeout * 0.7  # 工具链占 70% 预算
                    )

                    for name, result in zip(task_names, results):
                        if isinstance(result, Exception):
                            logger.error("Tool failed", tool=name, error=str(result))
                            tool_results[name] = {"status": "error", "detail": str(result)}
                            _append_unique(degraded_reasons, f"{name}_failed")
                        else:
                            tool_results[name] = result
                            tools_used.append(name)

                except asyncio.TimeoutError:
                    logger.warning("Tool execution timeout")
                    tool_results["_timeout"] = True
                    _append_unique(degraded_reasons, "tool_timeout")

            # ---- Step 3.25: 拉取场景元数据，避免编排器直接依赖 adapter 内部缓存 ----
            scenario_id = (
                tool_results.get("triage", {}).get("matched_scenario_id")
                or tool_results.get("_siem_scenario_id")
            )
            if scenario_id:
                try:
                    scenario_meta = await asyncio.wait_for(
                        self.siem.get_scenario_metadata(scenario_id),
                        timeout=scenario_meta_timeout_budget,
                    )
                except asyncio.TimeoutError:
                    scenario_meta = AdapterResult.timeout(None, gap_reason="siem_scenario_metadata_timeout")
                tool_results["_scenario_context"] = scenario_meta.data or {}
                tool_results["_scenario_context_status"] = scenario_meta.status
                if scenario_meta.status != "ok":
                    _append_unique(degraded_reasons, f"siem_adapter_{scenario_meta.status}")
                if scenario_meta.gap_reason:
                    _append_unique(degraded_reasons, f"siem_adapter_{scenario_meta.gap_reason}")

            tool_results["_errors"] = degraded_reasons
            tool_results["_planned_tools"] = plan

            # ---- Step 3.5: T3 提取的 IOC 补充送 T4 查询 ----
            t3_result = tool_results.get("process_tree", {})
            if (t3_result.get("status") in ("complete", "partial")
                    and t3_result.get("ioc_extracted")
                    and "threat_intel" in tools_used):
                # 从 T3 IOC 中提取 T4 可查的指标
                t3_indicators = [
                    ioc["value"] for ioc in t3_result.get("ioc_extracted", [])
                    if ioc["type"] in ("ip", "domain", "hash")
                ]
                if t3_indicators:
                    try:
                        t3_intel = await asyncio.wait_for(
                            self._run_intel(t3_indicators),
                            timeout=timeout * 0.2
                        )
                        # 合并到已有情报结果
                        existing_intel = tool_results.get("threat_intel", {})
                        if existing_intel.get("status") == "complete" and t3_intel.get("status") == "complete":
                            existing_intel["matches"].extend(t3_intel.get("matches", []))
                            existing_intel["indicators_checked"] += t3_intel.get("indicators_checked", 0)
                            if t3_intel.get("has_apt_association"):
                                existing_intel["has_apt_association"] = True
                            # 升级 threat_level
                            tl_order = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "CLEAN": 0}
                            if tl_order.get(t3_intel.get("overall_threat_level"), 0) > tl_order.get(existing_intel.get("overall_threat_level"), 0):
                                existing_intel["overall_threat_level"] = t3_intel["overall_threat_level"]
                    except Exception:
                        pass  # T3→T4 补充查询失败不影响主流程

            # ---- Step 4: 汇总为 AgenticThreatCase V3 ----
            elapsed = (time.monotonic() - start) * 1000
            threat_case = self._assemble_case(
                intent=intent,
                user_input=user_input,
                tool_results=tool_results,
                tools_used=tools_used,
                raw_alerts=raw_alerts,
                execution_ms=elapsed,
                hunt_plan=hunt_plan,
            )

            return threat_case

        except Exception as e:
            elapsed = (time.monotonic() - start) * 1000
            logger.error("Investigation failed", error=str(e))
            return {
                "case_id": "ERROR",
                "risk_score": 0.0,
                "confidence_score": 0.0,
                "confidence_label": "LOW",
                "verdict_status": "UNDER_INVESTIGATION",
                "error": str(e),
                "execution_ms": round(elapsed, 1),
            }

    # ============================================================
    # 工具链执行函数
    # ============================================================

    async def _run_triage(self, alerts: list) -> dict:
        """执行 T1 真实评分引擎"""
        t = time.monotonic()
        result = await asyncio.to_thread(self.triage.triage_batch, copy.deepcopy(alerts))
        elapsed = (time.monotonic() - t) * 1000

        # 从高分告警中提取场景信息
        top_alerts = result.for_investigation[:10]
        scenario_id = None
        for alert in top_alerts:
            sid = alert.get("enrichment", {}).get("scenario_id")
            if sid:
                scenario_id = sid
                break

        return {
            "status": "complete",
            "total_scanned": result.total_input,
            "noise_archived": result.auto_archived,
            "compression_ratio": round(result.compression_ratio, 4),
            "for_investigation": len(result.for_investigation),
            "top_risk_score": result.top_risk_score,
            "top_priority": result.top_priority_score,
            "score_distribution": result.score_distribution,
            "top_alerts": [
                {
                    "event_id": a.get("event_id", ""),
                    "activity": a.get("activity_name", ""),
                    "source_ip": a.get("source_ip", ""),
                    "destination": a.get("destination_asset_id", ""),
                    "severity": a.get("severity", ""),
                    "risk_score": a.get("_triage_score", 0),
                    "priority": a.get("_triage_priority", 0),
                    "factors": a.get("_triage_factors", {}),
                }
                for a in top_alerts[:5]
            ],
            "matched_scenario_id": scenario_id,
            "execution_ms": round(elapsed, 2),
        }

    async def _run_intel(self, indicators: list[str]) -> dict:
        """执行 T4 真实情报查询"""
        t = time.monotonic()
        if not indicators:
            return {
                "status": "complete",
                "indicators_checked": 0,
                "matches": [],
                "has_apt_association": False,
                "overall_threat_level": "CLEAN",
                "related_iocs": [],
                "execution_ms": 0.0,
            }

        reports = await asyncio.to_thread(self.intel.lookup_batch, indicators[:10])  # 最多查 10 个
        elapsed = (time.monotonic() - t) * 1000

        all_matches = []
        has_apt = False
        max_threat = "CLEAN"
        threat_order = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "CLEAN": 0}

        for report in reports:
            for match in report.matches:
                all_matches.append({
                    "indicator": match.indicator,
                    "match_type": match.match_type,
                    "ioc_type": match.ioc_type,
                    "threat_type": match.threat_type,
                    "actor": match.actor,
                    "confidence": match.confidence,
                    "match_score": match.match_score,
                    "country": match.country,
                    "mitre": match.mitre_techniques,
                })
                if match.actor in APT_PROFILES:
                    has_apt = True

            if threat_order.get(report.overall_threat_level, 0) > threat_order.get(max_threat, 0):
                max_threat = report.overall_threat_level

        # 收集关联 IOC
        related = []
        for report in reports:
            related.extend(report.related_iocs)

        return {
            "status": "complete",
            "indicators_checked": len(indicators),
            "matches": all_matches,
            "has_apt_association": has_apt,
            "overall_threat_level": max_threat,
            "related_iocs": related[:5],
            "execution_ms": round(elapsed, 2),
        }

    async def _run_blast(self, alerts: list, asset_id: str = None, ip: str = None,
                         user_input: str = None) -> dict:
        """执行 T5 真实爆炸半径计算"""
        t = time.monotonic()

        # 确定隔离目标
        selection = await self._pick_blast_target(alerts, asset_id, ip)
        target = selection.data

        if not target:
            return {
                "status": "no_target",
                "detail": selection.gap_reason or "",
                "identity_gaps": list(selection.metadata.get("identity_gaps", [])),
                "execution_ms": 0,
            }

        action_type = self._infer_action_type(alerts, user_input)
        report = await asyncio.to_thread(self.blast.calculate, action_type, target)
        elapsed = (time.monotonic() - t) * 1000

        if getattr(report, "error", ""):
            return {
                "status": "error",
                "detail": report.error,
                "execution_ms": round(elapsed, 2),
            }

        return {
            "status": "complete",
            "action_type": report.action_type,
            "target": report.target,
            "directly_affected": report.directly_affected,
            "cascade_affected": report.cascade_affected,
            "affected_assets": report.affected_assets,
            "affected_users": report.affected_users_count,
            "affected_services": report.affected_services,
            "estimated_downtime_hours": report.estimated_downtime_hours,
            "estimated_cost_rmb": report.estimated_cost_rmb,
            "recommendation": report.recommendation,
            "alternatives": report.alternatives,
            "execution_ms": round(elapsed, 2),
        }

    async def _run_t3(self, host_ids: list[str], identity_gaps: Optional[list[dict]] = None) -> dict:
        """执行 T3 进程树证据编译器（可分析多台主机）"""
        t = time.monotonic()
        identity_gaps = copy.deepcopy(identity_gaps or [])

        if not host_ids:
            return {
                "status": "degraded",
                "detail": "No matching hosts with process event telemetry",
                "hosts_analyzed": [],
                "missing_hosts": [],
                "total_chains": 0,
                "suspicious_chains": [],
                "persistence_mechanisms": [],
                "ioc_extracted": [],
                "gaps": identity_gaps,
                "analysis_scope": [],
                "execution_ms": 0.0,
            }

        all_chains = []
        all_persistence = []
        all_iocs = []
        all_gaps = list(identity_gaps)
        all_scopes = set()
        hosts_analyzed = []
        missing_hosts = []
        worst_status = "COMPLETE"
        status_priority = {"FAILED": 4, "DEGRADED": 3, "PARTIAL": 2, "COMPLETE": 1}

        for host_id in host_ids:
            events = self._process_events.get(host_id, [])
            if not events:
                # 尝试大小写变体
                events = self._process_events.get(host_id.upper(), [])
            if not events:
                all_gaps.append({
                    "gap_id": f"{host_id}:gap-no-data",
                    "type": "no_process_events",
                    "impact": f"No process event data available for {host_id}",
                })
                missing_hosts.append(host_id)
                continue

            result = await asyncio.to_thread(self.t3.analyze, host_id, events)
            hosts_analyzed.append(host_id)
            all_scopes.update(result.analysis_scope)

            all_chains.extend(result.suspicious_chains)
            all_persistence.extend(result.persistence_mechanisms)
            all_iocs.extend(result.ioc_extracted)
            all_gaps.extend(result.gaps)

            if status_priority.get(result.analysis_status, 0) > status_priority.get(worst_status, 0):
                worst_status = result.analysis_status

        # 排序链条：按 anomaly_score 降序
        all_chains.sort(key=lambda c: c.get("anomaly_score", 0), reverse=True)

        final_status = worst_status.lower()
        detail = ""
        if missing_hosts and not hosts_analyzed:
            final_status = "degraded"
            detail = "No requested hosts had process event telemetry"
        elif missing_hosts and final_status == "complete":
            final_status = "partial"
            detail = "Some requested hosts had no process event telemetry"

        elapsed = (time.monotonic() - t) * 1000

        return {
            "status": final_status,
            "detail": detail,
            "hosts_analyzed": hosts_analyzed,
            "missing_hosts": missing_hosts,
            "total_chains": len(all_chains),
            "suspicious_chains": all_chains[:3],  # Top-3
            "persistence_mechanisms": all_persistence,
            "ioc_extracted": all_iocs,
            "gaps": all_gaps,
            "analysis_scope": sorted(all_scopes),
            "execution_ms": round(elapsed, 2),
        }

    async def _resolve_host_identity(
        self,
        *,
        asset_id: str = None,
        ip: str = None,
        hostname: str = None,
        identifier: str = None,
    ) -> AdapterResult:
        if not self.host_identity_resolver:
            chosen = str(asset_id or ip or hostname or identifier or "").strip()
            return AdapterResult.ok(
                None,
                metadata={"matched_by": "none", "identifier": chosen, "candidate_asset_ids": []},
            )

        if asset_id:
            return await self.host_identity_resolver.resolve_asset_id(asset_id)
        if ip:
            return await self.host_identity_resolver.resolve_ip(ip)
        if hostname:
            return await self.host_identity_resolver.resolve_hostname(hostname)
        if identifier:
            return await self.host_identity_resolver.resolve_any(identifier)
        return AdapterResult.ok(None, metadata={"matched_by": "none", "identifier": "", "candidate_asset_ids": []})

    @staticmethod
    def _identity_gap(
        *,
        query_kind: str,
        query_value: str,
        result: AdapterResult,
        explicit: bool = False,
    ) -> Optional[dict]:
        reason = result.gap_reason
        if not reason and explicit and result.status == "ok" and result.data is None:
            reason = f"identity_not_found:{query_kind}:{query_value}"
        if not reason:
            return None

        gap_type = "identity_ambiguous" if reason.startswith("identity_ambiguous:") else "identity_unresolved"
        candidate_ids = list(result.metadata.get("candidate_asset_ids", []))
        matched_by = result.metadata.get("matched_by", query_kind)
        impact = (
            f"Unable to resolve {query_kind} '{query_value}' to one canonical asset id."
            if gap_type == "identity_ambiguous"
            else f"No canonical asset identity found for {query_kind} '{query_value}'."
        )
        return {
            "gap_id": f"identity:{query_kind}:{query_value}".replace(" ", "_"),
            "type": gap_type,
            "impact": impact,
            "reason": reason,
            "matched_by": matched_by,
            "candidate_asset_ids": candidate_ids,
        }

    @staticmethod
    def _append_identity_gap(gaps: list[dict], gap: Optional[dict]) -> None:
        if not gap:
            return
        gap_id = gap.get("gap_id")
        if any(existing.get("gap_id") == gap_id for existing in gaps):
            return
        gaps.append(gap)

    async def _determine_t3_hosts(
        self,
        alerts: list,
        asset_id: str = None,
        ip: str = None,
        user_input: str = None,
    ) -> dict:
        """确定 T3 应分析哪些主机，并显式记录身份解析歧义。"""
        hosts: set[str] = set()
        identity_gaps: list[dict] = []

        async def _maybe_add_identity(*, query_kind: str, query_value: str, explicit: bool = False) -> None:
            result = await self._resolve_host_identity(
                asset_id=query_value if query_kind == "asset_id" else None,
                ip=query_value if query_kind == "ip_address" else None,
                identifier=query_value if query_kind == "identifier" else None,
            )
            if result.data is not None:
                hosts.add(result.data.canonical_asset_id)
                return
            self._append_identity_gap(
                identity_gaps,
                self._identity_gap(
                    query_kind=query_kind,
                    query_value=query_value,
                    result=result,
                    explicit=explicit,
                ),
            )

        # 1. 显式目标
        if asset_id:
            await _maybe_add_identity(query_kind="asset_id", query_value=asset_id, explicit=True)
        if ip:
            await _maybe_add_identity(query_kind="ip_address", query_value=ip, explicit=True)

        # 2. 从高危告警中提取涉及的主机
        ranked = sorted(alerts, key=lambda a: a.get("_triage_score", 0), reverse=True)
        for alert in ranked[:10]:
            dest = str(alert.get("destination_asset_id", "") or "").strip()
            if dest and dest != "EXTERNAL":
                await _maybe_add_identity(query_kind="asset_id", query_value=dest)

            src_ip = str(alert.get("source_ip", "") or "").strip()
            if _is_internal_ip(src_ip):
                await _maybe_add_identity(query_kind="ip_address", query_value=src_ip)

        # 3. 从 user_input 关键词推断（场景→主机映射），但仍走 canonical resolver
        query = (user_input or "").lower()
        scenario_host_map = {
            "横向": ["DEV-WS-01", "WKST-047"],
            "lateral": ["DEV-WS-01", "WKST-047"],
            "勒索": ["HR-PORTAL-01"],
            "ransom": ["HR-PORTAL-01"],
            "c2": ["HR-PORTAL-01"],
        }
        for kw, host_list in scenario_host_map.items():
            if kw in query:
                for host_like in host_list:
                    await _maybe_add_identity(query_kind="identifier", query_value=host_like)

        # 过滤：只保留有进程事件数据的主机
        available = {str(host).upper() for host in self._process_events.keys()}
        valid = [host for host in hosts if host.upper() in available]

        return {
            "host_ids": valid[:5],
            "identity_gaps": identity_gaps,
        }

    # ============================================================
    # 辅助函数
    # ============================================================

    async def _gather_alerts(
        self,
        intent: str,
        user_input: str = "",
        asset_id: str = None,
        ip: str = None,
        time_range: Optional[TimeRangeSpec] = None,
    ) -> AdapterResult[list]:
        """从 SIEM 收集原始告警，始终通过 adapter contract 访问。"""
        spec = time_range or TimeRangeSpec.from_value("24h", settings.business_timezone)
        identity_metadata = {}
        if intent == "asset_query" and (asset_id or ip):
            identity_result = await self._resolve_host_identity(asset_id=asset_id, ip=ip)
            if identity_result.status != "ok" and identity_result.gap_reason:
                return AdapterResult(
                    status=identity_result.status,
                    data=[],
                    latency_ms=identity_result.latency_ms,
                    gap_reason=identity_result.gap_reason,
                    metadata=dict(identity_result.metadata or {}),
                )

            target = asset_id or ip
            if identity_result.data is not None:
                target = identity_result.data.canonical_asset_id
                identity_metadata = {
                    "identity_resolution": "resolved",
                    "identity_canonical_asset_id": target,
                    "identity_matched_by": identity_result.metadata.get("matched_by"),
                }
            else:
                identity_metadata = {
                    "identity_resolution": "no_match",
                    "identity_query": asset_id or ip,
                }
            result = await self.siem.query_asset_alerts(target, spec)
        else:
            result = await self.siem.query_intent_alerts(intent, user_input, spec)

        merged_metadata = dict(result.metadata or {})
        merged_metadata.update(identity_metadata)
        return AdapterResult(
            status=result.status,
            data=copy.deepcopy(result.data or []),
            latency_ms=result.latency_ms,
            gap_reason=result.gap_reason,
            metadata=merged_metadata,
        )

    @staticmethod
    def _extract_ips(alerts: list, extra_ip: str = None) -> list[str]:
        """从告警中提取需要查询情报的 IP 列表"""
        indicators = []
        seen = set()

        def add_indicator(value: str):
            if not value:
                return
            if value in seen:
                return
            seen.add(value)
            indicators.append(value)

        if extra_ip:
            add_indicator(extra_ip)

        for alert in alerts:
            src = alert.get("source_ip", "")
            if _is_public_ip(src):
                add_indicator(src)

            extra = alert.get("extra", {})
            dest_ip = extra.get("dest_ip", "")
            if _is_public_ip(dest_ip):
                add_indicator(dest_ip)

            domain = extra.get("query_domain", "")
            if domain:
                add_indicator(domain)

        return indicators[:10]

    async def _pick_blast_target(
        self,
        alerts: list,
        explicit_asset_id: str = None,
        explicit_ip: str = None,
    ) -> AdapterResult[Optional[str]]:
        """优先选择可解析到 canonical asset id 的内部资产，避免静默猜测。"""
        identity_gaps: list[dict] = []

        async def _resolve_target(*, query_kind: str, query_value: str, explicit: bool = False) -> Optional[str]:
            result = await self._resolve_host_identity(
                asset_id=query_value if query_kind == "asset_id" else None,
                ip=query_value if query_kind == "ip_address" else None,
            )
            if result.data is not None:
                candidate = result.data.canonical_asset_id
                if candidate in getattr(self.blast, "asset_index", {}):
                    return candidate
            self._append_identity_gap(
                identity_gaps,
                self._identity_gap(
                    query_kind=query_kind,
                    query_value=query_value,
                    result=result,
                    explicit=explicit,
                ),
            )
            return None

        if explicit_asset_id:
            target = await _resolve_target(query_kind="asset_id", query_value=explicit_asset_id, explicit=True)
            if target:
                return AdapterResult.ok(target, metadata={"identity_gaps": identity_gaps})

        if explicit_ip:
            target = await _resolve_target(query_kind="ip_address", query_value=explicit_ip, explicit=True)
            if target:
                return AdapterResult.ok(target, metadata={"identity_gaps": identity_gaps})

        ranked_alerts = sorted(
            alerts,
            key=lambda a: (
                SEVERITY_ORDER.get(a.get("severity", "INFO"), 0),
                int(a.get("count", 1) or 1),
            ),
            reverse=True,
        )

        for alert in ranked_alerts:
            dest_asset = str(alert.get("destination_asset_id", "") or "").strip()
            if dest_asset and dest_asset != "EXTERNAL":
                target = await _resolve_target(query_kind="asset_id", query_value=dest_asset)
                if target:
                    return AdapterResult.ok(target, metadata={"identity_gaps": identity_gaps})

            for candidate in (alert.get("source_ip", ""), alert.get("destination_ip", "")):
                candidate = str(candidate or "").strip()
                if _is_internal_ip(candidate):
                    target = await _resolve_target(query_kind="ip_address", query_value=candidate)
                    if target:
                        return AdapterResult.ok(target, metadata={"identity_gaps": identity_gaps})

        if identity_gaps:
            return AdapterResult.partial(
                None,
                gap_reason=identity_gaps[0].get("reason", "identity_unresolved"),
                metadata={"identity_gaps": identity_gaps},
            )
        return AdapterResult.ok(None, metadata={"identity_gaps": []})

    @staticmethod
    def _infer_action_type(alerts: list, user_input: str = "") -> str:
        text = (user_input or "").lower()
        max_severity = max((SEVERITY_ORDER.get(a.get("severity", "INFO"), 0) for a in alerts), default=0)
        max_count = max((int(a.get("count", 1) or 1) for a in alerts), default=0)

        if any(kw in text for kw in ["紧急", "emergency", "立即"]) or max_severity >= 4 or max_count >= 1000:
            return "EMERGENCY_ISOLATE"
        if any(kw in text for kw in ["隔离", "block", "isolate", "封禁"]) or max_severity >= 3 or max_count >= 20:
            return "NETWORK_ISOLATE"
        return "ALERT_AND_CONFIRM"

    def _assemble_case(self, intent: str, user_input: str,
                       tool_results: dict, tools_used: list,
                       raw_alerts: list, execution_ms: float,
                       hunt_plan: dict = None) -> dict:
        """汇总所有工具链结论为 AgenticThreatCase V3.1"""

        triage = tool_results.get("triage", {})
        intel = tool_results.get("threat_intel", {})
        blast = tool_results.get("blast_radius", {})
        t3 = tool_results.get("process_tree", {})
        degraded_reasons = list(tool_results.get("_errors", []))
        planned_tools = tool_results.get("_planned_tools", [])
        has_timeout = bool(tool_results.get("_timeout"))
        jarvis_error = tool_results.get("_jarvis_error")

        # ---- S2-D: 三层状态模型 ----
        # 检测工具级 DEGRADED/FAILED
        for tool_name in planned_tools:
            tr = tool_results.get(tool_name, {})
            status = tr.get("status", "")
            if status in ("error", "failed", "degraded"):
                _append_unique(degraded_reasons, f"{tool_name}_{status}")
            elif status == "no_target":
                _append_unique(degraded_reasons, f"{tool_name}_no_target")
                detail = tr.get("detail", "")
                if detail.startswith("identity_"):
                    _append_unique(degraded_reasons, detail)

        # blast 在计划中但没完成 → 处置建议不可靠
        blast_planned = "blast_radius" in planned_tools
        blast_complete = blast.get("status") == "complete"

        is_degraded = has_timeout or bool(degraded_reasons)

        # ---- 风险分数：综合多源 ----
        risk_score = 0.0

        # 来自 Triage
        triage_risk = triage.get("top_risk_score", 0)
        risk_score = max(risk_score, triage_risk)

        # 来自 T3
        if t3.get("suspicious_chains"):
            top_chain_score = t3["suspicious_chains"][0].get("anomaly_score", 0)
            risk_score = max(risk_score, top_chain_score)

        # 来自情报
        if intel.get("has_apt_association"):
            risk_score = min(10.0, risk_score * 1.3)
        if intel.get("overall_threat_level") == "CRITICAL":
            risk_score = max(risk_score, 8.5)

        # ---- 置信度（冻结协议：DEGRADED → ≤ MEDIUM）----
        confidence_factors = []
        if triage.get("status") == "complete":
            confidence_factors.append(0.7)
        if intel.get("status") == "complete" and intel.get("matches"):
            confidence_factors.append(0.9 if intel.get("has_apt_association") else 0.7)
        if blast_complete:
            confidence_factors.append(0.8)
        if t3.get("status") in ("complete", "partial") and t3.get("suspicious_chains"):
            confidence_factors.append(0.85)

        confidence = max(confidence_factors) if confidence_factors else 0.5
        if is_degraded:
            confidence = min(confidence, 0.45)  # 冻结协议：DEGRADED → ≤ MEDIUM

        if confidence >= 0.85:
            conf_label = "HIGH"
        elif confidence >= 0.50:
            conf_label = "MEDIUM"
        else:
            conf_label = "LOW"

        # ---- 判定状态（verdict_status）----
        if is_degraded:
            verdict = "DEGRADED"
        elif risk_score >= 8.5:
            verdict = "CRITICAL_ACTION_REQUIRED"
        elif risk_score >= 6.0:
            verdict = "HIGH_RISK"
        elif risk_score >= 3.0:
            verdict = "MEDIUM_RISK"
        else:
            verdict = "LOW_RISK"

        # ---- investigation_status（案卷级三层状态）----
        tool_statuses = []
        for tn in planned_tools:
            s = tool_results.get(tn, {}).get("status", "failed")
            tool_statuses.append(s)

        if is_degraded:
            investigation_status = "DEGRADED"
        elif all(s == "complete" for s in tool_statuses):
            investigation_status = "COMPLETE"
        else:
            investigation_status = "PARTIAL"

        # ---- 场景信息 ----
        scenario_id = triage.get("matched_scenario_id") or tool_results.get("_siem_scenario_id")
        scenario_context = tool_results.get("_scenario_context", {}) or {}
        scenario_data = {}
        if scenario_id:
            scenario_data = {
                "scenario_id": scenario_id,
                "scenario_name": scenario_context.get("name", ""),
                "kill_chain": scenario_context.get("kill_chain", ""),
                "narrative_arc": scenario_context.get("narrative_arc", {}),
            }

        # ---- 行动建议（冻结协议：DEGRADED 且 blast 未完成 → null）----
        suggested_action = None
        if not is_degraded and blast_complete:
            scene_action = {}
            if scenario_id:
                scene_action = scenario_context.get("action", {})
            suggested_action = {
                **scene_action,
                "blast_radius_assessment": {
                    "directly_affected": blast.get("directly_affected", 0),
                    "cascade_affected": blast.get("cascade_affected", 0),
                    "affected_users": blast.get("affected_users", 0),
                    "estimated_cost_rmb": blast.get("estimated_cost_rmb", 0),
                    "recommendation": blast.get("recommendation", ""),
                    "alternatives": blast.get("alternatives", []),
                },
                "blast_radius_desc": (
                    f"直接影响 {blast.get('directly_affected',0)} 个资产，"
                    f"级联影响 {blast.get('cascade_affected',0)} 个，"
                    f"影响 {blast.get('affected_users',0)} 名用户。"
                    f"预估停机 {blast.get('estimated_downtime_hours',0)}h，"
                    f"经济损失约 ¥{blast.get('estimated_cost_rmb',0):,}。"
                    f"建议：{blast.get('recommendation','')}"
                ),
            }
        elif not is_degraded and not blast_planned:
            # blast 不在计划中（如 summarize_recent），允许场景默认动作
            if scenario_id:
                scene_action = scenario_context.get("action", {})
                if scene_action:
                    suggested_action = scene_action
        # else: DEGRADED → suggested_action stays None（冻结协议）

        # ---- T3 forensic_result（单数，冻结协议）----
        forensic_result = None
        if t3.get("hosts_analyzed"):
            forensic_result = {
                "hosts_analyzed": t3.get("hosts_analyzed", []),
                "total_suspicious_chains": t3.get("total_chains", 0),
                "top_chains": t3.get("suspicious_chains", [])[:3],
                "attack_stages_observed": list(set(
                    stage
                    for chain in t3.get("suspicious_chains", [])
                    for stage in chain.get("attack_stages", [])
                )),
                "persistence_mechanisms": t3.get("persistence_mechanisms", []),
                "evidence_gaps": t3.get("gaps", []),
                "ioc_extracted_by_t3": t3.get("ioc_extracted", []),
                "analysis_scope": t3.get("analysis_scope", []),
            }

        # ---- 组装 V3.1 案卷 ----
        case_id = f"CASE-{int(time.time())}-{abs(hash(user_input)) % 999:03d}"

        case_payload = {
            "case_id": case_id,
            "version": "3.1",
            "risk_score": round(risk_score, 2),
            "confidence_score": round(confidence, 2),
            "confidence_label": conf_label,
            "verdict_status": verdict,
            "investigation_status": investigation_status,

            # 场景信息
            **scenario_data,

            # T3 证据（冻结协议：forensic_result 单数）
            "forensic_result": forensic_result,

            # Jarvis 被动巡猎规划
            "hunt_plan": hunt_plan,

            # 多工具链结论
            "tool_results": {
                "triage": {k: v for k, v in triage.items() if k != "top_alerts"} if triage else None,
                "threat_intel": intel if intel else None,
                "blast_radius": blast if blast else None,
                "process_tree": {k: v for k, v in t3.items()
                                 if k not in ("suspicious_chains", "ioc_extracted", "persistence_mechanisms")} if t3 else None,
            },
            "triage_summary": {
                "total_events_scanned": triage.get("total_scanned", len(raw_alerts)),
                "noise_archived": triage.get("noise_archived", 0),
                "compression_ratio": triage.get("compression_ratio", 0),
                "top_alerts": triage.get("top_alerts", []),
            },

            # 情报汇总
            "intel_summary": {
                "matches": intel.get("matches", []),
                "has_apt": intel.get("has_apt_association", False),
                "threat_level": intel.get("overall_threat_level", "CLEAN"),
                "related_iocs": intel.get("related_iocs", []),
            } if intel else None,

            # 行动建议
            "suggested_action": suggested_action,

            # 审计链
            "audit_trail": {
                "tools_invoked": tools_used,
                "tools_planned": planned_tools,
                "total_execution_ms": round(execution_ms, 1),
                "llm_calls": 0,
                "degraded": is_degraded,
                "degraded_reasons": degraded_reasons,
                "planner": "jarvis" if hunt_plan else None,
                "hunt_plan_id": hunt_plan.get("hunt_id") if hunt_plan else None,
                "jarvis_error": jarvis_error,
            },
        }
        case_payload["case_view"] = build_case_view(case_payload)
        return case_payload


# ============================================================
# 向后兼容接口（供 skill_registry.py 调用）
# ============================================================

# 导入 APT_PROFILES 供 intel 引用
from app.tools.threat_intel import APT_PROFILES

class InvestigationPipeline:
    """
    向后兼容封装器
    保持 skill_registry.py 的调用接口不变
    """

    def __init__(
        self,
        siem: SIEMAdapterProtocol,
        runtime_settings=None,
        static_data_adapters: Optional[StaticDataSourceAdapters] = None,
    ):
        import json

        runtime_settings = runtime_settings or settings
        static_root = runtime_settings.get_static_data_dir()
        adapters = static_data_adapters or build_static_data_source_adapters(runtime_settings)
        static_payloads = load_static_data_runtime_payloads_sync(adapters)

        asset_data = static_payloads.asset_inventory_payload
        baseline_data = static_payloads.baseline_payload
        ioc_data = static_payloads.threat_intel_seed_payload
        topology_data = static_payloads.topology_payload
        host_identity_resolver = build_asset_inventory_host_identity_resolver(
            static_payloads.asset_inventory_snapshot
        )

        # 确保拓扑包含完整资产数据
        if isinstance(topology_data.get("nodes", {}).get("assets"), int):
            topology_data["nodes"]["assets"] = asset_data.get("assets", [])

        # 加载进程事件数据（F-02 路径对齐）
        process_events_cache = {}
        pe_dir = static_root / "process_events"
        if pe_dir.exists():
            for pe_file in pe_dir.glob("process_events_*.json"):
                with open(pe_file) as f:
                    pe_data = json.load(f)
                host_id = pe_data.get("host_id", "")
                if host_id:
                    process_events_cache[host_id] = pe_data.get("events", [])
            logger.info("Process events loaded", hosts=list(process_events_cache.keys()),
                        total_events=sum(len(v) for v in process_events_cache.values()))

        # 初始化真实引擎
        triage = RealTriageEngine(
            asset_db=asset_data,
            baseline_db=baseline_data,
            business_timezone=runtime_settings.business_timezone,
        )
        intel = RealThreatIntelEngine(ioc_data)
        blast = RealBlastRadiusEngine(topology_data)
        t3 = ProcessTreeCompiler(top_k=3)
        jarvis = JarvisHuntEngine()

        self.orchestrator = SaiLouOrchestrator(
            siem=siem,
            triage=triage,
            intel=intel,
            blast=blast,
            t3=t3,
            jarvis=jarvis,
            process_events_cache=process_events_cache,
            host_identity_resolver=host_identity_resolver,
        )

        logger.info(
            "InvestigationPipeline V3.2 initialized",
            ioc_stats=intel.get_stats(),
            topology_nodes=blast.G.number_of_nodes(),
            process_event_hosts=len(process_events_cache),
            host_identity_records=static_payloads.asset_inventory_snapshot.metadata.record_count,
            static_data_modes={
                "asset_inventory": static_payloads.asset_inventory_snapshot.metadata.source_mode,
                "baseline": static_payloads.baseline_snapshot.metadata.source_mode,
                "intel_seed": static_payloads.threat_intel_seed_snapshot.metadata.source_mode,
                "topology": static_payloads.topology_snapshot.metadata.source_mode,
            },
        )

    async def investigate(self, intent: str, user_input: str,
                          target_asset_id: str = None,
                          target_ip: str = None,
                          time_range: str = "24h",
                          timeout: float = None) -> dict:
        """向后兼容接口"""
        from app.config import settings
        if timeout is None:
            timeout = settings.llm_timeout_seconds

        return await self.orchestrator.investigate(
            intent=intent,
            user_input=user_input,
            target_asset_id=target_asset_id,
            target_ip=target_ip,
            time_range=time_range,
            timeout=timeout,
        )
