import unittest

from _project_bootstrap import bootstrap

bootstrap()

from app.agents.case_view import build_case_view, generate_one_liner  # noqa: E402


def _sample_chain(chain_id="WKST-047:chain-000", host="WKST-047"):
    return {
        "chain_id": chain_id,
        "anomaly_score": 10.0,
        "path": [
            {
                "node_id": f"{host}:chain-000:node-001",
                "process_name": "services.exe",
                "anomalies": [],
            },
            {
                "node_id": f"{host}:chain-000:node-002",
                "process_name": "PSEXESVC.exe",
                "anomalies": [{"type": "suspicious_parent_child", "risk": 7, "mitre": "T1570", "desc": "PsExec remote service installation"}],
            },
            {
                "node_id": f"{host}:chain-000:node-003",
                "process_name": "mimikatz.exe",
                "anomalies": [{"type": "known_attack_tool", "risk": 10, "mitre": "T1003.001", "desc": "Known attack tool: Credential dumping tool"}],
            },
        ],
        "attack_stages": ["Execution", "Credential Access"],
    }


def _base_case():
    return {
        "case_id": "CASE-TEST-001",
        "version": "3.1",
        "risk_score": 9.2,
        "confidence_score": 0.92,
        "confidence_label": "HIGH",
        "verdict_status": "CRITICAL_ACTION_REQUIRED",
        "investigation_status": "COMPLETE",
        "scenario_name": "Lateral Movement + Credential Theft",
        "forensic_result": {
            "hosts_analyzed": ["DEV-WS-01", "WKST-047"],
            "total_suspicious_chains": 2,
            "top_chains": [_sample_chain()],
            "attack_stages_observed": ["Execution", "Lateral Movement", "Credential Access"],
            "persistence_mechanisms": [
                {
                    "type": "service_registration",
                    "key_path": "HKLM\\System\\CurrentControlSet\\Services\\PSEXESVC",
                }
            ],
            "evidence_gaps": [],
        },
        "hunt_plan": {
            "hypothesis": "内网可能存在横向移动行为",
            "planned_steps": [
                {"seq": 1, "tool": "T1"},
                {"seq": 2, "tool": "T3"},
                {"seq": 3, "tool": "T4"},
                {"seq": 4, "tool": "T5"},
            ],
        },
        "intel_summary": {
            "matches": [
                {
                    "indicator": "185.220.101.45",
                    "match_type": "exact",
                    "ioc_type": "ip",
                    "actor": "RANSOMWARE-X",
                },
                {
                    "indicator": "foo.example.com",
                    "match_type": "suffix",
                    "ioc_type": "domain",
                    "actor": "UNKNOWN",
                },
            ],
            "threat_level": "HIGH",
        },
        "suggested_action": {
            "type": "EMERGENCY_ISOLATE",
            "targets": ["DEV-WS-01", "WKST-047"],
            "blast_radius_desc": "隔离影响 12 个级联资产，预估损失 ¥2,310,000",
        },
        "audit_trail": {
            "degraded": False,
            "degraded_reasons": [],
        },
    }


class CaseViewTests(unittest.TestCase):
    def test_complete_case_has_all_panels(self):
        case = _base_case()
        view = build_case_view(case)
        self.assertIn("executive_summary", view)
        self.assertIn("what_happened", view)
        self.assertIn("why_it_matters", view)
        self.assertIn("jarvis_plan", view)
        self.assertIn("recommended_action", view)
        self.assertIn("evidence_panels", view)
        self.assertIn("analysis_limits", view)
        self.assertEqual(view["what_happened"]["primary_chain"]["highlight_node_id"], "WKST-047:chain-000:node-003")
        self.assertEqual(view["jarvis_plan"]["scope"]["targets"], [])
        self.assertEqual(view["jarvis_plan"]["steps_total"], 4)
        self.assertEqual(len(view["jarvis_plan"]["next_steps"]), 3)
        self.assertTrue(view["jarvis_plan"]["stop_conditions"])
        self.assertEqual(view["jarvis_plan"]["next_suggested"], "复核影响面后提交人工审批")

    def test_case_without_t3_chain_does_not_fail(self):
        case = _base_case()
        case["forensic_result"] = None
        view = build_case_view(case)
        self.assertIsNone(view["what_happened"]["primary_chain"])
        self.assertEqual(view["what_happened"]["affected_hosts"], [])

    def test_degraded_case_disables_recommended_action(self):
        case = _base_case()
        case["investigation_status"] = "DEGRADED"
        case["verdict_status"] = "DEGRADED"
        case["audit_trail"] = {"degraded": True, "degraded_reasons": ["tool_timeout"]}
        case["suggested_action"] = None
        view = build_case_view(case)
        self.assertFalse(view["recommended_action"]["available"])
        self.assertEqual(view["recommended_action"]["targets"], [])
        self.assertEqual(view["recommended_action"]["disabled_reason"], "调查降级，处置建议不可用")
        self.assertTrue(view["analysis_limits"]["degraded"])

    def test_case_without_hunt_plan_returns_null_jarvis_panel(self):
        case = _base_case()
        case["hunt_plan"] = None
        view = build_case_view(case)
        self.assertIsNone(view["jarvis_plan"])

    def test_jarvis_panel_in_degraded_case_points_to_reinvestigation(self):
        case = _base_case()
        case["investigation_status"] = "DEGRADED"
        case["suggested_action"] = None
        case["audit_trail"] = {"degraded": True, "degraded_reasons": ["tool_timeout"]}
        view = build_case_view(case)
        self.assertEqual(view["jarvis_plan"]["next_suggested"], "补齐缺失遥测后重新运行调查")

    def test_one_liner_generation_rules(self):
        case = _base_case()
        line = generate_one_liner(case)
        self.assertIn("mimikatz.exe", line)

        no_chain_case = _base_case()
        no_chain_case["forensic_result"]["top_chains"] = []
        no_chain_case["forensic_result"]["hosts_analyzed"] = ["A", "B", "C"]
        no_chain_case["confidence_label"] = "LOW"
        no_chain_line = generate_one_liner(no_chain_case)
        self.assertIn("已分析 3 台主机", no_chain_line)
        self.assertIn("置信度低", no_chain_line)

        degraded_case = _base_case()
        degraded_case["verdict_status"] = "DEGRADED"
        degraded_case["forensic_result"]["top_chains"] = []
        degraded_line = generate_one_liner(degraded_case)
        self.assertIn("调查数据不完整", degraded_line)


if __name__ == "__main__":
    unittest.main(verbosity=2)
