"""
SecuPilot T3: 进程树证据编译器 (Process Tree Evidence Compiler)

不是树组件，是证据编译器。

输入：符合冻结协议的 ProcessEvent 列表
     （由 `app.tools.edr_adapter.process_event_batch_to_runtime_payload()` 生成）
输出：
  1. Top-K 可疑链条（每条含异常评分 + 证据状态 + ATT&CK 映射）
  2. 持久化机制检测
  3. 日志缺口标注
  4. 提取的 IOC（typed objects，直接送 T4）

关键约束（冻结协议）：
  - evidence_status 只允许 VERIFIED / INFERRED / UNVERIFIED
  - analysis_status 只允许 COMPLETE / PARTIAL / DEGRADED / FAILED
  - ioc_extracted 是 typed objects: {type, value, source_chain_id, source_node_id, context, confidence}
  - ID 格式: {host_id}:chain-{NNN}:node-{NNN}
  - analysis_scope 必须标注 T3 只分析了什么（process_tree / network / registry / file）
"""

import time
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

try:
    import networkx as nx
except ImportError:
    nx = None

# ============================================================
# 检测规则库
# ============================================================

# 已知攻击工具（进程名 → 信息）
KNOWN_ATTACK_TOOLS = {
    "mimikatz.exe":    {"risk": 10, "mitre": "T1003.001", "tactic": "Credential Access", "desc": "Credential dumping tool"},
    "rubeus.exe":      {"risk": 10, "mitre": "T1558.003", "tactic": "Credential Access", "desc": "Kerberos attack tool"},
    "psexec.exe":      {"risk": 8,  "mitre": "T1570",     "tactic": "Lateral Movement",  "desc": "Remote execution tool"},
    "psexec64.exe":    {"risk": 8,  "mitre": "T1570",     "tactic": "Lateral Movement",  "desc": "Remote execution tool (64-bit)"},
    "sharphound.exe":  {"risk": 9,  "mitre": "T1087.002", "tactic": "Discovery",         "desc": "AD reconnaissance tool"},
    "bloodhound.exe":  {"risk": 9,  "mitre": "T1087.002", "tactic": "Discovery",         "desc": "AD attack path tool"},
    "cobalt":          {"risk": 10, "mitre": "T1071.001", "tactic": "Command and Control","desc": "C2 framework"},
    "vssadmin.exe":    {"risk": 7,  "mitre": "T1490",     "tactic": "Impact",            "desc": "Shadow copy deletion (when used with delete)"},
    "wmic.exe":        {"risk": 5,  "mitre": "T1047",     "tactic": "Execution",         "desc": "WMI execution (context-dependent)"},
}

# 可疑父子关系（parent_name, child_name → 信息）
SUSPICIOUS_PARENT_CHILD = {
    ("services.exe", "cmd.exe"):        {"risk": 6, "mitre": "T1059.003", "desc": "Service spawning command shell"},
    ("svchost.exe", "cmd.exe"):         {"risk": 7, "mitre": "T1059.003", "desc": "Service host spawning command shell"},
    ("svchost.exe", "powershell.exe"):  {"risk": 8, "mitre": "T1059.001", "desc": "Service host spawning PowerShell"},
    ("svchost.exe", "explorer.exe"):    {"risk": 7, "mitre": "T1055",     "desc": "Unusual child of svchost"},
    ("explorer.exe", "mshta.exe"):      {"risk": 8, "mitre": "T1218.005", "desc": "MSHTA abuse"},
    ("winword.exe", "cmd.exe"):         {"risk": 9, "mitre": "T1204.002", "desc": "Office macro execution"},
    ("winword.exe", "powershell.exe"):  {"risk": 9, "mitre": "T1204.002", "desc": "Office macro → PowerShell"},
    ("outlook.exe", "powershell.exe"):  {"risk": 8, "mitre": "T1566.001", "desc": "Email client → PowerShell"},
    ("services.exe", "psexesvc.exe"):   {"risk": 7, "mitre": "T1570",     "desc": "PsExec remote service installation"},
}

# 可疑路径
SUSPICIOUS_PATHS = [
    "\\users\\public", "\\temp\\", "\\appdata\\local\\temp",
    "\\programdata\\", "\\downloads\\", "\\desktop\\",
]

