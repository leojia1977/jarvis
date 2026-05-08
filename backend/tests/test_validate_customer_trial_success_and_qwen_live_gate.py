import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import validate_customer_trial_success_and_qwen_live_gate as gate  # noqa: E402


class ValidateCustomerTrialSuccessAndQwenLiveGateTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "artifacts" / "private" / "secupilot-private"
        self.output_dir = self.root / "artifacts" / "product_readiness" / "gate"
        self.qwen_spec = self.root / "docs" / "qwen_spec.md"
        (self.package_dir / "trial_output").mkdir(parents=True)
        self.qwen_spec.parent.mkdir(parents=True)
        self.write_inputs()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_json(self, relative: str, payload):
        path = self.package_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def write_inputs(self):
        self.write_json(
            "trial_output/customer_trial_status.json",
            {
                "status": "LOCAL_TRIAL_ENTRY_READY",
                "boundaries": {
                    "real_data": False,
                    "masked_real_data": False,
                    "live_qwen_api": False,
                    "live_connectors": False,
                    "network_request": False,
                    "production_writeback": False,
                    "customer_visible_output": False,
                    "deploy_executed": False,
                },
            },
        )
        self.write_json(
            "trial_output/customer_trial_feedback.sample.json",
            {
                "feedback": [
                    {"reviewer_role": "security_engineer"},
                    {"reviewer_role": "security_manager"},
                    {"reviewer_role": "cto"},
                ]
            },
        )
        self.write_json(
            "trial_output/internal_trial_kpi_report.json",
            {
                "feedback": {
                    "understanding_rate_percent": 100.0,
                    "usefulness_rate_percent": 66.67,
                },
                "blockers": [],
            },
        )
        self.write_json(
            "trial_output/private_deployment_precheck_result.json",
            {
                "status": "PRIVATE_DEPLOYMENT_PRECHECK_PASS",
                "boundaries": {
                    "deploy_executed": False,
                    "network_request": False,
                    "live_qwen_api": False,
                    "live_connectors": False,
                    "production_writeback": False,
                    "customer_visible_output": False,
                    "real_data": False,
                    "masked_real_data": False,
                },
            },
        )
        self.write_json(
            "trial_output/private_deployment_sizing_report.json",
            {
                "status": "SIZING_DRAFT_READY_NOT_BENCHMARKED",
                "sizing_profiles": [
                    {"production_claim": False, "customer_pilot_claim": False},
                    {"production_claim": False, "customer_pilot_claim": False},
                ],
            },
        )
        self.qwen_spec.write_text(
            "\n".join(
                [
                    "synthetic only and no real data",
                    "requires explicit GO before live qwen",
                    "does not authorize live Qwen calls now",
                    "forbidden fields raw_payload auth_header writeback_action",
                    "timeout and retry guard required",
                ]
            ),
            encoding="utf-8",
        )

    def test_generates_gate_report(self):
        report = gate.build_report(
            package_dir=self.package_dir,
            qwen_spec_path=self.qwen_spec,
            output_dir=self.output_dir,
            repo_root=self.root,
        )

        self.assertEqual(gate.SCHEMA_VERSION, report["schema_version"])
        self.assertEqual("READY_FOR_LOCAL_PRIVATE_TRIAL_AND_HOLD_FOR_QWEN_LIVE", report["overall_status"])
        self.assertEqual("PASS_FOR_LOCAL_PRIVATE_TRIAL", report["customer_trial_success"]["status"])
        self.assertEqual("HOLD_PENDING_EXPLICIT_QWEN_LIVE_SYNTHETIC_ONLY_GO", report["qwen_live_gate"]["status"])
        self.assertFalse(report["qwen_live_gate"]["customer_data_allowed"])
        self.assertTrue((self.output_dir / gate.DEFAULT_JSON_NAME).exists())
        self.assertTrue((self.output_dir / gate.DEFAULT_MD_NAME).exists())

    def test_cli_returns_pass_for_local_success_and_qwen_hold(self):
        with redirect_stdout(StringIO()):
            code = gate.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--qwen-spec",
                    str(self.qwen_spec),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(gate.PASS, code)

    def test_holds_when_understanding_rate_below_threshold(self):
        path = self.package_dir / "trial_output" / "internal_trial_kpi_report.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["feedback"]["understanding_rate_percent"] = 50
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        with redirect_stdout(StringIO()):
            code = gate.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--qwen-spec",
                    str(self.qwen_spec),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(gate.HOLD, code)

    def test_holds_when_precheck_boundary_true(self):
        path = self.package_dir / "trial_output" / "private_deployment_precheck_result.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["boundaries"]["network_request"] = True
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        with redirect_stdout(StringIO()):
            code = gate.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--qwen-spec",
                    str(self.qwen_spec),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(gate.HOLD, code)

    def test_holds_when_forbidden_literal_appears(self):
        path = self.package_dir / "trial_output" / "internal_trial_kpi_report.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["note"] = "Bearer should never appear"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        with redirect_stdout(StringIO()):
            code = gate.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--qwen-spec",
                    str(self.qwen_spec),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(gate.HOLD, code)

    def test_holds_when_qwen_spec_missing(self):
        self.qwen_spec.unlink()

        with redirect_stdout(StringIO()):
            code = gate.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--qwen-spec",
                    str(self.qwen_spec),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(gate.HOLD, code)


if __name__ == "__main__":
    unittest.main()
