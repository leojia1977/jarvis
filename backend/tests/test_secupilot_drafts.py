import unittest
from datetime import datetime
import types

from _project_bootstrap import bootstrap

bootstrap()

import scripts.generate_mock_data as generate_mock_data  # noqa: E402
from app.tools import threat_intel as threat_intel  # noqa: E402
from app.agents import graph as graph_orchestrator  # noqa: E402
from app.tools.host_identity import build_asset_inventory_host_identity_resolver  # noqa: E402
from app.tools.siem_adapter import AdapterResult, TimeRangeSpec  # noqa: E402
from app.tools.static_data_sources import (  # noqa: E402
    AssetInventorySnapshot,
    AssetRecord,
    StaticRefreshPolicy,
    StaticSourceMetadata,
)


class DummyBlast:
    def __init__(self):
        self.asset_index = {
            "HR-PORTAL-01": {"asset_id": "HR-PORTAL-01"},
            "10.1.6.10": {"asset_id": "HR-PORTAL-01"},
        }

    def calculate(self, action_type, target):
        return types.SimpleNamespace(
            action_type=action_type,
            target=target,
            directly_affected=1,
            cascade_affected=2,
            affected_assets=[target],
            affected_users_count=12,
            affected_services=["HR Portal"],
            estimated_downtime_hours=2.0,
            estimated_cost_rmb=50000,
            recommendation="REVIEW_ALTERNATIVES",
            alternatives=[],
            error="",
        )


class FakeSIEMAdapter:
    def __init__(self, scenarios, *, intent_status="ok", scenario_status="ok", intent_delay=0.0, scenario_delay=0.0):
        self.scenarios = scenarios
        self.intent_status = intent_status
        self.scenario_status = scenario_status
        self.intent_delay = intent_delay
        self.scenario_delay = scenario_delay
        self.asset_queries = []

    async def query_recent_summary(self, time_range: TimeRangeSpec):
        alerts = []
        for scenario in self.scenarios.values():
            alerts.extend(scenario.get("alerts", []))
        return AdapterResult.ok({"alerts_considered": len(alerts)})

    async def query_asset_alerts(self, asset_id: str, time_range: TimeRangeSpec):
        self.asset_queries.append(asset_id)
        results = []
        for scenario in self.scenarios.values():
            for alert in scenario.get("alerts", []):
                if (
                    alert.get("destination_asset_id") == asset_id
                    or alert.get("source_ip") == asset_id
                    or alert.get("destination_ip") == asset_id
                ):
                    results.append(alert)
        return AdapterResult.ok(results)

    async def query_intent_alerts(self, intent: str, user_input: str, time_range: TimeRangeSpec):
        if self.intent_delay:
            import asyncio
            await asyncio.sleep(self.intent_delay)
        if self.intent_status == "timeout":
            return AdapterResult.timeout([], gap_reason="adapter_timeout")
        if self.intent_status == "partial":
            query = (user_input or "").lower()
            matched_sid = "S-02"
            if "勒索" in query or "ransom" in query or "c2" in query:
                matched_sid = "S-04"
            scenario = self.scenarios.get(matched_sid, {})
            return AdapterResult.partial(
                list(scenario.get("alerts", [])),
                gap_reason="partial_time_window_data",
                metadata={"scenario_id": matched_sid},
            )
        if self.intent_status == "unavailable":
            return AdapterResult.unavailable([], gap_reason="adapter_unavailable")

        query = (user_input or "").lower()
        matched_sid = "S-02"
        if "勒索" in query or "ransom" in query or "c2" in query:
            matched_sid = "S-04"
        scenario = self.scenarios.get(matched_sid, {})
        return AdapterResult.ok(list(scenario.get("alerts", [])), metadata={"scenario_id": matched_sid})

    async def get_scenario_metadata(self, scenario_id: str):
        if self.scenario_delay:
            import asyncio
            await asyncio.sleep(self.scenario_delay)
        if self.scenario_status == "timeout":
            return AdapterResult.timeout(None, gap_reason="adapter_timeout")
        return AdapterResult.ok(self.scenarios.get(scenario_id, {}).get("scenario"))

    async def get_asset_context(self, asset_id: str):
        return AdapterResult.ok(None)

    def get_runtime_stats(self):
        return {"scenarios_loaded": len(self.scenarios), "assets_loaded": 0}


