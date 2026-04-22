import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.config import Settings  # noqa: E402
from backend.app.runtime_service import SecuPilotRuntimeService  # noqa: E402
from app.tools.persistent_case import (  # noqa: E402
    approve_action_request,
    build_initial_persistent_case_record,
    close_persistent_case,
    create_action_request_from_case,
    governed_case_close_reasons,
    has_pending_action_requests,
    persistent_case_record_to_dict,
    persistent_case_workflow_summary,
    pending_action_request_ids,
    submit_action_request_for_approval,
    transition_persistent_case_status,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
TMP_ROOT = REPO_ROOT / ".tmp_testdata"
TMP_ROOT.mkdir(exist_ok=True)


def _fresh_temp_root(name: str) -> Path:
    target = TMP_ROOT / name
    shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True, exist_ok=True)
    return target


def _workflow_summary_case() -> dict:
    return {
        "case_id": "CASE-S5C-IMPL8-SUMMARY-001",
        "version": "3.1",
        "risk_score": 8.3,
        "confidence_score": 0.88,
        "confidence_label": "HIGH",
        "verdict_status": "CRITICAL_ACTION_REQUIRED",
        "investigation_status": "COMPLETE",
        "scenario_name": "Workflow Summary Helper",
        "forensic_result": {
            "hosts_analyzed": ["WKST-047"],
            "total_suspicious_chains": 1,
            "top_chains": [],
            "attack_stages_observed": ["Execution"],
            "persistence_mechanisms": [],
            "evidence_gaps": [],
        },
        "suggested_action": {
            "type": "NETWORK_ISOLATE",
            "targets": ["WKST-047"],
            "blast_radius_desc": "synthetic isolation boundary",
        },
        "audit_trail": {"degraded": False, "degraded_reasons": []},
    }


