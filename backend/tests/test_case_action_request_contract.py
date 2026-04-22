from copy import deepcopy
from dataclasses import replace
from typing import get_args
import unittest

from _project_bootstrap import bootstrap

bootstrap()

from app.tools.persistent_case import (  # noqa: E402
    AuditEventType,
    approve_action_request,
    cancel_action_request,
    create_action_request_from_case,
    governed_action_request_statuses,
    governed_audit_event_types,
    governed_case_lifecycle_statuses,
    has_pending_action_requests,
    persistent_case_record_from_dict,
    persistent_case_record_to_dict,
    pending_action_request_ids,
    reject_action_request,
    submit_action_request_for_approval,
    build_initial_persistent_case_record,
    transition_persistent_case_status,
)


def _sample_chain(chain_id="WKST-047:chain-000", host="WKST-047"):
    return {
        "chain_id": chain_id,
        "anomaly_score": 10.0,
        "path": [
            {"node_id": f"{host}:chain-000:node-001", "process_name": "services.exe", "anomalies": []},
            {
                "node_id": f"{host}:chain-000:node-002",
                "process_name": "PSEXESVC.exe",
                "anomalies": [{"type": "suspicious_parent_child", "risk": 7, "mitre": "T1570", "desc": "PsExec"}],
            },
        ],
    }


def _base_case():
    return {
        "case_id": "CASE-S4C-ACTION-001",
        "version": "3.1",
        "risk_score": 9.2,
        "confidence_score": 0.92,
        "confidence_label": "HIGH",
        "verdict_status": "CRITICAL_ACTION_REQUIRED",
        "investigation_status": "COMPLETE",
        "scenario_name": "Lateral Movement + Credential Theft",
        "forensic_result": {
            "hosts_analyzed": ["WKST-047"],
            "total_suspicious_chains": 1,
            "top_chains": [_sample_chain()],
            "attack_stages_observed": ["Execution", "Credential Access"],
            "persistence_mechanisms": [],
            "evidence_gaps": [],
        },
        "hunt_plan": {
            "hypothesis": "存在凭据窃取与横向移动",
            "planned_steps": [{"seq": 1, "tool": "T1"}, {"seq": 2, "tool": "T3"}],
        },
        "intel_summary": {
            "matches": [
                {"indicator": "185.220.101.45", "match_type": "exact", "ioc_type": "ip", "actor": "RANSOMWARE-X"}
            ],
            "threat_level": "HIGH",
        },
        "suggested_action": {
            "type": "NETWORK_ISOLATE",
            "targets": ["WKST-047"],
            "blast_radius_desc": "隔离影响 3 个级联资产",
        },
        "audit_trail": {"degraded": False, "degraded_reasons": []},
    }


SENSITIVE_AUDIT_MARKERS = (
    "secret",
    "token",
    "api_key",
    "authorization",
    "cookie",
    "raw_log",
    "screenshot",
    "export",
    "payload_body",
    "customer_evidence",
)