# 高危命令行关键词
SUSPICIOUS_CMDLINE = [
    ("-enc ", 8, "T1059.001", "Encoded PowerShell command"),
    ("-encodedcommand", 8, "T1059.001", "Encoded PowerShell command"),
    ("lsadump::dcsync", 10, "T1003.006", "DCSync attack"),
    ("sekurlsa::logonpasswords", 10, "T1003.001", "Credential dumping"),
    ("kerberoast", 9, "T1558.003", "Kerberoasting"),
    ("delete shadows", 9, "T1490", "Shadow copy deletion"),
    ("/all /quiet", 7, "T1490", "Silent shadow deletion"),
    ("net use \\\\", 5, "T1021.002", "SMB share mounting"),
    ("net user /add", 7, "T1136.001", "Local account creation"),
]


# ============================================================
# 数据结构（冻结协议）
# ============================================================

@dataclass
class ChainNode:
    """链条中的单个节点"""
    node_id: str
    pid: int
    ppid: int
    process_name: str
    exe_path: str
    command_line: str
    user: str
    timestamp: str
    evidence_status: str  # VERIFIED / INFERRED / UNVERIFIED
    anomalies: list = field(default_factory=list)  # [{type, risk, mitre, desc}]
    tactic: str = ""


@dataclass
class SuspiciousChain:
    """一条可疑进程链"""
    chain_id: str
    anomaly_score: float
    path: list  # [ChainNode as dict]
    attack_stages: list  # ATT&CK tactics observed
    matched_rules: list
    risk_contribution: str  # HIGH / MEDIUM / LOW


@dataclass
class ExtractedIOC:
    """提取的 IOC（冻结协议 typed object）"""
    type: str           # ip / domain / hash
    value: str
    source_chain_id: str
    source_node_id: str
    context: str
    confidence: float


@dataclass
class T3Result:
    """T3 完整输出"""
    host_id: str
    analysis_status: str  # COMPLETE / PARTIAL / DEGRADED / FAILED
    analysis_scope: list  # ["process_tree", "network_connect", "registry_set", "file_write"]
    degraded_reason: Optional[str]
    process_tree_stats: dict
    suspicious_chains: list  # [SuspiciousChain as dict]
    persistence_mechanisms: list
    ioc_extracted: list  # [ExtractedIOC as dict]
    gaps: list
    execution_ms: float


# ============================================================
# 核心引擎
# ============================================================

