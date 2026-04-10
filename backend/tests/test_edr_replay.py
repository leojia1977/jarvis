import asyncio
import copy
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.agents.graph import InvestigationPipeline  # noqa: E402
from backend.app.config import Settings  # noqa: E402
from app.tools.edr_adapter import ProductionEDRAdapter  # noqa: E402
from app.tools.siem_adapter import MockSIEMAdapter, TimeRangeSpec  # noqa: E402
from app.tools.static_data_sources import HostIdentityRecord  # noqa: E402


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "vendor_replay"
REPO_ROOT = Path(__file__).resolve().parents[2]


class EDRReplayTransport:
    ENDPOINT_KEY_BY_SUFFIX = {
        "/process-events/query": "process_events",
    }

    def __init__(self, vendor: str, scenario: str):
        self.vendor = vendor
        self.scenario = scenario
        self.calls: list[dict] = []
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
            raise AssertionError(
                f"Missing EDR replay fixture for {self.vendor}:{self.scenario}:{endpoint_key}"
            )

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


class EDRReplayTests(unittest.TestCase):
    def _host_identity(self, asset_id: str, hostname: str, ip_address: str) -> HostIdentityRecord:
        return HostIdentityRecord(
            canonical_asset_id=asset_id,
            hostname=hostname,
            fqdn=f"{hostname}.corp.local",
            ip_addresses=[ip_address],
            aliases=[hostname],
            source_refs=[f"asset_inventory:{asset_id}"],
        )

    def _build_adapter(self, vendor: str, scenario: str):
        transport = EDRReplayTransport(vendor, scenario)
        adapter = ProductionEDRAdapter(
            Settings(
                edr_source_mode="replay",
                edr_vendor=vendor,
                edr_base_url="https://edr.example.local",
                edr_auth_token="secret-token",
            ),
            transport=transport,
        )
        return adapter, transport

    def test_replay_transport_rejects_unknown_endpoint(self):
        transport = EDRReplayTransport("crowdstrike_like", "lateral")

        with self.assertRaisesRegex(AssertionError, "Unexpected replay endpoint"):
            asyncio.run(
                transport.post_json(
                    "https://edr.example.local/api/v1/unknown",
                    {},
                    headers={},
                    timeout_seconds=1.0,
                )
            )

    def test_crowdstrike_like_replay_normalizes_process_events(self):
        adapter, transport = self._build_adapter("crowdstrike_like", "lateral")
        host_identity = self._host_identity("WKST-047", "wkst-047", "10.1.5.22")
        spec = TimeRangeSpec.from_value(
            "24h",
            tz_label="Asia/Shanghai",
            now=datetime(2026, 4, 9, 12, 0, tzinfo=timezone.utc),
        )

        result = asyncio.run(adapter.query_process_events(host_identity, spec))

        self.assertEqual(result.status, "ok")
        self.assertEqual(result.data.events[0].process_name, "PSEXESVC.exe")
        self.assertEqual(result.data.events[0].host_id, "WKST-047")
        self.assertTrue(
            any(event.event_type == "network_connect" and event.dst_port == 88 for event in result.data.events)
        )
        self.assertTrue(
            any(event.event_type == "file_write" and event.file_hash_sha256 for event in result.data.events)
        )
        self.assertEqual(transport.calls[0]["payload"]["canonical_asset_id"], "WKST-047")

    def test_elastic_defend_like_replay_normalizes_process_events(self):
        adapter, transport = self._build_adapter("elastic_defend_like", "ransomware")
        host_identity = self._host_identity("HR-PORTAL-01", "hr-portal-01", "10.1.6.10")
        spec = TimeRangeSpec.from_value(
            "24h",
            tz_label="Asia/Shanghai",
            now=datetime(2026, 4, 9, 12, 0, tzinfo=timezone.utc),
        )

        result = asyncio.run(adapter.query_process_events(host_identity, spec))

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.data.events[0].process_name, "vssadmin.exe")
        self.assertTrue(
            any(event.event_type == "dns_query" and event.query_domain == "update.legit-looking.xyz" for event in result.data.events)
        )
        self.assertTrue(
            any(event.event_type == "network_connect" and event.dst_ip == "185.220.101.45" for event in result.data.events)
        )
        self.assertEqual(transport.calls[0]["payload"]["canonical_asset_id"], "HR-PORTAL-01")

    def test_replay_investigate_path_returns_case(self):
        settings = Settings(
            project_root=str(REPO_ROOT),
            runtime_mode="mock",
            mock_data_path=str(REPO_ROOT / "mock_data"),
            edr_source_mode="replay",
            edr_vendor="crowdstrike_like",
            edr_base_url="https://edr.example.local",
            edr_auth_token="secret-token",
        )
        adapter = ProductionEDRAdapter(
            settings,
            transport=EDRReplayTransport("crowdstrike_like", "lateral"),
        )
        pipeline = InvestigationPipeline(
            MockSIEMAdapter(settings.get_static_data_dir()),
            runtime_settings=settings,
            edr_adapter=adapter,
        )

        case = asyncio.run(
            pipeline.investigate(
                intent="threat_hunt",
                user_input="请检查横向移动",
                target_asset_id="WKST-047",
                time_range="7d",
                timeout=2.0,
            )
        )

        self.assertEqual(case["scenario_id"], "S-02")
        self.assertTrue(case["forensic_result"]["top_chains"])
        self.assertIn("WKST-047", case["forensic_result"]["hosts_analyzed"])
        self.assertIn("process_tree", case["forensic_result"]["analysis_scope"])

    def test_elastic_replay_investigate_path_returns_case(self):
        settings = Settings(
            project_root=str(REPO_ROOT),
            runtime_mode="mock",
            mock_data_path=str(REPO_ROOT / "mock_data"),
            edr_source_mode="replay",
            edr_vendor="elastic_defend_like",
            edr_base_url="https://edr.example.local",
            edr_auth_token="secret-token",
        )
        transport = EDRReplayTransport("elastic_defend_like", "ransomware")
        adapter = ProductionEDRAdapter(settings, transport=transport)
        pipeline = InvestigationPipeline(
            MockSIEMAdapter(settings.get_static_data_dir()),
            runtime_settings=settings,
            edr_adapter=adapter,
        )

        case = asyncio.run(
            pipeline.investigate(
                intent="threat_hunt",
                user_input="请检查勒索和C2",
                target_asset_id="HR-PORTAL-01",
                time_range="7d",
                timeout=2.0,
            )
        )

        self.assertEqual(case["scenario_id"], "S-04")
        self.assertEqual(case["investigation_status"], "PARTIAL")
        self.assertEqual(case["forensic_result"]["hosts_analyzed"], ["HR-PORTAL-01"])
        self.assertTrue(case["forensic_result"]["top_chains"])
        self.assertTrue(any(call["endpoint_key"] == "process_events" for call in transport.calls))


if __name__ == "__main__":
    unittest.main(verbosity=2)
