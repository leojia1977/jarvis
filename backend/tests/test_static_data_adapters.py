import asyncio
import unittest

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.agents.graph import InvestigationPipeline
from backend.app.config import Settings
from app.tools.siem_adapter import AdapterResult, MockSIEMAdapter
from app.tools.static_data_adapters import (
    StaticDataSourceAdapters,
    build_static_data_source_adapters,
    load_static_data_runtime_payloads_sync,
    with_static_data_cache,
)
from app.tools.static_data_sources import (
    AssetInventorySnapshot,
    AssetRecord,
    BaselineRecord,
    BaselineSnapshot,
    StaticRefreshPolicy,
    StaticSourceMetadata,
    ThreatIntelSeedRecord,
    ThreatIntelSeedSnapshot,
    TopologySnapshot,
)


def _metadata(kind: str, count: int) -> StaticSourceMetadata:
    return StaticSourceMetadata(
        source_kind=kind,
        source_name=f"test:{kind}",
        source_mode="local_files",
        ownership="test",
        record_count=count,
        refresh_policy=StaticRefreshPolicy(strategy="ttl", ttl_seconds=300),
    )


class _FakeAssetSource:
    async def load_asset_inventory(self) -> AdapterResult[AssetInventorySnapshot]:
        return AdapterResult.ok(
            AssetInventorySnapshot(
                metadata=_metadata("asset_inventory", 1),
                assets=[
                    AssetRecord(
                        asset_id="WKST-047",
                        hostname="wkst-047",
                        ip_addresses=["10.1.5.22"],
                        business_unit="Finance",
                        role="Financial Analyst Workstation",
                        criticality_weight=3,
                        extra={"known_behaviors": ["nightly_db_backup"]},
                    )
                ],
            )
        )


class _FakeBaselineSource:
    async def load_baselines(self) -> AdapterResult[BaselineSnapshot]:
        return AdapterResult.ok(
            BaselineSnapshot(
                metadata=_metadata("baseline", 1),
                baselines=[
                    BaselineRecord(
                        baseline_id="FP-1",
                        category="finance",
                        pattern_description="nightly_db_backup",
                        confidence=0.9,
                        activity_names=["nightly_db_backup"],
                    )
                ],
            )
        )


class _FakeIntelSeedSource:
    async def load_threat_intel_seed(self) -> AdapterResult[ThreatIntelSeedSnapshot]:
        return AdapterResult.ok(
            ThreatIntelSeedSnapshot(
                metadata=_metadata("intel_seed", 1),
                records=[
                    ThreatIntelSeedRecord(
                        indicator="185.220.101.45",
                        indicator_type="ip",
                        threat_type="C2",
                        actor="APT-BEAR",
                        confidence=0.95,
                    )
                ],
            )
        )


class _FakeTopologySource:
    async def load_topology(self) -> AdapterResult[TopologySnapshot]:
        return AdapterResult.ok(
            TopologySnapshot(
                metadata=_metadata("topology", 1),
                nodes={"assets": [{"asset_id": "WKST-047", "criticality_weight": 3}]},
                edges=[{"from": "WKST-047", "to": "VLAN-Finance-01", "type": "belongs_to"}],
            )
        )


class _MutableClock:
    def __init__(self, start: float = 0.0):
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


class _CountingAssetSource:
    def __init__(self):
        self.calls = 0
        self.asset_id = "WKST-047"
        self.status = "ok"

    async def load_asset_inventory(self) -> AdapterResult[AssetInventorySnapshot]:
        self.calls += 1
        if self.status != "ok":
            return AdapterResult.unavailable(
                AssetInventorySnapshot(metadata=_metadata("asset_inventory", 0), assets=[]),
                gap_reason=f"static_source_missing:asset_inventory:{self.status}",
            )
        return AdapterResult.ok(
            AssetInventorySnapshot(
                metadata=_metadata("asset_inventory", 1),
                assets=[
                    AssetRecord(
                        asset_id=self.asset_id,
                        hostname=self.asset_id.lower(),
                        ip_addresses=["10.1.5.22"],
                    )
                ],
            )
        )


