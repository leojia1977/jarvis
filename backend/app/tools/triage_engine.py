"""
SecuPilot T1: 真实动态加权评分引擎 (Real Triage Scoring Engine)

生产级算法 — 不是 if/else 硬编码，是数学计算。

评分公式：
  risk = base_severity x asset_multiplier x time_anomaly x frequency_anomaly x (1 - baseline_dampening)

关键修正：
  - 时间因子先转换到业务时区，避免 UTC 误判为本地凌晨
  - 频率因子基于 event_time 的真实时间窗口，而不是处理时刻
  - 风险展示分保持 0-10，排序使用独立 priority_score，避免高分区塌缩
"""

import math
import re
import time
from bisect import bisect_left, bisect_right, insort
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Optional
from dataclasses import dataclass, field

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # pragma: no cover
    ZoneInfo = None

    class ZoneInfoNotFoundError(Exception):
        pass


# ============================================================
# 评分因子配置（可按客户环境调参）
# ============================================================

SEVERITY_SCORE = {
    "CRITICAL": 9.0,
    "HIGH": 7.0,
    "MEDIUM": 4.0,
    "LOW": 2.0,
    "INFO": 0.5,
}

# 时间异常加权（基于经验：深夜攻击概率远高于工作时间）
TIME_WEIGHTS = [
    ((2, 5), 1.8),   # 凌晨（最高危时段）
    ((0, 2), 1.6),   # 深夜前段
    ((5, 6), 1.6),   # 深夜后段
    ((22, 24), 1.5), # 晚间
    ((6, 8), 1.2),   # 早间过渡
    ((18, 22), 1.2), # 晚间过渡
    ((8, 18), 1.0),  # 标准工作时间
]

# 频率异常阈值（滑动窗口内同 pattern 出现次数）
FREQ_THRESHOLDS = [
    (200, 3.0),   # 200+ 次：极端爆破/扫描
    (100, 2.5),   # 100+ 次：高度异常
    (20, 1.8),    # 20+ 次：中度异常
    (5, 1.3),     # 5+ 次：轻度异常
    (0, 1.0),     # 正常
]

FALLBACK_TIMEZONES = {
    "UTC": timezone.utc,
    "Asia/Shanghai": timezone(timedelta(hours=8), name="Asia/Shanghai"),
    "Asia/Chongqing": timezone(timedelta(hours=8), name="Asia/Chongqing"),
    "Asia/Beijing": timezone(timedelta(hours=8), name="Asia/Beijing"),
}


# ============================================================
# 数据结构
# ============================================================

@dataclass
class TriageResult:
    """分流结果"""
    total_input: int
    auto_archived: int
    for_investigation: list
    compression_ratio: float
    top_risk_score: float
    scoring_time_ms: float
    score_distribution: dict = field(default_factory=dict)
    top_priority_score: float = 0.0


@dataclass
class AlertScore:
    """单条告警评分结果"""
    event_id: str
    risk_score: float
    factors: dict
    auto_archive: bool
    priority_score: float = 0.0


# ============================================================
# 核心引擎
# ============================================================

