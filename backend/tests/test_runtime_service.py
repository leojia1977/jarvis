import unittest
import shutil
from pathlib import Path
from unittest.mock import patch

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.config import Settings
from backend.app.runtime_service import SecuPilotRuntimeService
from app.tools.case_store import load_current_snapshot_id
from app.tools.persistent_case import build_initial_persistent_case_record
from app.tools.siem_adapter import ProductionSIEMAdapter


REPO_ROOT = Path(__file__).resolve().parents[2]
TMP_ROOT = REPO_ROOT / ".tmp_testdata"
TMP_ROOT.mkdir(exist_ok=True)


def _fresh_temp_root(name: str) -> Path:
    target = TMP_ROOT / name
    shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True, exist_ok=True)
    return target


class FakeProductionTransport:
    def __init__(self):
        self.calls = []

    async def post_json(self, endpoint, payload, *, headers, timeout_seconds):
        self.calls.append({"endpoint": endpoint, "payload": payload})
        if endpoint.endswith("/alerts/intent"):
            return {
                "status": "ok",
                "results": [
                    {
                        "event_id": "SPL-ALERT-1",
                        "severity": "high",
                        "timestamp": "2026-04-08T11:00:00Z",
                        "action": "SSH_BRUTE_FORCE",
                        "src_ip": "185.220.101.45",
                        "dest_asset": "WKST-047",
                        "dest_ip": "10.1.2.4",
                        "scenario": "S-02",
                    }
                ],
                "metadata": {"source": "splunk"},
            }
        if endpoint.endswith("/metadata/scenario"):
            return {
                "status": "ok",
                "results": [
                    {
                        "scenario_id": "S-02",
                        "name": "Lateral Movement",
                        "kill_chain": "lateral_movement",
                        "action": {"type": "NETWORK_ISOLATE"},
                    }
                ],
            }
        if endpoint.endswith("/metadata/asset"):
            return {
                "status": "ok",
                "results": [
                    {
                        "asset_id": "WKST-047",
                        "hostname": "WKST-047",
                        "owner": "SOC",
                    }
                ],
            }
        return {"status": "ok", "data": {}}


class _InMemoryCaseStore:
    def __init__(self):
        self.records = {}

    def save_case(self, record):
        self.records[record.case_id] = record
        return record

    def get_case(self, case_id):
        return self.records.get(case_id)

    def get_runtime_stats(self):
        return {
            "backend": "memory_test",
            "store_path": ":memory:",
            "retention_days": 0,
            "stored_cases": len(self.records),
        }