class StaticDataAdapterTests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings(
            project_root="C:/Users/Administrator/Documents/New project",
            runtime_mode="mock",
            static_data_path="./mock_data",
            mock_data_path="./legacy_mock_data",
            static_data_mode="local_files",
            asset_source_mode="local_files",
            baseline_source_mode="local_files",
            intel_seed_source_mode="local_files",
            topology_source_mode="local_files",
        )

    def test_local_file_adapter_bundle_loads_all_runtime_payloads(self):
        adapters = build_static_data_source_adapters(self.settings)
        bundle = load_static_data_runtime_payloads_sync(adapters)

        self.assertGreater(bundle.asset_inventory_snapshot.metadata.record_count, 0)
        self.assertGreater(bundle.baseline_snapshot.metadata.record_count, 0)
        self.assertGreater(bundle.threat_intel_seed_snapshot.metadata.record_count, 0)
        self.assertGreater(bundle.topology_snapshot.metadata.record_count, 0)
        self.assertGreater(len(bundle.asset_inventory_payload["assets"]), 0)
        self.assertGreater(len(bundle.baseline_payload["baselines"]), 0)
        self.assertGreater(len(bundle.threat_intel_seed_payload["malicious_ips"]), 0)
        self.assertIn("relationships", bundle.topology_payload)

    def test_bundle_mode_reuses_local_file_adapter_envelope(self):
        configured = Settings(
            project_root="C:/Users/Administrator/Documents/New project",
            static_data_path="./mock_data",
            static_data_mode="bundle",
            asset_source_mode="bundle",
        )
        adapters = build_static_data_source_adapters(configured)
        result = asyncio.run(adapters.asset_inventory.load_asset_inventory())

        self.assertEqual(result.status, "ok")
        self.assertEqual(result.data.metadata.source_mode, "bundle")
        self.assertGreater(result.data.metadata.record_count, 0)

    def test_unimplemented_api_mode_returns_unavailable(self):
        configured = Settings(
            project_root="C:/Users/Administrator/Documents/New project",
            static_data_path="./mock_data",
            static_data_mode="api",
            asset_source_mode="api",
        )
        adapters = build_static_data_source_adapters(configured)
        result = asyncio.run(adapters.asset_inventory.load_asset_inventory())

        self.assertEqual(result.status, "unavailable")
        self.assertIn("static_source_mode_not_implemented:asset_inventory:api", result.gap_reason)
        with self.assertRaisesRegex(RuntimeError, "static_source_asset_inventory_unavailable"):
            load_static_data_runtime_payloads_sync(adapters)

    def test_pipeline_bootstraps_from_static_data_adapters(self):
        fake_adapters = StaticDataSourceAdapters(
            asset_inventory=_FakeAssetSource(),
            baselines=_FakeBaselineSource(),
            threat_intel_seed=_FakeIntelSeedSource(),
            topology=_FakeTopologySource(),
        )
        siem = MockSIEMAdapter(self.settings.get_static_data_dir())

        pipeline = InvestigationPipeline(
            siem,
            runtime_settings=self.settings,
            static_data_adapters=fake_adapters,
        )

        self.assertIn("WKST-047", pipeline.orchestrator.triage.asset_db)
        self.assertIn("WKST-047", pipeline.orchestrator.blast.asset_index)
        self.assertEqual(
            pipeline.orchestrator.triage.asset_db["WKST-047"]["known_behaviors"][0],
            "nightly_db_backup",
        )
        identity = asyncio.run(pipeline.orchestrator.host_identity_resolver.resolve_ip("10.1.5.22"))
        self.assertEqual(identity.status, "ok")
        self.assertEqual(identity.data.canonical_asset_id, "WKST-047")

    def test_ttl_cache_reuses_snapshot_before_expiry(self):
        clock = _MutableClock()
        inner = _CountingAssetSource()
        cached = with_static_data_cache(
            StaticDataSourceAdapters(
                asset_inventory=inner,
                baselines=_FakeBaselineSource(),
                threat_intel_seed=_FakeIntelSeedSource(),
                topology=_FakeTopologySource(),
            ),
            ttl_seconds=300,
            clock=clock,
        )

        first = asyncio.run(cached.asset_inventory.load_asset_inventory())
        inner.asset_id = "WKST-999"
        second = asyncio.run(cached.asset_inventory.load_asset_inventory())

        self.assertEqual(inner.calls, 1)
        self.assertEqual(first.data.assets[0].asset_id, "WKST-047")
        self.assertEqual(second.data.assets[0].asset_id, "WKST-047")

    def test_ttl_cache_refreshes_after_expiry(self):
        clock = _MutableClock()
        inner = _CountingAssetSource()
        cached = with_static_data_cache(
            StaticDataSourceAdapters(
                asset_inventory=inner,
                baselines=_FakeBaselineSource(),
                threat_intel_seed=_FakeIntelSeedSource(),
                topology=_FakeTopologySource(),
            ),
            ttl_seconds=300,
            clock=clock,
        )

        first = asyncio.run(cached.asset_inventory.load_asset_inventory())
        inner.asset_id = "WKST-999"
        clock.advance(301)
        refreshed = asyncio.run(cached.asset_inventory.load_asset_inventory())

        self.assertEqual(inner.calls, 2)
        self.assertEqual(first.data.assets[0].asset_id, "WKST-047")
        self.assertEqual(refreshed.data.assets[0].asset_id, "WKST-999")

    def test_ttl_cache_does_not_hide_missing_source_after_expiry(self):
        clock = _MutableClock()
        inner = _CountingAssetSource()
        cached = with_static_data_cache(
            StaticDataSourceAdapters(
                asset_inventory=inner,
                baselines=_FakeBaselineSource(),
                threat_intel_seed=_FakeIntelSeedSource(),
                topology=_FakeTopologySource(),
            ),
            ttl_seconds=300,
            clock=clock,
        )

        first = asyncio.run(cached.asset_inventory.load_asset_inventory())
        self.assertEqual(first.status, "ok")

        inner.status = "removed"
        before_expiry = asyncio.run(cached.asset_inventory.load_asset_inventory())
        clock.advance(301)
        after_expiry = asyncio.run(cached.asset_inventory.load_asset_inventory())

        self.assertEqual(before_expiry.status, "ok")
        self.assertEqual(after_expiry.status, "unavailable")
        self.assertIn("static_source_missing:asset_inventory:removed", after_expiry.gap_reason)


if __name__ == "__main__":
    unittest.main(verbosity=2)
