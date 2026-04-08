"""
SecuPilot T5: 真实爆炸半径计算引擎 (Real Blast Radius Calculator)

基于 NetworkX CMDB 拓扑图的 DFS 级联影响分析。

关键修正：
- 多目标隔离先解析 target_id，避免 "a1,a2" 直接查库失败
- 影响传播不再只看 predecessors，而是按关系语义双向传播
- max_depth 改为可配置/动态深度，避免固定层数低估爆炸半径
"""

try:
    import networkx as nx
except ImportError:  # pragma: no cover
    class _NodeAccessor:
        def __init__(self, graph):
            self._graph = graph

        def __call__(self):
            return list(self._graph._nodes.keys())

        def __getitem__(self, key):
            return self._graph._nodes[key]

    class _EdgeAccessor:
        def __init__(self, graph):
            self._graph = graph

        def __call__(self, node=None, data=False):
            if node is None:
                edges = []
                for src, dsts in self._graph._out.items():
                    for dst, attrs in dsts.items():
                        edges.append((src, dst, attrs) if data else (src, dst))
                return edges
            dsts = self._graph._out.get(node, {})
            return [(node, dst, attrs) if data else (node, dst) for dst, attrs in dsts.items()]

        def __getitem__(self, key):
            src, dst = key
            return self._graph._out[src][dst]

    class _SimpleDiGraph:
        def __init__(self):
            self._nodes = {}
            self._out = {}
            self._in = {}
            self.nodes = _NodeAccessor(self)
            self.edges = _EdgeAccessor(self)

        def add_node(self, node, **attrs):
            self._nodes.setdefault(node, {}).update(attrs)
            self._out.setdefault(node, {})
            self._in.setdefault(node, {})

        def add_edge(self, src, dst, **attrs):
            if src not in self._nodes:
                self.add_node(src)
            if dst not in self._nodes:
                self.add_node(dst)
            self._out[src][dst] = attrs
            self._in[dst][src] = attrs

        def predecessors(self, node):
            return list(self._in.get(node, {}).keys())

        def successors(self, node):
            return list(self._out.get(node, {}).keys())

        def has_node(self, node):
            return node in self._nodes

        def number_of_nodes(self):
            return len(self._nodes)

        def number_of_edges(self):
            return sum(len(v) for v in self._out.values())

        def __contains__(self, node):
            return node in self._nodes

    class _FallbackNX:
        DiGraph = _SimpleDiGraph

    nx = _FallbackNX()

from dataclasses import dataclass, field
from typing import Optional
import math


@dataclass
class ImpactReport:
    """爆炸半径评估报告"""
    action_type: str
    target: str
    directly_affected: int = 0
    cascade_affected: int = 0
    affected_assets: list = field(default_factory=list)
    affected_asset_details: list = field(default_factory=list)
    cascade_assets: list = field(default_factory=list)
    affected_users_count: int = 0
    affected_services: list = field(default_factory=list)
    estimated_downtime_hours: float = 0
    estimated_cost_rmb: int = 0
    recommendation: str = "PROCEED"
    alternatives: list = field(default_factory=list)
    topology_summary: dict = field(default_factory=dict)
    error: str = ""


# 不同操作类型的基础停机时间估算（小时）
ACTION_DOWNTIME_MAP = {
    "NETWORK_ISOLATE": 2.0,
    "EMERGENCY_ISOLATE": 4.0,
    "EMERGENCY_ISOLATE_MULTI": 4.0,
    "BLOCK_IP": 0.5,
    "ISOLATE_AND_BLOCK": 3.0,
    "ALERT_AND_CONFIRM": 0.0,  # 仅告警不操作
    "SERVICE_RESTART": 1.0,
    "CREDENTIAL_RESET": 0.5,
}

# 每权重点每小时的停机成本估算（RMB）
COST_PER_WEIGHT_HOUR = 5000

RELATION_POLICIES = {
    "depends_on": {"forward": False, "reverse": True, "coupling": 1.0},
    "accesses": {"forward": False, "reverse": True, "coupling": 0.65},
    "connects_to": {"forward": True, "reverse": True, "coupling": 0.75},
    "critical_service": {"forward": True, "reverse": True, "coupling": 1.0},
    "hosts": {"forward": True, "reverse": False, "coupling": 0.9},
    "routes_for": {"forward": True, "reverse": False, "coupling": 1.0},
    "belongs_to": {"forward": False, "reverse": False, "coupling": 0.0},
}


