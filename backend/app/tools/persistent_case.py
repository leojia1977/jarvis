from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal, Optional

from app.agents.case_view import build_case_view
from app.config import Settings, settings


CASE_STORAGE_SCHEMA_VERSION = "4.0-persist-1"
CASE_VIEW_SCHEMA_VERSION = "3.1"
PERSISTENCE_BACKEND = "sqlite_local"

CaseLifecycleStatus = Literal["open", "in_review", "approved", "closed"]
ActionRequestStatus = Literal["draft", "pending_approval", "approved", "rejected", "cancelled"]
AuditEventType = Literal[
    "case_created",
    "status_changed",
    "action_request_created",
    "action_request_approved",
    "action_request_rejected",
    "case_closed",
    "case_reopened",
]

FROZEN_CASE_STATUS_TRANSITIONS: dict[CaseLifecycleStatus, set[CaseLifecycleStatus]] = {
    "open": {"in_review", "closed"},
    "in_review": {"approved", "closed", "open"},
    "approved": {"closed", "in_review"},
    "closed": {"open"},
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class PersistenceBackendChoice:
    backend: Literal["sqlite_local"]
    store_path: str
    ownership: str
    rationale: str
    sovereignty_alignment: str
    audit_alignment: str


@dataclass(frozen=True)
class CaseAuditEntry:
    event_id: str
    event_type: AuditEventType
    actor: str
    at_utc: str
    case_status: CaseLifecycleStatus
    reason: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CaseActionRequestRecord:
    action_request_id: str
    status: ActionRequestStatus
    action_type: str
    targets: list[str]
    requested_by: str
    requested_at_utc: str
    rationale: str
    approval_required: bool = True
    blast_summary: Optional[str] = None
    source_case_status: Optional[CaseLifecycleStatus] = None
    decision_by: Optional[str] = None
    decision_at_utc: Optional[str] = None
    decision_reason: Optional[str] = None


@dataclass(frozen=True)
class PersistentCaseRecord:
    schema_version: str
    case_view_schema_version: str
    storage_backend: str
    source_snapshot_id: str
    case_id: str
    threat_case_version: str
    lifecycle_status: CaseLifecycleStatus
    created_at_utc: str
    updated_at_utc: str
    review_owner: Optional[str]
    threat_case: dict[str, Any] = field(default_factory=dict)
    case_view: dict[str, Any] = field(default_factory=dict)
    action_requests: list[CaseActionRequestRecord] = field(default_factory=list)
    lifecycle_audit: list[CaseAuditEntry] = field(default_factory=list)


def frozen_persistence_backend(runtime_settings: Settings = settings) -> PersistenceBackendChoice:
    return PersistenceBackendChoice(
        backend=PERSISTENCE_BACKEND,
        store_path=str(runtime_settings.get_case_store_path()),
        ownership="Governed local case store for Sprint 4 pilot",
        rationale=(
            "SQLite provides durable local persistence without introducing a new service "
            "dependency before the pilot path is proven."
        ),
        sovereignty_alignment=(
            "The store remains local to the controlled deployment environment and does not "
            "require case data to leave the governed runtime boundary."
        ),
        audit_alignment=(
            "SQLite preserves append-safe audit history for case status and approval records "
            "while remaining simple enough for deterministic backup, review, and offline verification."
        ),
    )


def allowed_case_status_transitions(status: CaseLifecycleStatus) -> tuple[CaseLifecycleStatus, ...]:
    return tuple(sorted(FROZEN_CASE_STATUS_TRANSITIONS.get(status, set())))


def is_valid_case_status_transition(
    from_status: CaseLifecycleStatus,
    to_status: CaseLifecycleStatus,
) -> bool:
    return to_status in FROZEN_CASE_STATUS_TRANSITIONS.get(from_status, set())


def build_action_request_seed(
    threat_case: dict[str, Any],
    *,
    actor: str,
    rationale: str,
    requested_at_utc: Optional[str] = None,
) -> Optional[CaseActionRequestRecord]:
    suggested_action = threat_case.get("suggested_action") or {}
    action_type = suggested_action.get("type")
    if not action_type:
        return None

    timestamp = requested_at_utc or _utc_now_iso()
    case_id = str(threat_case.get("case_id") or "CASE-UNKNOWN")
    targets = list(suggested_action.get("targets") or [])
    if not targets and suggested_action.get("target"):
        targets = [str(suggested_action.get("target"))]

    return CaseActionRequestRecord(
        action_request_id=f"{case_id}:action-001",
        status="draft",
        action_type=str(action_type),
        targets=[str(item) for item in targets],
        requested_by=actor,
        requested_at_utc=timestamp,
        rationale=rationale,
        approval_required=True,
        blast_summary=suggested_action.get("blast_radius_desc"),
        source_case_status="open",
    )


def build_initial_persistent_case_record(
    threat_case: dict[str, Any],
    *,
    snapshot_id: str,
    actor: str = "secupilot.runtime",
    created_at_utc: Optional[str] = None,
) -> PersistentCaseRecord:
    timestamp = created_at_utc or _utc_now_iso()
    case_id = str(threat_case.get("case_id") or "CASE-UNKNOWN")
    case_view = build_case_view(threat_case)
    lifecycle_audit = [
        CaseAuditEntry(
            event_id=f"{case_id}:audit-001",
            event_type="case_created",
            actor=actor,
            at_utc=timestamp,
            case_status="open",
            reason="initial_case_persisted",
            details={
                "verdict_status": threat_case.get("verdict_status"),
                "investigation_status": threat_case.get("investigation_status"),
            },
        )
    ]

    return PersistentCaseRecord(
        schema_version=CASE_STORAGE_SCHEMA_VERSION,
        case_view_schema_version=CASE_VIEW_SCHEMA_VERSION,
        storage_backend=PERSISTENCE_BACKEND,
        source_snapshot_id=snapshot_id,
        case_id=case_id,
        threat_case_version=str(threat_case.get("version") or ""),
        lifecycle_status="open",
        created_at_utc=timestamp,
        updated_at_utc=timestamp,
        review_owner=None,
        threat_case=deepcopy(threat_case),
        case_view=case_view,
        action_requests=[],
        lifecycle_audit=lifecycle_audit,
    )


def persistent_case_record_to_dict(record: PersistentCaseRecord) -> dict[str, Any]:
    return asdict(record)
