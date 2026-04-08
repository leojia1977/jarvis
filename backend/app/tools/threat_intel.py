"""
SecuPilot T4: 真实威胁情报查询引擎 (Real Threat Intelligence Engine)

生产级本地情报库 — 不是字典查找，是向量检索 + 多策略匹配。

架构：
  Layer 1: 精确匹配（哈希表 O(1)）
  Layer 2: 前缀/子网匹配（IP CIDR 和域名后缀）
  Layer 3: 向量相似度（字符 n-gram 余弦相似度，用于模糊 IOC 关联）

POC 阶段使用纯 Python 实现（无需 Qdrant Docker）。
正式版替换 Layer 3 为 Qdrant 客户端，算法逻辑不变。

验证标准：
  - 精确匹配延迟 < 1ms
  - 模糊检索（Top-3）延迟 < 10ms
  - 48 条 IOC 全部可检索
"""

import math
import time
import ipaddress
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# 数据结构
# ============================================================

@dataclass
class IntelMatch:
    """单条情报匹配结果"""
    indicator: str
    match_type: str          # exact / subnet / suffix / similar
    ioc_type: str            # ip / domain / hash / c2_signature
    threat_type: str         # C2 / Scanner / Botnet / Phishing / Malware / ...
    actor: str               # APT-BEAR / RANSOMWARE-X / Unknown
    confidence: float        # 情报源置信度 0-1
    match_score: float       # 匹配分数 0-1 (精确=1.0, 模糊<1.0)
    country: str = ""
    first_seen: str = ""
    last_seen: str = ""
    tags: list = field(default_factory=list)
    related_campaigns: list = field(default_factory=list)
    mitre_techniques: list = field(default_factory=list)
    raw_record: dict = field(default_factory=dict)


@dataclass
class IntelReport:
    """情报查询报告"""
    query_indicator: str
    matches: list[IntelMatch]
    has_exact_match: bool
    has_apt_association: bool
    overall_threat_level: str   # CRITICAL / HIGH / MEDIUM / LOW / CLEAN
    lookup_time_ms: float
    related_iocs: list = field(default_factory=list)


# ============================================================
# APT 组织画像库
# ============================================================

APT_PROFILES = {
    "APT-BEAR": {
        "aliases": ["Fancy Bear", "APT28", "Sofacy", "Pawn Storm"],
        "origin": "Russia (GRU Unit 26165)",
        "motivation": "政治间谍 / 军事情报",
        "typical_ttps": ["T1566 Phishing", "T1071 C2", "T1003 Credential Dumping"],
        "target_sectors": ["Government", "Military", "Media", "Energy"],
        "risk_multiplier": 1.5,
    },
    "RANSOMWARE-X": {
        "aliases": ["LockBit Affiliate", "RaaS-Operator"],
        "origin": "Eastern Europe (suspected)",
        "motivation": "经济勒索",
        "typical_ttps": ["T1486 Data Encryption", "T1490 Inhibit Recovery", "T1071 C2"],
        "target_sectors": ["Healthcare", "Manufacturing", "Finance"],
        "risk_multiplier": 1.3,
    },
    "MIRAI-VARIANT": {
        "aliases": ["Mirai Botnet", "IoT Botnet"],
        "origin": "Distributed",
        "motivation": "DDoS / 加密挖矿",
        "typical_ttps": ["T1498 DDoS", "T1496 Cryptomining"],
        "target_sectors": ["IoT", "ISP", "Small Business"],
        "risk_multiplier": 0.8,
    },
}


# ============================================================
# 向量化工具（字符 n-gram）
# ============================================================

def char_ngrams(text: str, n: int = 3) -> Counter:
    """提取字符级 n-gram 频率向量"""
    text = text.lower().strip()
    if len(text) < n:
        return Counter({text: 1})
    return Counter(text[i:i+n] for i in range(len(text) - n + 1))


def cosine_similarity(vec_a: Counter, vec_b: Counter) -> float:
    """计算两个 Counter 向量的余弦相似度"""
    if not vec_a or not vec_b:
        return 0.0

    # 共有键
    common_keys = set(vec_a.keys()) & set(vec_b.keys())
    if not common_keys:
        return 0.0

    dot_product = sum(vec_a[k] * vec_b[k] for k in common_keys)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def ip_to_subnet(ip_str: str, prefix_len: int = 24) -> Optional[str]:
    """将 IP 转换为子网前缀"""
    try:
        network = ipaddress.ip_network(f"{ip_str}/{prefix_len}", strict=False)
        return str(network)
    except (ValueError, TypeError):
        return None


def parse_network(value: str) -> Optional[ipaddress._BaseNetwork]:
    """解析显式给定的 CIDR 范围；没有显式范围就不做网段泛化。"""
    try:
        return ipaddress.ip_network(str(value).strip(), strict=False)
    except (ValueError, TypeError):
        return None