class RealBlastRadiusEngine:
    """
    T5: 真实爆炸半径计算引擎

    从 CMDB 拓扑数据构建 NetworkX 有向图，
    通过 DFS 遍历计算隔离操作的级联影响。
    """

    def __init__(self, topology_data: dict,
                 max_depth: Optional[int] = None,
                 min_propagation_strength: float = 0.25):
        """
        Args:
            topology_data: 知识图谱数据 {
                nodes: {assets: [...], users: [...], segments: [...]},
                relationships: [{from, to, type}, ...]
            }
            max_depth: 可选最大传播深度；默认按拓扑规模动态计算
            min_propagation_strength: 低于该阈值的弱依赖不再继续传播
        """
        self.G = nx.DiGraph()
        self.asset_index = {}
        self.segment_index = {}
        self.user_access_map = {}  # user_id → [asset_ids]
        self.max_depth = max_depth
        self.min_propagation_strength = min_propagation_strength
        self._build_graph(topology_data)

    def _build_graph(self, data: dict):
        """从拓扑数据构建有向图"""
        nodes = data.get("nodes", {})

        # 添加资产节点
        assets = nodes.get("assets", [])
        if isinstance(assets, int):
            assets = []  # 兼容只存了数量的旧格式
        for asset in assets:
            aid = str(asset.get("asset_id", asset.get("id", "")))
            if not aid:
                continue
            self.G.add_node(aid, node_type="asset", **asset)
            self.asset_index[aid] = asset
            ip = asset.get("ip_address", "")
            if ip:
                self.asset_index[str(ip)] = asset

        # 添加网段节点
        segments = nodes.get("segments", nodes.get("network_segments", []))
        for seg in segments:
            sid = str(seg.get("id", seg.get("segment_id", "")))
            if sid:
                self.G.add_node(sid, node_type="segment", **seg)
                self.segment_index[sid] = seg

        # 添加用户节点
        users = nodes.get("users", [])
        for user in users:
            uid = str(user.get("user_id", ""))
            if uid:
                self.G.add_node(uid, node_type="user", **user)

        # 添加关系边
        for rel in data.get("relationships", []):
            src = str(rel.get("from", ""))
            dst = str(rel.get("to", ""))
            rel_type = rel.get("type", "unknown")
            if src and dst:
                default_policy = RELATION_POLICIES.get(rel_type, {"coupling": 0.5})
                self.G.add_edge(
                    src,
                    dst,
                    rel_type=rel_type,
                    coupling=float(rel.get("coupling", default_policy.get("coupling", 0.5))),
                    impact_direction=rel.get("impact_direction"),
                )

                if rel_type == "accesses":
                    self.user_access_map.setdefault(src, []).append(dst)

    def calculate(self, action_type: str, target_id: str) -> ImpactReport:
        """
        计算处置操作的爆炸半径

        Args:
            action_type: 操作类型（NETWORK_ISOLATE / BLOCK_IP / ...）
            target_id: 目标资产 ID 或 IP

        Returns:
            ImpactReport: 完整的影响评估报告
        """
        resolved_targets = self._resolve_targets(action_type, target_id)
        if not resolved_targets:
            return ImpactReport(
                action_type=action_type, target=target_id,
                error=f"Target '{target_id}' not found in CMDB topology"
            )

        actual_id = resolved_targets[0]

        if action_type == "ALERT_AND_CONFIRM":
            return ImpactReport(
                action_type=action_type, target=actual_id,
                recommendation="ALERT_ONLY",
                topology_summary={"note": "仅告警确认，不执行隔离操作"},
            )

        # ---- 1. 找到直接受影响的资产 ----
        affected = set(resolved_targets)

        if action_type in ("NETWORK_ISOLATE", "EMERGENCY_ISOLATE", "ISOLATE_AND_BLOCK", "EMERGENCY_ISOLATE_MULTI"):
            for asset_id in list(affected):
                target_segment = self._find_segment(asset_id)
                if target_segment:
                    affected.update(self._find_assets_in_segment(target_segment))

        # ---- 2. DFS 计算级联影响 ----
        cascade = set()
        max_depth = self._effective_max_depth()
        for node in list(affected):
            dependents = self._dfs_dependents(
                node,
                visited=set(affected),
                depth=0,
                max_depth=max_depth,
                impact_strength=1.0,
            )
            cascade.update(dependents)

        cascade -= affected

        cascade_assets = {
            n for n in cascade
            if self.G.nodes[n].get("node_type") == "asset"
        }

        # ---- 3. 统计受影响的用户 ----
        affected_users = {
            n for n in cascade
            if self.G.nodes[n].get("node_type") == "user"
        }
        for uid, asset_list in self.user_access_map.items():
            for aid in asset_list:
                if aid in affected or aid in cascade_assets:
                    affected_users.add(uid)
                    break

        # ---- 4. 识别受影响的服务/业务 ----
        all_impacted_assets = affected | cascade_assets
        affected_services = set()
        for aid in all_impacted_assets:
            asset = self.asset_index.get(aid, {})
            role = asset.get("role", "")
            bu = asset.get("business_unit", "")
            if role:
                affected_services.add(f"{bu}: {role}" if bu else role)

        # ---- 5. 经济影响估算 ----
        base_downtime = ACTION_DOWNTIME_MAP.get(action_type, 2.0)
        if len(cascade_assets) >= 2:
            downtime = base_downtime * 1.5
        else:
            downtime = base_downtime

        estimated_cost = int(sum(self._hourly_value(aid) for aid in all_impacted_assets) * downtime)

        # ---- 6. 生成建议 ----
        if estimated_cost > 100000 or len(cascade_assets) >= 5:
            recommendation = "HIGH_IMPACT_REVIEW"
        elif estimated_cost > 50000 or len(cascade_assets) >= 2:
            recommendation = "REVIEW_ALTERNATIVES"
        else:
            recommendation = "PROCEED"

        # ---- 7. 生成替代方案（当影响过大时）----
        alternatives = []
        if recommendation != "PROCEED":
            alternatives = self._generate_alternatives(action_type, actual_id, affected)

        affected_details = []
        for aid in sorted(all_impacted_assets):
            a = self.asset_index.get(aid, {})
            affected_details.append({
                "asset_id": aid,
                "role": a.get("role", "Unknown"),
                "criticality": a.get("criticality_weight", 0),
                "business_unit": a.get("business_unit", ""),
                "owner": a.get("owner", ""),
            })

        return ImpactReport(
            action_type=action_type,
            target=actual_id,
            directly_affected=len(affected),
            cascade_affected=len(cascade_assets),
            affected_assets=sorted(affected),
            affected_asset_details=affected_details,
            cascade_assets=sorted(cascade_assets),
            affected_users_count=len(affected_users),
            affected_services=sorted(affected_services),
            estimated_downtime_hours=round(downtime, 1),
            estimated_cost_rmb=estimated_cost,
            recommendation=recommendation,
            alternatives=alternatives,
            topology_summary={
                "total_nodes": self.G.number_of_nodes(),
                "total_edges": self.G.number_of_edges(),
                "target_segment": self._find_segment(actual_id),
                "resolved_targets": resolved_targets,
                "traversal_max_depth": max_depth,
            },
        )

    def _resolve_targets(self, action_type: str, target_id: str) -> list[str]:
        """支持 asset_id、IP，以及逗号分隔的多目标"""
        raw_targets = [target_id]
        if action_type == "EMERGENCY_ISOLATE_MULTI":
            raw_targets = [part.strip() for part in str(target_id).split(",") if part.strip()]

        resolved = []
        for raw in raw_targets:
            asset_info = self.asset_index.get(str(raw))
            if asset_info:
                actual_id = str(asset_info.get("asset_id", raw))
                if actual_id not in resolved:
                    resolved.append(actual_id)
        return resolved

    def _find_segment(self, asset_id: str) -> Optional[str]:
        """找到资产所属的网段"""
        if asset_id not in self.G:
            return None
        for _, neighbor, data in self.G.edges(asset_id, data=True):
            if data.get("rel_type") == "belongs_to":
                return neighbor
        return None

    def _find_assets_in_segment(self, segment_id: str) -> list[str]:
        """找到网段内的所有资产"""
        assets = []
        for node in self.G.nodes():
            if self.G.nodes[node].get("node_type") != "asset":
                continue
            for _, seg, data in self.G.edges(node, data=True):
                if seg == segment_id and data.get("rel_type") == "belongs_to":
                    assets.append(node)
        return assets

    def _effective_max_depth(self) -> int:
        """按拓扑规模动态估算合理的遍历深度"""
        if self.max_depth is not None:
            return self.max_depth
        return max(5, min(12, int(math.log2(max(self.G.number_of_nodes(), 2))) + 4))

    def _propagates(self, edge_data: dict, direction: str) -> bool:
        """根据关系语义决定是否沿该方向传播影响"""
        override = edge_data.get("impact_direction")
        if override == "both":
            return True
        if override == "none":
            return False
        if override in ("forward", "reverse"):
            return override == direction

        rel_type = edge_data.get("rel_type", "unknown")
        policy = RELATION_POLICIES.get(rel_type, {"forward": False, "reverse": True})
        return bool(policy.get(direction, False))

    def _dfs_dependents(self, start: str, visited: set = None,
                        depth: int = 0, max_depth: Optional[int] = None,
                        impact_strength: float = 1.0) -> set:
        """
        DFS 遍历找到所有受 start 影响的节点（按关系语义双向传播）。

        生产环境下改为显式栈，避免大图或异常环路带来的递归边界风险。
        """
        blocked = set(visited or set())
        if max_depth is None:
            max_depth = self._effective_max_depth()
        if depth >= max_depth:
            return set()

        dependents = set()
        best_strength = {start: impact_strength}
        stack = [(start, depth, impact_strength)]

        while stack:
            current, current_depth, current_strength = stack.pop()
            if current_depth >= max_depth:
                continue

            # 反向遍历：谁依赖于我？
            for predecessor in self.G.predecessors(current):
                if predecessor in blocked:
                    continue
                edge_data = self.G.edges[predecessor, current]
                if not self._propagates(edge_data, "reverse"):
                    continue

                edge_coupling = min(1.0, max(0.0, float(edge_data.get("coupling", 0.5))))
                next_strength = current_strength * edge_coupling
                if next_strength < self.min_propagation_strength:
                    continue
                if next_strength <= best_strength.get(predecessor, 0.0):
                    continue

                best_strength[predecessor] = next_strength
                dependents.add(predecessor)
                stack.append((predecessor, current_depth + 1, next_strength))

            # 正向遍历：某些强耦合关系中，我断了，下游也会受影响
            for successor in self.G.successors(current):
                if successor in blocked:
                    continue
                edge_data = self.G.edges[current, successor]
                if not self._propagates(edge_data, "forward"):
                    continue

                edge_coupling = min(1.0, max(0.0, float(edge_data.get("coupling", 0.5))))
                next_strength = current_strength * edge_coupling
                if next_strength < self.min_propagation_strength:
                    continue
                if next_strength <= best_strength.get(successor, 0.0):
                    continue

                best_strength[successor] = next_strength
                dependents.add(successor)
                stack.append((successor, current_depth + 1, next_strength))

        return dependents

    def _hourly_value(self, asset_id: str) -> float:
        """优先使用业务小时产值；缺失时退回权重点成本模型"""
        asset = self.asset_index.get(asset_id, {})
        explicit = asset.get("hourly_business_value", asset.get("service_value_per_hour"))
        if explicit is not None:
            try:
                return float(explicit)
            except (TypeError, ValueError):
                pass
        return float(asset.get("criticality_weight", 1)) * COST_PER_WEIGHT_HOUR

    def _generate_alternatives(self, action_type: str, target_id: str, affected: set) -> list:
        """当影响过大时，生成替代方案"""
        alts = []

        if action_type in ("NETWORK_ISOLATE", "EMERGENCY_ISOLATE", "EMERGENCY_ISOLATE_MULTI"):
            alts.append({
                "action": "TARGETED_ISOLATE",
                "description": f"仅隔离 {target_id} 的外网访问，保留内网关键依赖",
                "estimated_impact": "降低网段级误伤，但仍需防范横向移动",
                "risk_tradeoff": "中等风险",
            })

        alts.append({
            "action": "ENHANCED_MONITORING",
            "description": f"不隔离，但将 {target_id} 的所有流量镜像到分析引擎",
            "estimated_impact": "零业务影响，但无法阻止攻击继续",
            "risk_tradeoff": "高风险",
        })

        if len(affected) > 2:
            alts.append({
                "action": "PHASED_ISOLATE",
                "description": f"先隔离最高风险的 {target_id}，24 小时后评估是否扩大范围",
                "estimated_impact": "降低 40% 即时影响，但需持续关注",
                "risk_tradeoff": "中低风险",
            })

        return alts
