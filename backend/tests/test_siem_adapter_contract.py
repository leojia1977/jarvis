import unittest
from datetime import datetime, timezone

from _project_bootstrap import bootstrap

bootstrap()

from app.tools.siem_adapter import MockSIEMAdapter, TimeRangeSpec  # noqa: E402


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