def domain_suffixes(domain: str) -> list[str]:
    """提取域名的所有后缀层级"""
    parts = domain.lower().strip().split(".")
    suffixes = []
    for i in range(len(parts)):
        suffixes.append(".".join(parts[i:]))
    return suffixes


# ============================================================
# 核心引擎
# ============================================================

class RealThreatIntelEngine:
    """
    T4: 真实威胁情报查询引擎

    三层匹配策略：
    Layer 1: 精确匹配（O(1) 哈希表）
    Layer 2: 网络匹配（IP 子网 / 域名后缀）
    Layer 3: 模糊匹配（字符 n-gram 余弦相似度）
    """

    def __init__(self, ioc_database: dict, similarity_threshold: float = 0.6):
        """
        Args:
            ioc_database: IOC 数据库 {malicious_ips, malicious_domains, malicious_hashes, c2_signatures}
            similarity_threshold: 模糊匹配最低相似度阈值
        """
        self.similarity_threshold = similarity_threshold

        # Layer 1: 精确匹配索引
        self._exact_ip = {}
        self._exact_domain = {}
        self._exact_hash = {}

        # Layer 2: 网络匹配索引
        self._subnet_index = {}     # 显式威胁网段 → [records]
        self._domain_suffix = {}    # 已知恶意域名（用于子域匹配）→ [records]

        # Layer 3: 向量索引
        self._vectors = []  # [(indicator, ngram_vector, record)]

        # C2 签名库
        self._c2_signatures = []

        # 构建索引
        self._build_indexes(ioc_database)

    def _build_indexes(self, db: dict):
        """从 IOC 数据库构建三层索引"""
        # IP
        for record in db.get("malicious_ips", []):
            ip = str(record.get("ip", "")).strip()
            if not ip:
                continue
            enriched = {**record, "_ioc_type": "ip"}
            self._exact_ip[ip] = enriched

            # 只有情报源显式给出 CIDR 时，才允许网段级关联，避免 /24 邻居误伤
            subnet = record.get("cidr") or record.get("subnet")
            parsed_subnet = parse_network(subnet) if subnet else None
            if parsed_subnet:
                self._subnet_index.setdefault(str(parsed_subnet), []).append(enriched)

            # 向量索引
            text = f"{ip} {record.get('threat_type','')} {record.get('actor','')} {record.get('country','')}"
            self._vectors.append((ip, char_ngrams(text), enriched))

        # Domain
        for record in db.get("malicious_domains", []):
            domain = str(record.get("domain", "")).strip().lower()
            if not domain:
                continue
            enriched = {**record, "_ioc_type": "domain"}
            self._exact_domain[domain] = enriched

            # 只保留完整恶意域名作为“可被子域继承”的根，避免 example.com 级泛匹配
            self._domain_suffix.setdefault(domain, []).append(enriched)

            text = f"{domain} {record.get('threat_type','')} {record.get('confidence','')}"
            self._vectors.append((domain, char_ngrams(text), enriched))

        # Hash
        for record in db.get("malicious_hashes", []):
            h = str(record.get("hash", "")).strip().lower()
            if not h:
                continue
            enriched = {**record, "_ioc_type": "hash"}
            self._exact_hash[h] = enriched
            self._vectors.append((h, char_ngrams(h), enriched))

        # C2 signatures
        self._c2_signatures = db.get("c2_signatures", [])

    def lookup(self, indicator: str) -> IntelReport:
        """
        查询单个 IOC 指标

        按优先级依次尝试：精确匹配 → 网络匹配 → 模糊匹配
        """
        start = time.monotonic()
        indicator = str(indicator).strip()
        indicator_lower = indicator.lower()
        matches = []

        # ---- Layer 1: 精确匹配 ----
        exact = (
            self._exact_ip.get(indicator)
            or self._exact_domain.get(indicator_lower)
            or self._exact_hash.get(indicator_lower)
        )
        if exact:
            matches.append(self._build_match(indicator, exact, "exact", 1.0))

        # ---- Layer 2: 网络匹配（仅当无精确命中时）----
        if not matches:
            # IP 子网匹配
            try:
                query_ip = ipaddress.ip_address(indicator)
            except ValueError:
                query_ip = None

            if query_ip:
                for subnet_str, records in self._subnet_index.items():
                    try:
                        if query_ip in ipaddress.ip_network(subnet_str, strict=False):
                            for record in records[:3]:
                                matches.append(self._build_match(indicator, record, "subnet", 0.65))
                    except ValueError:
                        continue

            # 域名后缀匹配
            if "." in indicator_lower:
                for suffix in domain_suffixes(indicator_lower):
                    if suffix in self._domain_suffix and suffix != indicator_lower:
                        for record in self._domain_suffix[suffix][:2]:
                            matches.append(self._build_match(indicator, record, "suffix", 0.6))
                        break  # 只取最长匹配后缀

        # ---- Layer 3: 模糊匹配（仅当前两层无结果时）----
        if not matches:
            query_vec = char_ngrams(indicator_lower)
            scored = []
            for stored_indicator, stored_vec, record in self._vectors:
                sim = cosine_similarity(query_vec, stored_vec)
                if sim >= self.similarity_threshold:
                    scored.append((sim, stored_indicator, record))

            scored.sort(key=lambda x: x[0], reverse=True)
            for sim, stored_ind, record in scored[:3]:  # Top-3
                matches.append(self._build_match(indicator, record, "similar", round(sim, 3)))

        # ---- 汇总报告 ----
        has_exact = any(m.match_type == "exact" for m in matches)
        has_apt = any(m.actor in APT_PROFILES for m in matches)

        # 威胁等级判定
        if matches:
            max_conf = max(m.confidence * m.match_score for m in matches)
            if max_conf >= 0.9 and has_apt:
                threat_level = "CRITICAL"
            elif max_conf >= 0.7:
                threat_level = "HIGH"
            elif max_conf >= 0.4:
                threat_level = "MEDIUM"
            else:
                threat_level = "LOW"
        else:
            threat_level = "CLEAN"

        # 关联 IOC 检索（从匹配到的 actor 反向查找其他 IOC）
        related = []
        if has_apt:
            actor = next((m.actor for m in matches if m.actor in APT_PROFILES), None)
            if actor:
                related = self._find_related_by_actor(actor, indicator)

        elapsed = (time.monotonic() - start) * 1000

        return IntelReport(
            query_indicator=indicator,
            matches=matches,
            has_exact_match=has_exact,
            has_apt_association=has_apt,
            overall_threat_level=threat_level,
            lookup_time_ms=round(elapsed, 3),
            related_iocs=related,
        )

    def lookup_batch(self, indicators: list[str]) -> list[IntelReport]:
        """批量查询多个 IOC"""
        unique = []
        seen = set()
        for ind in indicators:
            normalized = str(ind).strip().lower()
            if normalized in seen:
                continue
            seen.add(normalized)
            unique.append(ind)
        return [self.lookup(ind) for ind in unique]

    def check_c2_signature(self, pattern_description: str) -> Optional[dict]:
        """检查是否匹配已知 C2 通信特征"""
        desc_lower = pattern_description.lower()
        for sig in self._c2_signatures:
            sig_pattern = sig.get("pattern", "").lower()
            # 特征关键词匹配
            keywords = [kw.strip() for kw in sig_pattern.split(",")]
            matched_count = sum(1 for kw in keywords if kw in desc_lower)
            if matched_count >= len(keywords) * 0.5:  # 50% 关键词命中
                return {
                    "matched_signature": sig,
                    "match_ratio": matched_count / len(keywords),
                    "family": sig.get("family", "Unknown"),
                    "confidence": sig.get("confidence", 0.5),
                }
        return None

    def get_actor_profile(self, actor_name: str) -> Optional[dict]:
        """获取 APT 组织详细画像"""
        return APT_PROFILES.get(actor_name)

    def get_stats(self) -> dict:
        """返回情报库统计信息"""
        return {
            "total_ips": len(self._exact_ip),
            "total_domains": len(self._exact_domain),
            "total_hashes": len(self._exact_hash),
            "total_c2_signatures": len(self._c2_signatures),
            "total_vectors": len(self._vectors),
            "subnet_prefixes": len(self._subnet_index),
            "domain_suffixes": len(self._domain_suffix),
        }

    # ---- 内部方法 ----

    def _build_match(self, query: str, record: dict, match_type: str, score: float) -> IntelMatch:
        """构建标准化匹配结果"""
        actor = record.get("actor", record.get("family", "Unknown"))
        profile = APT_PROFILES.get(actor, {})

        return IntelMatch(
            indicator=record.get("ip", record.get("domain", record.get("hash", query))),
            match_type=match_type,
            ioc_type=record.get("_ioc_type", "unknown"),
            threat_type=record.get("threat_type", "Unknown"),
            actor=actor,
            confidence=float(record.get("confidence", 0.5)),
            match_score=score,
            country=record.get("country", ""),
            first_seen=record.get("first_seen", ""),
            last_seen=record.get("last_seen", ""),
            tags=record.get("tags", []),
            related_campaigns=profile.get("target_sectors", []),
            mitre_techniques=profile.get("typical_ttps", []),
            raw_record=record,
        )

    def _find_related_by_actor(self, actor: str, exclude_indicator: str) -> list[dict]:
        """根据 APT 组织反向查找关联 IOC"""
        related = []
        exclude_lower = exclude_indicator.lower().strip()

        for ip, record in self._exact_ip.items():
            if record.get("actor") == actor and ip != exclude_lower:
                related.append({"type": "ip", "indicator": ip, "threat_type": record.get("threat_type")})

        for domain, record in self._exact_domain.items():
            if record.get("actor") == actor and domain != exclude_lower:
                related.append({"type": "domain", "indicator": domain, "threat_type": record.get("threat_type")})

        return related[:10]  # 最多返回 10 条关联
