import unittest

from _project_bootstrap import bootstrap

bootstrap()

from app.tools.persistent_case import (  # noqa: E402
    approve_action_request,
    cancel_action_request,
    create_action_request_from_case,
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


class CaseActionRequestContractTests(unittest.TestCase):
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
        self.assertEqual(approved.action_requests[0].decision_by, "manager.chen")
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

        self.assertEqual(cancelled.action_requests[0].status, "cancelled")

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
        self.assertEqual(rejected.action_requests[0].decision_reason, "证据不足，拒绝执行")

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

    def test_closed_case_blocks_reject_and_cancel_updates(self):
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
