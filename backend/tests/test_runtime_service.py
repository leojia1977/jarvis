import unittest

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.config import Settings
from backend.app.runtime_service import SecuPilotRuntimeService


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
        self.assertIn("production_adapter_not_implemented", readiness["reasons"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