def _identity_metadata(kind: str, count: int) -> StaticSourceMetadata:
    return StaticSourceMetadata(
        source_kind=kind,
        source_name=f"test:{kind}",
        source_mode="local_files",
        ownership="test",
        record_count=count,
        refresh_policy=StaticRefreshPolicy(strategy="ttl", ttl_seconds=300),
    )


class GenerateMockDataTests(unittest.TestCase):
    def test_scenario_alerts_include_scenario_metadata(self):
        scenario = generate_mock_data.SCENARIOS[0]
        alerts = generate_mock_data.generate_scenario_alerts(scenario)
        self.assertEqual(alerts[0]["enrichment"]["scenario_id"], scenario["scenario_id"])
        self.assertEqual(alerts[0]["enrichment"]["scenario_name"], scenario["name"])

    def test_knowledge_graph_contains_assets_and_dependencies(self):
        graph = generate_mock_data.generate_knowledge_graph()
        self.assertIsInstance(graph["nodes"]["assets"], list)
        self.assertGreater(len(graph["nodes"]["assets"]), 0)
        self.assertTrue(any(rel["type"] == "depends_on" for rel in graph["relationships"]))

    def test_noise_alerts_emit_parseable_utc_timestamps(self):
        alerts = generate_mock_data.generate_noise_alerts(
            2,
            datetime(2026, 4, 1, 8, 0, 0, tzinfo=generate_mock_data.UTC),
        )
        self.assertTrue(alerts[0]["event_time"].endswith("Z"))
        parsed = datetime.fromisoformat(alerts[0]["event_time"].replace("Z", "+00:00"))
        self.assertIsNotNone(parsed.tzinfo)


class ThreatIntelTests(unittest.TestCase):
    def test_no_implicit_subnet_false_positive_without_cidr(self):
        engine = threat_intel.RealThreatIntelEngine(
            {
                "malicious_ips": [{"ip": "45.33.49.12", "threat_type": "C2", "actor": "APT-BEAR", "confidence": 0.95}],
                "malicious_domains": [],
                "malicious_hashes": [],
                "c2_signatures": [],
            }
        )
        report = engine.lookup("45.33.49.99")
        self.assertEqual(report.matches, [])
        self.assertEqual(report.overall_threat_level, "CLEAN")

    def test_subdomain_match_still_works_for_known_malicious_domain(self):
        engine = threat_intel.RealThreatIntelEngine(
            {
                "malicious_ips": [],
                "malicious_domains": [{"domain": "data.evil-c2.example.com", "threat_type": "C2", "confidence": 0.95}],
                "malicious_hashes": [],
                "c2_signatures": [],
            }
        )
        report = engine.lookup("foo.data.evil-c2.example.com")
        self.assertTrue(report.matches)
        self.assertEqual(report.matches[0].match_type, "suffix")


class OrchestratorTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.scenarios = {
            "S-02": {
                "alerts": [{"event_id": "S-02-001", "severity": "HIGH", "destination_asset_id": "WKST-047"}],
                "scenario": {"name": "Lateral Movement", "action": {"type": "NETWORK_ISOLATE"}},
            },
            "S-04": {
                "alerts": [{"event_id": "S-04-001", "severity": "CRITICAL", "destination_asset_id": "HR-PORTAL-01"}],
                "scenario": {"name": "Ransomware Precursor", "action": {"type": "EMERGENCY_ISOLATE"}},
            },
        }
        self.siem = FakeSIEMAdapter(self.scenarios)
        self.identity_resolver = build_asset_inventory_host_identity_resolver(
            AssetInventorySnapshot(
                metadata=_identity_metadata("asset_inventory", 2),
                assets=[
                    AssetRecord(
                        asset_id="WKST-047",
                        hostname="wkst-047",
                        ip_addresses=["10.1.5.22"],
                        aliases=["wkst-047.local"],
                        extra={"fqdn": "wkst-047.corp.local"},
                    ),
                    AssetRecord(
                        asset_id="HR-PORTAL-01",
                        hostname="hr-portal-01",
                        ip_addresses=["10.1.6.10"],
                        aliases=["portal"],
                        extra={"fqdn": "hr-portal-01.corp.local"},
                    ),
                ],
            )
        )
        self.orchestrator = graph_orchestrator.SaiLouOrchestrator(
            siem=self.siem,
            triage=types.SimpleNamespace(),
            intel=types.SimpleNamespace(),
            blast=DummyBlast(),
            process_events_cache={
                "WKST-047": [
                    {
                        "host_id": "WKST-047",
                        "event_type": "process_create",
                        "timestamp": "2026-04-03T01:00:00Z",
                        "pid": 100,
                        "ppid": 4,
                        "process_name": "services.exe",
                        "exe_path": "C:\\Windows\\System32\\services.exe",
                        "command_line": "services.exe",
                        "user": "SYSTEM",
                    }
                ],
                "HR-PORTAL-01": [
                    {
                        "host_id": "HR-PORTAL-01",
                        "event_type": "process_create",
                        "timestamp": "2026-04-03T02:00:00Z",
                        "pid": 200,
                        "ppid": 4,
                        "process_name": "svchost.exe",
                        "exe_path": "C:\\Windows\\System32\\svchost.exe",
                        "command_line": "svchost.exe",
                        "user": "SYSTEM",
                    }
                ],
            },
            host_identity_resolver=self.identity_resolver,
        )

    async def test_gather_alerts_uses_user_input_keywords(self):
        result = await self.orchestrator._gather_alerts(
            intent="threat_hunt",
            user_input="帮我查一下有没有勒索和C2痕迹",
        )
        self.assertEqual(result.status, "ok")
        self.assertEqual(result.metadata["scenario_id"], "S-04")
        self.assertEqual(result.data[0]["event_id"], "S-04-001")

    def test_extract_ips_uses_ipaddress_not_prefix(self):
        indicators = self.orchestrator._extract_ips(
            [
                {"source_ip": "172.217.14.206", "extra": {"dest_ip": "10.1.1.5", "query_domain": "data.evil-c2.example.com"}},
                {"source_ip": "10.1.1.5", "extra": {"dest_ip": "198.51.100.23"}},
            ]
        )
        self.assertIn("172.217.14.206", indicators)
        self.assertIn("198.51.100.23", indicators)
        self.assertNotIn("10.1.1.5", indicators)

    def test_assemble_case_marks_timeout_as_degraded(self):
        case = self.orchestrator._assemble_case(
            intent="threat_hunt",
            user_input="查勒索",
            tool_results={
                "triage": {"status": "complete", "top_risk_score": 9.2, "matched_scenario_id": "S-04"},
                "_timeout": True,
                "_errors": ["tool_timeout"],
                "_planned_tools": ["triage", "blast_radius"],
            },
            tools_used=["triage"],
            raw_alerts=[],
            execution_ms=321.0,
        )
        self.assertEqual(case["verdict_status"], "DEGRADED")
        self.assertIsNone(case["suggested_action"])
        self.assertTrue(case["audit_trail"]["degraded"])
        self.assertTrue(case["case_view"]["executive_summary"]["status_banner"]["visible"])
        self.assertEqual(case["case_view"]["recommended_action"]["action_state"], "DISABLED_DEGRADED")

    async def test_determine_t3_hosts_does_not_fallback_to_all_hosts(self):
        selection = await self.orchestrator._determine_t3_hosts(
            alerts=[],
            asset_id="NO-SUCH-HOST",
            user_input="帮我查指定主机",
        )
        self.assertEqual(selection["host_ids"], [])
        self.assertTrue(selection["identity_gaps"])

    async def test_gather_alerts_resolves_explicit_ip_to_canonical_asset_id(self):
        result = await self.orchestrator._gather_alerts(
            intent="asset_query",
            ip="10.1.6.10",
        )
        self.assertEqual(result.status, "ok")
        self.assertEqual(self.siem.asset_queries[-1], "HR-PORTAL-01")
        self.assertEqual(result.metadata["identity_canonical_asset_id"], "HR-PORTAL-01")
        self.assertEqual(result.metadata["identity_matched_by"], "ip_address")

    async def test_determine_t3_hosts_uses_identity_resolver_for_alert_ip(self):
        selection = await self.orchestrator._determine_t3_hosts(
            alerts=[
                {
                    "event_id": "S-04-001",
                    "severity": "CRITICAL",
                    "source_ip": "10.1.6.10",
                }
            ],
        )
        self.assertEqual(selection["host_ids"], ["HR-PORTAL-01"])

    async def test_run_blast_uses_canonical_asset_id_for_explicit_ip(self):
        result = await self.orchestrator._run_blast(
            alerts=[],
            ip="10.1.6.10",
            user_input="隔离可疑主机",
        )
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["target"], "HR-PORTAL-01")

    def test_assemble_case_uses_t3_analysis_scope(self):
        case = self.orchestrator._assemble_case(
            intent="threat_hunt",
            user_input="查横向移动",
            tool_results={
                "triage": {"status": "complete", "top_risk_score": 8.0, "matched_scenario_id": "S-02"},
                "_scenario_context": self.scenarios["S-02"]["scenario"],
                "process_tree": {
                    "status": "complete",
                    "hosts_analyzed": ["WKST-047"],
                    "total_chains": 1,
                    "suspicious_chains": [{"anomaly_score": 9.4, "attack_stages": ["Execution"]}],
                    "persistence_mechanisms": [],
                    "gaps": [],
                    "ioc_extracted": [],
                    "analysis_scope": ["process_tree", "dns_query"],
                },
                "_errors": [],
                "_planned_tools": ["triage", "process_tree"],
            },
            tools_used=["triage", "process_tree"],
            raw_alerts=[],
            execution_ms=12.3,
            hunt_plan={"hunt_id": "HUNT-TEST-001", "planned_steps": []},
        )
        self.assertEqual(case["forensic_result"]["analysis_scope"], ["process_tree", "dns_query"])
        self.assertEqual(case["hunt_plan"]["hunt_id"], "HUNT-TEST-001")

    async def test_investigate_includes_hunt_plan(self):
        async def fake_gather_alerts(**kwargs):
            return AdapterResult.ok(
                [
                    {
                        "event_id": "S-02-001",
                        "severity": "HIGH",
                        "destination_asset_id": "WKST-047",
                        "source_ip": "10.1.1.5",
                        "extra": {"query_domain": "data.evil-c2.example.com"},
                    }
                ],
                metadata={"scenario_id": "S-02"},
            )

        async def fake_run_triage(alerts):
            return {
                "status": "complete",
                "top_risk_score": 8.8,
                "matched_scenario_id": "S-02",
                "top_alerts": [],
                "total_scanned": 1,
                "noise_archived": 0,
                "compression_ratio": 0.0,
            }

        async def fake_run_intel(indicators):
            return {
                "status": "complete",
                "indicators_checked": len(indicators),
                "matches": [],
                "has_apt_association": False,
                "overall_threat_level": "CLEAN",
                "related_iocs": [],
            }

        async def fake_run_blast(alerts, asset_id=None, ip=None, user_input=None):
            return {
                "status": "complete",
                "directly_affected": 1,
                "cascade_affected": 2,
                "affected_users": 12,
                "estimated_cost_rmb": 50000,
                "estimated_downtime_hours": 2.0,
                "recommendation": "REVIEW_ALTERNATIVES",
                "alternatives": [],
            }

        async def fake_run_t3(host_ids, identity_gaps=None):
            return {
                "status": "complete",
                "hosts_analyzed": ["WKST-047"],
                "missing_hosts": [],
                "total_chains": 1,
                "suspicious_chains": [{"anomaly_score": 9.6, "attack_stages": ["Credential Access"]}],
                "persistence_mechanisms": [],
                "ioc_extracted": [{"type": "hash", "value": "abcd", "source_chain_id": "WKST-047:chain-001", "source_node_id": "WKST-047:chain-001:node-001", "context": "tool", "confidence": 0.9}],
                "gaps": [],
                "analysis_scope": ["process_tree"],
            }

        self.orchestrator._gather_alerts = fake_gather_alerts
        self.orchestrator._run_triage = fake_run_triage
        self.orchestrator._run_intel = fake_run_intel
        self.orchestrator._run_blast = fake_run_blast
        self.orchestrator._run_t3 = fake_run_t3

        case = await self.orchestrator.investigate(
            intent="threat_hunt",
            user_input="帮我查一下内网有没有横向移动",
            timeout=2.0,
        )
        self.assertIsNotNone(case.get("hunt_plan"))
        self.assertEqual(case["audit_trail"]["planner"], "jarvis")
        self.assertGreaterEqual(len(case["hunt_plan"]["planned_steps"]), 3)
        self.assertEqual(case["case_view"]["jarvis_plan"]["hypothesis"], case["hunt_plan"]["hypothesis"])
        self.assertIn("scope", case["case_view"]["jarvis_plan"])
        self.assertIn("stop_conditions", case["case_view"]["jarvis_plan"])
        self.assertIn("status_banner", case["case_view"]["executive_summary"])
        self.assertIn("action_state", case["case_view"]["recommended_action"])
        self.assertIn("missing_telemetry_summary", case["case_view"]["analysis_limits"])
        self.assertIn("unavailable_tools_summary", case["case_view"]["analysis_limits"])

    async def test_siem_timeout_maps_to_degraded_not_error(self):
        timed_out = graph_orchestrator.SaiLouOrchestrator(
            siem=FakeSIEMAdapter(self.scenarios, intent_status="timeout"),
            triage=types.SimpleNamespace(),
            intel=types.SimpleNamespace(),
            blast=DummyBlast(),
            process_events_cache={},
        )

        async def fake_run_triage(alerts):
            return {
                "status": "complete",
                "top_risk_score": 4.2,
                "matched_scenario_id": None,
                "top_alerts": [],
                "total_scanned": 0,
                "noise_archived": 0,
                "compression_ratio": 0.0,
            }

        timed_out._run_triage = fake_run_triage

        case = await timed_out.investigate(
            intent="summarize_recent",
            user_input="帮我总结最近态势",
            timeout=2.0,
        )
        self.assertEqual(case["verdict_status"], "DEGRADED")
        self.assertEqual(case["investigation_status"], "DEGRADED")
        self.assertIn("siem_adapter_timeout", case["audit_trail"]["degraded_reasons"])
        self.assertNotEqual(case["case_id"], "ERROR")

    async def test_siem_unavailable_maps_to_degraded(self):
        unavailable = graph_orchestrator.SaiLouOrchestrator(
            siem=FakeSIEMAdapter(self.scenarios, intent_status="unavailable"),
            triage=types.SimpleNamespace(),
            intel=types.SimpleNamespace(),
            blast=DummyBlast(),
            process_events_cache={},
        )

        async def fake_run_triage(alerts):
            return {
                "status": "complete",
                "top_risk_score": 4.2,
                "matched_scenario_id": None,
                "top_alerts": [],
                "total_scanned": 0,
                "noise_archived": 0,
                "compression_ratio": 0.0,
            }

        unavailable._run_triage = fake_run_triage

        case = await unavailable.investigate(
            intent="summarize_recent",
            user_input="帮我总结最近态势",
            timeout=2.0,
        )
        self.assertEqual(case["verdict_status"], "DEGRADED")
        self.assertEqual(case["investigation_status"], "DEGRADED")
        self.assertIn("siem_adapter_unavailable", case["audit_trail"]["degraded_reasons"])
        self.assertIn("siem_adapter_adapter_unavailable", case["audit_trail"]["degraded_reasons"])

    async def test_siem_partial_maps_to_degraded_with_partial_data(self):
        partial = graph_orchestrator.SaiLouOrchestrator(
            siem=FakeSIEMAdapter(self.scenarios, intent_status="partial"),
            triage=types.SimpleNamespace(),
            intel=types.SimpleNamespace(),
            blast=DummyBlast(),
            process_events_cache={},
        )

        async def fake_run_triage(alerts):
            return {
                "status": "complete",
                "top_risk_score": 7.8,
                "matched_scenario_id": "S-02",
                "top_alerts": [],
                "total_scanned": len(alerts),
                "noise_archived": 0,
                "compression_ratio": 0.0,
            }

        partial._run_triage = fake_run_triage

        case = await partial.investigate(
            intent="threat_hunt",
            user_input="帮我查一下横向移动",
            timeout=2.0,
        )
        self.assertEqual(case["verdict_status"], "DEGRADED")
        self.assertEqual(case["investigation_status"], "DEGRADED")
        self.assertEqual(case["triage_summary"]["total_events_scanned"], 1)
        self.assertIn("siem_adapter_partial", case["audit_trail"]["degraded_reasons"])
        self.assertIn("siem_adapter_partial_time_window_data", case["audit_trail"]["degraded_reasons"])

    async def test_siem_gather_timeout_maps_to_degraded(self):
        slow = graph_orchestrator.SaiLouOrchestrator(
            siem=FakeSIEMAdapter(self.scenarios, intent_delay=0.2),
            triage=types.SimpleNamespace(),
            intel=types.SimpleNamespace(),
            blast=DummyBlast(),
            process_events_cache={},
        )

        async def fake_run_triage(alerts):
            return {
                "status": "complete",
                "top_risk_score": 4.2,
                "matched_scenario_id": None,
                "top_alerts": [],
                "total_scanned": 0,
                "noise_archived": 0,
                "compression_ratio": 0.0,
            }

        slow._run_triage = fake_run_triage

        case = await slow.investigate(
            intent="summarize_recent",
            user_input="帮我总结最近态势",
            timeout=0.2,
        )
        self.assertEqual(case["verdict_status"], "DEGRADED")
        self.assertIn("siem_adapter_timeout", case["audit_trail"]["degraded_reasons"])
        self.assertIn("siem_adapter_siem_gather_timeout", case["audit_trail"]["degraded_reasons"])
        self.assertNotEqual(case["case_id"], "ERROR")

    async def test_siem_scenario_metadata_timeout_keeps_case_degraded_not_error(self):
        slow_meta = graph_orchestrator.SaiLouOrchestrator(
            siem=FakeSIEMAdapter(self.scenarios, scenario_delay=0.2),
            triage=types.SimpleNamespace(),
            intel=types.SimpleNamespace(),
            blast=DummyBlast(),
            process_events_cache={},
        )

        async def fake_run_triage(alerts):
            return {
                "status": "complete",
                "top_risk_score": 7.8,
                "matched_scenario_id": "S-02",
                "top_alerts": [],
                "total_scanned": len(alerts),
                "noise_archived": 0,
                "compression_ratio": 0.0,
            }

        slow_meta._run_triage = fake_run_triage

        case = await slow_meta.investigate(
            intent="threat_hunt",
            user_input="帮我查一下横向移动",
            timeout=0.4,
        )
        self.assertEqual(case["verdict_status"], "DEGRADED")
        self.assertEqual(case["investigation_status"], "DEGRADED")
        self.assertEqual(case["scenario_name"], "")
        self.assertIn("siem_adapter_timeout", case["audit_trail"]["degraded_reasons"])
        self.assertIn("siem_adapter_siem_scenario_metadata_timeout", case["audit_trail"]["degraded_reasons"])


if __name__ == "__main__":
    unittest.main()