class ProcessTreeCompiler:
    """
    T3: 进程树证据编译器

    1. 从 ProcessEvent 列表构建进程树（NetworkX DiGraph）
    2. 对每个进程节点做异常检测
    3. 提取 Top-K 最可疑链条
    4. 检测持久化机制
    5. 标注日志缺口
    6. 提取 IOC 供 T4 消费
    """

    def __init__(self, top_k: int = 3):
        self.top_k = top_k

    def analyze(self, host_id: str, events: list[dict]) -> T3Result:
        """分析单台主机的行为事件"""
        start = time.monotonic()
        events = [event for event in events if event.get("host_id") == host_id]

        if not events:
            return T3Result(
                host_id=host_id, analysis_status="FAILED",
                analysis_scope=[], degraded_reason="No events provided",
                process_tree_stats={"total_processes": 0, "analyzed": 0, "suspicious": 0},
                suspicious_chains=[], persistence_mechanisms=[],
                ioc_extracted=[], gaps=[], execution_ms=0,
            )

        # 分离事件类型
        proc_events = [e for e in events if e.get("event_type") == "process_create"]
        net_events = [e for e in events if e.get("event_type") == "network_connect"]
        dns_events = [e for e in events if e.get("event_type") == "dns_query"]
        reg_events = [e for e in events if e.get("event_type") == "registry_set"]
        file_events = [e for e in events if e.get("event_type") == "file_write"]

        scope = []
        if proc_events: scope.append("process_tree")
        if net_events: scope.append("network_connect")
        if dns_events: scope.append("dns_query")
        if reg_events: scope.append("registry_set")
        if file_events: scope.append("file_write")

        # Step 1: 构建进程树
        tree, node_data = self._build_tree(proc_events)

        # Step 2: 异常检测（每个节点）
        self._detect_anomalies(tree, node_data, net_events, dns_events, file_events)

        # Step 3: 提取 Top-K 可疑链条
        chains = self._extract_suspicious_chains(host_id, tree, node_data)

        # Step 4: 检测持久化机制
        persistence = self._detect_persistence(host_id, reg_events, proc_events)

        # Step 5: 标注日志缺口
        gaps = self._detect_gaps(host_id, events, node_data)

        # Step 6: 提取 IOC
        iocs = self._extract_iocs(host_id, chains, net_events, dns_events, file_events)

        # 判定 analysis_status
        degraded_reason = None
        if gaps:
            status = "PARTIAL"
            degraded_reason = f"{len(gaps)} log gap(s) detected"
        elif not proc_events:
            status = "DEGRADED"
            degraded_reason = "No process_create events"
        else:
            status = "COMPLETE"

        suspicious_count = sum(1 for pid, data in node_data.items() if data.get("_anomalies"))

        elapsed = (time.monotonic() - start) * 1000

        return T3Result(
            host_id=host_id,
            analysis_status=status,
            analysis_scope=scope,
            degraded_reason=degraded_reason,
            process_tree_stats={
                "total_processes": len(proc_events),
                "analyzed": len(proc_events),
                "suspicious": suspicious_count,
            },
            suspicious_chains=[self._chain_to_dict(c) for c in chains[:self.top_k]],
            persistence_mechanisms=persistence,
            ioc_extracted=[self._ioc_to_dict(i) for i in iocs],
            gaps=gaps,
            execution_ms=round(elapsed, 2),
        )

    # ---- 内部方法 ----

    def _build_tree(self, proc_events: list) -> tuple:
        """构建进程树"""
        tree = {}  # pid → ppid
        node_data = {}  # pid → event dict + metadata

        for event in proc_events:
            pid = event["pid"]
            ppid = event.get("ppid", 0)
            tree[pid] = ppid
            node_data[pid] = {
                **event,
                "_anomalies": [],
                "_risk_score": 0,
            }

        return tree, node_data

    def _detect_anomalies(self, tree, node_data, net_events, dns_events, file_events):
        """对每个进程节点做异常检测"""
        for pid, data in node_data.items():
            name = data.get("process_name", "").lower()
            path = data.get("exe_path", "").lower()
            cmdline = data.get("command_line", "").lower()
            ppid = data.get("ppid", 0)
            parent_data = node_data.get(ppid, {})
            parent_name = parent_data.get("process_name", "").lower()

            anomalies = []

            # 检测 1: 已知攻击工具
            for tool_name, info in KNOWN_ATTACK_TOOLS.items():
                if tool_name in name:
                    # vssadmin 特殊处理：只在 delete 上下文中才高危
                    if tool_name == "vssadmin.exe" and "delete" not in cmdline:
                        continue
                    anomalies.append({
                        "type": "known_attack_tool",
                        "risk": info["risk"],
                        "mitre": info["mitre"],
                        "tactic": info["tactic"],
                        "desc": f"Known attack tool: {info['desc']}",
                    })

            # 检测 2: 可疑父子关系
            pair = (parent_name, name)
            if pair in SUSPICIOUS_PARENT_CHILD:
                info = SUSPICIOUS_PARENT_CHILD[pair]
                anomalies.append({
                    "type": "suspicious_parent_child",
                    "risk": info["risk"],
                    "mitre": info["mitre"],
                    "desc": info["desc"],
                })

            # 检测 3: 可疑启动路径
            for sus_path in SUSPICIOUS_PATHS:
                if sus_path in path:
                    anomalies.append({
                        "type": "suspicious_path",
                        "risk": 6,
                        "mitre": "T1036",
                        "desc": f"Launched from suspicious directory: {path}",
                    })
                    break

            # 检测 4: 命令行关键词
            for keyword, risk, mitre, desc in SUSPICIOUS_CMDLINE:
                if keyword in cmdline:
                    anomalies.append({
                        "type": "suspicious_cmdline",
                        "risk": risk,
                        "mitre": mitre,
                        "desc": desc,
                    })

            data["_anomalies"] = anomalies
            data["_risk_score"] = max((a["risk"] for a in anomalies), default=0)

    def _extract_suspicious_chains(self, host_id, tree, node_data) -> list[SuspiciousChain]:
        """提取 Top-K 可疑链条"""
        # 找到所有有异常的叶节点，回溯到根
        suspicious_pids = [
            pid for pid, data in node_data.items()
            if data.get("_anomalies")
        ]

        chains = []
        seen_paths = set()

        for leaf_pid in suspicious_pids:
            # 回溯到根
            path_pids = []
            current = leaf_pid
            visited = set()
            while current in node_data and current not in visited:
                visited.add(current)
                path_pids.append(current)
                current = tree.get(current, 0)
            path_pids.reverse()

            # 去重（避免同一条路径的子路径重复）
            path_key = tuple(path_pids)
            if path_key in seen_paths:
                continue
            seen_paths.add(path_key)

            # 构建 ChainNode 列表
            chain_idx = len(chains)
            chain_id = f"{host_id}:chain-{chain_idx:03d}"
            nodes = []
            tactics = set()
            rules = []
            max_risk = 0

            for i, pid in enumerate(path_pids):
                data = node_data[pid]
                node_id = f"{chain_id}:node-{i:03d}"

                for anomaly in data.get("_anomalies", []):
                    if anomaly.get("tactic"):
                        tactics.add(anomaly["tactic"])
                    rules.append(anomaly.get("desc", ""))
                    max_risk = max(max_risk, anomaly.get("risk", 0))

                nodes.append(ChainNode(
                    node_id=node_id,
                    pid=pid,
                    ppid=data.get("ppid", 0),
                    process_name=data.get("process_name", ""),
                    exe_path=data.get("exe_path", ""),
                    command_line=data.get("command_line", ""),
                    user=data.get("user", ""),
                    timestamp=data.get("timestamp", ""),
                    evidence_status="VERIFIED",  # 有原始事件 = VERIFIED
                    anomalies=data.get("_anomalies", []),
                    tactic=data.get("_anomalies", [{}])[0].get("tactic", "") if data.get("_anomalies") else "",
                ))

            if max_risk > 0:
                # 异常度 = 链条内最高风险 × (1 + 异常节点占比加成)
                anomaly_ratio = sum(1 for n in nodes if n.anomalies) / max(len(nodes), 1)
                anomaly_score = round(min(10.0, max_risk * (1 + anomaly_ratio * 0.3)), 1)

                risk_level = "HIGH" if anomaly_score >= 7 else ("MEDIUM" if anomaly_score >= 4 else "LOW")

                chains.append(SuspiciousChain(
                    chain_id=chain_id,
                    anomaly_score=anomaly_score,
                    path=nodes,
                    attack_stages=sorted(tactics),
                    matched_rules=list(set(rules)),
                    risk_contribution=risk_level,
                ))

        # 按异常度排序
        chains.sort(key=lambda c: c.anomaly_score, reverse=True)
        return chains

    def _detect_persistence(self, host_id, reg_events, proc_events) -> list:
        """检测持久化机制"""
        persistence = []
        idx = 0

        for event in reg_events:
            key_path = event.get("key_path", "").lower()
            if any(marker in key_path for marker in ["\\run", "\\runonce", "\\services\\"]):
                persistence.append({
                    "evidence_id": f"{host_id}:persist-{idx:03d}",
                    "type": "registry_run_key" if "\\run" in key_path else "service_registration",
                    "key_path": event.get("key_path", ""),
                    "value_name": event.get("value_name", ""),
                    "value_data": event.get("value_data", ""),
                    "timestamp": event.get("timestamp", ""),
                    "process": event.get("process_name", ""),
                    "evidence_status": "VERIFIED",
                    "mitre": "T1547.001" if "\\run" in key_path else "T1543.003",
                })
                idx += 1

        return persistence

    def _detect_gaps(self, host_id, events, node_data) -> list:
        """
        检测日志缺口。

        Sprint 2 的行为事件是抽样关键行为，不是全量遥测流，因此不能把任意稀疏时间间隔
        直接当成日志丢失。这里只在“首个可疑进程出现之后”的活跃调查窗口内检测较大缺口。
        """
        suspicious_times = []
        for data in node_data.values():
            if data.get("_anomalies") and data.get("timestamp"):
                try:
                    suspicious_times.append(datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")))
                except ValueError:
                    continue

        if len(suspicious_times) < 1:
            return []

        active_window_start = min(suspicious_times)
        active_timestamps = []
        for event in events:
            timestamp = event.get("timestamp")
            if not timestamp:
                continue
            try:
                parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except ValueError:
                continue
            if parsed >= active_window_start:
                active_timestamps.append((timestamp, parsed))

        if len(active_timestamps) < 2:
            return []

        gaps = []
        gap_threshold_seconds = 300  # 5 分钟，避免把稀疏关键行为样本误判为日志缺口

        active_timestamps.sort(key=lambda item: item[1])
        for i in range(1, len(active_timestamps)):
            prev_raw, prev_dt = active_timestamps[i - 1]
            curr_raw, curr_dt = active_timestamps[i]
            delta = (curr_dt - prev_dt).total_seconds()
            if delta > gap_threshold_seconds:
                gaps.append({
                    "gap_id": f"{host_id}:gap-{len(gaps):03d}",
                    "time_range": f"{prev_raw} - {curr_raw}",
                    "duration_seconds": int(delta),
                    "type": "syslog_gap",
                    "impact": "events_in_this_window_may_be_missing",
                })

        return gaps

    def _extract_iocs(self, host_id, chains, net_events, dns_events, file_events) -> list[ExtractedIOC]:
        """提取 IOC（严格遵循冻结协议 typed schema）"""
        iocs = []
        seen = set()

        # 从文件事件中提取 Hash
        for event in file_events:
            hash_val = event.get("file_hash_sha256", "")
            if not hash_val or hash_val in seen:
                continue
            chain_ref = self._find_chain_node_for_pid(chains, event.get("pid", 0))
            if not chain_ref:
                continue
            chain_id, node_id = chain_ref
            seen.add(hash_val)
            iocs.append(ExtractedIOC(
                type="hash", value=hash_val,
                source_chain_id=chain_id,
                source_node_id=node_id,
                context=f"File hash from {event.get('file_path', 'unknown')}",
                confidence=0.9,
            ))

        # 从网络事件中提取外部 IP
        import ipaddress
        for event in net_events:
            dst_ip = event.get("dst_ip", "")
            if not dst_ip or dst_ip in seen:
                continue
            chain_ref = self._find_chain_node_for_pid(chains, event.get("pid", 0))
            if not chain_ref:
                continue
            try:
                if ipaddress.ip_address(dst_ip).is_private:
                    continue
            except (ValueError, TypeError):
                continue

            chain_id, node_id = chain_ref
            seen.add(dst_ip)
            iocs.append(ExtractedIOC(
                type="ip", value=dst_ip,
                source_chain_id=chain_id,
                source_node_id=node_id,
                context=f"Outbound connection to {dst_ip}:{event.get('dst_port', '?')}",
                confidence=0.85,
            ))

        # 从 DNS 事件中提取可疑域名
        for event in dns_events:
            domain = event.get("query_domain", "")
            if not domain or domain in seen:
                continue
            if domain.endswith((".local", ".internal", ".corp", ".lan")):
                continue
            chain_ref = self._find_chain_node_for_pid(chains, event.get("pid", 0))
            if not chain_ref:
                continue

            chain_id, node_id = chain_ref
            seen.add(domain)
            iocs.append(ExtractedIOC(
                type="domain", value=domain,
                source_chain_id=chain_id,
                source_node_id=node_id,
                context=f"DNS {event.get('query_type', 'A')} query for {domain}",
                confidence=0.7,
            ))

        return iocs

    @staticmethod
    def _find_chain_node_for_pid(chains, pid) -> Optional[tuple[str, str]]:
        """找到包含指定 PID 的链条与稳定 node_id。只接受可回链的可疑上下文。"""
        for chain in chains:
            for node in chain.path:
                if node.pid == pid:
                    return chain.chain_id, node.node_id
        return None

    @staticmethod
    def _chain_to_dict(chain: SuspiciousChain) -> dict:
        """序列化链条"""
        return {
            "chain_id": chain.chain_id,
            "anomaly_score": chain.anomaly_score,
            "path": [
                {
                    "node_id": n.node_id,
                    "pid": n.pid,
                    "ppid": n.ppid,
                    "process_name": n.process_name,
                    "exe_path": n.exe_path,
                    "command_line": n.command_line,
                    "user": n.user,
                    "timestamp": n.timestamp,
                    "evidence_status": n.evidence_status,
                    "anomalies": n.anomalies,
                    "tactic": n.tactic,
                }
                for n in chain.path
            ],
            "attack_stages": chain.attack_stages,
            "matched_rules": chain.matched_rules,
            "risk_contribution": chain.risk_contribution,
        }

    @staticmethod
    def _ioc_to_dict(ioc: ExtractedIOC) -> dict:
        """序列化 IOC"""
        return {
            "type": ioc.type,
            "value": ioc.value,
            "source_chain_id": ioc.source_chain_id,
            "source_node_id": ioc.source_node_id,
            "context": ioc.context,
            "confidence": ioc.confidence,
        }
