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
    persistent_case_record_from_dict,
    persistent_case_record_to_dict,
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
