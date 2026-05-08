import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import build_private_deployment_package as package_builder  # noqa: E402
from scripts import generate_internal_trial_kpi_report as kpi_report  # noqa: E402


class GenerateInternalTrialKpiReportTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "artifacts" / "private" / "secupilot-private"
        self.output_dir = self.package_dir / "trial_output"
        package_builder.build_package(
            package_id="secupilot-private-test",
            output_dir=self.package_dir,
            repo_root=self.root,
        )
        self.manifest = json.loads((self.package_dir / "package_manifest.json").read_text(encoding="utf-8"))
        self.write_trial_status()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_trial_status(self, *, status="LOCAL_TRIAL_ENTRY_READY", boundary_overrides=None):
        boundaries = dict(self.manifest["boundaries"])
        if boundary_overrides:
            boundaries.update(boundary_overrides)
        payload = {
            "schema_version": "secupilot.local_trial_start_result.v1",
            "generated_at_utc": "2026-05-08T00:00:00Z",
            "package_id": self.manifest["package_id"],
            "package_type": self.manifest["package_type"],
            "status": status,
            "mode": "local_offline_dry_run",
            "entry_document": "CUSTOMER_TRIAL_START_HERE_中文.md",
            "entry_script": "START_SECUPILOT_LOCAL_TRIAL.cmd",
            "boundaries": boundaries,
            "boundary_check": {
                "status": "PASS",
                "output": ["BOUNDARY_CHECK_PASS"],
            },
            "generated_files": ["trial_output/customer_trial_status.json"],
        }
        status_path = self.package_dir / "trial_output" / "customer_trial_status.json"
        status_path.parent.mkdir(parents=True, exist_ok=True)
        status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_generates_ready_kpi_report_without_feedback(self):
        report = kpi_report.build_report(
            package_dir=self.package_dir,
            output_dir=self.output_dir,
            repo_root=self.root,
        )

        self.assertEqual(kpi_report.SCHEMA_VERSION, report["schema_version"])
        self.assertEqual("READY_FOR_INTERNAL_TRIAL_FEEDBACK_COLLECTION", report["status"])
        self.assertEqual(100, report["metrics"]["trial_completion_rate_percent"])
        self.assertEqual("PASS", report["metrics"]["boundary_check_status"])
        self.assertEqual(12, report["metrics"]["boundary_false_count"])
        self.assertEqual([], report["blockers"])
        self.assertEqual(0, report["feedback"]["feedback_count"])
        self.assertIsNone(report["feedback"]["understanding_rate_percent"])
        self.assertEqual("PENDING_FEEDBACK", report["feedback"]["measurement_status"])
        self.assertTrue((self.output_dir / kpi_report.DEFAULT_JSON_NAME).exists())
        self.assertTrue((self.output_dir / kpi_report.DEFAULT_MD_NAME).exists())

    def test_feedback_json_computes_understanding_and_usefulness_rates(self):
        feedback_path = self.output_dir / "sample_feedback.json"
        feedback_path.write_text(
            json.dumps(
                {
                    "responses": [
                        {"understood": True, "useful": "yes"},
                        {"understood": False, "useful": False, "missing_information": "need install prereqs"},
                    ]
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        report = kpi_report.build_report(
            package_dir=self.package_dir,
            output_dir=self.output_dir,
            repo_root=self.root,
            feedback_json=feedback_path,
        )

        self.assertEqual(2, report["feedback"]["feedback_count"])
        self.assertEqual(50.0, report["feedback"]["understanding_rate_percent"])
        self.assertEqual(50.0, report["feedback"]["usefulness_rate_percent"])
        self.assertEqual(1, report["feedback"]["missing_information_count"])
        self.assertEqual("MEASURED", report["feedback"]["measurement_status"])

    def test_cli_returns_pass_for_ready_trial_status(self):
        with redirect_stdout(StringIO()):
            code = kpi_report.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(kpi_report.PASS, code)
        self.assertTrue((self.output_dir / kpi_report.DEFAULT_JSON_NAME).exists())

    def test_cli_returns_hold_when_boundary_is_true(self):
        self.write_trial_status(boundary_overrides={"real_data": True})

        with redirect_stdout(StringIO()):
            code = kpi_report.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(kpi_report.HOLD, code)
        report = json.loads((self.output_dir / kpi_report.DEFAULT_JSON_NAME).read_text(encoding="utf-8"))
        self.assertEqual("HOLD", report["status"])
        self.assertIn("real_data is not false", {item["reason"] for item in report["blockers"]})

    def test_holds_when_package_id_mismatch(self):
        status_path = self.package_dir / "trial_output" / "customer_trial_status.json"
        payload = json.loads(status_path.read_text(encoding="utf-8"))
        payload["package_id"] = "different-package"
        status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        with redirect_stdout(StringIO()):
            code = kpi_report.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(kpi_report.HOLD, code)


if __name__ == "__main__":
    unittest.main()
