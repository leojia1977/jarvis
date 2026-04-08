#!/usr/bin/env python3
"""
SecuPilot Sprint 2: T3 + JARVIS 测试套件
"""

import json
import unittest
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from app.tools.process_tree_t3 import ProcessTreeCompiler, T3Result  # noqa: E402
from app.agents.jarvis_hunt_engine import JarvisHuntEngine  # noqa: E402


DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data" / "process_events"


def load_events(host_id: str) -> list:
    fname = f"process_events_{host_id.lower().replace('-', '_')}.json"
    fpath = DATA_DIR / fname
    if not fpath.exists():
        return []
    with open(fpath, encoding="utf-8") as f:
        return json.load(f)["events"]


class TestT3BasicAnalysis(unittest.TestCase):
    def setUp(self):
        self.compiler = ProcessTreeCompiler(top_k=3)

    def test_lateral_movement_detection(self):
        events = load_events("WKST-047")
        result = self.compiler.analyze("WKST-047", events)
        self.assertIn(result.analysis_status, ("COMPLETE", "PARTIAL"))
        self.assertGreater(len(result.suspicious_chains), 0)
        top_chain = result.suspicious_chains[0]
        process_names = [n["process_name"] for n in top_chain["path"]]
        has_attack_tool = any(name in ("mimikatz.exe", "rubeus.exe") for name in process_names)
        self.assertTrue(has_attack_tool, f"Top chain should contain attack tool, got: {process_names}")
        self.assertGreaterEqual(top_chain["anomaly_score"], 7.0)

    def test_ransomware_precursor_detection(self):
        events = load_events("HR-PORTAL-01")
        result = self.compiler.analyze("HR-PORTAL-01", events)
        self.assertIn(result.analysis_status, ("COMPLETE", "PARTIAL"))
        self.assertGreater(len(result.suspicious_chains), 0)
        all_rules = []
        for chain in result.suspicious_chains:
            all_rules.extend(chain["matched_rules"])
        all_rules_lower = " ".join(all_rules).lower()
        self.assertTrue("shadow" in all_rules_lower or "vssadmin" in all_rules_lower or "c2" in all_rules_lower)

    def test_noise_host_no_high_risk_chains(self):
        events = load_events("SIEM-SRV-01")
        result = self.compiler.analyze("SIEM-SRV-01", events)
        for chain in result.suspicious_chains:
            self.assertLess(chain["anomaly_score"], 7.0)
        self.assertEqual(result.ioc_extracted, [])

    def test_empty_events_returns_failed(self):
        result = self.compiler.analyze("EMPTY-HOST", [])
        self.assertEqual(result.analysis_status, "FAILED")


class TestT3FrozenContracts(unittest.TestCase):
    def setUp(self):
        self.compiler = ProcessTreeCompiler(top_k=3)
        events = load_events("WKST-047")
        self.result = self.compiler.analyze("WKST-047", events)

    def test_evidence_status_values(self):
        allowed = {"VERIFIED", "INFERRED", "UNVERIFIED"}
        for chain in self.result.suspicious_chains:
            for node in chain["path"]:
                self.assertIn(node["evidence_status"], allowed)

    def test_analysis_status_values(self):
        self.assertIn(self.result.analysis_status, {"COMPLETE", "PARTIAL", "DEGRADED", "FAILED"})

    def test_analysis_scope_declared(self):
        self.assertIsInstance(self.result.analysis_scope, list)
        self.assertGreater(len(self.result.analysis_scope), 0)
        self.assertIn("process_tree", self.result.analysis_scope)

    def test_ioc_extracted_typed_schema(self):
        allowed_types = {"ip", "domain", "hash"}
        for ioc in self.result.ioc_extracted:
            self.assertIn(ioc["type"], allowed_types)
            self.assertTrue(ioc["source_chain_id"])
            self.assertRegex(ioc["source_node_id"], r"^WKST-047:chain-\d{3}:node-\d{3}$")

    def test_chain_id_format(self):
        for chain in self.result.suspicious_chains:
            self.assertTrue(chain["chain_id"].startswith("WKST-047:chain-"))

    def test_node_id_format(self):
        for chain in self.result.suspicious_chains:
            for node in chain["path"]:
                self.assertRegex(node["node_id"], r"^WKST-047:chain-\d{3}:node-\d{3}$")


class TestT3Persistence(unittest.TestCase):
    def test_registry_run_key_detected(self):
        compiler = ProcessTreeCompiler()
        events = load_events("WKST-047")
        result = compiler.analyze("WKST-047", events)
        self.assertGreater(len(result.persistence_mechanisms), 0)
        types = [p["type"] for p in result.persistence_mechanisms]
        self.assertTrue("service_registration" in types or "registry_run_key" in types)

    def test_ransomware_persistence(self):
        compiler = ProcessTreeCompiler()
        events = load_events("HR-PORTAL-01")
        result = compiler.analyze("HR-PORTAL-01", events)
        run_keys = [p for p in result.persistence_mechanisms if p["type"] == "registry_run_key"]
        self.assertGreater(len(run_keys), 0)


