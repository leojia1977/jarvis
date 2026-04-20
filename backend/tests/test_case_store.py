import shutil
import unittest
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.config import Settings  # noqa: E402
from app.tools.case_store import SQLitePersistentCaseStore  # noqa: E402
from app.tools.persistent_case import (  # noqa: E402
    append_action_request_record,
    approve_action_request,
    build_action_request_seed,
    build_initial_persistent_case_record,
    cancel_action_request,
    close_persistent_case,
    create_action_request_from_case,
    persistent_case_record_from_dict,
    persistent_case_record_to_dict,
    reject_action_request,
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
        "case_id": "CASE-S4C-STORE-001",
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


class CaseStoreTests(unittest.TestCase):
    def test_sqlite_store_round_trips_without_mutating_stored_case(self):
        temp_dir = _fresh_temp_root("case_store_roundtrip")
        settings = Settings(
            project_root=str(temp_dir),
            case_store_path="./data/secupilot_case_store.sqlite3",
        )
        store = SQLitePersistentCaseStore(settings)
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S4-C-2026-04-10-002",
            actor="analyst.leo",
            created_at_utc="2026-04-10T10:10:00Z",
        )

        store.save_case(record)
        first = store.get_case(record.case_id)
        second = store.get_case(record.case_id)

        self.assertIsNotNone(first)
        self.assertIsNotNone(second)
        first.threat_case["verdict_status"] = "BROKEN"
        self.assertEqual(second.threat_case["verdict_status"], "CRITICAL_ACTION_REQUIRED")

    def test_sqlite_store_creates_parent_directory(self):
        temp_dir = _fresh_temp_root("case_store_parent")
        settings = Settings(
            project_root=str(temp_dir),
            case_store_path="./data/nested/cases.sqlite3",
        )
        store = SQLitePersistentCaseStore(settings)
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S4-C-2026-04-10-002",
        )

        store.save_case(record)

        self.assertTrue((Path(temp_dir) / "data" / "nested").exists())
        self.assertTrue(settings.get_case_store_path().exists())

    def test_append_and_transition_helpers_return_new_record_versions(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S4-C-2026-04-10-002",
            created_at_utc="2026-04-10T10:10:00Z",
        )

        request_one = build_action_request_seed(
            _base_case(),
            actor="analyst.leo",
            rationale="进入审批流",
            requested_at_utc="2026-04-10T10:11:00Z",
            existing_requests=record.action_requests,
        )
        updated = append_action_request_record(
            record,
            request_one,
            updated_at_utc="2026-04-10T10:11:00Z",
        )
        request_two = build_action_request_seed(
            _base_case(),
            actor="analyst.leo",
            rationale="第二个审批请求",
            requested_at_utc="2026-04-10T10:12:00Z",
            existing_requests=updated.action_requests,
        )
        reviewed = transition_persistent_case_status(
            updated,
            to_status="in_review",
            actor="analyst.leo",
            review_owner="analyst.leo",
            reason="开始人工复核",
            at_utc="2026-04-10T10:13:00Z",
        )

        self.assertEqual(record.action_requests, [])
        self.assertEqual(updated.action_requests[0].action_request_id, "CASE-S4C-STORE-001:action-001")
        self.assertEqual(request_two.action_request_id, "CASE-S4C-STORE-001:action-002")
        self.assertEqual(reviewed.lifecycle_status, "in_review")
        self.assertEqual(reviewed.lifecycle_audit[-1].event_id, "CASE-S4C-STORE-001:audit-002")
        self.assertEqual(record.lifecycle_status, "open")

    def test_in_review_transition_requires_owner(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S4-C-2026-04-10-002",
        )

        with self.assertRaisesRegex(ValueError, "review_owner_required_for_in_review"):
            transition_persistent_case_status(
                record,
                to_status="in_review",
                actor="analyst.leo",
                reason="开始人工复核",
            )

    def test_store_returns_plain_dict_shape_via_record_serializer(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S4-C-2026-04-10-002",
        )
        payload = persistent_case_record_to_dict(record)

        self.assertEqual(payload["case_id"], "CASE-S4C-STORE-001")
        self.assertEqual(payload["lifecycle_status"], "open")
        self.assertEqual(payload["case_view"]["recommended_action"]["action_type"], "NETWORK_ISOLATE")

    def test_action_request_and_audit_serializer_round_trip_remains_replayable(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S5-C-IMPL5-STORE-001",
            actor="analyst.leo",
            created_at_utc="2026-04-10T10:00:00Z",
        )
        drafted = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="synthetic approval request",
            at_utc="2026-04-10T10:01:00Z",
        )
        submitted = submit_action_request_for_approval(
            drafted,
            action_request_id=drafted.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="submit synthetic request",
            at_utc="2026-04-10T10:02:00Z",
        )
        rejected = reject_action_request(
            submitted,
            action_request_id=submitted.action_requests[0].action_request_id,
            actor="manager.chen",
            reason="synthetic request rejected",
            at_utc="2026-04-10T10:03:00Z",
        )

        restored = persistent_case_record_from_dict(persistent_case_record_to_dict(rejected))

        self.assertEqual(persistent_case_record_to_dict(restored), persistent_case_record_to_dict(rejected))
        self.assertEqual(restored.lifecycle_status, "in_review")
        self.assertEqual(restored.action_requests[0].status, "rejected")
        self.assertEqual(restored.action_requests[0].rationale, "synthetic approval request")
        self.assertEqual(restored.action_requests[0].decision_reason, "synthetic request rejected")
        self.assertEqual(
            [entry.event_type for entry in restored.lifecycle_audit],
            [
                "case_created",
                "action_request_created",
                "status_changed",
                "action_request_submitted",
                "action_request_rejected",
            ],
        )
        self.assertEqual(
            [entry.event_id for entry in restored.lifecycle_audit],
            [
                "CASE-S4C-STORE-001:audit-001",
                "CASE-S4C-STORE-001:audit-002",
                "CASE-S4C-STORE-001:audit-003",
                "CASE-S4C-STORE-001:audit-004",
                "CASE-S4C-STORE-001:audit-005",
            ],
        )

    def test_close_reason_audit_details_survive_serializer_round_trip(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S5-C-IMPL6-STORE-001",
            actor="analyst.leo",
            created_at_utc="2026-04-20T09:30:00Z",
        )
        closed = close_persistent_case(
            record,
            actor="manager.chen",
            close_reason="resolved_expected_activity",
            reason="synthetic expected activity close",
            at_utc="2026-04-20T09:31:00Z",
        )

        restored = persistent_case_record_from_dict(persistent_case_record_to_dict(closed))

        self.assertEqual(restored.lifecycle_status, "closed")
        final_audit = restored.lifecycle_audit[-1]
        self.assertEqual(final_audit.event_type, "case_closed")
        self.assertEqual(final_audit.reason, "synthetic expected activity close")
        self.assertEqual(final_audit.details, {"close_reason": "resolved_expected_activity"})
        self.assertNotIn("close_reason", persistent_case_record_to_dict(restored))

    def test_closed_case_serializer_round_trip_rejects_action_request_mutations(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S5-C-IMPL5-STORE-002",
            actor="analyst.leo",
            created_at_utc="2026-04-10T11:00:00Z",
        )
        drafted = create_action_request_from_case(
            record,
            actor="analyst.leo",
            rationale="synthetic closed-case request",
            at_utc="2026-04-10T11:01:00Z",
        )
        submitted = submit_action_request_for_approval(
            drafted,
            action_request_id=drafted.action_requests[0].action_request_id,
            actor="analyst.leo",
            review_owner="manager.chen",
            reason="submit before close",
            at_utc="2026-04-10T11:02:00Z",
        )
        closed = transition_persistent_case_status(
            submitted,
            to_status="closed",
            actor="manager.chen",
            reason="synthetic close",
            at_utc="2026-04-10T11:03:00Z",
        )

        restored = persistent_case_record_from_dict(persistent_case_record_to_dict(closed))

        action_request_id = restored.action_requests[0].action_request_id
        with self.assertRaisesRegex(ValueError, "action_request_not_allowed_for_closed_case"):
            create_action_request_from_case(
                restored,
                actor="analyst.leo",
                rationale="closed case must reject create",
                at_utc="2026-04-10T11:04:00Z",
            )
        with self.assertRaisesRegex(ValueError, "action_request_not_allowed_for_closed_case"):
            submit_action_request_for_approval(
                restored,
                action_request_id=action_request_id,
                actor="analyst.leo",
                review_owner="manager.chen",
                reason="closed case must reject submit",
                at_utc="2026-04-10T11:05:00Z",
            )
        with self.assertRaisesRegex(ValueError, "action_request_not_allowed_for_closed_case"):
            approve_action_request(
                restored,
                action_request_id=action_request_id,
                actor="manager.chen",
                reason="closed case must reject approve",
                at_utc="2026-04-10T11:06:00Z",
            )
        with self.assertRaisesRegex(ValueError, "action_request_not_allowed_for_closed_case"):
            reject_action_request(
                restored,
                action_request_id=action_request_id,
                actor="manager.chen",
                reason="closed case must reject reject",
                at_utc="2026-04-10T11:07:00Z",
            )
        with self.assertRaisesRegex(ValueError, "action_request_not_allowed_for_closed_case"):
            cancel_action_request(
                restored,
                action_request_id=action_request_id,
                actor="manager.chen",
                reason="closed case must reject cancel",
                at_utc="2026-04-10T11:08:00Z",
            )

        self.assertEqual(restored.lifecycle_status, "closed")
        self.assertEqual(restored.action_requests[0].status, "pending_approval")
        self.assertEqual(restored.lifecycle_audit[-1].event_type, "case_closed")


if __name__ == "__main__":
    unittest.main(verbosity=2)