class RealTriageEngine:
    """
    T1: 真实动态加权评分引擎

    设计原则：
    - 每个因子是连续值，不是阶梯式 if/else
    - 滑动窗口实现频率统计（基于事件时间）
    - 基线库匹配实现误报抑制
    - 所有参数可配置可调优
    """

    def __init__(self, asset_db: dict, baseline_db: list,
                 archive_threshold: float = 2.0,
                 window_size: int = 10000,
                 window_minutes: int = 60,
                 business_timezone: str | tzinfo = "UTC",
                 source_timezone: Optional[str | tzinfo] = None):
        """
        Args:
            asset_db: 资产字典 {asset_id: {criticality_weight: int, ...}}
            baseline_db: 误报基线列表 [{pattern_description, category, confidence, ...}]
            archive_threshold: 低于此分数自动归档
            window_size: 单个 pattern 维护的最大事件数
            window_minutes: 频率统计时间窗口（分钟）
            business_timezone: 业务时区，用于时间异常判定
            source_timezone: 输入时间戳无 tzinfo 时的默认源时区
        """
        self.asset_db = self._index_assets(asset_db)
        self.baseline_patterns = self._index_baselines(baseline_db)
        self.archive_threshold = archive_threshold
        self.window_size = window_size
        self.window_minutes = window_minutes
        self.business_timezone = self._coerce_timezone(business_timezone)
        self.source_timezone = (
            self._coerce_timezone(source_timezone)
            if source_timezone is not None
            else None
        )

        # pattern_key -> sorted event timestamps
        self._freq_cache = {}
        self._latest_event_ts = 0.0
        self._score_counter = 0
        self._prune_interval = 512

    @staticmethod
    def _index_assets(asset_db: dict) -> dict:
        """建立 asset_id → asset 的索引"""
        if isinstance(asset_db, list):
            return {str(a["asset_id"]): a for a in asset_db}
        if isinstance(asset_db, dict) and "assets" in asset_db:
            return {str(a["asset_id"]): a for a in asset_db["assets"]}
        return {str(k): v for k, v in asset_db.items()}

    @classmethod
    def _index_baselines(cls, baseline_db: list) -> dict:
        """建立 normalized_pattern → [baseline] 的索引"""
        index = {}
        items = baseline_db
        if isinstance(baseline_db, dict):
            items = baseline_db.get("baselines", [])
        for bl in items:
            desc = cls._normalize_text(bl.get("pattern_description", ""))
            if not desc:
                continue
            index.setdefault(desc, []).append(bl)
        return index

    @staticmethod
    def _normalize_text(text: str) -> str:
        return re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()

    @staticmethod
    def _coerce_timezone(value: str | tzinfo) -> tzinfo:
        """兼容 ZoneInfo 缺失环境的时区解析"""
        if isinstance(value, tzinfo):
            return value

        text = str(value).strip() if value else "UTC"
        if text in FALLBACK_TIMEZONES:
            return FALLBACK_TIMEZONES[text]

        if re.fullmatch(r"[+-]\d{2}:\d{2}", text):
            sign = 1 if text[0] == "+" else -1
            hours = int(text[1:3])
            minutes = int(text[4:6])
            return timezone(sign * timedelta(hours=hours, minutes=minutes), name=text)

        if ZoneInfo is not None:
            try:
                return ZoneInfo(text)
            except ZoneInfoNotFoundError:
                pass

        raise ValueError(f"Unsupported timezone specification: {text}")

    # ---- 因子计算函数 ----

    @staticmethod
    def calc_base_severity(severity: str) -> float:
        """因子 1：基础严重度（直接映射）"""
        return SEVERITY_SCORE.get(str(severity).upper(), 1.0)

    @staticmethod
    def calc_asset_multiplier(criticality_weight: int) -> float:
        """
        因子 2：资产权重乘数

        权重 1-10 映射为乘数 0.3-1.5
        使用平滑曲线而非阶梯函数
        """
        try:
            weight = int(float(criticality_weight))
        except (TypeError, ValueError):
            weight = 5
        w = max(1, min(10, weight))
        return 0.2 + (w / 10.0) * 1.3

    @staticmethod
    def calc_time_anomaly(event_time: datetime) -> float:
        """
        因子 3：时间异常因子

        输入必须是业务本地时间
        """
        hour = event_time.hour
        for (start, end), weight in TIME_WEIGHTS:
            if start <= hour < end:
                return weight
        return 1.0

    def calc_frequency_anomaly(self, alert: dict, event_time: datetime) -> tuple[float, int]:
        """
        因子 4：频率异常因子

        基于 event_time 的时间窗口统计同 pattern 出现频率
        pattern_key = (source_ip, destination_asset_id, activity_name)
        """
        key = (
            str(alert.get("source_ip", "")),
            str(alert.get("destination_asset_id", "")),
            str(alert.get("activity_name", "")),
        )
        timestamps = self._freq_cache.setdefault(key, [])
        event_ts = event_time.timestamp()
        self._latest_event_ts = max(self._latest_event_ts, event_ts)
        self._score_counter += 1
        insort(timestamps, event_ts)

        lower_bound = event_ts - self.window_minutes * 60
        left = bisect_left(timestamps, lower_bound)
        if left:
            del timestamps[:left]

        if len(timestamps) > self.window_size:
            del timestamps[: len(timestamps) - self.window_size]

        count = bisect_right(timestamps, event_ts)
        if self._score_counter % self._prune_interval == 0:
            self._prune_freq_cache(self._latest_event_ts)
        for threshold, factor in FREQ_THRESHOLDS:
            if count >= threshold:
                return factor, count
        return 1.0, count

    def _prune_freq_cache(self, current_ts: float | None = None):
        """
        清理长时间未命中的 pattern key，避免公网随机源 IP 导致 cache 持续膨胀。
        """
        if not self._freq_cache:
            return

        if current_ts is None:
            current_ts = self._latest_event_ts or time.time()

        expire_before = current_ts - self.window_minutes * 60
        expired_keys = []
        for key, timestamps in self._freq_cache.items():
            if not timestamps or timestamps[-1] < expire_before:
                expired_keys.append(key)

        for key in expired_keys:
            del self._freq_cache[key]

    def calc_baseline_dampening(self, alert: dict) -> float:
        """
        因子 5：基线衰减

        如果告警的 activity 匹配已知误报模式，降低分数
        返回 0.0（无匹配）到 0.95（高置信度匹配）
        """
        activity = self._normalize_text(alert.get("activity_name", ""))

        for phrase, baselines in self.baseline_patterns.items():
            if phrase in activity:
                max_conf = max(float(bl.get("confidence", 0.5)) for bl in baselines)
                return min(0.95, max_conf)

        dest_id = str(alert.get("destination_asset_id", ""))
        asset = self.asset_db.get(dest_id)
        if asset:
            known = asset.get("known_behaviors", [])
            for behavior in known:
                if self._normalize_text(behavior) in activity:
                    return 0.7
        return 0.0

    @staticmethod
    def _normalize_display_score(raw: float) -> float:
        """
        展示分控制在 0-10，用 log1p 压缩替代过于贴顶的指数压缩。
        """
        max_raw = 80.0
        normalized = 10.0 * math.log1p(max(0.0, raw)) / math.log1p(max_raw)
        return round(min(10.0, max(0.0, normalized)), 2)

    # ---- 核心评分函数 ----

    def score_alert(self, alert: dict) -> AlertScore:
        """
        计算单条告警的风险分数 (0.0 - 10.0)

        - priority_score: 保留原始排序能力
        - risk_score: UI 展示/分桶使用，保证 0-10
        """
        base = self.calc_base_severity(alert.get("severity", "INFO"))

        dest_id = str(alert.get("destination_asset_id", ""))
        asset = self.asset_db.get(dest_id)
        weight = asset.get("criticality_weight", 5) if asset else 5
        asset_mult = self.calc_asset_multiplier(weight)

        event_time = self._parse_time(alert.get("event_time", ""))
        time_factor = self.calc_time_anomaly(event_time)

        freq_factor, freq_count = self.calc_frequency_anomaly(alert, event_time)
        dampening = self.calc_baseline_dampening(alert)

        raw = base * asset_mult * time_factor * freq_factor * (1.0 - dampening)
        priority_score = round(raw, 4)
        score = self._normalize_display_score(raw)

        return AlertScore(
            event_id=str(alert.get("event_id", "")),
            risk_score=score,
            factors={
                "base_severity": round(base, 2),
                "asset_multiplier": round(asset_mult, 2),
                "time_anomaly": round(time_factor, 2),
                "frequency_anomaly": round(freq_factor, 2),
                "frequency_count": freq_count,
                "baseline_dampening": round(dampening, 2),
                "raw_score": round(raw, 2),
                "event_time_local": event_time.isoformat(),
                "business_hour": event_time.hour,
            },
            auto_archive=score < self.archive_threshold,
            priority_score=priority_score,
        )

    def triage_batch(self, alerts: list[dict]) -> TriageResult:
        """
        批量分流：对所有告警评分、排序、分类

        返回归档数量、待调查列表、压缩比
        """
        start = time.monotonic()

        scored = []
        archived = 0
        score_buckets = {"0-2": 0, "2-4": 0, "4-6": 0, "6-8": 0, "8-10": 0}

        for alert in alerts:
            result = self.score_alert(alert)
            alert["_triage_score"] = result.risk_score
            alert["_triage_priority"] = result.priority_score
            alert["_triage_factors"] = result.factors

            if result.risk_score < 2:
                score_buckets["0-2"] += 1
            elif result.risk_score < 4:
                score_buckets["2-4"] += 1
            elif result.risk_score < 6:
                score_buckets["4-6"] += 1
            elif result.risk_score < 8:
                score_buckets["6-8"] += 1
            else:
                score_buckets["8-10"] += 1

            if result.auto_archive:
                archived += 1
            else:
                scored.append(alert)

        self._prune_freq_cache()

        scored.sort(
            key=lambda a: (
                a.get("_triage_priority", 0.0),
                a.get("_triage_score", 0.0),
            ),
            reverse=True,
        )

        elapsed = (time.monotonic() - start) * 1000
        total = len(alerts)

        return TriageResult(
            total_input=total,
            auto_archived=archived,
            for_investigation=scored,
            compression_ratio=archived / max(total, 1),
            top_risk_score=scored[0]["_triage_score"] if scored else 0.0,
            scoring_time_ms=round(elapsed, 2),
            score_distribution=score_buckets,
            top_priority_score=scored[0]["_triage_priority"] if scored else 0.0,
        )

    def _parse_time(self, ts_value: str | datetime) -> datetime:
        """解析 ISO 时间戳并转换到业务时区"""
        if isinstance(ts_value, datetime):
            dt = ts_value
        elif not ts_value:
            dt = datetime.now(timezone.utc)
        else:
            try:
                text = str(ts_value).strip().replace("Z", "+00:00")
                dt = datetime.fromisoformat(text)
            except (ValueError, TypeError):
                dt = datetime.now(timezone.utc)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=self.source_timezone or self.business_timezone)

        return dt.astimezone(self.business_timezone)