class RuntimeServiceTests(unittest.TestCase):
    def setUp(self):
        self.mock_settings = Settings(
            runtime_mode="mock",
            mock_data_path="./mock_data",
            service_name="secupilot-runtime",
            service_version="3.2.0-s3a",
        )

    def test_health_endpoint_payload(self):
        service = SecuPilotRuntimeService(self.mock_settings)
        payload = service.health()
        self.assertEqual(payload["status"], "healthy")
        self.assertEqual(payload["state_class"], "READY")
        self.assertEqual(payload["failure_category"], "none")
        self.assertEqual(payload["service"], "secupilot-runtime")

    def test_readiness_in_mock_mode(self):
        service = SecuPilotRuntimeService(self.mock_settings)
        payload = service.readiness()
        self.assertTrue(payload["ready"])
        self.assertEqual(payload["state_class"], "READY")
        self.assertEqual(payload["failure_category"], "none")
        self.assertGreaterEqual(payload["scenarios_loaded"], 1)
        self.assertGreaterEqual(payload["process_event_hosts"], 1)
        self.assertEqual(payload["adapter_type"], "MockSIEMAdapter")

    def test_investigate_returns_case(self):
        service = SecuPilotRuntimeService(self.mock_settings)
        status_code, payload = service.investigate_sync({
            "user_input": "请检查最近是否有横向移动",
            "intent": "threat_hunt",
            "time_range": "24h",
        })
        self.assertEqual(status_code, 200)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["request"]["intent_resolved"], "threat_hunt")
        self.assertEqual(payload["request"]["time_range"], "24h")
        self.assertEqual(payload["threat_case"]["version"], "3.1")

    def test_empty_user_input_rejected(self):
        service = SecuPilotRuntimeService(self.mock_settings)
        status_code, payload = service.investigate_sync({"intent": "summarize_recent"})
        self.assertEqual(status_code, 400)
        self.assertEqual(payload["error"], "user_input_required")

    def test_production_mode_not_ready_yet(self):
        with self.assertLogs("secupilot.runtime", level="WARNING") as captured:
            service = SecuPilotRuntimeService(
                Settings(runtime_mode="production", mock_data_path="./mock_data")
            )
        readiness = service.readiness()
        self.assertFalse(readiness["ready"])
        self.assertEqual(readiness["state_class"], "MISCONFIGURED")
        self.assertEqual(readiness["failure_category"], "adapter_config")
        self.assertIn("siem_base_url", readiness["operator_message"])
        self.assertIn("production_adapter_not_configured", readiness["reasons"])
        self.assertTrue(any("runtime.context.not_ready" in line for line in captured.output))

    def test_production_mode_with_adapter_config_bootstraps(self):
        service = SecuPilotRuntimeService(
            Settings(
                runtime_mode="production",
                mock_data_path="./mock_data",
                siem_base_url="https://siem.example.local",
                siem_auth_token="secret-token",
            )
        )
        readiness = service.readiness()
        self.assertTrue(readiness["ready"])
        self.assertEqual(readiness["mode"], "production")
        self.assertEqual(readiness["state_class"], "READY")
        self.assertEqual(readiness["adapter_type"], "ProductionSIEMAdapter")
        self.assertTrue(readiness["adapter_configured"])
        self.assertTrue(readiness["static_data_present"])

    def test_production_investigate_smoke_path_returns_case(self):
        transport = FakeProductionTransport()

        def factory(mode, runtime_settings):
            self.assertEqual(mode, "production")
            return ProductionSIEMAdapter(runtime_settings, transport=transport)

        service = SecuPilotRuntimeService(
            Settings(
                runtime_mode="production",
                mock_data_path="./mock_data",
                siem_base_url="https://siem.example.local",
                siem_auth_token="secret-token",
                siem_vendor="splunk_like",
            ),
            adapter_factory=factory,
        )

        status_code, payload = service.investigate_sync({
            "user_input": "请检查是否存在横向移动",
            "intent": "threat_hunt",
            "time_range": "24h",
        })

        self.assertEqual(status_code, 200)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["request"]["runtime_mode"], "production")
        self.assertEqual(payload["threat_case"]["version"], "3.1")
        self.assertEqual(
            payload["threat_case"]["triage_summary"]["top_alerts"][0]["activity"],
            "SSH_BRUTE_FORCE",
        )
        self.assertTrue(any(call["endpoint"].endswith("/alerts/intent") for call in transport.calls))
        self.assertTrue(any(call["endpoint"].endswith("/metadata/scenario") for call in transport.calls))

    def test_pilot_smoke_path_round_trips_case_in_production_mode(self):
        transport = FakeProductionTransport()

        def factory(mode, runtime_settings):
            self.assertEqual(mode, "production")
            return ProductionSIEMAdapter(runtime_settings, transport=transport)

        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="production",
                static_data_path="./mock_data",
                siem_base_url="https://siem.example.local",
                siem_auth_token="secret-token",
                siem_vendor="splunk_like",
                edr_source_mode="local_files",
            ),
            adapter_factory=factory,
        )
        service._case_store = _InMemoryCaseStore()
        service._case_store_error = None

        status_code, payload = service.pilot_smoke_sync({
            "user_input": "请检查是否存在横向移动",
            "intent": "threat_hunt",
            "time_range": "24h",
            "actor": "pilot.operator",
        })

        self.assertEqual(status_code, 200)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["readiness"]["environment_profile"], "pilot_local")
        self.assertEqual(payload["request"]["runtime_mode"], "production")
        self.assertEqual(payload["request"]["time_range"], "24h")
        self.assertEqual(payload["persistent_case"]["case_id"], payload["case_id"])
        self.assertEqual(payload["persistent_case"]["lifecycle_status"], "open")
        self.assertEqual(
            [step["step"] for step in payload["smoke_path"]["steps"]],
            ["readiness", "investigate", "create_case", "get_case"],
        )
        self.assertEqual(payload["smoke_path"]["steps"][0]["http_status"], 200)
        self.assertEqual(payload["smoke_path"]["steps"][2]["http_status"], 201)
        self.assertIsNone(payload["smoke_path"]["failed_step"])
        self.assertTrue(any(call["endpoint"].endswith("/alerts/intent") for call in transport.calls))
        self.assertTrue(any(call["endpoint"].endswith("/metadata/scenario") for call in transport.calls))

    def test_pilot_smoke_path_reports_investigation_validation_failure(self):
        transport = FakeProductionTransport()

        def factory(mode, runtime_settings):
            self.assertEqual(mode, "production")
            return ProductionSIEMAdapter(runtime_settings, transport=transport)

        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="production",
                static_data_path="./mock_data",
                siem_base_url="https://siem.example.local",
                siem_auth_token="secret-token",
                siem_vendor="splunk_like",
                edr_source_mode="local_files",
            ),
            adapter_factory=factory,
        )
        service._case_store = _InMemoryCaseStore()
        service._case_store_error = None

        status_code, payload = service.pilot_smoke_sync({
            "user_input": "   ",
            "intent": "threat_hunt",
            "time_range": "24h",
        })

        self.assertEqual(status_code, 400)
        self.assertEqual(payload["error"], "user_input_required")
        self.assertEqual(payload["readiness"]["state_class"], "READY")
        self.assertEqual(payload["smoke_path"]["failed_step"], "investigate")
        self.assertEqual(
            [step["step"] for step in payload["smoke_path"]["steps"]],
            ["readiness", "investigate"],
        )
        self.assertEqual(payload["smoke_path"]["steps"][0]["http_status"], 200)
        self.assertEqual(payload["smoke_path"]["steps"][1]["http_status"], 400)
        self.assertEqual(payload["smoke_path"]["steps"][1]["failure_category"], "runtime")

    def test_pilot_smoke_path_reports_readiness_failure(self):
        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="production",
                static_data_path="./mock_data",
                siem_vendor="splunk_like",
                siem_base_url="https://siem.example.local",
            )
        )

        status_code, payload = service.pilot_smoke_sync({
            "user_input": "请检查是否存在横向移动",
            "intent": "threat_hunt",
        })

        self.assertEqual(status_code, 503)
        self.assertEqual(payload["error"], "pilot_smoke_not_ready")
        self.assertEqual(payload["runtime_status"]["state_class"], "MISCONFIGURED")
        self.assertEqual(payload["runtime_status"]["failure_category"], "adapter_config")
        self.assertEqual(payload["smoke_path"]["failed_step"], "readiness")
        self.assertEqual(payload["smoke_path"]["steps"][0]["http_status"], 503)

    def test_pilot_smoke_path_reports_case_store_failure_stage(self):
        transport = FakeProductionTransport()

        def factory(mode, runtime_settings):
            self.assertEqual(mode, "production")
            return ProductionSIEMAdapter(runtime_settings, transport=transport)

        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="production",
                static_data_path="./mock_data",
                siem_base_url="https://siem.example.local",
                siem_auth_token="secret-token",
                siem_vendor="splunk_like",
                case_store_backend="unsupported_store",
            ),
            adapter_factory=factory,
        )

        status_code, payload = service.pilot_smoke_sync({
            "user_input": "请检查是否存在横向移动",
            "intent": "threat_hunt",
        })

        self.assertEqual(status_code, 503)
        self.assertEqual(payload["error"], "case_store_unavailable")
        self.assertEqual(payload["storage"]["reason"], "case_store_backend_not_supported")
        self.assertEqual(payload["smoke_path"]["failed_step"], "create_case")
        self.assertEqual(
            [step["step"] for step in payload["smoke_path"]["steps"]],
            ["readiness", "investigate", "create_case"],
        )

    def test_pilot_smoke_path_reports_get_case_failure_stage(self):
        transport = FakeProductionTransport()

        def factory(mode, runtime_settings):
            self.assertEqual(mode, "production")
            return ProductionSIEMAdapter(runtime_settings, transport=transport)

        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="production",
                static_data_path="./mock_data",
                siem_base_url="https://siem.example.local",
                siem_auth_token="secret-token",
                siem_vendor="splunk_like",
                edr_source_mode="local_files",
            ),
            adapter_factory=factory,
        )
        service._case_store = _InMemoryCaseStore()
        service._case_store_error = None

        with patch.object(
            service,
            "get_case_sync",
            return_value=(503, {"status": "error", "error": "case_store_unavailable"}),
        ):
            status_code, payload = service.pilot_smoke_sync({
                "user_input": "请检查是否存在横向移动",
                "intent": "threat_hunt",
            })

        self.assertEqual(status_code, 503)
        self.assertEqual(payload["error"], "case_store_unavailable")
        self.assertEqual(payload["smoke_path"]["failed_step"], "get_case")
        self.assertEqual(
            [step["step"] for step in payload["smoke_path"]["steps"]],
            ["readiness", "investigate", "create_case", "get_case"],
        )
        self.assertEqual(payload["smoke_path"]["steps"][2]["http_status"], 201)
        self.assertEqual(payload["smoke_path"]["steps"][3]["http_status"], 503)
        self.assertEqual(payload["smoke_path"]["steps"][3]["failure_category"], "runtime")

    def test_missing_static_data_is_classified_as_misconfigured(self):
        with self.assertLogs("secupilot.runtime", level="ERROR") as captured:
            service = SecuPilotRuntimeService(
                Settings(runtime_mode="mock", mock_data_path="./does-not-exist")
            )
        readiness = service.readiness()
        self.assertFalse(readiness["ready"])
        self.assertEqual(readiness["state_class"], "MISCONFIGURED")
        self.assertEqual(readiness["failure_category"], "static_data")
        self.assertFalse(readiness["static_data_present"])
        self.assertIn("does-not-exist", readiness["operator_message"])
        self.assertTrue(any("runtime.context.not_ready" in line for line in captured.output))

    def test_production_static_data_missing_is_logged_and_misconfigured(self):
        with self.assertLogs("secupilot.runtime", level="ERROR") as captured:
            service = SecuPilotRuntimeService(
                Settings(
                    runtime_mode="production",
                    mock_data_path="./does-not-exist",
                    siem_base_url="https://siem.example.local",
                    siem_auth_token="secret-token",
                )
            )
        readiness = service.readiness()
        self.assertFalse(readiness["ready"])
        self.assertEqual(readiness["state_class"], "MISCONFIGURED")
        self.assertEqual(readiness["failure_category"], "static_data")
        self.assertIn("does-not-exist", readiness["operator_message"])
        self.assertTrue(any("runtime.context.not_ready" in line for line in captured.output))

    def test_bootstrap_failure_is_classified_and_logged(self):
        with patch("backend.app.runtime_service.InvestigationPipeline", side_effect=RuntimeError("boom")):
            with self.assertLogs("secupilot.runtime", level="ERROR") as captured:
                service = SecuPilotRuntimeService(self.mock_settings)
        readiness = service.readiness()
        self.assertFalse(readiness["ready"])
        self.assertEqual(readiness["state_class"], "BOOTSTRAP_FAILED")
        self.assertEqual(readiness["failure_category"], "bootstrap")
        self.assertIn("runtime.context.bootstrap_failed", readiness["operator_message"])
        self.assertIn("bootstrap_failed", ",".join(readiness["reasons"]))
        self.assertTrue(any("runtime.context.bootstrap_failed" in line for line in captured.output))

    def test_unimplemented_static_source_mode_is_classified_as_static_data(self):
        with self.assertLogs("secupilot.runtime", level="ERROR") as captured:
            service = SecuPilotRuntimeService(
                Settings(
                    runtime_mode="mock",
                    mock_data_path="./mock_data",
                    static_data_mode="api",
                    asset_source_mode="api",
                )
            )
        readiness = service.readiness()
        self.assertFalse(readiness["ready"])
        self.assertEqual(readiness["state_class"], "MISCONFIGURED")
        self.assertEqual(readiness["failure_category"], "static_data")
        self.assertIn("Static data sources failed to load", readiness["operator_message"])
        self.assertTrue(
            any("static_data_unavailable:static_source_asset_inventory_unavailable" in reason for reason in readiness["reasons"])
        )
        self.assertTrue(any("runtime.context.not_ready" in line for line in captured.output))

    def test_not_ready_investigate_returns_runtime_status_contract(self):
        service = SecuPilotRuntimeService(
            Settings(runtime_mode="production", mock_data_path="./mock_data")
        )
        status_code, payload = service.investigate_sync({
            "user_input": "请检查最近是否有横向移动",
            "intent": "threat_hunt",
        })
        self.assertEqual(status_code, 503)
        self.assertEqual(payload["error"], "runtime_not_ready")
        self.assertEqual(payload["runtime_status"]["state_class"], "MISCONFIGURED")
        self.assertEqual(payload["runtime_status"]["failure_category"], "adapter_config")
        self.assertEqual(payload["readiness"]["state_class"], "MISCONFIGURED")

    def test_create_case_persists_and_retrieves_by_case_id(self):
        temp_dir = _fresh_temp_root("runtime_case_create")
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
        stored_verdict = create_payload["persistent_case"]["case_view"]["executive_summary"]["verdict"]
        self.assertEqual(create_payload["persistent_case"]["case_id"], case_id)
        self.assertEqual(
            create_payload["persistent_case"]["source_snapshot_id"],
            load_current_snapshot_id(service.settings),
        )

        get_status, get_payload = service.get_case_sync(case_id)
        self.assertEqual(get_status, 200)
        self.assertEqual(get_payload["persistent_case"]["case_id"], case_id)
        self.assertEqual(get_payload["persistent_case"]["lifecycle_status"], "open")

        get_payload["persistent_case"]["case_view"]["executive_summary"]["verdict"] = "BROKEN"
        get_again_status, get_again_payload = service.get_case_sync(case_id)
        self.assertEqual(get_again_status, 200)
        self.assertEqual(
            get_again_payload["persistent_case"]["case_view"]["executive_summary"]["verdict"],
            stored_verdict,
        )

    def test_create_case_returns_diagnosable_store_failure(self):
        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="mock",
                mock_data_path="./mock_data",
                case_store_backend="unsupported_store",
            )
        )

        status_code, payload = service.create_case_sync({
            "user_input": "请检查最近是否有横向移动",
            "intent": "threat_hunt",
            "time_range": "24h",
            "actor": "analyst.leo",
        })

        self.assertEqual(status_code, 503)
        self.assertEqual(payload["error"], "case_store_unavailable")
        self.assertEqual(payload["storage"]["reason"], "case_store_backend_not_supported")

    def test_get_case_returns_not_found(self):
        temp_dir = _fresh_temp_root("runtime_case_missing")
        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="mock",
                mock_data_path="./mock_data",
                case_store_path=str(temp_dir / "cases.sqlite3"),
            )
        )

        status_code, payload = service.get_case_sync("CASE-MISSING-001")

        self.assertEqual(status_code, 404)
        self.assertEqual(payload["error"], "case_not_found")

    def test_create_case_returns_structured_internal_error_when_record_build_fails(self):
        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="mock",
                mock_data_path="./mock_data",
            )
        )

        with patch("backend.app.runtime_service.build_initial_persistent_case_record", side_effect=RuntimeError("record_boom")):
            status_code, payload = service.create_case_sync({
                "user_input": "请检查最近是否有横向移动",
                "intent": "threat_hunt",
            })

        self.assertEqual(status_code, 500)
        self.assertEqual(payload["error"], "internal_error")
        self.assertEqual(payload["detail"], "record_boom")

    def test_create_submit_and_approve_action_request_round_trip(self):
        temp_dir = _fresh_temp_root("runtime_case_actions")
        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="mock",
                mock_data_path="./mock_data",
                case_store_path=str(temp_dir / "cases.sqlite3"),
            )
        )

        threat_case = {
            "case_id": "CASE-ACTION-ROUNDTRIP-001",
            "version": "3.1",
            "risk_score": 9.2,
            "confidence_score": 0.92,
            "confidence_label": "HIGH",
            "verdict_status": "CRITICAL_ACTION_REQUIRED",
            "investigation_status": "COMPLETE",
            "scenario_name": "Action Approval Flow",
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
        record = build_initial_persistent_case_record(
            threat_case,
            snapshot_id="S4-C-2026-04-10-003",
            actor="analyst.leo",
        )
        service._require_case_store().save_case(record)
        case_id = record.case_id

        draft_status, draft_payload = service.create_action_request_sync(case_id, {
            "actor": "analyst.leo",
            "rationale": "需要先走人工审批",
        })
        self.assertEqual(draft_status, 201)
        self.assertEqual(draft_payload["action_request"]["status"], "draft")
        action_request_id = draft_payload["action_request_id"]

        submit_status, submit_payload = service.submit_action_request_sync(case_id, action_request_id, {
            "actor": "analyst.leo",
            "review_owner": "manager.chen",
            "reason": "提交审批",
        })
        self.assertEqual(submit_status, 200)
        self.assertEqual(submit_payload["action_request"]["status"], "pending_approval")
        self.assertEqual(submit_payload["persistent_case"]["lifecycle_status"], "in_review")

        approve_status, approve_payload = service.approve_action_request_sync(case_id, action_request_id, {
            "actor": "manager.chen",
            "reason": "批准执行",
        })
        self.assertEqual(approve_status, 200)
        self.assertEqual(approve_payload["action_request"]["status"], "approved")
        self.assertEqual(approve_payload["persistent_case"]["lifecycle_status"], "approved")
        self.assertIn(
            "action_request_approved",
            [item["event_type"] for item in approve_payload["persistent_case"]["lifecycle_audit"]],
        )

    def test_degraded_case_blocks_action_request_creation(self):
        temp_dir = _fresh_temp_root("runtime_case_actions_degraded")
        service = SecuPilotRuntimeService(
            Settings(
                project_root=str(REPO_ROOT),
                runtime_mode="mock",
                mock_data_path="./mock_data",
                case_store_path=str(temp_dir / "cases.sqlite3"),
            )
        )

        threat_case = {
            "case_id": "CASE-DEGRADED-001",
            "version": "3.1",
            "risk_score": 6.2,
            "confidence_score": 0.42,
            "confidence_label": "LOW",
            "verdict_status": "DEGRADED",
            "investigation_status": "DEGRADED",
            "scenario_name": "Degraded replay",
            "forensic_result": {
                "hosts_analyzed": [],
                "total_suspicious_chains": 0,
                "top_chains": [],
                "attack_stages_observed": [],
                "persistence_mechanisms": [],
                "evidence_gaps": ["missing_edr"],
            },
            "suggested_action": {
                "type": "NETWORK_ISOLATE",
                "targets": ["WKST-047"],
                "blast_radius_desc": "隔离影响未知",
            },
            "audit_trail": {"degraded": True, "degraded_reasons": ["production_edr_unavailable"]},
        }
        record = build_initial_persistent_case_record(
            threat_case,
            snapshot_id="S4-C-2026-04-10-003",
            actor="analyst.leo",
        )
        service._require_case_store().save_case(record)

        status_code, payload = service.create_action_request_sync("CASE-DEGRADED-001", {
            "actor": "analyst.leo",
            "rationale": "降级案卷不应允许动作请求",
        })

        self.assertEqual(status_code, 409)
        self.assertEqual(payload["error"], "action_request_unavailable")


if __name__ == "__main__":
    unittest.main(verbosity=2)
