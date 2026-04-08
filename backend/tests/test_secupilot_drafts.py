import unittest
from datetime import datetime
import types

from _project_bootstrap import bootstrap

bootstrap()

import scripts.generate_mock_data as generate_mock_data  # noqa: E402
from app.tools import threat_intel as threat_intel  # noqa: E402
from app.agents import graph as graph_orchestrator  # noqa: E402


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
        self.siem = types.SimpleNamespace(
            _cache={
                "scenarios": {
                    "S-02": {
                        "alerts": [{"event_id": "S-02-001", "severity": "HIGH", "destination_asset_id": "WKST-047"}],
                        "scenario": {"name": "Lateral Movement", "action": {"type": "NETWORK_ISOLATE"}},
                    },
                    "S-04": {
                        "alerts": [{"event_id": "S-04-001", "severity": "CRITICAL", "destination_asset_id": "HR-PORTAL-01"}],
                        "scenario": {"name": "Ransomware Precursor", "action": {"type": "EMERGENCY_ISOLATE"}},
                    },
                }
            }
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
        )

    async def test_gather_alerts_uses_user_input_keywords(self):
        alerts = await self.orchestrator._gather_alerts(
            intent="threat_hunt",
            user_input="帮我查一下有没有勒索和C2痕迹",
        )
        self.assertEqual(alerts[0]["event_id"], "S-04-001")

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

    def test_determine_t3_hosts_does_not_fallback_to_all_hosts(self):
        hosts = self.orchestrator._determine_t3_hosts(
            alerts=[],
            asset_id="NO-SUCH-HOST",
            user_input="帮我查指定主机",
        )
        self.assertEqual(hosts, [])

    def test_assemble_case_uses_t3_analysis_scope(self):
        case = self.orchestrator._assemble_case(
            intent="threat_hunt",
            user_input="查横向移动",
            tool_results={
                "triage": {"status": "complete", "top_risk_score": 8.0, "matched_scenario_id": "S-02"},
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
            return [
                {
                    "event_id": "S-02-001",
                    "severity": "HIGH",
                    "destination_asset_id": "WKST-047",
                    "source_ip": "10.1.1.5",
                    "extra": {"query_domain": "data.evil-c2.example.com"},
                }
            ]

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

        async def fake_run_t3(host_ids):
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


if __name__ == "__main__":
    unittest.main()