class TestT3IOCExtraction(unittest.TestCase):
    def test_extracts_external_ip(self):
        compiler = ProcessTreeCompiler()
        events = load_events("HR-PORTAL-01")
        result = compiler.analyze("HR-PORTAL-01", events)
        ip_iocs = [i for i in result.ioc_extracted if i["type"] == "ip"]
        self.assertGreater(len(ip_iocs), 0)
        ips = [i["value"] for i in ip_iocs]
        self.assertIn("185.220.101.45", ips)

    def test_extracts_suspicious_domain(self):
        compiler = ProcessTreeCompiler()
        events = load_events("HR-PORTAL-01")
        result = compiler.analyze("HR-PORTAL-01", events)
        domain_iocs = [i for i in result.ioc_extracted if i["type"] == "domain"]
        self.assertGreater(len(domain_iocs), 0)

    def test_no_private_ip_in_iocs(self):
        compiler = ProcessTreeCompiler()
        events = load_events("WKST-047")
        result = compiler.analyze("WKST-047", events)
        for ioc in result.ioc_extracted:
            if ioc["type"] == "ip":
                self.assertFalse(ioc["value"].startswith(("10.", "192.168.")))

    def test_no_internal_domain_in_iocs(self):
        compiler = ProcessTreeCompiler()
        events = load_events("DEV-WS-01")
        result = compiler.analyze("DEV-WS-01", events)
        for ioc in result.ioc_extracted:
            if ioc["type"] == "domain":
                self.assertFalse(ioc["value"].endswith((".local", ".corp", ".internal")))


class TestJarvisHuntPlan(unittest.TestCase):
    def setUp(self):
        self.jarvis = JarvisHuntEngine()

    def test_lateral_movement_hypothesis(self):
        plan = self.jarvis.create_hunt_plan(
            trigger_type="user_query",
            user_input="帮我查一下有没有横向移动",
            intent="threat_hunt",
        )
        self.assertIn("横向", plan.hypothesis)
        self.assertEqual(plan.priority, "HIGH")
        self.assertGreaterEqual(len(plan.planned_steps), 3)

    def test_ransomware_hypothesis(self):
        plan = self.jarvis.create_hunt_plan(
            trigger_type="user_query",
            user_input="有没有勒索软件的迹象",
        )
        self.assertIn("勒索", plan.hypothesis)
        self.assertEqual(plan.priority, "CRITICAL")

    def test_plan_injects_target(self):
        plan = self.jarvis.create_hunt_plan(
            trigger_type="user_query",
            user_input="查一下这台机器",
            target_asset_id="HR-PORTAL-01",
        )
        t3_steps = [s for s in plan.planned_steps if s.tool == "T3"]
        self.assertTrue(any(s.target == "HR-PORTAL-01" for s in t3_steps))

    def test_plan_schema_compliance(self):
        plan = self.jarvis.create_hunt_plan(
            trigger_type="user_query",
            user_input="查横向移动",
        )
        d = self.jarvis.plan_to_dict(plan)
        self.assertIn("hunt_id", d)
        self.assertIn("hypothesis", d)
        self.assertIn("planned_steps", d)
        for step in d["planned_steps"]:
            self.assertIn("seq", step)
            self.assertIn("tool", step)
            self.assertIn("action", step)
            self.assertIn("purpose", step)

    def test_generic_fallback(self):
        plan = self.jarvis.create_hunt_plan(
            trigger_type="user_query",
            user_input="看看情况",
        )
        self.assertEqual(plan.priority, "MEDIUM")


class TestT3Performance(unittest.TestCase):
    def test_analysis_under_200ms(self):
        compiler = ProcessTreeCompiler()
        events = []
        for i in range(500):
            events.append({
                "event_type": "process_create",
                "pid": i + 100,
                "ppid": max(1, i + 99),
                "process_name": f"proc_{i}.exe",
                "exe_path": f"C:\\Windows\\proc_{i}.exe",
                "command_line": f"proc_{i}.exe",
                "user": "SYSTEM",
                "timestamp": f"2026-04-01T12:{i % 60:02d}:00Z",
                "host_id": "PERF-TEST",
            })

        import time

        start = time.monotonic()
        result = compiler.analyze("PERF-TEST", events)
        elapsed = (time.monotonic() - start) * 1000
        self.assertLess(elapsed, 200)
        self.assertEqual(result.process_tree_stats["total_processes"], 500)


if __name__ == "__main__":
    unittest.main(verbosity=2)
