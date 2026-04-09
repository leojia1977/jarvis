import unittest
from datetime import datetime, timezone

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.config import Settings  # noqa: E402
from app.tools.siem_adapter import MockSIEMAdapter, ProductionSIEMAdapter, TimeRangeSpec  # noqa: E402


class TimeRangeSpecTests(unittest.TestCase):
    def test_parse_relative_range_to_utc_window(self):
        fixed_now = datetime(2026, 4, 8, 12, 0, 0, tzinfo=timezone.utc)
        spec = TimeRangeSpec.from_value("24h", tz_label="Asia/Shanghai", now=fixed_now)
        self.assertEqual(spec.end_utc, fixed_now)
        self.assertEqual((spec.end_utc - spec.start_utc).total_seconds(), 24 * 3600)
        self.assertEqual(spec.tz_label, "Asia/Shanghai")


class MockSIEMAdapterContractTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.adapter = object.__new__(MockSIEMAdapter)
        self.adapter._cache = {
            "siem_responses": {"queries": {"summarize_recent_12h": {"response": {"total_alerts": 2}}}},
            "assets": {"assets": [{"asset_id": "WKST-047"}]},
            "ioc": {"malicious_ips": [], "malicious_domains": [], "malicious_hashes": []},
            "knowledge_graph": {"nodes": {"assets": []}, "relationships": []},
            "baselines": {"baselines": []},
            "scenarios": {
                "S-02": {
                    "scenario": {"scenario_id": "S-02", "name": "Lateral Movement"},
                    "alerts": [
                        {
                            "event_id": "S-02-OLD",
                            "event_time": "2026-04-01T01:00:00Z",
                            "destination_asset_id": "WKST-047",
                        },
                        {
                            "event_id": "S-02-NEW",
                            "event_time": "2026-04-08T10:00:00Z",
                            "destination_asset_id": "WKST-047",
                        },
                    ],
                }
            },
        }

    async def test_query_intent_alerts_returns_adapter_result_and_honors_time_range(self):
        spec = TimeRangeSpec(
            start_utc=datetime(2026, 4, 8, 0, 0, 0, tzinfo=timezone.utc),
            end_utc=datetime(2026, 4, 8, 23, 59, 59, tzinfo=timezone.utc),
            tz_label="Asia/Shanghai",
        )
        result = await self.adapter.query_intent_alerts("threat_hunt", "请查横向移动", spec)
        self.assertEqual(result.status, "ok")
        self.assertEqual(result.metadata["scenario_id"], "S-02")
        self.assertEqual([alert["event_id"] for alert in result.data], ["S-02-NEW"])

    async def test_query_asset_alerts_uses_same_time_range_contract(self):
        spec = TimeRangeSpec(
            start_utc=datetime(2026, 4, 8, 0, 0, 0, tzinfo=timezone.utc),
            end_utc=datetime(2026, 4, 8, 23, 59, 59, tzinfo=timezone.utc),
            tz_label="Asia/Shanghai",
        )
        result = await self.adapter.query_asset_alerts("WKST-047", spec)
        self.assertEqual(result.status, "ok")
        self.assertEqual([alert["event_id"] for alert in result.data], ["S-02-NEW"])

    async def test_get_scenario_metadata_returns_envelope(self):
        result = await self.adapter.get_scenario_metadata("S-02")
        self.assertEqual(result.status, "ok")
        self.assertEqual(result.data["name"], "Lateral Movement")


class FakeProductionTransport:
    def __init__(self, response=None, error=None):
        self.response = response or {}
        self.error = error
        self.calls = []

    async def post_json(self, endpoint, payload, *, headers, timeout_seconds):
        self.calls.append(
            {
                "endpoint": endpoint,
                "payload": payload,
                "headers": headers,
                "timeout_seconds": timeout_seconds,
            }
        )
        if self.error:
            raise self.error
        return self.response


class ProductionSIEMAdapterTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.settings = Settings(
            runtime_mode="production",
            mock_data_path="./mock_data",
            siem_base_url="https://siem.example.local",
            siem_auth_token="secret-token",
            siem_vendor="splunk_like",
            siem_request_timeout_seconds=7.5,
        )

    async def test_query_intent_alerts_normalizes_generic_envelope(self):
        transport = FakeProductionTransport(
            {
                "status": "partial",
                "alerts": [{"event_id": "ALERT-1"}],
                "gap_reason": "partial_time_window_data",
                "metadata": {"source": "splunk"},
            }
        )
        adapter = ProductionSIEMAdapter(self.settings, transport=transport)
        spec = TimeRangeSpec(
            start_utc=datetime(2026, 4, 8, 0, 0, 0, tzinfo=timezone.utc),
            end_utc=datetime(2026, 4, 8, 12, 0, 0, tzinfo=timezone.utc),
            tz_label="Asia/Shanghai",
        )

        result = await adapter.query_intent_alerts("threat_hunt", "查横向移动", spec)
        self.assertEqual(result.status, "partial")
        self.assertEqual(result.gap_reason, "partial_time_window_data")
        self.assertEqual(result.data[0]["event_id"], "ALERT-1")
        self.assertEqual(transport.calls[0]["payload"]["intent"], "threat_hunt")
        self.assertEqual(transport.calls[0]["headers"]["Authorization"], "Bearer secret-token")

    async def test_get_scenario_metadata_uses_generic_data_fallback(self):
        transport = FakeProductionTransport(
            {
                "status": "ok",
                "data": {"name": "Ransomware"},
            }
        )
        adapter = ProductionSIEMAdapter(self.settings, transport=transport)
        result = await adapter.get_scenario_metadata("S-04")
        self.assertEqual(result.status, "ok")
        self.assertEqual(result.data["name"], "Ransomware")

    async def test_unconfigured_production_adapter_returns_unavailable(self):
        transport = FakeProductionTransport({"status": "ok", "alerts": [{"event_id": "ALERT-1"}]})
        adapter = ProductionSIEMAdapter(
            Settings(runtime_mode="production", mock_data_path="./mock_data"),
            transport=transport,
        )
        spec = TimeRangeSpec(
            start_utc=datetime(2026, 4, 8, 0, 0, 0, tzinfo=timezone.utc),
            end_utc=datetime(2026, 4, 8, 12, 0, 0, tzinfo=timezone.utc),
            tz_label="Asia/Shanghai",
        )
        result = await adapter.query_recent_summary(spec)
        self.assertEqual(result.status, "unavailable")
        self.assertEqual(result.gap_reason, "production_adapter_not_configured")
        self.assertEqual(transport.calls, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
