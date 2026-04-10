from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Callable, Literal, Optional

from app.config import Settings, settings
from app.agents.graph import InvestigationPipeline
from app.tools.case_store import (
    CaseStoreProtocol,
    CaseStoreRuntimeError,
    build_case_store,
    load_current_snapshot_id,
)
from app.tools.persistent_case import (
    approve_action_request,
    build_initial_persistent_case_record,
    cancel_action_request,
    create_action_request_from_case,
    PersistentCaseRecord,
    persistent_case_record_to_dict,
    reject_action_request,
    submit_action_request_for_approval,
)
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
        self._case_store: Optional[CaseStoreProtocol] = None
        self._case_store_error: Optional[CaseStoreRuntimeError] = None
        self._configure_logging()
        self._configure_case_store()
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

    def _configure_case_store(self) -> None:
        try:
            self._case_store = build_case_store(self.settings)
            self._case_store_error = None
        except CaseStoreRuntimeError as exc:
            self._case_store = None
            self._case_store_error = exc

    def _case_store_details(self) -> dict[str, Any]:
        details = {
            "backend": str(self.settings.case_store_backend or "sqlite_local"),
            "store_path": str(self.settings.get_case_store_path()),
        }
        if self._case_store:
            try:
                details.update(self._case_store.get_runtime_stats())
            except CaseStoreRuntimeError as exc:
                details.update(
                    {
                        "reason": exc.reason,
                        "operator_message": exc.operator_message,
                        "detail": exc.detail,
                    }
                )
        if self._case_store_error:
            details.update(
                {
                    "reason": self._case_store_error.reason,
                    "operator_message": self._case_store_error.operator_message,
                    "detail": self._case_store_error.detail,
                }
            )
        return details

    def _persistence_error_payload(self, exc: CaseStoreRuntimeError) -> dict[str, Any]:
        return {
            "status": "error",
            "error": "case_store_unavailable",
            "storage": {
                **self._case_store_details(),
                "reason": exc.reason,
                "operator_message": exc.operator_message,
                "detail": exc.detail,
            },
        }

    def _internal_error_payload(self, *, detail: str) -> dict[str, Any]:
        return {
            "status": "error",
            "error": "internal_error",
            "detail": detail,
        }

    def _action_request_error_payload(
        self,
        *,
        error: str,
        case_id: str,
        detail: str,
        action_request_id: Optional[str] = None,
    ) -> dict[str, Any]:
        payload = {
            "status": "error",
            "error": error,
            "case_id": case_id,
            "detail": detail,
        }
        if action_request_id:
            payload["action_request_id"] = action_request_id
        return payload

    def _require_case_store(self) -> CaseStoreProtocol:
        if self._case_store_error:
            raise self._case_store_error
        if self._case_store:
            return self._case_store
        raise CaseStoreRuntimeError(
            reason="case_store_not_initialized",
            operator_message="Case store is not initialized for the current runtime service.",
            detail="case_store_not_initialized",
        )

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
        elif any(
            reason.startswith("mock_data_missing:")
            or reason.startswith("static_data_unavailable:")
            for reason in reasons
        ):
            state_class = "MISCONFIGURED"
            failure_category = "static_data"
            if any(reason.startswith("mock_data_missing:") for reason in reasons):
                operator_message = (
                    f"Static data directory is missing at {self.settings.get_mock_data_dir()}. "
                    "Runtime cannot bootstrap until local datasets are present."
                )
            else:
                operator_message = (
                    "Static data sources failed to load. Check source mode, refresh semantics, "
                    "and readiness reasons before retrying bootstrap."
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
            pipeline = InvestigationPipeline(siem, runtime_settings=self.settings)
        except Exception as exc:
            detail = str(exc)
            if detail.startswith("static_source_"):
                reasons.append(f"static_data_unavailable:{detail}")
                self._emit_runtime_log(
                    logging.ERROR,
                    "runtime.context.not_ready",
                    mode=mode,
                    failure_category="static_data",
                    reasons=reasons,
                )
                return RuntimeContext(
                    pipeline=None,
                    siem=siem,
                    mode=mode,
                    ready=False,
                    reasons=reasons,
                )

            reasons.append(f"bootstrap_failed:{detail}")
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
        environment_contract = self.settings.get_environment_contract()
        if self._context.siem:
            stats = self._context.siem.get_runtime_stats()
            scenarios = stats.get("scenarios_loaded", 0)
            adapter_type = self._context.siem.__class__.__name__
            if isinstance(self._context.siem, ProductionSIEMAdapter):
                adapter_configured = self._context.siem.is_configured()
        if self._context.pipeline:
            process_hosts = self._context.pipeline.orchestrator.edr.get_runtime_stats().get(
                "process_event_hosts",
                0,
            )

        runtime_state = self._runtime_state()
        static_data_path = str(self.settings.get_mock_data_dir())
        static_data_present = self.settings.get_mock_data_dir().exists()

        return {
            "ready": self._context.ready,
            "service": self.settings.service_name,
            "mode": self._context.mode,
            "environment_profile": environment_contract["environment_profile"],
            "profile_contract_ready": environment_contract["profile_contract_ready"],
            "profile_contract_missing": environment_contract["profile_contract_missing"],
            "required_environment_fields": environment_contract["required_environment_fields"],
            "required_secret_names": environment_contract["required_secret_names"],
            "optional_secret_names": environment_contract["optional_secret_names"],
            "state_class": runtime_state["state_class"],
            "failure_category": runtime_state["failure_category"],
            "operator_message": runtime_state["operator_message"],
            "adapter_type": adapter_type,
            "adapter_configured": adapter_configured,
            "case_store_backend": str(self.settings.case_store_backend or "sqlite_local"),
            "case_store_path": str(self.settings.get_case_store_path()),
            "case_store_ready": self._case_store_error is None,
            "case_store_reason": self._case_store_error.reason if self._case_store_error else None,
            "case_store_operator_message": self._case_store_error.operator_message if self._case_store_error else None,
            "case_store_detail": self._case_store_error.detail if self._case_store_error else None,
            "mock_data_path": static_data_path,  # legacy alias; static_data_path is authoritative
            "static_data_path": static_data_path,
            "static_data_present": static_data_present,
            "scenarios_loaded": scenarios,
            "process_event_hosts": process_hosts,
            "reasons": runtime_state["reasons"],
        }

    def _execute_investigation(
        self,
        payload: dict[str, Any],
    ) -> tuple[int, dict[str, Any], Optional[dict[str, Any]], Optional[dict[str, Any]]]:
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
            }, None, None

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
            }, None, None

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

        response = {
            "status": "ok",
            "request": request_meta,
            "threat_case": result,
        }
        return 200, response, request_meta, result

    def investigate_sync(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        status_code, response, _, _ = self._execute_investigation(payload)
        return status_code, response

    def _load_case_record(
        self,
        case_id: str,
    ) -> tuple[Optional[PersistentCaseRecord], Optional[tuple[int, dict[str, Any]]]]:
        normalized_case_id = str(case_id or "").strip()
        if not normalized_case_id:
            return None, (400, {"status": "error", "error": "case_id_required"})

        try:
            record = self._require_case_store().get_case(normalized_case_id)
        except CaseStoreRuntimeError as exc:
            self._emit_runtime_log(
                logging.ERROR,
                "runtime.case_store.read_failed",
                failure_category="runtime",
                reason=exc.reason,
                detail=exc.detail,
            )
            return None, (503, self._persistence_error_payload(exc))

        if record is None:
            return None, (
                404,
                {
                    "status": "error",
                    "error": "case_not_found",
                    "case_id": normalized_case_id,
                },
            )

        return record, None

    def _save_case_record(
        self,
        record: PersistentCaseRecord,
    ) -> tuple[Optional[PersistentCaseRecord], Optional[tuple[int, dict[str, Any]]]]:
        try:
            stored_record = self._require_case_store().save_case(record)
        except CaseStoreRuntimeError as exc:
            self._emit_runtime_log(
                logging.ERROR,
                "runtime.case_store.write_failed",
                failure_category="runtime",
                reason=exc.reason,
                detail=exc.detail,
            )
            return None, (503, self._persistence_error_payload(exc))
        return stored_record, None

    def create_case_sync(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        status_code, response, request_meta, threat_case = self._execute_investigation(payload)
        if status_code != 200 or threat_case is None or request_meta is None:
            return status_code, response

        actor = str(payload.get("actor") or "secupilot.runtime")
        snapshot_id = load_current_snapshot_id(self.settings)
        try:
            record = build_initial_persistent_case_record(
                threat_case,
                snapshot_id=snapshot_id,
                actor=actor,
            )
        except Exception as exc:
            self._emit_runtime_log(
                logging.ERROR,
                "runtime.case_store.record_build_failed",
                failure_category="runtime",
                detail=str(exc),
            )
            return 500, self._internal_error_payload(detail=str(exc))

        stored_record, store_error = self._save_case_record(record)
        if store_error:
            return store_error
        assert stored_record is not None

        return 201, {
            "status": "ok",
            "case_id": stored_record.case_id,
            "request": request_meta,
            "storage": self._case_store_details(),
            "persistent_case": persistent_case_record_to_dict(stored_record),
        }

    def get_case_sync(self, case_id: str) -> tuple[int, dict[str, Any]]:
        normalized_case_id = str(case_id or "").strip()
        if not normalized_case_id:
            return 400, {
                "status": "error",
                "error": "case_id_required",
            }

        try:
            record = self._require_case_store().get_case(normalized_case_id)
        except CaseStoreRuntimeError as exc:
            self._emit_runtime_log(
                logging.ERROR,
                "runtime.case_store.read_failed",
                failure_category="runtime",
                reason=exc.reason,
                detail=exc.detail,
            )
            return 503, self._persistence_error_payload(exc)

        if record is None:
            return 404, {
                "status": "error",
                "error": "case_not_found",
                "case_id": normalized_case_id,
            }

        return 200, {
            "status": "ok",
            "case_id": normalized_case_id,
            "storage": self._case_store_details(),
            "persistent_case": persistent_case_record_to_dict(record),
        }

    def create_action_request_sync(
        self,
        case_id: str,
        payload: dict[str, Any],
    ) -> tuple[int, dict[str, Any]]:
        record, error_response = self._load_case_record(case_id)
        if error_response:
            return error_response
        assert record is not None

        actor = str(payload.get("actor") or "secupilot.runtime")
        rationale = str(payload.get("rationale") or "").strip()
        if not rationale:
            return 400, {
                "status": "error",
                "error": "rationale_required",
                "case_id": record.case_id,
            }

        try:
            updated = create_action_request_from_case(
                record,
                actor=actor,
                rationale=rationale,
            )
        except ValueError as exc:
            detail = str(exc)
            return 409, self._action_request_error_payload(
                error="action_request_unavailable",
                case_id=record.case_id,
                detail=detail,
            )

        stored_record, store_error = self._save_case_record(updated)
        if store_error:
            return store_error
        assert stored_record is not None

        action_request = persistent_case_record_to_dict(stored_record)["action_requests"][-1]
        return 201, {
            "status": "ok",
            "case_id": stored_record.case_id,
            "action_request_id": action_request["action_request_id"],
            "storage": self._case_store_details(),
            "action_request": action_request,
            "persistent_case": persistent_case_record_to_dict(stored_record),
        }

    def submit_action_request_sync(
        self,
        case_id: str,
        action_request_id: str,
        payload: dict[str, Any],
    ) -> tuple[int, dict[str, Any]]:
        record, error_response = self._load_case_record(case_id)
        if error_response:
            return error_response
        assert record is not None

        actor = str(payload.get("actor") or "secupilot.runtime")
        review_owner = str(payload.get("review_owner") or "").strip()
        reason = str(payload.get("reason") or "").strip()
        if not reason:
            return 400, {"status": "error", "error": "reason_required", "case_id": record.case_id}
        if not review_owner:
            return 400, {"status": "error", "error": "review_owner_required", "case_id": record.case_id}

        try:
            updated = submit_action_request_for_approval(
                record,
                action_request_id=action_request_id,
                actor=actor,
                review_owner=review_owner,
                reason=reason,
            )
        except ValueError as exc:
            detail = str(exc)
            error = "action_request_not_found" if detail.startswith("action_request_not_found:") else "invalid_action_request_transition"
            status_code = 404 if error == "action_request_not_found" else 409
            return status_code, self._action_request_error_payload(
                error=error,
                case_id=record.case_id,
                action_request_id=action_request_id,
                detail=detail,
            )

        stored_record, store_error = self._save_case_record(updated)
        if store_error:
            return store_error
        assert stored_record is not None

        action_request = next(
            item
            for item in persistent_case_record_to_dict(stored_record)["action_requests"]
            if item["action_request_id"] == action_request_id
        )
        return 200, {
            "status": "ok",
            "case_id": stored_record.case_id,
            "action_request_id": action_request_id,
            "storage": self._case_store_details(),
            "action_request": action_request,
            "persistent_case": persistent_case_record_to_dict(stored_record),
        }

    def approve_action_request_sync(
        self,
        case_id: str,
        action_request_id: str,
        payload: dict[str, Any],
    ) -> tuple[int, dict[str, Any]]:
        return self._decide_action_request_sync(
            case_id,
            action_request_id,
            payload,
            decision="approved",
        )

    def reject_action_request_sync(
        self,
        case_id: str,
        action_request_id: str,
        payload: dict[str, Any],
    ) -> tuple[int, dict[str, Any]]:
        return self._decide_action_request_sync(
            case_id,
            action_request_id,
            payload,
            decision="rejected",
        )

    def cancel_action_request_sync(
        self,
        case_id: str,
        action_request_id: str,
        payload: dict[str, Any],
    ) -> tuple[int, dict[str, Any]]:
        record, error_response = self._load_case_record(case_id)
        if error_response:
            return error_response
        assert record is not None

        actor = str(payload.get("actor") or "secupilot.runtime")
        reason = str(payload.get("reason") or "").strip()
        if not reason:
            return 400, {"status": "error", "error": "reason_required", "case_id": record.case_id}

        try:
            updated = cancel_action_request(
                record,
                action_request_id=action_request_id,
                actor=actor,
                reason=reason,
            )
        except ValueError as exc:
            detail = str(exc)
            error = "action_request_not_found" if detail.startswith("action_request_not_found:") else "invalid_action_request_transition"
            status_code = 404 if error == "action_request_not_found" else 409
            return status_code, self._action_request_error_payload(
                error=error,
                case_id=record.case_id,
                action_request_id=action_request_id,
                detail=detail,
            )

        stored_record, store_error = self._save_case_record(updated)
        if store_error:
            return store_error
        assert stored_record is not None

        action_request = next(
            item
            for item in persistent_case_record_to_dict(stored_record)["action_requests"]
            if item["action_request_id"] == action_request_id
        )
        return 200, {
            "status": "ok",
            "case_id": stored_record.case_id,
            "action_request_id": action_request_id,
            "storage": self._case_store_details(),
            "action_request": action_request,
            "persistent_case": persistent_case_record_to_dict(stored_record),
        }

    def _decide_action_request_sync(
        self,
        case_id: str,
        action_request_id: str,
        payload: dict[str, Any],
        *,
        decision: Literal["approved", "rejected"],
    ) -> tuple[int, dict[str, Any]]:
        record, error_response = self._load_case_record(case_id)
        if error_response:
            return error_response
        assert record is not None

        actor = str(payload.get("actor") or "secupilot.runtime")
        reason = str(payload.get("reason") or "").strip()
        if not reason:
            return 400, {"status": "error", "error": "reason_required", "case_id": record.case_id}

        try:
            if decision == "approved":
                updated = approve_action_request(
                    record,
                    action_request_id=action_request_id,
                    actor=actor,
                    reason=reason,
                )
            else:
                updated = reject_action_request(
                    record,
                    action_request_id=action_request_id,
                    actor=actor,
                    reason=reason,
                )
        except ValueError as exc:
            detail = str(exc)
            error = "action_request_not_found" if detail.startswith("action_request_not_found:") else "invalid_action_request_transition"
            status_code = 404 if error == "action_request_not_found" else 409
            return status_code, self._action_request_error_payload(
                error=error,
                case_id=record.case_id,
                action_request_id=action_request_id,
                detail=detail,
            )

        stored_record, store_error = self._save_case_record(updated)
        if store_error:
            return store_error
        assert stored_record is not None

        action_request = next(
            item
            for item in persistent_case_record_to_dict(stored_record)["action_requests"]
            if item["action_request_id"] == action_request_id
        )
        return 200, {
            "status": "ok",
            "case_id": stored_record.case_id,
            "action_request_id": action_request_id,
            "storage": self._case_store_details(),
            "action_request": action_request,
            "persistent_case": persistent_case_record_to_dict(stored_record),
        }
