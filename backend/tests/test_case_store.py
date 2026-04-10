import shutil
import unittest
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.config import Settings  # noqa: E402
from app.tools.case_store import SQLitePersistentCaseStore  # noqa: E402
from app.tools.persistent_case import (  # noqa: E402
    append_action_request_record,
    build_action_request_seed,
    build_initial_persistent_case_record,
    persistent_case_record_to_dict,
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
