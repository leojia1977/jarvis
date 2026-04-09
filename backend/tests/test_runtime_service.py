import unittest

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.config import Settings
from backend.app.runtime_service import SecuPilotRuntimeService
from app.tools.siem_adapter import ProductionSIEMAdapter


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
        self.assertEqual(payload["service"], "secupilot-runtime")

    def test_readiness_in_mock_mode(self):
        service = SecuPilotRuntimeService(self.mock_settings)
        payload = service.readiness()
        self.assertTrue(payload["ready"])
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
        self.assertEqual(payload["threat_case"]["version"], "3.1")

    def test_empty_user_input_rejected(self):
        service = SecuPilotRuntimeService(self.mock_settings)
        status_code, payload = service.investigate_sync({"intent": "summarize_recent"})
        self.assertEqual(status_code, 400)
        self.assertEqual(payload["error"], "user_input_required")

    def test_production_mode_not_ready_yet(self):
        service = SecuPilotRuntimeService(
            Settings(runtime_mode="production", mock_data_path="./mock_data")
        )
        readiness = service.readiness()
        self.assertFalse(readiness["ready"])
        self.assertIn("production_adapter_not_configured", readiness["reasons"])

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
        self.assertEqual(readiness["adapter_type"], "ProductionSIEMAdapter")
        self.assertTrue(readiness["adapter_configured"])

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
