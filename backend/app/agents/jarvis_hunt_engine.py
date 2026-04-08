"""
SecuPilot 贾维斯巡猎引擎 (JARVIS Hunt Engine) — Sprint 2 被动模式

Sprint 2 范围（冻结协议）：
  ✅ 被动 hunt_plan 生成（接收意图 → 输出结构化计划）
  ❌ 后台巡猎循环（推迟到 Sprint 3）
  ❌ L3 自学习规则（推迟到 Sprint 3）

贾维斯不是聊天层，是巡猎规划器。
输出是结构化的 hunt_plan JSON，不是自然语言。
"""

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class HuntStep:
    """巡猎计划的单个步骤"""
    seq: int
    tool: str
    action: str
    target: Optional[str] = None
    focus: Optional[str] = None
    indicators: Optional[list] = None
    purpose: str = ""


@dataclass
class HuntPlan:
    """结构化巡猎计划"""
    hunt_id: str
    trigger_type: str       # user_query / jarvis_proactive / system_alert
    trigger_detail: str
    hypothesis: str         # 待验证假说（不是结论）
    priority: str           # CRITICAL / HIGH / MEDIUM / LOW
    planned_steps: list     # [HuntStep]
    scope: dict
    stop_conditions: list[str]
    timeout_ms: int = 8000
    fallback: str = "partial_results_with_degraded_flag"


# ============================================================
# 巡猎假说模板库
# ============================================================

HUNT_HYPOTHESES = {
    "lateral_movement": {
        "hypothesis": "内网可能存在横向移动行为",
        "keywords": ["横向", "lateral", "移动", "psexec", "smb", "rdp", "wmi"],
        "priority": "HIGH",
        "default_steps": [
            HuntStep(1, "T1", "triage_batch", purpose="从全量告警中筛选可疑事件"),
            HuntStep(2, "T3", "analyze_process_tree", focus="psexec|mimikatz|rubeus|smbclient",
                     purpose="还原可疑主机的进程树，提取攻击链"),
            HuntStep(3, "T4", "lookup_ioc", purpose="查询 T3 提取到的 IOC"),
            HuntStep(4, "T5", "blast_radius", purpose="评估隔离处置的业务影响"),
        ],
    },
    "ransomware": {
        "hypothesis": "可能存在勒索软件部署前兆",
        "keywords": ["勒索", "ransom", "加密", "encrypt", "c2", "vssadmin", "shadow"],
        "priority": "CRITICAL",
        "default_steps": [
            HuntStep(1, "T1", "triage_batch", purpose="筛选 C2/加密相关告警"),
            HuntStep(2, "T3", "analyze_process_tree", focus="vssadmin|cipher|c2_beacon|svchost_anomaly",
                     purpose="还原进程树，检测加密前准备行为"),
            HuntStep(3, "T4", "lookup_ioc", purpose="查询 C2 IP/域名情报"),
            HuntStep(4, "T5", "blast_radius", purpose="评估紧急隔离的影响"),
        ],
    },
    "data_exfiltration": {
        "hypothesis": "可能存在数据外泄行为",
        "keywords": ["外泄", "exfil", "外发", "传输", "泄漏", "leak", "dns tunnel"],
        "priority": "HIGH",
        "default_steps": [
            HuntStep(1, "T1", "triage_batch", purpose="筛选大流量/异常连接告警"),
            HuntStep(2, "T3", "analyze_process_tree", focus="curl|wget|ftp|dns_txt|encoded",
                     purpose="还原进程树，检测数据传输工具"),
            HuntStep(3, "T4", "lookup_ioc", purpose="查询外泄目标 IP/域名情报"),
            HuntStep(4, "T5", "blast_radius", purpose="评估处置影响"),
        ],
    },
    "insider_threat": {
        "hypothesis": "可能存在内部人员异常访问",
        "keywords": ["内部", "insider", "特权", "ceo", "越权", "非工作时间"],
        "priority": "MEDIUM",
        "default_steps": [
            HuntStep(1, "T1", "triage_batch", purpose="筛选非工作时间的特权账号活动"),
            HuntStep(2, "T3", "analyze_process_tree", focus="ssms|sqlplus|export|csv",
                     purpose="还原数据访问进程链"),
            HuntStep(3, "T4", "lookup_ioc", purpose="检查是否有外部关联"),
            HuntStep(4, "T5", "blast_radius", purpose="评估告警确认的影响"),
        ],
    },
    "generic": {
        "hypothesis": "需要对指定范围进行安全调查",
        "keywords": [],
        "priority": "MEDIUM",
        "default_steps": [
            HuntStep(1, "T1", "triage_batch", purpose="全量告警筛选"),
            HuntStep(2, "T3", "analyze_process_tree", purpose="可疑主机进程树分析"),
            HuntStep(3, "T4", "lookup_ioc", purpose="IOC 情报查询"),
            HuntStep(4, "T5", "blast_radius", purpose="处置影响评估"),
        ],
    },
}


