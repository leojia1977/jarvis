from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Callable, Literal, Optional

from app.config import Settings, settings
from app.agents.graph import InvestigationPipeline
from app.tools.siem_adapter import MockSIEMAdapter, ProductionSIEMAdapter, SIEMAdapterProtocol


SUPPORTED_INTENTS = {
    "summarize_recent",
    "asset_query",
    "threat_hunt",
    "data_exfil_check",
}

RUNTIME_STATE = Literal["READY", "MISCONFIGURED", "BOOTSTRAP_FAILED", "DEGRADED"]
FAILURE_CATEGORY = Literal["none", "adapter_config", "static_data", "bootstrap", "runtime"]

logger = logging.getLogger("secupilot.runtime")


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
        self._configure_logging()
        self._context = self._build_context()

    def _configure_logging(self) -> None:
        configured = str(getattr(self.settings, "log_level", "INFO") or "INFO").upper()
        logger.setLevel(getattr(logging, configured, logging.INFO))

    def _emit_runtime_log(self, level: int, event: str, **fields: Any) -> None:
        context = getattr(self, "_context", None)
        payload = {
            "event": event,
            "service": self.settings.service_name,
            "mode": getattr(context, "mode", None) or fields.pop("mode", None),
            **fields,
        }
        logger.log(level, json.dumps(payload, ensure_ascii=False, sort_keys=True))

    def _runtime_state(self) -> dict[str, Any]:
        reasons = list(self._context.reasons)
        state_class: RUNTIME_STATE
        failure_category: FAILURE_CATEGORY
        operator_message: str

        if self._context.ready and self._context.pipeline:
            state_class = "READY"
            failure_category = "none"
            operator_message = "Runtime ready. Investigation pipeline and adapter are available."
        elif "production_adapter_not_configured" in reasons:
            state_class = "MISCONFIGURED"
            failure_category = "adapter_config"
            operator_message = (
                "Production SIEM adapter is not configured. Set siem_base_url and siem_auth_token."
            )
        elif any(reason.startswith("mock_data_missing:") for reason in reasons):
            state_class = "MISCONFIGURED"
            failure_category = "static_data"
            operator_message = (
                f"Static data directory is missing at {self.settings.get_mock_data_dir()}. "
                "Runtime cannot bootstrap until local datasets are present."
            )
        elif any(reason.startswith("bootstrap_failed:") for reason in reasons):
            state_class = "BOOTSTRAP_FAILED"
            failure_category = "bootstrap"
            operator_message = (
                "Runtime bootstrap failed while building the investigation pipeline. "
                "Check secupilot.runtime logger at ERROR level for event "
                "runtime.context.bootstrap_failed."
            )
        else:
            state_class = "DEGRADED"
            failure_category = "runtime"
            operator_message = (
                "Runtime is degraded. Review readiness reasons for the affected dependency."
            )

        return {
            "state_class": state_class,
            "failure_category": failure_category,
            "operator_message": operator_message,
            "reasons": reasons,
        }

    def _build_context(self) -> RuntimeContext:
        mode = (self.settings.runtime_mode or "mock").lower()
        reasons: list[str] = []
        mock_root = self.settings.get_mock_data_dir()

        if mode != "production" and not mock_root.exists():
            reasons.append(f"mock_data_missing:{mock_root}")
            self._emit_runtime_log(
                logging.ERROR,
                "runtime.context.not_ready",
                mode=mode,
                failure_category="static_data",
                reasons=reasons,
            )
            return RuntimeContext(
                pipeline=None,
                siem=None,
                mode=mode,
                ready=False,
                reasons=reasons,
            )

        siem = self._build_siem_adapter(mode)

        if mode == "production" and isinstance(siem, ProductionSIEMAdapter) and not siem.is_configured():
            reasons.append("production_adapter_not_configured")
            self._emit_runtime_log(
                logging.WARNING,
                "runtime.context.not_ready",
                mode=mode,
                failure_category="adapter_config",
                reasons=reasons,
            )
            return RuntimeContext(
                pipeline=None,
                siem=siem,
                mode=mode,
                ready=False,
                reasons=reasons,
            )

        if not mock_root.exists():
            reasons.append(f"mock_data_missing:{mock_root}")
            self._emit_runtime_log(
                logging.ERROR,
                "runtime.context.not_ready",
                mode=mode,
                failure_category="static_data",
                reasons=reasons,
            )
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
            self._emit_runtime_log(
                logging.ERROR,
                "runtime.context.bootstrap_failed",
                mode=mode,
                failure_category="bootstrap",
                reasons=reasons,
            )
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
        runtime_state = self._runtime_state()
        return {
            "status": "healthy" if runtime_state["state_class"] == "READY" else "degraded",
            "service": self.settings.service_name,
            "version": self.settings.service_version,
            "mode": self._context.mode,
            "state_class": runtime_state["state_class"],
            "failure_category": runtime_state["failure_category"],
            "operator_message": runtime_state["operator_message"],
            "reasons": runtime_state["reasons"],
            "uptime_seconds": round(time.time() - self.started_at, 2),
            "timestamp": time.time(),
        }

    def readiness(self) -> dict[str, Any]:
        scenarios = 0
        process_hosts = 0
        adapter_type = None
        adapter_configured = None
        if self._context.siem:
            stats = self._context.siem.get_runtime_stats()
            scenarios = stats.get("scenarios_loaded", 0)
            adapter_type = self._context.siem.__class__.__name__
            if isinstance(self._context.siem, ProductionSIEMAdapter):
                adapter_configured = self._context.siem.is_configured()
        if self._context.pipeline:
            process_hosts = len(self._context.pipeline.orchestrator._process_events)

        runtime_state = self._runtime_state()
        static_data_path = str(self.settings.get_mock_data_dir())
        static_data_present = self.settings.get_mock_data_dir().exists()

        return {
            "ready": self._context.ready,
            "service": self.settings.service_name,
            "mode": self._context.mode,
            "state_class": runtime_state["state_class"],
            "failure_category": runtime_state["failure_category"],
            "operator_message": runtime_state["operator_message"],
            "adapter_type": adapter_type,
            "adapter_configured": adapter_configured,
            "mock_data_path": static_data_path,  # legacy alias; static_data_path is authoritative
            "static_data_path": static_data_path,
            "static_data_present": static_data_present,
            "scenarios_loaded": scenarios,
            "process_event_hosts": process_hosts,
            "reasons": runtime_state["reasons"],
        }

    def investigate_sync(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        if not self._context.ready or not self._context.pipeline:
            readiness = self.readiness()
            self._emit_runtime_log(
                logging.WARNING,
                "runtime.investigate.not_ready",
                failure_category=readiness["failure_category"],
                state_class=readiness["state_class"],
                reasons=readiness["reasons"],
            )
            return 503, {
                "status": "error",
                "error": "runtime_not_ready",
                "runtime_status": {
                    "state_class": readiness["state_class"],
                    "failure_category": readiness["failure_category"],
                    "operator_message": readiness["operator_message"],
                },
                "readiness": readiness,
            }

        user_input = (payload.get("user_input") or "").strip()
        if not user_input:
            self._emit_runtime_log(
                logging.WARNING,
                "runtime.investigate.invalid_request",
                failure_category="runtime",
                reason="user_input_required",
            )
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
