import unittest
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from app.tools.persistent_case import (  # noqa: E402
    CASE_STORAGE_SCHEMA_VERSION,
    PERSISTENCE_BACKEND,
    allowed_case_status_transitions,
    build_action_request_seed,
    build_initial_persistent_case_record,
    frozen_persistence_backend,
    is_valid_case_status_transition,
    persistent_case_record_to_dict,
)
from backend.app.config import Settings  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]


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
            {
                "node_id": f"{host}:chain-000:node-003",
                "process_name": "mimikatz.exe",
                "anomalies": [{"type": "known_attack_tool", "risk": 10, "mitre": "T1003.001", "desc": "Credential dump"}],
            },
        ],
    }


def _base_case():
    return {
        "case_id": "CASE-S4C-001",
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


class PersistentCaseContractTests(unittest.TestCase):
    def test_initial_record_aligns_with_case_view_contract(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S4-C-2026-04-10-001",
            actor="analyst.leo",
            created_at_utc="2026-04-10T10:00:00Z",
        )

        self.assertEqual(record.schema_version, CASE_STORAGE_SCHEMA_VERSION)
        self.assertEqual(record.storage_backend, PERSISTENCE_BACKEND)
        self.assertEqual(record.lifecycle_status, "open")
        self.assertEqual(record.case_id, "CASE-S4C-001")
        self.assertEqual(record.case_view["executive_summary"]["verdict"], "CRITICAL_ACTION_REQUIRED")
        self.assertEqual(record.case_view["recommended_action"]["action_type"], "NETWORK_ISOLATE")
        self.assertEqual(record.action_requests, [])
        self.assertEqual(len(record.lifecycle_audit), 1)
        self.assertEqual(record.lifecycle_audit[0].event_type, "case_created")

    def test_status_transition_matrix_is_explicit(self):
        self.assertTrue(is_valid_case_status_transition("open", "in_review"))
        self.assertTrue(is_valid_case_status_transition("in_review", "approved"))
        self.assertTrue(is_valid_case_status_transition("approved", "closed"))
        self.assertTrue(is_valid_case_status_transition("closed", "open"))
        self.assertFalse(is_valid_case_status_transition("open", "approved"))
        self.assertEqual(allowed_case_status_transitions("open"), ("closed", "in_review"))

    def test_action_request_seed_is_first_class_and_non_destructive(self):
        request = build_action_request_seed(
            _base_case(),
            actor="analyst.leo",
            rationale="需要先进入审批流，不直接执行隔离",
            requested_at_utc="2026-04-10T10:01:00Z",
        )

        self.assertIsNotNone(request)
        self.assertEqual(request.status, "draft")
        self.assertEqual(request.action_type, "NETWORK_ISOLATE")
        self.assertEqual(request.targets, ["WKST-047"])
        self.assertTrue(request.approval_required)

    def test_backend_choice_is_frozen_to_sqlite_local(self):
        configured = Settings(project_root=str(REPO_ROOT), case_store_path="./data/cases.sqlite3")
        backend = frozen_persistence_backend(configured)

        self.assertEqual(backend.backend, "sqlite_local")
        self.assertIn("cases.sqlite3", backend.store_path)
        self.assertIn("local", backend.sovereignty_alignment.lower())
        self.assertIn("audit", backend.audit_alignment.lower())

    def test_record_round_trips_to_plain_dict(self):
        record = build_initial_persistent_case_record(
            _base_case(),
            snapshot_id="S4-C-2026-04-10-001",
            created_at_utc="2026-04-10T10:00:00Z",
        )
        payload = persistent_case_record_to_dict(record)

        self.assertEqual(payload["case_id"], "CASE-S4C-001")
        self.assertEqual(payload["lifecycle_status"], "open")
        self.assertEqual(payload["case_view"]["executive_summary"]["verdict"], "CRITICAL_ACTION_REQUIRED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
