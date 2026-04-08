"""
SecuPilot Mock SIEM Integration Adapter
模拟 Splunk/Elastic 查询接口，统一返回 OCSF 格式

正式部署时替换为真实 SIEM API 集成
"""

import json
from pathlib import Path
from typing import Optional

try:
    import structlog
    logger = structlog.get_logger()
except ImportError:
    import logging
    logger = logging.getLogger("secupilot.siem_adapter")

from app.config import settings

MOCK_DIR = Path(settings.mock_data_path)


class MockSIEMAdapter:
    """Mock SIEM Integration Adapter"""

    def __init__(self):
        self._cache = {}
        self._load_data()

    def _load_data(self):
        """预加载所有 Mock 数据到内存"""
        try:
            with open(MOCK_DIR / "siem_adapter" / "mock_splunk_responses.json", "r") as f:
                self._cache["siem_responses"] = json.load(f)
            with open(MOCK_DIR / "assets" / "asset_dictionary.json", "r") as f:
                self._cache["assets"] = json.load(f)
            with open(MOCK_DIR / "threat_intel" / "mock_ioc_database.json", "r") as f:
                self._cache["ioc"] = json.load(f)
            with open(MOCK_DIR / "knowledge_graph" / "entity_relationships.json", "r") as f:
                self._cache["knowledge_graph"] = json.load(f)
            with open(MOCK_DIR / "baselines" / "false_positive_baseline.json", "r") as f:
                self._cache["baselines"] = json.load(f)

            # 加载所有场景告警
            self._cache["scenarios"] = {}
            alerts_dir = MOCK_DIR / "alerts"
            for f in alerts_dir.glob("scenario_*.json"):
                with open(f, "r") as fh:
                    data = json.load(fh)
                    sid = data.get("scenario", {}).get("scenario_id", f.stem)
                    self._cache["scenarios"][sid] = data

            logger.info("Mock SIEM data loaded", scenarios=len(self._cache["scenarios"]))
        except Exception as e:
            logger.error("Failed to load mock data", error=str(e))

    async def query_recent_summary(self, hours: int = 12) -> dict:
        """查询最近 N 小时的态势汇总"""
        responses = self._cache.get("siem_responses", {})
        return responses.get("queries", {}).get("summarize_recent_12h", {}).get("response", {})

    async def query_asset_alerts(self, asset_id: str, time_range: str = "24h") -> list:
        """查询指定资产的相关告警"""
        results = []
        for sid, scenario_data in self._cache.get("scenarios", {}).items():
            for alert in scenario_data.get("alerts", []):
                if alert.get("destination_asset_id") == asset_id:
                    results.append(alert)
        return results

    async def query_scenario(self, scenario_id: str) -> Optional[dict]:
        """获取完整攻击场景数据"""
        return self._cache.get("scenarios", {}).get(scenario_id)

    async def get_asset_context(self, asset_id: str) -> Optional[dict]:
        """查询资产上下文"""
        assets = self._cache.get("assets", {}).get("assets", [])
        for asset in assets:
            if asset["asset_id"] == asset_id:
                return asset
        return None

    async def search_ioc(self, indicator: str) -> Optional[dict]:
        """查询 IOC 威胁情报"""
        ioc_db = self._cache.get("ioc", {})
        # 搜索 IP
        for ip_record in ioc_db.get("malicious_ips", []):
            if ip_record["ip"] == indicator:
                return {"type": "ip", "match": ip_record}
        # 搜索域名
        for domain_record in ioc_db.get("malicious_domains", []):
            if domain_record["domain"] == indicator:
                return {"type": "domain", "match": domain_record}
        # 搜索 Hash
        for hash_record in ioc_db.get("malicious_hashes", []):
            if hash_record["hash"] == indicator:
                return {"type": "hash", "match": hash_record}
        return None

    async def check_baseline(self, activity_name: str) -> bool:
        """检查是否命中误报基线"""
        baselines = self._cache.get("baselines", {}).get("baselines", [])
        for bl in baselines:
            if activity_name.lower() in bl.get("pattern_description", "").lower():
                return True
        return False

    async def get_knowledge_graph(self) -> dict:
        """获取知识图谱数据"""
        return self._cache.get("knowledge_graph", {})
