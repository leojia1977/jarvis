import asyncio
import copy
import json
import unittest
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.config import Settings  # noqa: E402
from backend.app.runtime_service import SecuPilotRuntimeService  # noqa: E402
from app.tools.siem_adapter import ProductionSIEMAdapter, TimeRangeSpec  # noqa: E402


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "vendor_replay"


class ReplayTransport:
    ENDPOINT_KEY_BY_SUFFIX = {
        "/alerts/intent": "intent_alerts",
        "/metadata/scenario": "scenario_metadata",
    }

    def __init__(self, vendor: str, scenario: str):
        self.vendor = vendor
        self.scenario = scenario
        self.calls = []
        self.fixtures = self._load_fixtures()

    def _load_fixtures(self) -> dict[str, dict]:
        fixtures: dict[str, dict] = {}
        for path in FIXTURE_DIR.glob(f"{self.vendor}_*_{self.scenario}.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            fixtures[payload["endpoint_key"]] = payload
        return fixtures

    async def post_json(self, endpoint, payload, *, headers, timeout_seconds):
        endpoint_key = None
        for suffix, key in self.ENDPOINT_KEY_BY_SUFFIX.items():
            if endpoint.endswith(suffix):
                endpoint_key = key
                break
        if endpoint_key is None:
            raise AssertionError(f"Unexpected replay endpoint: {endpoint}")
        if endpoint_key not in self.fixtures:
            raise AssertionError(f"Missing replay fixture for {self.vendor}:{self.scenario}:{endpoint_key}")

        fixture = self.fixtures[endpoint_key]
        self.calls.append(
            {
                "endpoint": endpoint,
                "endpoint_key": endpoint_key,
                "payload": copy.deepcopy(payload),
                "headers": copy.deepcopy(headers),
                "timeout_seconds": timeout_seconds,
            }
        )
        return copy.deepcopy(fixture["response"])


class VendorReplayTests(unittest.TestCase):
    def _build_service(self, vendor: str, scenario: str):
        capture = {}

        def factory(mode, runtime_settings):
            self.assertEqual(mode, "production")
            transport = ReplayTransport(vendor, scenario)
            adapter = ProductionSIEMAdapter(runtime_settings, transport=transport)
            capture["adapter"] = adapter
            capture["transport"] = transport
            return adapter

        service = SecuPilotRuntimeService(
            Settings(
                runtime_mode="production",
                mock_data_path="./mock_data",
                siem_base_url="https://siem.example.local",
                siem_auth_token="secret-token",
                siem_vendor=vendor,
            ),
            adapter_factory=factory,
        )
        return service, capture

    def test_splunk_replay_investigate(self):
        service, capture = self._build_service("splunk_like", "lateral")
        adapter = capture["adapter"]
        transport = capture["transport"]

        spec = TimeRangeSpec.from_value("24h", tz_label="Asia/Shanghai")
        normalized = asyncio.run(adapter.query_intent_alerts("threat_hunt", "请检查横向移动", spec))
        self.assertEqual(normalized.data[0]["event_time"], "2026-04-09T01:22:00Z")
        self.assertEqual(normalized.data[0]["activity_name"], "Remote Service Execution")

        status_code, payload = service.investigate_sync({
            "user_input": "请检查横向移动",
            "intent": "threat_hunt",
            "time_range": "24h",
        })

        self.assertEqual(status_code, 200)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["threat_case"]["scenario_id"], "S-02")
        self.assertEqual(payload["threat_case"]["triage_summary"]["top_alerts"][0]["activity"], "Remote Service Execution")
        self.assertEqual(payload["threat_case"]["triage_summary"]["top_alerts"][0]["severity"], "HIGH")
        self.assertTrue(any(call["endpoint_key"] == "intent_alerts" for call in transport.calls))
        self.assertTrue(any(call["endpoint_key"] == "scenario_metadata" for call in transport.calls))

    def test_elastic_replay_investigate(self):
        service, capture = self._build_service("elastic_like", "ransomware")
        adapter = capture["adapter"]
        transport = capture["transport"]

        spec = TimeRangeSpec.from_value("24h", tz_label="Asia/Shanghai")
        normalized = asyncio.run(adapter.query_intent_alerts("threat_hunt", "请检查勒索和C2", spec))
        self.assertEqual(normalized.data[0]["event_time"], "2026-04-09T02:15:00Z")
        self.assertEqual(normalized.data[0]["activity_name"], "Credential Dumping")

        status_code, payload = service.investigate_sync({
            "user_input": "请检查勒索和C2",
            "intent": "threat_hunt",
            "time_range": "24h",
        })

        self.assertEqual(status_code, 200)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["threat_case"]["scenario_id"], "S-04")
        self.assertEqual(payload["threat_case"]["triage_summary"]["top_alerts"][0]["activity"], "Credential Dumping")
        self.assertEqual(payload["threat_case"]["triage_summary"]["top_alerts"][0]["severity"], "HIGH")
        self.assertTrue(any(call["endpoint_key"] == "intent_alerts" for call in transport.calls))
        self.assertTrue(any(call["endpoint_key"] == "scenario_metadata" for call in transport.calls))


if __name__ == "__main__":
    unittest.main(verbosity=2)
