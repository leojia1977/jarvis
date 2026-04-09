import unittest

from _project_bootstrap import bootstrap

bootstrap()

from app.tools.host_identity import build_asset_inventory_host_identity_resolver
from app.tools.static_data_sources import (
    AssetInventorySnapshot,
    AssetRecord,
    StaticRefreshPolicy,
    StaticSourceMetadata,
)


def _metadata(count: int) -> StaticSourceMetadata:
    return StaticSourceMetadata(
        source_kind="asset_inventory",
        source_name="test:asset_inventory",
        source_mode="local_files",
        ownership="test",
        record_count=count,
        refresh_policy=StaticRefreshPolicy(strategy="ttl", ttl_seconds=300),
    )


class HostIdentityResolverTests(unittest.IsolatedAsyncioTestCase):
    async def test_resolve_any_uses_frozen_priority_order(self):
        resolver = build_asset_inventory_host_identity_resolver(
            AssetInventorySnapshot(
                metadata=_metadata(1),
                assets=[
                    AssetRecord(
                        asset_id="ASSET-WKST-047",
                        hostname="wkst-047",
                        ip_addresses=["10.1.5.22"],
                        aliases=["wkst-047.local"],
                        extra={"fqdn": "wkst-047.corp.local"},
                    )
                ],
            )
        )

        by_asset = await resolver.resolve_any("ASSET-WKST-047")
        by_host = await resolver.resolve_any("wkst-047")
        by_fqdn = await resolver.resolve_any("wkst-047.corp.local")
        by_ip = await resolver.resolve_any("10.1.5.22")
        by_alias = await resolver.resolve_any("wkst-047.local")

        self.assertEqual(by_asset.status, "ok")
        self.assertEqual(by_asset.data.canonical_asset_id, "ASSET-WKST-047")
        self.assertEqual(by_asset.metadata["matched_by"], "asset_id")
        self.assertEqual(by_host.metadata["matched_by"], "hostname")
        self.assertEqual(by_fqdn.metadata["matched_by"], "fqdn")
        self.assertEqual(by_ip.metadata["matched_by"], "ip_address")
        self.assertEqual(by_alias.metadata["matched_by"], "aliases")

    async def test_resolve_any_returns_partial_for_ambiguous_alias(self):
        resolver = build_asset_inventory_host_identity_resolver(
            AssetInventorySnapshot(
                metadata=_metadata(2),
                assets=[
                    AssetRecord(
                        asset_id="WKST-047",
                        hostname="wkst-047",
                        ip_addresses=["10.1.5.22"],
                        aliases=["finance-terminal"],
                    ),
                    AssetRecord(
                        asset_id="WKST-099",
                        hostname="wkst-099",
                        ip_addresses=["10.1.5.99"],
                        aliases=["finance-terminal"],
                    ),
                ],
            )
        )

        result = await resolver.resolve_any("finance-terminal")

        self.assertEqual(result.status, "partial")
        self.assertIsNone(result.data)
        self.assertIn("identity_ambiguous:aliases:finance-terminal", result.gap_reason)
        self.assertEqual(sorted(result.metadata["candidate_asset_ids"]), ["WKST-047", "WKST-099"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
