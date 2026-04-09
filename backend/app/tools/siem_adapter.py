"""
SecuPilot SIEM Adapter Contract + Mock Implementation

S3-C-0 目标：
- 冻结 orchestrator 与 SIEM/EDR 之间的最小契约
- 统一时间范围表达
- 统一 adapter 状态信封，接入 DEGRADED 语义
"""

from __future__ import annotations

import asyncio
import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Generic, Literal, Optional, Protocol, TypeVar

try:
    import structlog
    logger = structlog.get_logger()
except ImportError:
    import logging
    logger = logging.getLogger("secupilot.siem_adapter")

from app.config import settings


T = TypeVar("T")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_iso_utc(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


@dataclass(frozen=True)
class TimeRangeSpec:
    start_utc: datetime
    end_utc: datetime
    tz_label: str = "UTC"

    @classmethod
    def from_value(
        cls,
        value: "TimeRangeSpec | str | int | float | None",
        tz_label: str = "UTC",
        now: Optional[datetime] = None,
    ) -> "TimeRangeSpec":
        if isinstance(value, cls):
            return value

        now_utc = (now or _utc_now()).astimezone(timezone.utc)
        delta = timedelta(hours=24)

        if isinstance(value, (int, float)):
            delta = timedelta(hours=max(float(value), 0.0))
        elif isinstance(value, str):
            token = value.strip().lower() or "24h"
            match = re.fullmatch(r"(\d+)\s*([mhd])", token)
            if match:
                amount = int(match.group(1))
                unit = match.group(2)
                if unit == "m":
                    delta = timedelta(minutes=amount)
                elif unit == "h":
                    delta = timedelta(hours=amount)
                elif unit == "d":
                    delta = timedelta(days=amount)
            else:
                logger.warning("Unrecognized time_range, falling back to 24h", value=value)

        return cls(
            start_utc=now_utc - delta,
            end_utc=now_utc,
            tz_label=tz_label or "UTC",
        )

    def contains(self, timestamp: Optional[datetime]) -> bool:
        if timestamp is None:
            return True
        return self.start_utc <= timestamp <= self.end_utc


@dataclass
class AdapterResult(Generic[T]):
    status: Literal["ok", "timeout", "partial", "unavailable"]
    data: T
    latency_ms: float = 0.0
    gap_reason: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def ok(
        cls,
        data: T,
        *,
        latency_ms: float = 0.0,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "AdapterResult[T]":
        return cls("ok", data, latency_ms=latency_ms, metadata=metadata or {})

    @classmethod
    def partial(
        cls,
        data: T,
        *,
        gap_reason: str,
        latency_ms: float = 0.0,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "AdapterResult[T]":
        return cls("partial", data, latency_ms=latency_ms, gap_reason=gap_reason, metadata=metadata or {})

    @classmethod
    def timeout(
        cls,
        data: T,
        *,
        gap_reason: str = "adapter_timeout",
        latency_ms: float = 0.0,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "AdapterResult[T]":
        return cls("timeout", data, latency_ms=latency_ms, gap_reason=gap_reason, metadata=metadata or {})

    @classmethod
    def unavailable(
        cls,
        data: T,
        *,
        gap_reason: str,
        latency_ms: float = 0.0,
        metadata: Optional[dict[str, Any]] = None,
    ) -> "AdapterResult[T]":
        return cls("unavailable", data, latency_ms=latency_ms, gap_reason=gap_reason, metadata=metadata or {})


class SIEMAdapterProtocol(Protocol):
    async def query_recent_summary(self, time_range: TimeRangeSpec) -> AdapterResult[dict]:
        ...

    async def query_asset_alerts(self, asset_id: str, time_range: TimeRangeSpec) -> AdapterResult[list]:
        ...

    async def query_intent_alerts(
        self,
        intent: str,
        user_input: str,
        time_range: TimeRangeSpec,
    ) -> AdapterResult[list]:
        ...

    async def get_scenario_metadata(self, scenario_id: str) -> AdapterResult[Optional[dict]]:
        ...

    async def get_asset_context(self, asset_id: str) -> AdapterResult[Optional[dict]]:
        ...

    def get_runtime_stats(self) -> dict[str, int]:
        ...


class ProductionSIEMTransportProtocol(Protocol):
    async def post_json(
        self,
        endpoint: str,
        payload: dict[str, Any],
        *,
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]:
        ...


class UrllibSIEMTransport:
    async def post_json(
        self,
        endpoint: str,
        payload: dict[str, Any],
        *,
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]:
        return await asyncio.to_thread(
            self._post_json_sync,
            endpoint,
            payload,
            headers,
            timeout_seconds,
        )

    @staticmethod
    def _post_json_sync(
        endpoint: str,
        payload: dict[str, Any],
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]:
        request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json", **headers},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
        return json.loads(body or "{}")


class MockSIEMAdapter:
    """Mock SIEM Integration Adapter"""

    def __init__(self, data_root: Optional[Path] = None):
        self._cache: dict[str, Any] = {}
        self.data_root = Path(data_root).resolve() if data_root else settings.get_mock_data_dir()
        self._load_data()

    def _load_data(self) -> None:
        """预加载所有 Mock 数据到内存"""
        try:
            with open(self.data_root / "siem_adapter" / "mock_splunk_responses.json", "r", encoding="utf-8") as f:
                self._cache["siem_responses"] = json.load(f)
            with open(self.data_root / "assets" / "asset_dictionary.json", "r", encoding="utf-8") as f:
                self._cache["assets"] = json.load(f)
            with open(self.data_root / "threat_intel" / "mock_ioc_database.json", "r", encoding="utf-8") as f:
                self._cache["ioc"] = json.load(f)
            with open(self.data_root / "knowledge_graph" / "entity_relationships.json", "r", encoding="utf-8") as f:
                self._cache["knowledge_graph"] = json.load(f)
            with open(self.data_root / "baselines" / "false_positive_baseline.json", "r", encoding="utf-8") as f:
                self._cache["baselines"] = json.load(f)

            self._cache["scenarios"] = {}
            alerts_dir = self.data_root / "alerts"
            for file_path in alerts_dir.glob("scenario_*.json"):
                with open(file_path, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                    sid = data.get("scenario", {}).get("scenario_id", file_path.stem)
                    self._cache["scenarios"][sid] = data

            logger.info(
                "Mock SIEM data loaded",
                root=str(self.data_root),
                scenarios=len(self._cache["scenarios"]),
            )
        except Exception as exc:
            logger.error("Failed to load mock data", error=str(exc))

    def _all_alerts(self) -> list[dict]:
        alerts: list[dict] = []
        for scenario_data in self._cache.get("scenarios", {}).values():
            alerts.extend(scenario_data.get("alerts", []))
        return alerts

    @staticmethod
    def _filter_alerts_by_time(alerts: list[dict], time_range: TimeRangeSpec) -> list[dict]:
        filtered = []
        for alert in alerts:
            alert_ts = _parse_iso_utc(alert.get("event_time", ""))
            if time_range.contains(alert_ts):
                filtered.append(alert)
        return filtered

    async def query_recent_summary(self, time_range: TimeRangeSpec) -> AdapterResult[dict]:
        started = time.monotonic()
        responses = self._cache.get("siem_responses", {})
        summary = responses.get("queries", {}).get("summarize_recent_12h", {}).get("response", {})
        alerts = self._filter_alerts_by_time(self._all_alerts(), time_range)
        payload = {
            **summary,
            "alerts_considered": len(alerts),
            "time_range": {
                "start_utc": time_range.start_utc.isoformat(),
                "end_utc": time_range.end_utc.isoformat(),
                "tz_label": time_range.tz_label,
            },
        }
        return AdapterResult.ok(payload, latency_ms=(time.monotonic() - started) * 1000)

    async def query_asset_alerts(self, asset_id: str, time_range: TimeRangeSpec) -> AdapterResult[list]:
        started = time.monotonic()
        results: list[dict] = []
        for scenario_data in self._cache.get("scenarios", {}).values():
            for alert in scenario_data.get("alerts", []):
                if (
                    alert.get("destination_asset_id") == asset_id
                    or alert.get("source_ip") == asset_id
                    or alert.get("destination_ip") == asset_id
                ):
                    results.append(alert)

        filtered = self._filter_alerts_by_time(results, time_range)
        return AdapterResult.ok(filtered, latency_ms=(time.monotonic() - started) * 1000)

    async def query_intent_alerts(
        self,
        intent: str,
        user_input: str,
        time_range: TimeRangeSpec,
    ) -> AdapterResult[list]:
        started = time.monotonic()
        scenarios = self._cache.get("scenarios", {})

        if intent == "summarize_recent":
            alerts = self._filter_alerts_by_time(self._all_alerts(), time_range)
            return AdapterResult.ok(alerts, latency_ms=(time.monotonic() - started) * 1000)

        scenario_map = {
            "横向": "S-02",
            "lateral": "S-02",
            "移动": "S-02",
            "外泄": "S-03",
            "exfil": "S-03",
            "流量": "S-03",
            "勒索": "S-04",
            "ransom": "S-04",
            "c2": "S-04",
            "内部": "S-05",
            "insider": "S-05",
            "ceo": "S-05",
        }
        matched_sid = None
        query = (user_input or "").lower()
        for keyword, scenario_id in scenario_map.items():
            if keyword in query:
                matched_sid = scenario_id
                break

        if not matched_sid:
            matched_sid = "S-03" if intent == "data_exfil_check" else "S-02"

        alerts = scenarios.get(matched_sid, {}).get("alerts", [])
        filtered = self._filter_alerts_by_time(alerts, time_range)
        return AdapterResult.ok(
            filtered,
            latency_ms=(time.monotonic() - started) * 1000,
            metadata={"scenario_id": matched_sid},
        )

    async def get_scenario_metadata(self, scenario_id: str) -> AdapterResult[Optional[dict]]:
        started = time.monotonic()
        metadata = self._cache.get("scenarios", {}).get(scenario_id, {}).get("scenario")
        return AdapterResult.ok(metadata, latency_ms=(time.monotonic() - started) * 1000)

    async def get_asset_context(self, asset_id: str) -> AdapterResult[Optional[dict]]:
        started = time.monotonic()
        assets = self._cache.get("assets", {}).get("assets", [])
        for asset in assets:
            if asset.get("asset_id") == asset_id:
                return AdapterResult.ok(asset, latency_ms=(time.monotonic() - started) * 1000)
        return AdapterResult.ok(None, latency_ms=(time.monotonic() - started) * 1000)

    async def search_ioc(self, indicator: str) -> Optional[dict]:
        # LEGACY: not part of SIEMAdapterProtocol, kept for backward compatibility only.
        ioc_db = self._cache.get("ioc", {})
        for ip_record in ioc_db.get("malicious_ips", []):
            if ip_record["ip"] == indicator:
                return {"type": "ip", "match": ip_record}
        for domain_record in ioc_db.get("malicious_domains", []):
            if domain_record["domain"] == indicator:
                return {"type": "domain", "match": domain_record}
        for hash_record in ioc_db.get("malicious_hashes", []):
            if hash_record["hash"] == indicator:
                return {"type": "hash", "match": hash_record}
        return None

    async def check_baseline(self, activity_name: str) -> bool:
        # LEGACY: not part of SIEMAdapterProtocol, kept for backward compatibility only.
        baselines = self._cache.get("baselines", {}).get("baselines", [])
        for baseline in baselines:
            if activity_name.lower() in baseline.get("pattern_description", "").lower():
                return True
        return False

    async def get_knowledge_graph(self) -> dict:
        # LEGACY: not part of SIEMAdapterProtocol, kept for backward compatibility only.
        return self._cache.get("knowledge_graph", {})

    async def query_scenario(self, scenario_id: str) -> Optional[dict]:
        # LEGACY: not part of SIEMAdapterProtocol, kept for backward compatibility only.
        result = await self.get_scenario_metadata(scenario_id)
        return result.data

    def get_runtime_stats(self) -> dict[str, int]:
        return {
            "scenarios_loaded": len(self._cache.get("scenarios", {})),
            "assets_loaded": len(self._cache.get("assets", {}).get("assets", [])),
        }


class ProductionSIEMAdapter:
    """S3-C-1 第一版：消费运行时配置并规范化真实 SIEM 返回。"""

    def __init__(
        self,
        runtime_settings=settings,
        *,
        transport: Optional[ProductionSIEMTransportProtocol] = None,
    ):
        self.settings = runtime_settings
        self.transport = transport or UrllibSIEMTransport()
        self.base_url = (getattr(runtime_settings, "siem_base_url", "") or "").rstrip("/")
        self.auth_token = getattr(runtime_settings, "siem_auth_token", "") or ""
        self.vendor = getattr(runtime_settings, "siem_vendor", "generic_http")
        self.timeout_seconds = float(getattr(runtime_settings, "siem_request_timeout_seconds", 5.0))
        self._endpoint_map = {
            "recent_summary": "/api/v1/summary/recent",
            "asset_alerts": "/api/v1/alerts/asset",
            "intent_alerts": "/api/v1/alerts/intent",
            "scenario_metadata": "/api/v1/metadata/scenario",
            "asset_context": "/api/v1/metadata/asset",
        }

    def is_configured(self) -> bool:
        return bool(self.base_url and self.auth_token)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.auth_token}",
            "X-SecuPilot-SIEM-Vendor": self.vendor,
        }

    def _endpoint(self, key: str) -> str:
        return f"{self.base_url}{self._endpoint_map[key]}"

    @staticmethod
    def _normalize_status(value: Any) -> Literal["ok", "timeout", "partial", "unavailable"]:
        normalized = str(value or "ok").lower()
        if normalized in {"ok", "timeout", "partial", "unavailable"}:
            return normalized  # type: ignore[return-value]
        return "unavailable"

    async def _post_envelope(
        self,
        endpoint_key: str,
        payload: dict[str, Any],
        *,
        data_keys: tuple[str, ...],
        default_data: T,
    ) -> AdapterResult[T]:
        if not self.is_configured():
            return AdapterResult.unavailable(default_data, gap_reason="production_adapter_not_configured")

        started = time.monotonic()
        try:
            raw = await self.transport.post_json(
                self._endpoint(endpoint_key),
                payload,
                headers=self._headers(),
                timeout_seconds=self.timeout_seconds,
            )
        except TimeoutError:
            return AdapterResult.timeout(default_data, gap_reason="production_transport_timeout")
        except urllib.error.URLError as exc:
            return AdapterResult.unavailable(default_data, gap_reason=f"production_transport_unavailable:{exc.reason}")

        latency_ms = (time.monotonic() - started) * 1000
        status = self._normalize_status(raw.get("status"))
        data = raw.get("data")
        if data is None:
            for key in data_keys:
                if key in raw:
                    data = raw.get(key)
                    break
        if data is None:
            data = default_data

        gap_reason = raw.get("gap_reason")
        metadata = raw.get("metadata") or {}
        return AdapterResult(
            status=status,
            data=data,
            latency_ms=latency_ms,
            gap_reason=gap_reason,
            metadata=metadata,
        )

    async def query_recent_summary(self, time_range: TimeRangeSpec) -> AdapterResult[dict]:
        return await self._post_envelope(
            "recent_summary",
            {
                "time_range": {
                    "start_utc": time_range.start_utc.isoformat(),
                    "end_utc": time_range.end_utc.isoformat(),
                    "tz_label": time_range.tz_label,
                }
            },
            data_keys=("summary",),
            default_data={},
        )

    async def query_asset_alerts(self, asset_id: str, time_range: TimeRangeSpec) -> AdapterResult[list]:
        return await self._post_envelope(
            "asset_alerts",
            {
                "asset_id": asset_id,
                "time_range": {
                    "start_utc": time_range.start_utc.isoformat(),
                    "end_utc": time_range.end_utc.isoformat(),
                    "tz_label": time_range.tz_label,
                },
            },
            data_keys=("alerts",),
            default_data=[],
        )

    async def query_intent_alerts(
        self,
        intent: str,
        user_input: str,
        time_range: TimeRangeSpec,
    ) -> AdapterResult[list]:
        return await self._post_envelope(
            "intent_alerts",
            {
                "intent": intent,
                "user_input": user_input,
                "time_range": {
                    "start_utc": time_range.start_utc.isoformat(),
                    "end_utc": time_range.end_utc.isoformat(),
                    "tz_label": time_range.tz_label,
                },
            },
            data_keys=("alerts",),
            default_data=[],
        )

    async def get_scenario_metadata(self, scenario_id: str) -> AdapterResult[Optional[dict]]:
        return await self._post_envelope(
            "scenario_metadata",
            {"scenario_id": scenario_id},
            data_keys=("scenario",),
            default_data=None,
        )

    async def get_asset_context(self, asset_id: str) -> AdapterResult[Optional[dict]]:
        return await self._post_envelope(
            "asset_context",
            {"asset_id": asset_id},
            data_keys=("asset",),
            default_data=None,
        )

    def get_runtime_stats(self) -> dict[str, int]:
        return {
            "scenarios_loaded": 0,
            "assets_loaded": 0,
        }
