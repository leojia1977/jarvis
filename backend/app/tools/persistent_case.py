from __future__ import annotations

"""Governed persistent case schema and immutable record helpers.

The dataclasses below are frozen snapshots, but their nested dict/list fields are
still Python mutables. Callers must never append into ``action_requests`` or
``lifecycle_audit`` in place. All durable changes must return a new
``PersistentCaseRecord`` through the helper functions in this module so audit
and status semantics remain deterministic.
"""

from copy import deepcopy
from dataclasses import asdict, dataclass, field, replace
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
    "action_request_submitted",
    "action_request_approved",
    "action_request_rejected",
    "action_request_cancelled",
    "case_closed",
    "case_reopened",
]

FROZEN_CASE_STATUS_TRANSITIONS: dict[CaseLifecycleStatus, set[CaseLifecycleStatus]] = {
    "open": {"in_review", "closed"},
    "in_review": {"approved", "closed", "open"},
    "approved": {"closed", "in_review"},
    "closed": {"open"},
}

FROZEN_ACTION_REQUEST_TRANSITIONS: dict[ActionRequestStatus, set[ActionRequestStatus]] = {
    "draft": {"pending_approval", "cancelled"},
    "pending_approval": {"approved", "rejected", "cancelled"},
    "approved": set(),
    "rejected": set(),
    "cancelled": set(),
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


def _next_case_item_id(case_id: str, scope: str, existing_ids: list[str]) -> str:
    prefix = f"{case_id}:{scope}-"
    highest = 0
    for item_id in existing_ids:
        if not item_id.startswith(prefix):
            continue
        suffix = item_id[len(prefix) :]
        if suffix.isdigit():
            highest = max(highest, int(suffix))
    return f"{prefix}{highest + 1:03d}"


def next_action_request_id(
    case_id: str,
    existing_requests: list[CaseActionRequestRecord] | list[dict[str, Any]],
) -> str:
    existing_ids: list[str] = []
    for item in existing_requests:
        if isinstance(item, dict):
            value = item.get("action_request_id")
        else:
            value = item.action_request_id
        if value:
            existing_ids.append(str(value))
    return _next_case_item_id(case_id, "action", existing_ids)


def next_audit_event_id(
    case_id: str,
    existing_entries: list[CaseAuditEntry] | list[dict[str, Any]],
) -> str:
    existing_ids: list[str] = []
    for item in existing_entries:
        if isinstance(item, dict):
            value = item.get("event_id")
        else:
            value = item.event_id
        if value:
            existing_ids.append(str(value))
    return _next_case_item_id(case_id, "audit", existing_ids)


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


def allowed_action_request_transitions(status: ActionRequestStatus) -> tuple[ActionRequestStatus, ...]:
    return tuple(sorted(FROZEN_ACTION_REQUEST_TRANSITIONS.get(status, set())))


def is_valid_action_request_transition(
    from_status: ActionRequestStatus,
    to_status: ActionRequestStatus,
) -> bool:
    return to_status in FROZEN_ACTION_REQUEST_TRANSITIONS.get(from_status, set())


def build_action_request_seed(
    threat_case: dict[str, Any],
    *,
    actor: str,
    rationale: str,
    requested_at_utc: Optional[str] = None,
    existing_requests: Optional[list[CaseActionRequestRecord] | list[dict[str, Any]]] = None,
    source_case_status: Optional[CaseLifecycleStatus] = None,
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
        action_request_id=next_action_request_id(case_id, existing_requests or []),
        status="draft",
        action_type=str(action_type),
        targets=[str(item) for item in targets],
        requested_by=actor,
        requested_at_utc=timestamp,
        rationale=rationale,
        approval_required=True,
        blast_summary=suggested_action.get("blast_radius_desc"),
        source_case_status=source_case_status or "open",
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
            event_id=next_audit_event_id(case_id, []),
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


def append_action_request_record(
    record: PersistentCaseRecord,
    action_request: CaseActionRequestRecord,
    *,
    updated_at_utc: Optional[str] = None,
) -> PersistentCaseRecord:
    return replace(
        record,
        action_requests=[*record.action_requests, action_request],
        updated_at_utc=updated_at_utc or _utc_now_iso(),
    )


def _find_action_request(
    record: PersistentCaseRecord,
    action_request_id: str,
) -> tuple[int, CaseActionRequestRecord]:
    for index, item in enumerate(record.action_requests):
        if item.action_request_id == action_request_id:
            return index, item
    raise ValueError(f"action_request_not_found:{action_request_id}")


def _replace_action_request(
    record: PersistentCaseRecord,
    index: int,
    updated_request: CaseActionRequestRecord,
    *,
    updated_at_utc: str,
    audit_entry: CaseAuditEntry,
    lifecycle_status: Optional[CaseLifecycleStatus] = None,
    review_owner: Optional[str] = None,
) -> PersistentCaseRecord:
    updated_requests = list(record.action_requests)
    updated_requests[index] = updated_request
    return replace(
        record,
        action_requests=updated_requests,
        updated_at_utc=updated_at_utc,
        lifecycle_status=lifecycle_status or record.lifecycle_status,
        review_owner=review_owner if review_owner is not None else record.review_owner,
        lifecycle_audit=[*record.lifecycle_audit, audit_entry],
    )


def _recommended_action_enabled(record: PersistentCaseRecord) -> bool:
    recommended_action = record.case_view.get("recommended_action") or {}
    return bool(recommended_action.get("available")) and recommended_action.get("action_state") == "AVAILABLE"


def create_action_request_from_case(
    record: PersistentCaseRecord,
    *,
    actor: str,
    rationale: str,
    at_utc: Optional[str] = None,
) -> PersistentCaseRecord:
    if record.lifecycle_status == "closed":
        raise ValueError("action_request_not_allowed_for_closed_case")
    if not _recommended_action_enabled(record):
        raise ValueError("action_request_unavailable")

    timestamp = at_utc or _utc_now_iso()
    action_request = build_action_request_seed(
        record.threat_case,
        actor=actor,
        rationale=rationale,
        requested_at_utc=timestamp,
        existing_requests=record.action_requests,
        source_case_status=record.lifecycle_status,
    )
    if action_request is None:
        raise ValueError("suggested_action_missing")

    audit_entry = CaseAuditEntry(
        event_id=next_audit_event_id(record.case_id, record.lifecycle_audit),
        event_type="action_request_created",
        actor=actor,
        at_utc=timestamp,
        case_status=record.lifecycle_status,
        reason="action_request_created",
        details={
            "action_request_id": action_request.action_request_id,
            "action_type": action_request.action_type,
            "targets": deepcopy(action_request.targets),
            "approval_required": action_request.approval_required,
        },
    )
    return replace(
        record,
        action_requests=[*record.action_requests, action_request],
        updated_at_utc=timestamp,
        lifecycle_audit=[*record.lifecycle_audit, audit_entry],
    )


def submit_action_request_for_approval(
    record: PersistentCaseRecord,
    *,
    action_request_id: str,
    actor: str,
    review_owner: str,
    reason: str,
    at_utc: Optional[str] = None,
) -> PersistentCaseRecord:
    if record.lifecycle_status == "closed":
        raise ValueError("action_request_not_allowed_for_closed_case")

    timestamp = at_utc or _utc_now_iso()
    base_record = record
    if record.lifecycle_status == "open":
        base_record = transition_persistent_case_status(
            record,
            to_status="in_review",
            actor=actor,
            review_owner=review_owner,
            reason="action_request_submitted",
            details={"action_request_id": action_request_id},
            at_utc=timestamp,
        )

    index, existing = _find_action_request(base_record, action_request_id)
    if not is_valid_action_request_transition(existing.status, "pending_approval"):
        raise ValueError(f"invalid_action_request_transition:{existing.status}->pending_approval")

    updated_request = replace(
        existing,
        status="pending_approval",
        source_case_status=base_record.lifecycle_status,
    )
    audit_entry = CaseAuditEntry(
        event_id=next_audit_event_id(base_record.case_id, base_record.lifecycle_audit),
        event_type="action_request_submitted",
        actor=actor,
        at_utc=timestamp,
        case_status=base_record.lifecycle_status,
        reason=reason,
        details={
            "action_request_id": action_request_id,
            "review_owner": review_owner,
        },
    )
    return _replace_action_request(
        base_record,
        index,
        updated_request,
        updated_at_utc=timestamp,
        audit_entry=audit_entry,
        review_owner=review_owner,
    )


def approve_action_request(
    record: PersistentCaseRecord,
    *,
    action_request_id: str,
    actor: str,
    reason: str,
    at_utc: Optional[str] = None,
) -> PersistentCaseRecord:
    timestamp = at_utc or _utc_now_iso()
    base_record = record
    if record.lifecycle_status != "approved":
        base_record = transition_persistent_case_status(
            record,
            to_status="approved",
            actor=actor,
            reason="action_request_approved",
            at_utc=timestamp,
        )

    index, existing = _find_action_request(base_record, action_request_id)
    if not is_valid_action_request_transition(existing.status, "approved"):
        raise ValueError(f"invalid_action_request_transition:{existing.status}->approved")

    updated_request = replace(
        existing,
        status="approved",
        decision_by=actor,
        decision_at_utc=timestamp,
        decision_reason=reason,
    )
    audit_entry = CaseAuditEntry(
        event_id=next_audit_event_id(base_record.case_id, base_record.lifecycle_audit),
        event_type="action_request_approved",
        actor=actor,
        at_utc=timestamp,
        case_status=base_record.lifecycle_status,
        reason=reason,
        details={"action_request_id": action_request_id},
    )
    return _replace_action_request(
        base_record,
        index,
        updated_request,
        updated_at_utc=timestamp,
        audit_entry=audit_entry,
    )


def reject_action_request(
    record: PersistentCaseRecord,
    *,
    action_request_id: str,
    actor: str,
    reason: str,
    at_utc: Optional[str] = None,
) -> PersistentCaseRecord:
    if record.lifecycle_status == "closed":
        raise ValueError("action_request_not_allowed_for_closed_case")
    timestamp = at_utc or _utc_now_iso()
    index, existing = _find_action_request(record, action_request_id)
    if not is_valid_action_request_transition(existing.status, "rejected"):
        raise ValueError(f"invalid_action_request_transition:{existing.status}->rejected")

    updated_request = replace(
        existing,
        status="rejected",
        decision_by=actor,
        decision_at_utc=timestamp,
        decision_reason=reason,
    )
    audit_entry = CaseAuditEntry(
        event_id=next_audit_event_id(record.case_id, record.lifecycle_audit),
        event_type="action_request_rejected",
        actor=actor,
        at_utc=timestamp,
        case_status=record.lifecycle_status,
        reason=reason,
        details={"action_request_id": action_request_id},
    )
    return _replace_action_request(
        record,
        index,
        updated_request,
        updated_at_utc=timestamp,
        audit_entry=audit_entry,
    )


def cancel_action_request(
    record: PersistentCaseRecord,
    *,
    action_request_id: str,
    actor: str,
    reason: str,
    at_utc: Optional[str] = None,
) -> PersistentCaseRecord:
    if record.lifecycle_status == "closed":
        raise ValueError("action_request_not_allowed_for_closed_case")
    timestamp = at_utc or _utc_now_iso()
    index, existing = _find_action_request(record, action_request_id)
    if not is_valid_action_request_transition(existing.status, "cancelled"):
        raise ValueError(f"invalid_action_request_transition:{existing.status}->cancelled")

    updated_request = replace(
        existing,
        status="cancelled",
        decision_by=actor,
        decision_at_utc=timestamp,
        decision_reason=reason,
    )
    audit_entry = CaseAuditEntry(
        event_id=next_audit_event_id(record.case_id, record.lifecycle_audit),
        event_type="action_request_cancelled",
        actor=actor,
        at_utc=timestamp,
        case_status=record.lifecycle_status,
        reason=reason,
        details={"action_request_id": action_request_id},
    )
    return _replace_action_request(
        record,
        index,
        updated_request,
        updated_at_utc=timestamp,
        audit_entry=audit_entry,
    )


def transition_persistent_case_status(
    record: PersistentCaseRecord,
    *,
    to_status: CaseLifecycleStatus,
    actor: str,
    reason: str,
    review_owner: Optional[str] = None,
    details: Optional[dict[str, Any]] = None,
    at_utc: Optional[str] = None,
) -> PersistentCaseRecord:
    if not is_valid_case_status_transition(record.lifecycle_status, to_status):
        raise ValueError(f"invalid_case_status_transition:{record.lifecycle_status}->{to_status}")

    resolved_review_owner = review_owner if review_owner is not None else record.review_owner
    if to_status == "in_review" and not resolved_review_owner:
        raise ValueError("review_owner_required_for_in_review")

    timestamp = at_utc or _utc_now_iso()
    if to_status == "closed":
        event_type: AuditEventType = "case_closed"
    elif record.lifecycle_status == "closed" and to_status == "open":
        event_type = "case_reopened"
    else:
        event_type = "status_changed"

    audit_entry = CaseAuditEntry(
        event_id=next_audit_event_id(record.case_id, record.lifecycle_audit),
        event_type=event_type,
        actor=actor,
        at_utc=timestamp,
        case_status=to_status,
        reason=reason,
        details=deepcopy(details or {}),
    )

    return replace(
        record,
        lifecycle_status=to_status,
        updated_at_utc=timestamp,
        review_owner=resolved_review_owner,
        lifecycle_audit=[*record.lifecycle_audit, audit_entry],
    )


def persistent_case_record_from_dict(payload: dict[str, Any]) -> PersistentCaseRecord:
    action_requests = [
        CaseActionRequestRecord(**deepcopy(item))
        for item in payload.get("action_requests", [])
    ]
    lifecycle_audit = [
        CaseAuditEntry(**deepcopy(item))
        for item in payload.get("lifecycle_audit", [])
    ]
    return PersistentCaseRecord(
        schema_version=str(payload.get("schema_version") or ""),
        case_view_schema_version=str(payload.get("case_view_schema_version") or ""),
        storage_backend=str(payload.get("storage_backend") or ""),
        source_snapshot_id=str(payload.get("source_snapshot_id") or ""),
        case_id=str(payload.get("case_id") or ""),
        threat_case_version=str(payload.get("threat_case_version") or ""),
        lifecycle_status=str(payload.get("lifecycle_status") or "open"),
        created_at_utc=str(payload.get("created_at_utc") or ""),
        updated_at_utc=str(payload.get("updated_at_utc") or ""),
        review_owner=payload.get("review_owner"),
        threat_case=deepcopy(payload.get("threat_case") or {}),
        case_view=deepcopy(payload.get("case_view") or {}),
        action_requests=action_requests,
        lifecycle_audit=lifecycle_audit,
    )


def persistent_case_record_to_dict(record: PersistentCaseRecord) -> dict[str, Any]:
    return asdict(record)
