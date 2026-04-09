import unittest

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.config import Settings
from app.tools.static_data_sources import (
    AssetInventorySnapshot,
    AssetRecord,
    BaselineRecord,
    BaselineSnapshot,
    HostIdentityRecord,
    StaticRefreshPolicy,
    StaticSourceMetadata,
    ThreatIntelSeedRecord,
    ThreatIntelSeedSnapshot,
    TopologySnapshot,
)


class StaticDataContractTests(unittest.TestCase):
    def test_get_static_data_dir_aliases_mock_data_dir(self):
        configured = Settings(
            project_root="C:/Users/Administrator/Documents/New project",
            static_data_path="",
            mock_data_path="./mock_data",
        )
        self.assertEqual(configured.get_static_data_dir(), configured.get_mock_data_dir())

    def test_get_static_data_dir_prefers_explicit_static_data_path(self):
        configured = Settings(
            project_root="C:/Users/Administrator/Documents/New project",
            static_data_path="./mock_data",
            mock_data_path="./legacy_mock_data",
        )
        self.assertTrue(str(configured.get_static_data_dir()).endswith("mock_data"))

    def test_contract_dataclasses_cover_all_static_domains(self):
        refresh = StaticRefreshPolicy(strategy="startup", ttl_seconds=300)

        assets = AssetInventorySnapshot(
            metadata=StaticSourceMetadata(
                source_kind="asset_inventory",
                source_name="mock_assets",
                source_mode="local_files",
                ownership="T1/T5 asset inventory",
                record_count=1,
                refresh_policy=refresh,
            ),
            assets=[
                AssetRecord(
                    asset_id="WKST-047",
                    hostname="wkst-047",
                    ip_addresses=["10.1.2.4"],
                )
            ],
        )
        baselines = BaselineSnapshot(
            metadata=StaticSourceMetadata(
                source_kind="baseline",
                source_name="mock_baselines",
                source_mode="local_files",
                ownership="T1 baseline dampening",
                record_count=1,
                refresh_policy=refresh,
            ),
            baselines=[
                BaselineRecord(
                    baseline_id="FP-1",
                    category="normal_admin",
                    pattern_description="Known admin activity",
                    confidence=0.9,
                )
            ],
        )
        intel_seed = ThreatIntelSeedSnapshot(
            metadata=StaticSourceMetadata(
                source_kind="intel_seed",
                source_name="mock_ioc_seed",
                source_mode="local_files",
                ownership="T4 intel enrichment seed",
                record_count=1,
                refresh_policy=refresh,
            ),
            records=[
                ThreatIntelSeedRecord(
                    indicator="185.220.101.45",
                    indicator_type="ip",
                    threat_type="C2",
                )
            ],
        )
        topology = TopologySnapshot(
            metadata=StaticSourceMetadata(
                source_kind="topology",
                source_name="mock_topology",
                source_mode="local_files",
                ownership="T5 blast radius graph",
                record_count=1,
                refresh_policy=refresh,
            ),
            nodes={"assets": [{"asset_id": "WKST-047"}]},
            edges=[{"from": "WKST-047", "to": "HR-PORTAL-01"}],
        )
        identity = HostIdentityRecord(
            canonical_asset_id="WKST-047",
            hostname="wkst-047",
            ip_addresses=["10.1.2.4"],
            aliases=["wkst-047.local"],
            source_refs=["asset_inventory:WKST-047"],
        )

        self.assertEqual(assets.assets[0].asset_id, "WKST-047")
        self.assertEqual(baselines.baselines[0].baseline_id, "FP-1")
        self.assertEqual(intel_seed.records[0].indicator_type, "ip")
        self.assertEqual(topology.nodes["assets"][0]["asset_id"], "WKST-047")
        self.assertEqual(identity.canonical_asset_id, "WKST-047")
