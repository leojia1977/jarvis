from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Callable, Optional

from app.config import Settings, settings
from app.agents.graph import InvestigationPipeline
from app.tools.siem_adapter import MockSIEMAdapter, ProductionSIEMAdapter, SIEMAdapterProtocol


SUPPORTED_INTENTS = {
    "summarize_recent",
    "asset_query",
    "threat_hunt",
    "data_exfil_check",
}


def infer_intent(user_input: str, requested: Optional[str] = None) -> str:
    if requested in SUPPORTED_INTENTS:
        return requested

    text = (user_input or "").lower()
    if any(token in text for token in ("外泄", "外发", "exfil", "leak")):
        return "data_exfil_check"
    if any(token in text for token in ("横向移动", "lateral", "攻击", "入侵", "ransom", "勒索", "c2")):
        return "threat_hunt"
    if any(token in text for token in ("服务器", "主机", "资产", "server", "host", "db", "工作站")):
        return "asset_query"
    return "summarize_recent"


@dataclass
class RuntimeContext:
    pipeline: Optional[InvestigationPipeline]
    siem: Optional[SIEMAdapterProtocol]
    mode: str
    ready: bool
    reasons: list[str]


class SecuPilotRuntimeService:
    def __init__(
        self,
        runtime_settings: Optional[Settings] = None,
        adapter_factory: Optional[Callable[[str, Settings], SIEMAdapterProtocol]] = None,
    ):
        self.settings = runtime_settings or settings
        self._adapter_factory = adapter_factory
        self.started_at = time.time()
        self._context = self._build_context()

    def _build_context(self) -> RuntimeContext:
        mode = (self.settings.runtime_mode or "mock").lower()
        reasons: list[str] = []
        siem = self._build_siem_adapter(mode)

        if mode == "production" and isinstance(siem, ProductionSIEMAdapter) and not siem.is_configured():
            reasons.append("production_adapter_not_configured")
            return RuntimeContext(
                pipeline=None,
                siem=siem,
                mode=mode,
                ready=False,
                reasons=reasons,
            )

        mock_root = self.settings.get_mock_data_dir()
        if not mock_root.exists():
            reasons.append(f"mock_data_missing:{mock_root}")
            return RuntimeContext(
                pipeline=None,
                siem=None,
                mode=mode,
                ready=False,
                reasons=reasons,
            )

        try:
            pipeline = InvestigationPipeline(siem)
        except Exception as exc:
            reasons.append(f"bootstrap_failed:{exc}")
            return RuntimeContext(
                pipeline=None,
                siem=None,
                mode=mode,
                ready=False,
                reasons=reasons,
            )

        return RuntimeContext(
            pipeline=pipeline,
            siem=siem,
            mode=mode,
            ready=True,
            reasons=[],
        )

    def _build_siem_adapter(self, mode: str) -> SIEMAdapterProtocol:
        if self._adapter_factory:
            return self._adapter_factory(mode, self.settings)
        if mode == "production":
            return ProductionSIEMAdapter(self.settings)
        return MockSIEMAdapter(self.settings.get_mock_data_dir())

    def health(self) -> dict[str, Any]:
        return {
            "status": "healthy" if self._context.pipeline else "degraded",
            "service": self.settings.service_name,
            "version": self.settings.service_version,
            "mode": self._context.mode,
            "uptime_seconds": round(time.time() - self.started_at, 2),
            "timestamp": time.time(),
        }

    def readiness(self) -> dict[str, Any]:
        scenarios = 0
        process_hosts = 0
        if self._context.siem:
            stats = self._context.siem.get_runtime_stats()
            scenarios = stats.get("scenarios_loaded", 0)
        if self._context.pipeline:
            process_hosts = len(self._context.pipeline.orchestrator._process_events)

        return {
            "ready": self._context.ready,
            "service": self.settings.service_name,
            "mode": self._context.mode,
            "mock_data_path": str(self.settings.get_mock_data_dir()),
            "scenarios_loaded": scenarios,
            "process_event_hosts": process_hosts,
            "reasons": list(self._context.reasons),
        }

    def investigate_sync(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        if not self._context.ready or not self._context.pipeline:
            return 503, {
                "status": "error",
                "error": "runtime_not_ready",
                "readiness": self.readiness(),
            }

        user_input = (payload.get("user_input") or "").strip()
        if not user_input:
            return 400, {
                "status": "error",
                "error": "user_input_required",
            }

        target_asset_id = payload.get("target_asset_id")
        target_ip = payload.get("target_ip")
        requested_intent = payload.get("intent")
        resolved_intent = infer_intent(user_input, requested_intent)

        request_meta = {
            "intent_requested": requested_intent,
            "intent_resolved": resolved_intent,
            "target_asset_id": target_asset_id,
            "target_ip": target_ip,
            "time_range": payload.get("time_range", "24h"),
            "runtime_mode": self._context.mode,
        }

        result = asyncio.run(
            self._context.pipeline.investigate(
                intent=resolved_intent,
                user_input=user_input,
                target_asset_id=target_asset_id,
                target_ip=target_ip,
                time_range=payload.get("time_range", "24h"),
                timeout=float(payload.get("timeout", self.settings.llm_timeout_seconds)),
            )
        )

        return 200, {
            "status": "ok",
            "request": request_meta,
            "threat_case": result,
        }