class CaseLifecycleRegressionTests(unittest.TestCase):
    def test_governed_case_close_reasons_match_s5c2_taxonomy(self):
        self.assertEqual(
            set(governed_case_close_reasons()),
            {
                "resolved_false_positive",
                "resolved_expected_activity",
                "resolved_contained",
                "duplicate_case",
                "insufficient_evidence",
                "out_of_scope",
                "deferred_to_external_process",
            },
        )

    def test_internal_close_helper_records_governed_reason_in_audit_details(self):
        record = build_initial_persistent_case_record(
            {
                "case_id": "CASE-S5C-IMPL6-CLOSE-001",
                "version": "3.1",
                "risk_score": 4.0,
                "confidence_score": 0.72,
                "confidence_label": "MEDIUM",
                "verdict_status": "REVIEW_REQUIRED",
                "investigation_status": "COMPLETE",
                "scenario_name": "Close Reason Semantics",
                "forensic_result": {
                    "hosts_analyzed": ["WKST-047"],
                    "total_suspicious_chains": 0,
                    "top_chains": [],
                    "attack_stages_observed": [],
                    "persistence_mechanisms": [],
                    "evidence_gaps": [],
                },
                "suggested_action": {},
                "audit_trail": {"degraded": False, "degraded_reasons": []},
            },
            snapshot_id="S5-C-IMPL6-CLOSE-001",
            actor="analyst.leo",
            created_at_utc="2026-04-20T09:00:00Z",
        )

        closed = close_persistent_case(
            record,
            actor="manager.chen",
            close_reason="insufficient_evidence",
            reason="synthetic close reason validation",
            at_utc="2026-04-20T09:05:00Z",
        )

        self.assertEqual(closed.lifecycle_status, "closed")
        final_audit = closed.lifecycle_audit[-1]
        self.assertEqual(final_audit.event_type, "case_closed")
        self.assertEqual(final_audit.actor, "manager.chen")
        self.assertEqual(final_audit.reason, "synthetic close reason validation")
        self.assertEqual(final_audit.details, {"close_reason": "insufficient_evidence"})

    def test_internal_close_helper_rejects_unknown_close_reason(self):
        record = build_initial_persistent_case_record(
            {
                "case_id": "CASE-S5C-IMPL6-CLOSE-INVALID",
                "version": "3.1",
                "risk_score": 4.0,
                "confidence_score": 0.72,
                "confidence_label": "MEDIUM",
                "verdict_status": "REVIEW_REQUIRED",
                "investigation_status": "COMPLETE",
                "scenario_name": "Invalid Close Reason",
                "forensic_result": {
                    "hosts_analyzed": ["WKST-047"],
                    "total_suspicious_chains": 0,
                    "top_chains": [],
                    "attack_stages_observed": [],
                    "persistence_mechanisms": [],
                    "evidence_gaps": [],
                },
                "suggested_action": {},
                "audit_trail": {"degraded": False, "degraded_reasons": []},
            },
            snapshot_id="S5-C-IMPL6-CLOSE-INVALID",
            actor="analyst.leo",
            created_at_utc="2026-04-20T09:10:00Z",
        )

        with self.assertRaisesRegex(ValueError, "invalid_case_close_reason:archived"):
            close_persistent_case(
                record,
                actor="manager.chen",
                close_reason="archived",
                reason="invalid close reason",
                at_utc="2026-04-20T09:11:00Z",
            )

    def test_internal_close_helper_rejects_closed_to_closed_transition(self):
        record = build_initial_persistent_case_record(
            {
                "case_id": "CASE-S5C-IMPL6-DOUBLE-CLOSE",
                "version": "3.1",
                "risk_score": 4.0,
                "confidence_score": 0.72,
                "confidence_label": "MEDIUM",
                "verdict_status": "REVIEW_REQUIRED",
                "investigation_status": "COMPLETE",
                "scenario_name": "Double Close Boundary",
                "forensic_result": {
                    "hosts_analyzed": ["WKST-047"],
                    "total_suspicious_chains": 0,
                    "top_chains": [],
                    "attack_stages_observed": [],
                    "persistence_mechanisms": [],
                    "evidence_gaps": [],
                },
                "suggested_action": {},
                "audit_trail": {"degraded": False, "degraded_reasons": []},
            },
            snapshot_id="S5-C-IMPL6-DOUBLE-CLOSE",
            actor="analyst.leo",
            created_at_utc="2026-04-20T09:20:00Z",
        )
        closed = close_persistent_case(
            record,
            actor="manager.chen",
            close_reason="resolved_false_positive",
            reason="first synthetic close",
            at_utc="2026-04-20T09:21:00Z",
        )

        with self.assertRaisesRegex(ValueError, "invalid_case_status_transition:closed->closed"):
            close_persistent_case(
                closed,
                actor="manager.chen",
                close_reason="duplicate_case",
                reason="second synthetic close",
                at_utc="2026-04-20T09:22:00Z",
            )

    def test_reopen_from_closed_case_records_reopen_audit_and_preserves_close_reason(self):
        record = build_initial_persistent_case_record(
            {
                "case_id": "CASE-S5C-IMPL12-REOPEN-AUDIT",
                "version": "3.1",
                "risk_score": 5.1,
                "confidence_score": 0.74,
                "confidence_label": "MEDIUM",
                "verdict_status": "REVIEW_REQUIRED",
                "investigation_status": "COMPLETE",
                "scenario_name": "Reopen Lifecycle Audit",
                "forensic_result": {
                    "hosts_analyzed": ["WKST-047"],
                    "total_suspicious_chains": 0,
                    "top_chains": [],
                    "attack_stages_observed": [],
                    "persistence_mechanisms": [],
                    "evidence_gaps": [],
                },
                "suggested_action": {},
                "audit_trail": {"degraded": False, "degraded_reasons": []},
            },
            snapshot_id="S5C-IMPL12-REOPEN-LIFECYCLE-AUDIT",
            actor="analyst.leo",
            created_at_utc="2026-04-21T08:00:00Z",
        )
        closed = close_persistent_case(
            record,
            actor="manager.chen",
            close_reason="resolved_false_positive",
            reason="close before reopen regression",
            at_utc="2026-04-21T08:01:00Z",
        )

        reopened = transition_persistent_case_status(
            closed,
            to_status="open",
            actor="manager.chen",
            reason="reopen after additional review",
            at_utc="2026-04-21T08:02:00Z",
        )

        self.assertEqual(reopened.lifecycle_status, "open")
        self.assertEqual(reopened.lifecycle_audit[-1].event_type, "case_reopened")
        self.assertEqual(reopened.lifecycle_audit[-1].case_status, "open")
        self.assertEqual(reopened.lifecycle_audit[-1].reason, "reopen after additional review")
        self.assertEqual(reopened.lifecycle_audit[-2].details["close_reason"], "resolved_false_positive")

    def test_workflow_summary_tracks_pending_approved_and_closed_sources_without_mutation(self):
        record = build_initial_persistent_case_record(
            _workflow_summary_case(),
            snapshot_id="S5C-IMPL8-SUMMARY-001",
            actor="analyst.leo",
            created_at_utc="2026-04-20T10:00:00Z",
        )
        before_summary = persistent_case_record_to_dict(record)

        open_summary = persistent_case_workflow_summary(record)
        self.assertEqual(open_summary["lifecycle_status"], "open")
        self.assertEqual(open_summary["pending_action_request_count"], 0)
        self.assertEqual(open_summary["action_request_counts"]["pending_approval"], 0)
        self.assertEqual(open_summary["latest_audit_event_type"], "case_created")
        self.assertFalse(open_summary["execution_authorized"])
        self.assertNotIn("close_reason", open_summary)

        self.assertEqual(persistent_case_record_to_dict(record), before_summary)

        drafted = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="synthetic summary approval request",
            at_utc="2026-04-20T10:01:00Z",
        )
        submitted = submit_action_request_for_approval(
            drafted,
            action_request_id=drafted.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="submit for workflow summary",
            at_utc="2026-04-20T10:02:00Z",
        )

        submitted_summary = persistent_case_workflow_summary(submitted)
        self.assertEqual(submitted_summary["lifecycle_status"], "in_review")
        self.assertEqual(submitted_summary["review_owner"], "manager.chen")
        self.assertEqual(submitted_summary["pending_action_request_count"], 1)
        self.assertEqual(
            pending_action_request_ids(submitted),
            (submitted.action_requests[0].action_request_id,),
        )
        self.assertTrue(has_pending_action_requests(submitted))
        self.assertEqual(submitted_summary["action_request_counts"]["pending_approval"], 1)
        self.assertEqual(submitted_summary["latest_audit_event_type"], "action_request_submitted")
        self.assertEqual(submitted_summary["latest_audit_reason"], "submit for workflow summary")

        approved = approve_action_request(
            submitted,
            action_request_id=submitted.action_requests[0].action_request_id,
            actor="manager.chen",
            reason="approve summary request",
            at_utc="2026-04-20T10:03:00Z",
        )
        approved_summary = persistent_case_workflow_summary(approved)
        self.assertEqual(approved_summary["lifecycle_status"], "approved")
        self.assertEqual(approved_summary["action_request_counts"]["approved"], 1)
        self.assertEqual(approved_summary["pending_action_request_count"], 0)
        self.assertEqual(pending_action_request_ids(approved), ())
        self.assertFalse(has_pending_action_requests(approved))
        self.assertFalse(approved_summary["execution_authorized"])

        closed = close_persistent_case(
            approved,
            actor="manager.chen",
            close_reason="resolved_contained",
            reason="close after summary review",
            at_utc="2026-04-20T10:04:00Z",
        )
        closed_summary = persistent_case_workflow_summary(closed)
        self.assertEqual(closed_summary["lifecycle_status"], "closed")
        self.assertEqual(closed_summary["latest_audit_event_type"], "case_closed")
        self.assertEqual(closed_summary["latest_audit_reason"], "close after summary review")
        self.assertEqual(closed_summary["close_reason"], "resolved_contained")

    def test_workflow_summary_mutation_does_not_change_future_summary(self):
        record = build_initial_persistent_case_record(
            _workflow_summary_case(),
            snapshot_id="S5C-IMPL14-WORKFLOW-SUMMARY-IMMUTABILITY",
            actor="analyst.leo",
            created_at_utc="2026-04-22T10:00:00Z",
        )
        drafted = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="synthetic immutability request",
            at_utc="2026-04-22T10:01:00Z",
        )
        submitted = submit_action_request_for_approval(
            drafted,
            action_request_id=drafted.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="submit before summary mutation",
            at_utc="2026-04-22T10:02:00Z",
        )

        first_summary = persistent_case_workflow_summary(submitted)
        first_summary["lifecycle_status"] = "closed"
        first_summary["pending_action_request_count"] = 0
        first_summary["execution_authorized"] = True
        first_summary["action_request_counts"]["pending_approval"] = 0
        first_summary["action_request_counts"]["approved"] = 99

        second_summary = persistent_case_workflow_summary(submitted)

        self.assertIsNot(first_summary, second_summary)
        self.assertIsNot(first_summary["action_request_counts"], second_summary["action_request_counts"])
        self.assertEqual(second_summary["lifecycle_status"], "in_review")
        self.assertEqual(second_summary["pending_action_request_count"], 1)
        self.assertEqual(second_summary["action_request_counts"]["pending_approval"], 1)
        self.assertEqual(second_summary["action_request_counts"]["approved"], 0)
        self.assertFalse(second_summary["execution_authorized"])

    def test_pending_action_request_helpers_detect_closed_pending_case_without_mutation(self):
        record = build_initial_persistent_case_record(
            _workflow_summary_case(),
            snapshot_id="S5C-IMPL10-PENDING-HELPERS-002",
            actor="analyst.leo",
            created_at_utc="2026-04-20T11:10:00Z",
        )
        drafted = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="synthetic pending helper close boundary",
            at_utc="2026-04-20T11:11:00Z",
        )
        submitted = submit_action_request_for_approval(
            drafted,
            action_request_id=drafted.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="submit before close boundary",
            at_utc="2026-04-20T11:12:00Z",
        )
        closed = close_persistent_case(
            submitted,
            actor="manager.chen",
            close_reason="insufficient_evidence",
            reason="close without deciding pending request",
            at_utc="2026-04-20T11:13:00Z",
        )
        before_closed = persistent_case_record_to_dict(closed)

        self.assertEqual(closed.lifecycle_status, "closed")
        self.assertEqual(
            pending_action_request_ids(closed),
            (submitted.action_requests[0].action_request_id,),
        )
        self.assertTrue(has_pending_action_requests(closed))
        self.assertEqual(persistent_case_record_to_dict(closed), before_closed)

    def test_create_retrieve_review_approve_close_lifecycle_is_deterministic(self):
        temp_dir = _fresh_temp_root("case_lifecycle_regression")
        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="mock",
                mock_data_path="./mock_data",
                case_store_path=str(temp_dir / "cases.sqlite3"),
            )
        )

        threat_case = {
            "case_id": "CASE-LIFECYCLE-001",
            "version": "3.1",
            "risk_score": 9.2,
            "confidence_score": 0.92,
            "confidence_label": "HIGH",
            "verdict_status": "CRITICAL_ACTION_REQUIRED",
            "investigation_status": "COMPLETE",
            "scenario_name": "Lifecycle Regression",
            "forensic_result": {
                "hosts_analyzed": ["WKST-047"],
                "total_suspicious_chains": 1,
                "top_chains": [],
                "attack_stages_observed": ["Execution"],
                "persistence_mechanisms": [],
                "evidence_gaps": [],
            },
            "suggested_action": {
                "type": "NETWORK_ISOLATE",
                "targets": ["WKST-047"],
                "blast_radius_desc": "隔离影响 3 个级联资产",
            },
            "audit_trail": {"degraded": False, "degraded_reasons": []},
        }
        # Keep the lifecycle create step on the runtime-service path while
        # fixing the investigation output for deterministic audit assertions.
        with patch.object(
            service,
            "_execute_investigation",
            return_value=(
                200,
                {"status": "ok"},
                {
                    "intent": "threat_hunt",
                    "time_range": "24h",
                    "user_input": "请检查最近是否有横向移动",
                },
                threat_case,
            ),
        ):
            create_status, create_payload = service.create_case_sync({
                "user_input": "请检查最近是否有横向移动",
                "intent": "threat_hunt",
                "time_range": "24h",
                "actor": "analyst.leo",
            })
        self.assertEqual(create_status, 201)
        case_id = create_payload["case_id"]

        retrieve_status, retrieve_payload = service.get_case_sync(case_id)
        self.assertEqual(retrieve_status, 200)
        self.assertEqual(retrieve_payload["persistent_case"]["case_id"], case_id)
        self.assertEqual(retrieve_payload["persistent_case"]["lifecycle_status"], "open")

        draft_status, draft_payload = service.create_action_request_sync(case_id, {
            "actor": "analyst.leo",
            "rationale": "需要先走审批再执行处置",
        })
        self.assertEqual(draft_status, 201)
        action_request_id = draft_payload["action_request_id"]

        submit_status, submit_payload = service.submit_action_request_sync(case_id, action_request_id, {
            "actor": "analyst.leo",
            "review_owner": "manager.chen",
            "reason": "提交审批",
        })
        self.assertEqual(submit_status, 200)
        self.assertEqual(submit_payload["persistent_case"]["lifecycle_status"], "in_review")
        self.assertEqual(submit_payload["action_request"]["status"], "pending_approval")

        approve_status, approve_payload = service.approve_action_request_sync(case_id, action_request_id, {
            "actor": "manager.chen",
            "reason": "证据充分，批准执行",
        })
        self.assertEqual(approve_status, 200)
        self.assertEqual(approve_payload["persistent_case"]["lifecycle_status"], "approved")
        self.assertEqual(approve_payload["action_request"]["status"], "approved")

        record = service._require_case_store().get_case(case_id)
        self.assertIsNotNone(record)
        closed = transition_persistent_case_status(
            record,
            to_status="closed",
            actor="manager.chen",
            reason="处置完成，关闭案例",
            at_utc="2026-04-10T12:00:00Z",
        )
        service._require_case_store().save_case(closed)

        closed_status, closed_payload = service.get_case_sync(case_id)
        self.assertEqual(closed_status, 200)
        persistent_case = closed_payload["persistent_case"]
        self.assertEqual(persistent_case["case_id"], case_id)
        self.assertIn(persistent_case["lifecycle_status"], {"open", "in_review", "approved", "closed"})
        self.assertEqual(persistent_case["lifecycle_status"], "closed")
        self.assertEqual(len(persistent_case["action_requests"]), 1)
        action_request = persistent_case["action_requests"][0]
        self.assertEqual(action_request["status"], "approved")
        self.assertEqual(action_request["action_request_id"], action_request_id)
        self.assertEqual(action_request["decision_by"], "manager.chen")
        self.assertEqual(action_request["decision_reason"], "证据充分，批准执行")
        lifecycle_audit = persistent_case["lifecycle_audit"]
        self.assertEqual(len(lifecycle_audit), 7)
        final_audit = lifecycle_audit[-1]
        self.assertEqual(final_audit["event_type"], "case_closed")
        self.assertEqual(final_audit["actor"], "manager.chen")
        self.assertEqual(final_audit["reason"], "处置完成，关闭案例")
        event_types = [entry["event_type"] for entry in lifecycle_audit]
        self.assertNotIn("action_request_rejected", event_types)
        self.assertNotIn("action_request_cancelled", event_types)
        self.assertEqual(
            event_types,
            [
                "case_created",
                "action_request_created",
                "status_changed",
                "action_request_submitted",
                "status_changed",
                "action_request_approved",
                "case_closed",
            ],
        )

    def test_retrieval_after_close_keeps_schema_stable(self):
        temp_dir = _fresh_temp_root("case_lifecycle_retrieve_after_close")
        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="mock",
                mock_data_path="./mock_data",
                case_store_path=str(temp_dir / "cases.sqlite3"),
            )
        )

        create_status, create_payload = service.create_case_sync({
            "user_input": "请检查最近是否有横向移动",
            "intent": "threat_hunt",
            "time_range": "24h",
            "actor": "analyst.leo",
        })
        self.assertEqual(create_status, 201)
        case_id = create_payload["case_id"]

        record = service._require_case_store().get_case(case_id)
        self.assertIsNotNone(record)
        closed = transition_persistent_case_status(
            record,
            to_status="closed",
            actor="manager.chen",
            reason="人工关闭",
            at_utc="2026-04-10T12:10:00Z",
        )
        service._require_case_store().save_case(closed)

        first_status, first_payload = service.get_case_sync(case_id)
        self.assertEqual(first_status, 200)
        self.assertIn("action_requests", first_payload["persistent_case"])
        self.assertIn("lifecycle_audit", first_payload["persistent_case"])
        first_audit_length = len(first_payload["persistent_case"]["lifecycle_audit"])
        self.assertEqual(first_payload["persistent_case"]["lifecycle_audit"][-1]["event_type"], "case_closed")
        first_payload["persistent_case"]["case_view"]["executive_summary"]["verdict"] = "BROKEN"

        second_status, second_payload = service.get_case_sync(case_id)
        self.assertEqual(second_status, 200)
        self.assertIsNot(first_payload, second_payload)
        self.assertIsNot(first_payload["persistent_case"], second_payload["persistent_case"])
        self.assertIn("action_requests", second_payload["persistent_case"])
        self.assertIn("lifecycle_audit", second_payload["persistent_case"])
        self.assertEqual(len(second_payload["persistent_case"]["lifecycle_audit"]), first_audit_length)
        self.assertEqual(second_payload["persistent_case"]["lifecycle_audit"][-1]["event_type"], "case_closed")
        self.assertIn(second_payload["persistent_case"]["lifecycle_status"], {"open", "in_review", "approved", "closed"})
        self.assertEqual(second_payload["persistent_case"]["lifecycle_status"], "closed")
        self.assertNotEqual(
            second_payload["persistent_case"]["case_view"]["executive_summary"]["verdict"],
            "BROKEN",
        )
        self.assertIn("recommended_action", second_payload["persistent_case"]["case_view"])

    def test_invalid_lifecycle_status_transition_is_rejected(self):
        record = build_initial_persistent_case_record(
            {
                "case_id": "CASE-LIFECYCLE-INVALID-001",
                "version": "3.1",
                "risk_score": 4.0,
                "confidence_score": 0.72,
                "confidence_label": "MEDIUM",
                "verdict_status": "REVIEW_REQUIRED",
                "investigation_status": "COMPLETE",
                "scenario_name": "Invalid Lifecycle Transition",
                "forensic_result": {
                    "hosts_analyzed": ["WKST-047"],
                    "total_suspicious_chains": 0,
                    "top_chains": [],
                    "attack_stages_observed": [],
                    "persistence_mechanisms": [],
                    "evidence_gaps": [],
                },
                "suggested_action": {},
                "audit_trail": {"degraded": False, "degraded_reasons": []},
            },
            snapshot_id="S5-C-IMPL-2026-04-14-002",
            actor="analyst.leo",
            created_at_utc="2026-04-10T12:19:00Z",
        )
        closed = transition_persistent_case_status(
            record,
            to_status="closed",
            actor="manager.chen",
            reason="人工关闭",
            at_utc="2026-04-10T12:20:00Z",
        )

        with self.assertRaisesRegex(ValueError, "invalid_case_status_transition:closed->archived"):
            transition_persistent_case_status(
                closed,
                to_status="archived",
                actor="manager.chen",
                reason="invalid future status",
                at_utc="2026-04-10T12:21:00Z",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
