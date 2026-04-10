import asyncio
import unittest
from datetime import datetime, timezone
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from backend.app.config import Settings
from app.tools.edr_adapter import (
    CanonicalProcessEvent,
    EDRSourceMetadata,
    LocalFileEDRAdapter,
    ProcessEventBatch,
    ProductionEDRAdapter,
    process_event_batch_to_runtime_payload,
)
from app.tools.siem_adapter import TimeRangeSpec
from app.tools.static_data_sources import HostIdentityRecord

REPO_ROOT = Path(__file__).resolve().parents[2]


class _FakeEDRTransport:
    def __init__(self, response):
        self.response = response
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
        return self.response


class EDRAdapterContractTests(unittest.TestCase):
    def test_config_freezes_edr_fields(self):
        configured = Settings(
            edr_source_mode="replay",
            edr_vendor="elastic_defend_like",
            edr_base_url="https://edr.example.local",
            edr_auth_token="test-token",
            edr_request_timeout_seconds=9.5,
        )

        self.assertEqual(configured.edr_source_mode, "replay")
        self.assertEqual(configured.edr_vendor, "elastic_defend_like")
        self.assertEqual(configured.edr_base_url, "https://edr.example.local")
        self.assertEqual(configured.edr_auth_token, "test-token")
        self.assertEqual(configured.edr_request_timeout_seconds, 9.5)

    def test_contract_batch_preserves_canonical_process_event_schema(self):
        time_range = TimeRangeSpec.from_value(
            "24h",
            "Asia/Shanghai",
            now=datetime(2026, 4, 9, 12, 0, tzinfo=timezone.utc),
        )
        host_identity = HostIdentityRecord(
            canonical_asset_id="WKST-047",
            hostname="wkst-047",
            fqdn="wkst-047.corp.local",
            ip_addresses=["10.1.5.22"],
            aliases=["finance-terminal"],
            source_refs=["asset_inventory:WKST-047"],
        )
        batch = ProcessEventBatch(
            metadata=EDRSourceMetadata(
                source_name="mock_process_events",
                source_mode="replay",
                vendor="crowdstrike_like",
                ownership="T3 production process-event ingestion",
                collected_at_utc="2026-04-09T12:00:00Z",
                record_count=3,
            ),
            host_identity=host_identity,
            time_range=time_range,
            events=[
                CanonicalProcessEvent(
                    event_type="process_create",
                    host_id="WKST-047",
                    timestamp="2026-04-09T11:00:00Z",
                    pid=3100,
                    ppid=1,
                    process_name="services.exe",
                    exe_path="C:\\Windows\\System32\\services.exe",
                    command_line="services.exe",
                    user="SYSTEM",
                ),
                CanonicalProcessEvent(
                    event_type="network_connect",
                    host_id="WKST-047",
                    timestamp="2026-04-09T11:01:00Z",
                    pid=3100,
                    ppid=1,
                    process_name="services.exe",
                    exe_path="C:\\Windows\\System32\\services.exe",
                    command_line="services.exe",
                    user="SYSTEM",
                    src_ip="10.1.5.22",
                    dst_ip="10.1.1.5",
                    dst_port=88,
                    protocol="TCP",
                ),
                CanonicalProcessEvent(
                    event_type="dns_query",
                    host_id="WKST-047",
                    timestamp="2026-04-09T11:02:00Z",
                    pid=3100,
                    ppid=1,
                    process_name="services.exe",
                    exe_path="C:\\Windows\\System32\\services.exe",
                    command_line="services.exe",
                    user="SYSTEM",
                    query_domain="update.legit-looking.xyz",
                    query_type="A",
                ),
            ],
        )

        runtime_payload = process_event_batch_to_runtime_payload(batch)

        self.assertEqual(batch.host_identity.canonical_asset_id, "WKST-047")
        self.assertEqual(batch.time_range.tz_label, "Asia/Shanghai")
        self.assertEqual(runtime_payload[0]["event_type"], "process_create")
        self.assertEqual(runtime_payload[1]["dst_ip"], "10.1.1.5")
        self.assertEqual(runtime_payload[1]["protocol"], "TCP")
        self.assertEqual(runtime_payload[2]["query_domain"], "update.legit-looking.xyz")
        self.assertEqual(runtime_payload[2]["host_id"], "WKST-047")

    def test_local_file_adapter_loads_mock_process_events(self):
        spec = TimeRangeSpec.from_value(
            "24h",
            "Asia/Shanghai",
            now=datetime(2026, 4, 9, 12, 0, tzinfo=timezone.utc),
        )
        host_identity = HostIdentityRecord(
            canonical_asset_id="WKST-047",
            hostname="wkst-047",
            fqdn="wkst-047.corp.local",
            ip_addresses=["10.1.5.22"],
            aliases=["finance-terminal"],
            source_refs=["asset_inventory:WKST-047"],
        )
        adapter = LocalFileEDRAdapter(
            REPO_ROOT / "mock_data" / "process_events"
        )

        result = asyncio.run(adapter.query_process_events(host_identity, spec))

        self.assertEqual(result.status, "ok")
        self.assertGreater(len(result.data.events), 0)
        self.assertEqual(result.data.events[0].host_id, "WKST-047")
        self.assertEqual(adapter.get_runtime_stats()["process_event_hosts"], 4)

    def test_production_adapter_returns_unavailable_when_not_configured(self):
        spec = TimeRangeSpec.from_value(
            "24h",
            "Asia/Shanghai",
            now=datetime(2026, 4, 9, 12, 0, tzinfo=timezone.utc),
        )
        host_identity = HostIdentityRecord(
            canonical_asset_id="WKST-047",
            hostname="wkst-047",
            fqdn="wkst-047.corp.local",
            ip_addresses=["10.1.5.22"],
            aliases=[],
            source_refs=["asset_inventory:WKST-047"],
        )
        adapter = ProductionEDRAdapter(Settings())

        result = asyncio.run(adapter.query_process_events(host_identity, spec))

        self.assertEqual(result.status, "unavailable")
        self.assertEqual(result.gap_reason, "production_edr_not_configured")

    def test_production_adapter_normalizes_process_events(self):
        spec = TimeRangeSpec.from_value(
            "24h",
            "Asia/Shanghai",
            now=datetime(2026, 4, 9, 12, 0, tzinfo=timezone.utc),
        )
        host_identity = HostIdentityRecord(
            canonical_asset_id="WKST-047",
            hostname="wkst-047",
            fqdn="wkst-047.corp.local",
            ip_addresses=["10.1.5.22"],
            aliases=["finance-terminal"],
            source_refs=["asset_inventory:WKST-047"],
        )
        transport = _FakeEDRTransport(
            {
                "status": "partial",
                "events": [
                    {
                        "host": {"id": "WKST-047"},
                        "event": {
                            "type": "process_create",
                            "created": "2026-04-09T11:00:00Z",
                        },
                        "process": {
                            "pid": 3100,
                            "parent": {"pid": 4},
                            "name": "rundll32.exe",
                            "executable": "C:\\Windows\\System32\\rundll32.exe",
                            "command_line": "rundll32.exe advapi32.dll,ProcessIdleTasks",
                        },
                        "user": {"name": "SYSTEM"},
                    }
                ],
                "metadata": {"source": "fake-edr"},
            }
        )
        adapter = ProductionEDRAdapter(
            Settings(
                edr_base_url="https://edr.example.local",
                edr_auth_token="token",
                edr_vendor="generic_http",
            ),
            transport=transport,
        )

        result = asyncio.run(adapter.query_process_events(host_identity, spec))

        self.assertEqual(result.status, "partial")
        self.assertEqual(result.data.events[0].event_type, "process_create")
        self.assertEqual(result.data.events[0].process_name, "rundll32.exe")
        self.assertEqual(result.data.events[0].user, "SYSTEM")
        self.assertNotIn("process", result.data.events[0].extra)
        self.assertTrue(transport.calls[0]["endpoint"].endswith("/api/v1/process-events/query"))