def _audit_strings(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from _audit_strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _audit_strings(item)
    elif value is not None:
        yield str(value)


def _assert_no_sensitive_audit_values(test_case, record):
    for entry in record.lifecycle_audit:
        for value in _audit_strings(entry.__dict__):
            lowered = value.lower()
            for marker in SENSITIVE_AUDIT_MARKERS:
                test_case.assertNotIn(marker, lowered)


class CaseActionRequestContractTests(unittest.TestCase):
    def test_governed_status_vocabularies_are_locked(self):
        expected_audit_events = {
            "case_created",
            "status_changed",
            "action_request_created",
            "action_request_submitted",
            "action_request_approved",
            "action_request_rejected",
            "action_request_cancelled",
            "case_closed",
            "case_reopened",
        }
        self.assertEqual(
            set(governed_action_request_statuses()),
            {"draft", "pending_approval", "approved", "rejected", "cancelled"},
        )
        self.assertEqual(
            set(governed_case_lifecycle_statuses()),
            {"open", "in_review", "approved", "closed"},
        )
        self.assertEqual(set(get_args(AuditEventType)), expected_audit_events)
        self.assertEqual(set(governed_audit_event_types()), expected_audit_events)
        for forbidden_status in (
            "denied",
            "withdrawn",
            "expired",
            "escalated",
            "auto_approved",
            "under_review",
            "archived",
        ):
            self.assertNotIn(forbidden_status, governed_action_request_statuses())
            self.assertNotIn(forbidden_status, governed_case_lifecycle_statuses())
            self.assertNotIn(forbidden_status, governed_audit_event_types())

        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S5-C-IMPL5-STATUS-001",
            actor="analyst.leo",
            created_at_utc="2026-04-10T10:00:00Z",
        )
        drafted = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="synthetic governed action request",
            at_utc="2026-04-10T10:01:00Z",
        )

        invalid_action_payload = persistent_case_record_to_dict(drafted)
        invalid_action_payload["action_requests"][0]["status"] = "denied"
        with self.assertRaisesRegex(ValueError, "invalid_action_request_status:denied"):
            persistent_case_record_from_dict(invalid_action_payload)

        invalid_lifecycle_payload = persistent_case_record_to_dict(record)
        invalid_lifecycle_payload["lifecycle_status"] = "under_review"
        with self.assertRaisesRegex(ValueError, "invalid_case_lifecycle_status:under_review"):
            persistent_case_record_from_dict(invalid_lifecycle_payload)

        invalid_source_payload = deepcopy(persistent_case_record_to_dict(drafted))
        invalid_source_payload["action_requests"][0]["source_case_status"] = "under_review"
        with self.assertRaisesRegex(ValueError, "invalid_case_lifecycle_status:under_review"):
            persistent_case_record_from_dict(invalid_source_payload)

        invalid_audit_payload = persistent_case_record_to_dict(record)
        invalid_audit_payload["lifecycle_audit"][0]["event_type"] = "audit_log_uploaded"
        with self.assertRaisesRegex(ValueError, "invalid_audit_event_type:audit_log_uploaded"):
            persistent_case_record_from_dict(invalid_audit_payload)

        mutated_audit = replace(record.lifecycle_audit[0], event_type="audit_log_uploaded")
        mutated_record = replace(record, lifecycle_audit=[mutated_audit])
        with self.assertRaisesRegex(ValueError, "invalid_audit_event_type:audit_log_uploaded"):
            persistent_case_record_to_dict(mutated_record)

    def test_create_submit_and_approve_action_request_are_auditable(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S4-C-2026-04-10-003",
            actor="analyst.leo",
            created_at_utc="2026-04-10T11:00:00Z",
        )

        drafted = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="需要先进入审批流，不直接执行隔离",
            at_utc="2026-04-10T11:01:00Z",
        )
        submitted = submit_action_request_for_approval(
            drafted,
            action_request_id=drafted.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="提交审批",
            at_utc="2026-04-10T11:02:00Z",
        )
        approved = approve_action_request(
            submitted,
            action_request_id=submitted.action_requests[0].action_request_id,
            actor="manager.chen",
            reason="风险确认，可以执行",
            at_utc="2026-04-10T11:03:00Z",
        )

        self.assertEqual(record.action_requests, [])
        self.assertEqual(drafted.action_requests[0].status, "draft")
        self.assertEqual(submitted.lifecycle_status, "in_review")
        self.assertEqual(submitted.review_owner, "manager.chen")
        self.assertEqual(submitted.action_requests[0].status, "pending_approval")
        self.assertEqual(approved.lifecycle_status, "approved")
        self.assertEqual(approved.action_requests[0].status, "approved")
        self.assertEqual(approved.action_requests[0].action_request_id, submitted.action_requests[0].action_request_id)
        self.assertEqual(approved.action_requests[0].action_type, "NETWORK_ISOLATE")
        self.assertEqual(approved.action_requests[0].targets, ["WKST-047"])
        self.assertEqual(approved.action_requests[0].rationale, "需要先进入审批流，不直接执行隔离")
        self.assertEqual(approved.action_requests[0].source_case_status, "in_review")
        self.assertEqual(approved.action_requests[0].decision_by, "manager.chen")
        self.assertEqual(approved.action_requests[0].decision_reason, "风险确认，可以执行")
        self.assertEqual(approved.action_requests[0].decision_at_utc, "2026-04-10T11:03:00Z")
        self.assertEqual(submitted.lifecycle_status, "in_review")
        self.assertEqual(submitted.action_requests[0].status, "pending_approval")
        self.assertIsNone(submitted.action_requests[0].decision_by)
        self.assertIsNone(submitted.action_requests[0].decision_reason)
        self.assertIsNone(submitted.action_requests[0].decision_at_utc)
        self.assertEqual(
            [entry.event_type for entry in approved.lifecycle_audit],
            [
                "case_created",
                "action_request_created",
                "status_changed",
                "action_request_submitted",
                "status_changed",
                "action_request_approved",
            ],
        )
        creation_audit = approved.lifecycle_audit[1]
        self.assertEqual(creation_audit.event_type, "action_request_created")
        self.assertNotIn("targets", creation_audit.details)
        approval_audit = approved.lifecycle_audit[-1]
        self.assertEqual(approval_audit.event_type, "action_request_approved")
        self.assertEqual(approval_audit.actor, "manager.chen")
        self.assertEqual(approval_audit.reason, "风险确认，可以执行")
        self.assertEqual(approval_audit.details["action_request_id"], submitted.action_requests[0].action_request_id)
        self.assertEqual(set(approval_audit.details), {"action_request_id"})
        self.assertEqual(approval_audit.case_status, "approved")
        self.assertNotIn("execution", approval_audit.details)
        self.assertNotIn("customer_signoff", approval_audit.details)
        _assert_no_sensitive_audit_values(self, approved)

    def test_pending_action_request_helpers_are_read_only_status_boundary(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S5C-IMPL10-PENDING-HELPERS-001",
            actor="analyst.leo",
            created_at_utc="2026-04-20T11:00:00Z",
        )
        drafted = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="synthetic pending helper draft",
            at_utc="2026-04-20T11:01:00Z",
        )
        before_drafted = persistent_case_record_to_dict(drafted)

        self.assertEqual(pending_action_request_ids(drafted), ())
        self.assertFalse(has_pending_action_requests(drafted))
        self.assertEqual(persistent_case_record_to_dict(drafted), before_drafted)

        submitted = submit_action_request_for_approval(
            drafted,
            action_request_id=drafted.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="submit pending helper request",
            at_utc="2026-04-20T11:02:00Z",
        )
        before_submitted = persistent_case_record_to_dict(submitted)

        self.assertEqual(
            pending_action_request_ids(submitted),
            (submitted.action_requests[0].action_request_id,),
        )
        self.assertTrue(has_pending_action_requests(submitted))
        self.assertEqual(persistent_case_record_to_dict(submitted), before_submitted)

        approved = approve_action_request(
            submitted,
            action_request_id=submitted.action_requests[0].action_request_id,
            actor="manager.chen",
            reason="approve helper request",
            at_utc="2026-04-20T11:03:00Z",
        )
        self.assertEqual(pending_action_request_ids(approved), ())
        self.assertFalse(has_pending_action_requests(approved))

        rejected_draft = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="synthetic pending helper rejection",
            at_utc="2026-04-20T11:04:00Z",
        )
        rejected_submitted = submit_action_request_for_approval(
            rejected_draft,
            action_request_id=rejected_draft.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="submit rejection helper request",
            at_utc="2026-04-20T11:05:00Z",
        )
        rejected = reject_action_request(
            rejected_submitted,
            action_request_id=rejected_submitted.action_requests[0].action_request_id,
            actor="manager.chen",
            reason="reject helper request",
            at_utc="2026-04-20T11:06:00Z",
        )
        self.assertEqual(pending_action_request_ids(rejected), ())
        self.assertFalse(has_pending_action_requests(rejected))

        cancelled = cancel_action_request(
            drafted,
            action_request_id=drafted.action_requests[0].action_request_id,
            actor="analyst.leo",
            reason="cancel helper request",
            at_utc="2026-04-20T11:07:00Z",
        )
        self.assertEqual(pending_action_request_ids(cancelled), ())
        self.assertFalse(has_pending_action_requests(cancelled))

    def test_reject_and_cancel_follow_frozen_status_transitions(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S4-C-2026-04-10-003",
            created_at_utc="2026-04-10T11:00:00Z",
        )
        drafted = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="进入审批流",
            at_utc="2026-04-10T11:01:00Z",
        )
        cancelled = cancel_action_request(
            drafted,
            action_request_id=drafted.action_requests[0].action_request_id,
            actor="analyst.leo",
            reason="误触发，撤销",
            at_utc="2026-04-10T11:02:00Z",
        )

        self.assertEqual(cancelled.lifecycle_status, "open")
        self.assertEqual(cancelled.action_requests[0].status, "cancelled")
        self.assertEqual(cancelled.action_requests[0].action_request_id, drafted.action_requests[0].action_request_id)
        self.assertEqual(cancelled.action_requests[0].action_type, "NETWORK_ISOLATE")
        self.assertEqual(cancelled.action_requests[0].targets, ["WKST-047"])
        self.assertEqual(cancelled.action_requests[0].rationale, "进入审批流")
        self.assertEqual(cancelled.action_requests[0].requested_by, "analyst.leo")
        self.assertEqual(cancelled.action_requests[0].source_case_status, "open")
        self.assertEqual(cancelled.action_requests[0].decision_by, "analyst.leo")
        self.assertEqual(cancelled.action_requests[0].decision_reason, "误触发，撤销")
        self.assertEqual(cancelled.action_requests[0].decision_at_utc, "2026-04-10T11:02:00Z")
        self.assertEqual(drafted.action_requests[0].status, "draft")
        self.assertIsNone(drafted.action_requests[0].decision_by)
        self.assertIsNone(drafted.action_requests[0].decision_reason)
        self.assertIsNone(drafted.action_requests[0].decision_at_utc)
        cancellation_audit = cancelled.lifecycle_audit[-1]
        self.assertEqual(cancellation_audit.event_type, "action_request_cancelled")
        self.assertEqual(cancellation_audit.details["action_request_id"], drafted.action_requests[0].action_request_id)
        self.assertEqual(cancellation_audit.case_status, "open")

        redrafted = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="重新进入审批流",
            at_utc="2026-04-10T11:03:00Z",
        )
        submitted = submit_action_request_for_approval(
            redrafted,
            action_request_id=redrafted.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="提交审批",
            at_utc="2026-04-10T11:04:00Z",
        )
        rejected = reject_action_request(
            submitted,
            action_request_id=submitted.action_requests[0].action_request_id,
            actor="manager.chen",
            reason="证据不足，拒绝执行",
            at_utc="2026-04-10T11:05:00Z",
        )

        self.assertEqual(rejected.lifecycle_status, "in_review")
        self.assertEqual(rejected.action_requests[0].status, "rejected")
        self.assertEqual(rejected.action_requests[0].action_request_id, submitted.action_requests[0].action_request_id)
        self.assertEqual(rejected.action_requests[0].action_type, "NETWORK_ISOLATE")
        self.assertEqual(rejected.action_requests[0].targets, ["WKST-047"])
        self.assertEqual(rejected.action_requests[0].rationale, "重新进入审批流")
        self.assertEqual(rejected.action_requests[0].requested_by, "analyst.leo")
        self.assertEqual(rejected.action_requests[0].source_case_status, "in_review")
        self.assertEqual(rejected.action_requests[0].decision_by, "manager.chen")
        self.assertEqual(rejected.action_requests[0].decision_reason, "证据不足，拒绝执行")
        self.assertEqual(rejected.action_requests[0].decision_at_utc, "2026-04-10T11:05:00Z")
        rejection_audit = rejected.lifecycle_audit[-1]
        self.assertEqual(rejection_audit.event_type, "action_request_rejected")
        self.assertEqual(rejection_audit.details["action_request_id"], submitted.action_requests[0].action_request_id)
        self.assertEqual(rejection_audit.case_status, "in_review")
        self.assertNotIn("case_closed", [entry.event_type for entry in rejected.lifecycle_audit])

    def test_terminal_approved_action_request_rejects_further_transitions(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S5C-IMPL13-ACTION-REQUEST-TERMINAL-GUARDS-APPROVED-001",
            created_at_utc="2026-04-21T10:00:00Z",
        )

        approved_draft = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="approve terminal guard request",
            at_utc="2026-04-21T10:01:00Z",
        )
        approved_submitted = submit_action_request_for_approval(
            approved_draft,
            action_request_id=approved_draft.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="submit request for approval",
            at_utc="2026-04-21T10:02:00Z",
        )
        approved = approve_action_request(
            approved_submitted,
            action_request_id=approved_submitted.action_requests[0].action_request_id,
            actor="manager.chen",
            reason="approve request",
            at_utc="2026-04-21T10:03:00Z",
        )

        with self.assertRaisesRegex(ValueError, "invalid_action_request_transition:approved->pending_approval"):
            submit_action_request_for_approval(
                approved,
                action_request_id=approved.action_requests[0].action_request_id,
                actor="analyst.leo",
                review_owner="manager.chen",
                reason="resubmit approved request",
                at_utc="2026-04-21T10:04:00Z",
            )
        with self.assertRaisesRegex(ValueError, "invalid_action_request_transition:approved->rejected"):
            reject_action_request(
                approved,
                action_request_id=approved.action_requests[0].action_request_id,
                actor="manager.chen",
                reason="reject approved request",
                at_utc="2026-04-21T10:05:00Z",
            )
        with self.assertRaisesRegex(ValueError, "invalid_action_request_transition:approved->cancelled"):
            cancel_action_request(
                approved,
                action_request_id=approved.action_requests[0].action_request_id,
                actor="analyst.leo",
                reason="cancel approved request",
                at_utc="2026-04-21T10:06:00Z",
            )

        self.assertEqual(approved.action_requests[0].status, "approved")

    def test_terminal_rejected_action_request_rejects_further_transitions(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S5C-IMPL13-ACTION-REQUEST-TERMINAL-GUARDS-REJECTED-001",
            created_at_utc="2026-04-21T10:07:00Z",
        )

        rejected_draft = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="reject terminal guard request",
            at_utc="2026-04-21T10:07:00Z",
        )
        rejected_submitted = submit_action_request_for_approval(
            rejected_draft,
            action_request_id=rejected_draft.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="submit request for rejection",
            at_utc="2026-04-21T10:08:00Z",
        )
        rejected = reject_action_request(
            rejected_submitted,
            action_request_id=rejected_submitted.action_requests[0].action_request_id,
            actor="manager.chen",
            reason="reject request",
            at_utc="2026-04-21T10:09:00Z",
        )

        with self.assertRaisesRegex(ValueError, "invalid_action_request_transition:rejected->approved"):
            approve_action_request(
                rejected,
                action_request_id=rejected.action_requests[0].action_request_id,
                actor="manager.chen",
                reason="approve rejected request",
                at_utc="2026-04-21T10:10:00Z",
            )
        with self.assertRaisesRegex(ValueError, "invalid_action_request_transition:rejected->pending_approval"):
            submit_action_request_for_approval(
                rejected,
                action_request_id=rejected.action_requests[0].action_request_id,
                actor="analyst.leo",
                review_owner="manager.chen",
                reason="resubmit rejected request",
                at_utc="2026-04-21T10:11:00Z",
            )
        with self.assertRaisesRegex(ValueError, "invalid_action_request_transition:rejected->cancelled"):
            cancel_action_request(
                rejected,
                action_request_id=rejected.action_requests[0].action_request_id,
                actor="analyst.leo",
                reason="cancel rejected request",
                at_utc="2026-04-21T10:12:00Z",
            )

        self.assertEqual(rejected.action_requests[0].status, "rejected")

    def test_terminal_cancelled_action_request_rejects_further_transitions(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S5C-IMPL13-ACTION-REQUEST-TERMINAL-GUARDS-CANCELLED-001",
            created_at_utc="2026-04-21T10:20:00Z",
        )

        cancelled_draft = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="cancel terminal guard request",
            at_utc="2026-04-21T10:20:00Z",
        )
        cancelled = cancel_action_request(
            cancelled_draft,
            action_request_id=cancelled_draft.action_requests[0].action_request_id,
            actor="analyst.leo",
            reason="cancel request",
            at_utc="2026-04-21T10:21:00Z",
        )

        with self.assertRaisesRegex(ValueError, "invalid_action_request_transition:cancelled->approved"):
            approve_action_request(
                cancelled,
                action_request_id=cancelled.action_requests[0].action_request_id,
                actor="manager.chen",
                reason="approve cancelled request",
                at_utc="2026-04-21T10:22:00Z",
            )
        with self.assertRaisesRegex(ValueError, "invalid_action_request_transition:cancelled->pending_approval"):
            submit_action_request_for_approval(
                cancelled,
                action_request_id=cancelled.action_requests[0].action_request_id,
                actor="analyst.leo",
                review_owner="manager.chen",
                reason="resubmit cancelled request",
                at_utc="2026-04-21T10:23:00Z",
            )
        with self.assertRaisesRegex(ValueError, "invalid_action_request_transition:cancelled->rejected"):
            reject_action_request(
                cancelled,
                action_request_id=cancelled.action_requests[0].action_request_id,
                actor="manager.chen",
                reason="reject cancelled request",
                at_utc="2026-04-21T10:24:00Z",
            )

        self.assertEqual(cancelled.action_requests[0].status, "cancelled")

    def test_action_request_status_vocabulary_remains_frozen(self):
        self.assertEqual(
            set(governed_action_request_statuses()),
            {"draft", "pending_approval", "approved", "rejected", "cancelled"},
        )

    def test_degraded_case_suppresses_action_request_creation(self):
        degraded_case = _base_case()
        degraded_case["investigation_status"] = "DEGRADED"
        degraded_case["audit_trail"] = {"degraded": True, "degraded_reasons": ["siem_adapter_partial"]}
        record = build_initial_persistent_case_record(
            degraded_case,
            snapshot_id="S4-C-2026-04-10-003",
        )

        with self.assertRaisesRegex(ValueError, "action_request_unavailable"):
            create_action_request_from_case(
                record,
                actor="analyst.leo",
                rationale="降级案卷不应允许创建动作请求",
            )

    def test_closed_case_blocks_action_request_create_submit_approve_reject_and_cancel(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S4-C-2026-04-10-004",
            created_at_utc="2026-04-10T11:00:00Z",
        )
        drafted = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="进入审批流",
            at_utc="2026-04-10T11:01:00Z",
        )
        closed_draft = transition_persistent_case_status(
            drafted,
            to_status="closed",
            actor="manager.chen",
            reason="人工关闭案例",
            at_utc="2026-04-10T11:01:30Z",
        )

        with self.assertRaisesRegex(ValueError, "action_request_not_allowed_for_closed_case"):
            create_action_request_from_case(
                closed_draft,
                actor="analyst.leo",
                rationale="关闭后不允许新建",
                at_utc="2026-04-10T11:01:40Z",
            )

        with self.assertRaisesRegex(ValueError, "action_request_not_allowed_for_closed_case"):
            submit_action_request_for_approval(
                closed_draft,
                action_request_id=drafted.action_requests[0].action_request_id,
                actor="analyst.leo",
                review_owner="manager.chen",
                reason="关闭后不允许提交",
                at_utc="2026-04-10T11:01:50Z",
            )

        submitted = submit_action_request_for_approval(
            drafted,
            action_request_id=drafted.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="提交审批",
            at_utc="2026-04-10T11:02:00Z",
        )
        closed = transition_persistent_case_status(
            submitted,
            to_status="closed",
            actor="manager.chen",
            reason="人工关闭案例",
            at_utc="2026-04-10T11:03:00Z",
        )

        with self.assertRaisesRegex(ValueError, "action_request_not_allowed_for_closed_case"):
            approve_action_request(
                closed,
                action_request_id=submitted.action_requests[0].action_request_id,
                actor="manager.chen",
                reason="关闭后不允许批准",
                at_utc="2026-04-10T11:03:30Z",
            )

        with self.assertRaisesRegex(ValueError, "action_request_not_allowed_for_closed_case"):
            reject_action_request(
                closed,
                action_request_id=submitted.action_requests[0].action_request_id,
                actor="manager.chen",
                reason="关闭后不允许拒绝",
                at_utc="2026-04-10T11:04:00Z",
            )

        with self.assertRaisesRegex(ValueError, "action_request_not_allowed_for_closed_case"):
            cancel_action_request(
                closed,
                action_request_id=submitted.action_requests[0].action_request_id,
                actor="manager.chen",
                reason="关闭后不允许取消",
                at_utc="2026-04-10T11:05:00Z",
            )

        self.assertEqual(closed.lifecycle_status, "closed")
        self.assertEqual(closed.action_requests[0].status, "pending_approval")
        self.assertEqual(closed.lifecycle_audit[-1].event_type, "case_closed")
        self.assertNotIn("action_request_approved", [entry.event_type for entry in closed.lifecycle_audit])
        self.assertNotIn("action_request_rejected", [entry.event_type for entry in closed.lifecycle_audit])
        self.assertNotIn("action_request_cancelled", [entry.event_type for entry in closed.lifecycle_audit])
        _assert_no_sensitive_audit_values(self, closed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
