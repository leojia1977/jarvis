import asyncio
import copy
import json
import unittest
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.agents.graph import InvestigationPipeline  # noqa: E402
from backend.app.config import Settings  # noqa: E402
from app.tools.edr_adapter import (  # noqa: E402
    EDRSourceMetadata,
    ProcessEventBatch,
    ProductionEDRAdapter,
    process_event_batch_to_runtime_payload,
)
from app.tools.process_tree_t3 import ProcessTreeCompiler  # noqa: E402
from app.tools.siem_adapter import AdapterResult, MockSIEMAdapter, TimeRangeSpec  # noqa: E402
from app.tools.static_data_sources import HostIdentityRecord  # noqa: E402


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "vendor_replay"
REPO_ROOT = Path(__file__).resolve().parents[2]
FORBIDDEN_VENDOR_KEYS = {"event", "host", "process", "source", "destination", "network", "dns", "file", "registry"}


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


class _UnavailableEDRTransport:
    async def post_json(self, endpoint, payload, *, headers, timeout_seconds):
        raise urllib.error.URLError("replay-offline")


class T3ProductionParityTests(unittest.TestCase):
    def setUp(self):
        self.compiler = ProcessTreeCompiler(top_k=3)
        self.time_spec = TimeRangeSpec.from_value(
            "24h",
            tz_label="Asia/Shanghai",
            now=datetime(2026, 4, 9, 12, 0, tzinfo=timezone.utc),
        )

    def _host_identity(self, asset_id: str, hostname: str, ip_address: str) -> HostIdentityRecord:
        return HostIdentityRecord(
            canonical_asset_id=asset_id,
            hostname=hostname,
            fqdn=f"{hostname}.corp.local",
            ip_addresses=[ip_address],
            aliases=[hostname],
            source_refs=[f"asset_inventory:{asset_id}"],
        )

    def _build_production_adapter(self, vendor: str, scenario: str) -> ProductionEDRAdapter:
        settings = Settings(
            edr_source_mode="replay",
            edr_vendor=vendor,
            edr_base_url="https://edr.example.local",
            edr_auth_token="secret-token",
        )
        return ProductionEDRAdapter(settings, transport=EDRReplayTransport(vendor, scenario))

    def _runtime_events_from_replay(self, vendor: str, scenario: str, host_identity: HostIdentityRecord):
        adapter = self._build_production_adapter(vendor, scenario)
        result = asyncio.run(adapter.query_process_events(host_identity, self.time_spec))
        self.assertIn(result.status, {"ok", "partial"})
        payload = process_event_batch_to_runtime_payload(result.data)
        return result, payload

    def _assert_runtime_payload_is_vendor_free(self, payload: list[dict]):
        self.assertTrue(payload)
        for event in payload:
            self.assertTrue(FORBIDDEN_VENDOR_KEYS.isdisjoint(set(event.keys())))

    def _assert_t3_frozen_contract(self, result):
        self.assertIn(result.analysis_status, {"COMPLETE", "PARTIAL", "DEGRADED", "FAILED"})
        for chain in result.suspicious_chains:
            self.assertIn("chain_id", chain)
            self.assertIn("anomaly_score", chain)
            self.assertIn("path", chain)
            for node in chain["path"]:
                self.assertTrue(FORBIDDEN_VENDOR_KEYS.isdisjoint(set(node.keys())))
                self.assertIn(node["evidence_status"], {"VERIFIED", "INFERRED", "UNVERIFIED"})
        for ioc in result.ioc_extracted:
            self.assertIn(ioc["type"], {"ip", "domain", "hash"})
            self.assertIn("source_chain_id", ioc)
            self.assertIn("source_node_id", ioc)

    def test_crowdstrike_replay_keeps_t3_frozen_contract(self):
        host_identity = self._host_identity("WKST-047", "wkst-047", "10.1.5.22")
        _, runtime_events = self._runtime_events_from_replay(
            "crowdstrike_like",
            "lateral",
            host_identity,
        )

        self._assert_runtime_payload_is_vendor_free(runtime_events)
        result = self.compiler.analyze("WKST-047", runtime_events)

        self._assert_t3_frozen_contract(result)
        self.assertIn(result.analysis_status, {"COMPLETE", "PARTIAL"})
        self.assertGreater(len(result.suspicious_chains), 0)
        self.assertTrue(
            any("rubeus.exe" in node["process_name"].lower() for chain in result.suspicious_chains for node in chain["path"])
        )
        self.assertTrue(any(ioc["type"] == "hash" for ioc in result.ioc_extracted))

    def test_elastic_replay_keeps_t3_persistence_and_iocs(self):
        host_identity = self._host_identity("HR-PORTAL-01", "hr-portal-01", "10.1.6.10")
        replay_result, runtime_events = self._runtime_events_from_replay(
            "elastic_defend_like",
            "ransomware",
            host_identity,
        )

        self.assertEqual(replay_result.status, "partial")
        self._assert_runtime_payload_is_vendor_free(runtime_events)
        result = self.compiler.analyze("HR-PORTAL-01", runtime_events)

        self._assert_t3_frozen_contract(result)
        self.assertIn(result.analysis_status, {"COMPLETE", "PARTIAL"})
        self.assertTrue(any(ioc["type"] == "ip" and ioc["value"] == "185.220.101.45" for ioc in result.ioc_extracted))
        self.assertTrue(any(ioc["type"] == "domain" and ioc["value"] == "update.legit-looking.xyz" for ioc in result.ioc_extracted))
        self.assertTrue(any(ioc["type"] == "hash" for ioc in result.ioc_extracted))
        self.assertTrue(any(persist["type"] == "registry_run_key" for persist in result.persistence_mechanisms))

    def test_orchestrator_keeps_partial_semantics_for_partial_edr_replay(self):
        settings = Settings(
            project_root=str(REPO_ROOT),
            runtime_mode="mock",
            mock_data_path=str(REPO_ROOT / "mock_data"),
            edr_source_mode="replay",
            edr_vendor="elastic_defend_like",
            edr_base_url="https://edr.example.local",
            edr_auth_token="secret-token",
        )
        pipeline = InvestigationPipeline(
            MockSIEMAdapter(settings.get_static_data_dir()),
            runtime_settings=settings,
            edr_adapter=ProductionEDRAdapter(
                settings,
                transport=EDRReplayTransport("elastic_defend_like", "ransomware"),
            ),
        )

        result = asyncio.run(
            pipeline.orchestrator._run_t3(
                ["HR-PORTAL-01"],
                time_range=self.time_spec,
            )
        )

        self.assertEqual(result["status"], "partial")
        self.assertTrue(result["suspicious_chains"])
        self.assertTrue(any("production_edr_partial" in gap["reason"] for gap in result["gaps"]))

    def test_orchestrator_keeps_degraded_semantics_for_unavailable_edr(self):
        settings = Settings(
            project_root=str(REPO_ROOT),
            runtime_mode="mock",
            mock_data_path=str(REPO_ROOT / "mock_data"),
            edr_source_mode="replay",
            edr_vendor="generic_http",
            edr_base_url="https://edr.example.local",
            edr_auth_token="secret-token",
        )
        pipeline = InvestigationPipeline(
            MockSIEMAdapter(settings.get_static_data_dir()),
            runtime_settings=settings,
            edr_adapter=ProductionEDRAdapter(
                settings,
                transport=_UnavailableEDRTransport(),
            ),
        )

        result = asyncio.run(
            pipeline.orchestrator._run_t3(
                ["WKST-047"],
                time_range=self.time_spec,
            )
        )

        self.assertEqual(result["status"], "degraded")
        self.assertEqual(result["hosts_analyzed"], [])
        self.assertTrue(any("production_edr_unavailable" in gap["reason"] for gap in result["gaps"]))
        self.assertEqual(result["suspicious_chains"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