class JarvisHuntEngine:
    """
    贾维斯巡猎引擎 — Sprint 2 被动模式

    输入：用户意图（自然语言 / intent 类型）+ 上下文
    输出：结构化 hunt_plan
    """

    def __init__(self):
        self._hunt_counter = 0

    def create_hunt_plan(
        self,
        trigger_type: str,
        user_input: str,
        intent: str = "",
        target_asset_id: str = None,
        target_ip: str = None,
        context: dict = None,
    ) -> HuntPlan:
        """
        根据触发条件生成结构化巡猎计划

        Args:
            trigger_type: user_query / jarvis_proactive / system_alert
            user_input: 用户原始输入或系统触发描述
            intent: Intent Router 识别的意图类型
            target_asset_id: 目标资产（如果有）
            target_ip: 目标 IP（如果有）
            context: 额外上下文（如已有的 T1 结果）
        """
        self._hunt_counter += 1
        hunt_id = f"HUNT-{int(time.time())}-{self._hunt_counter:03d}"

        # 匹配巡猎假说
        template = self._match_hypothesis(user_input, intent)

        # 定制步骤（注入目标信息）
        steps = self._customize_steps(
            template["default_steps"],
            target_asset_id=target_asset_id,
            target_ip=target_ip,
            context=context,
        )

        return HuntPlan(
            hunt_id=hunt_id,
            trigger_type=trigger_type,
            trigger_detail=user_input[:200] if user_input else "",
            hypothesis=template["hypothesis"],
            priority=template["priority"],
            planned_steps=steps,
            scope=self._build_scope(
                trigger_type=trigger_type,
                target_asset_id=target_asset_id,
                target_ip=target_ip,
                steps=steps,
                context=context,
            ),
            stop_conditions=self._build_stop_conditions(steps, context=context),
        )

    def plan_to_dict(self, plan: HuntPlan) -> dict:
        """序列化为 JSON-safe dict"""
        return {
            "hunt_id": plan.hunt_id,
            "trigger_type": plan.trigger_type,
            "trigger_detail": plan.trigger_detail,
            "hypothesis": plan.hypothesis,
            "priority": plan.priority,
            "scope": plan.scope,
            "stop_conditions": plan.stop_conditions,
            "planned_steps": [
                {
                    "seq": s.seq,
                    "tool": s.tool,
                    "action": s.action,
                    "target": s.target,
                    "focus": s.focus,
                    "indicators": s.indicators,
                    "purpose": s.purpose,
                }
                for s in plan.planned_steps
            ],
            "timeout_ms": plan.timeout_ms,
            "fallback": plan.fallback,
        }

    def _match_hypothesis(self, user_input: str, intent: str) -> dict:
        """根据输入关键词匹配巡猎假说模板"""
        input_lower = (user_input or "").lower()

        # 按优先级匹配（CRITICAL > HIGH > MEDIUM）
        priority_order = ["ransomware", "lateral_movement", "data_exfiltration", "insider_threat"]

        for template_key in priority_order:
            template = HUNT_HYPOTHESES[template_key]
            for kw in template["keywords"]:
                if kw in input_lower:
                    return template

        # 按 intent 兜底
        intent_map = {
            "threat_hunt": "lateral_movement",
            "data_exfil_check": "data_exfiltration",
            "summarize_recent": "generic",
            "asset_query": "generic",
        }
        template_key = intent_map.get(intent, "generic")
        return HUNT_HYPOTHESES[template_key]

    @staticmethod
    def _build_scope(
        trigger_type: str,
        target_asset_id: str = None,
        target_ip: str = None,
        steps: list[HuntStep] | None = None,
        context: dict = None,
    ) -> dict:
        targets = []
        if target_asset_id:
            targets.append(target_asset_id)
        elif target_ip:
            targets.append(target_ip)

        tools = []
        focus = []
        for step in steps or []:
            if step.tool and step.tool not in tools:
                tools.append(step.tool)
            if step.focus and step.focus not in focus:
                focus.append(step.focus)
            if step.target and step.target not in targets and not str(step.target).startswith("from_"):
                targets.append(step.target)

        planned_tools = list((context or {}).get("planned_tools", []))
        if not tools and planned_tools:
            tools = planned_tools

        return {
            "trigger_type": trigger_type,
            "targets": targets,
            "tools": tools,
            "focus": focus,
        }

    @staticmethod
    def _build_stop_conditions(steps: list[HuntStep] | None = None, context: dict = None) -> list[str]:
        stop_conditions = [
            "完成计划步骤并形成结构化调查结论",
            "若关键遥测缺失，则以降级结果结束并停止不安全处置建议",
        ]

        tools = {step.tool for step in (steps or []) if step.tool}
        if "T5" in tools:
            stop_conditions.append("若影响评估不可接受，则停止直接处置并转人工审批")
        if (context or {}).get("initial_alert_count", 0) == 0:
            stop_conditions.append("若没有可用原始告警，则停止扩展调查并返回空结果")

        return stop_conditions

    @staticmethod
    def _customize_steps(
        default_steps: list[HuntStep],
        target_asset_id: str = None,
        target_ip: str = None,
        context: dict = None,
    ) -> list[HuntStep]:
        """根据目标信息定制步骤"""
        steps = []
        for step in default_steps:
            # 深拷贝
            new_step = HuntStep(
                seq=step.seq,
                tool=step.tool,
                action=step.action,
                target=step.target or target_asset_id or target_ip,
                focus=step.focus,
                indicators=step.indicators,
                purpose=step.purpose,
            )

            # T3 步骤注入目标主机
            if new_step.tool == "T3" and not new_step.target:
                new_step.target = target_asset_id or target_ip or "from_T1_top_alerts"

            # T5 步骤注入目标
            if new_step.tool == "T5" and not new_step.target:
                new_step.target = target_asset_id or target_ip or "from_T3_most_suspicious"

            steps.append(new_step)

        return steps
