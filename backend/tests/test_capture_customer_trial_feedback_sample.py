import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import build_private_deployment_package as package_builder  # noqa: E402
from scripts import capture_customer_trial_feedback_sample as feedback_sample  # noqa: E402
from scripts import generate_internal_trial_kpi_report as kpi_report  # noqa: E402


class CaptureCustomerTrialFeedbackSampleTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "artifacts" / "private" / "secupilot-private"
        self.feedback_path = self.package_dir / "trial_output" / feedback_sample.DEFAULT_OUTPUT_NAME
        package_builder.build_package(
            package_id="secupilot-private-test",
            output_dir=self.package_dir,
            repo_root=self.root,
        )
        self.write_trial_status()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_trial_status(self, *, boundary_overrides=None):
        manifest = json.loads((self.package_dir / "package_manifest.json").read_text(encoding="utf-8"))
        boundaries = dict(manifest["boundaries"])
        if boundary_overrides:
            boundaries.update(boundary_overrides)
        payload = {
            "schema_version": "secupilot.local_trial_start_result.v1",
            "generated_at_utc": "2026-05-08T00:00:00Z",
            "package_id": manifest["package_id"],
            "package_type": manifest["package_type"],
            "status": "LOCAL_TRIAL_ENTRY_READY",
            "mode": "local_offline_dry_run",
            "entry_document": "CUSTOMER_TRIAL_START_HERE_中文.md",
            "entry_script": "START_SECUPILOT_LOCAL_TRIAL.cmd",
            "boundaries": boundaries,
            "boundary_check": {"status": "PASS", "output": ["BOUNDARY_CHECK_PASS"]},
        }
        status_path = self.package_dir / "trial_output" / "customer_trial_status.json"
        status_path.parent.mkdir(parents=True, exist_ok=True)
        status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_builds_feedback_sample_schema(self):
        payload = feedback_sample.build_feedback_sample(
            package_dir=self.package_dir,
            output_path=self.feedback_path,
            repo_root=self.root,
        )

        self.assertEqual(feedback_sample.SCHEMA_VERSION, payload["schema_version"])
        self.assertEqual("local_offline_feedback_sample", payload["data_mode"])
        self.assertEqual(3, payload["summary"]["feedback_count"])
        self.assertEqual(2, payload["summary"]["missing_information_count"])
        self.assertEqual(0, payload["summary"]["blocker_count"])
        self.assertTrue(self.feedback_path.exists())

    def test_validate_only_passes_for_generated_sample(self):
        feedback_sample.build_feedback_sample(
            package_dir=self.package_dir,
            output_path=self.feedback_path,
            repo_root=self.root,
        )

        with redirect_stdout(StringIO()):
            code = feedback_sample.run(
                [
                    "--validate-only",
                    "--feedback-json",
                    str(self.feedback_path),
                    "--package-dir",
                    str(self.package_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(feedback_sample.PASS, code)

    def test_validate_only_holds_for_invalid_role(self):
        payload = feedback_sample.build_feedback_sample(
            package_dir=self.package_dir,
            output_path=self.feedback_path,
            repo_root=self.root,
        )
        payload["feedback"][0]["reviewer_role"] = "admin"
        self.feedback_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        with redirect_stdout(StringIO()):
            code = feedback_sample.run(
                [
                    "--validate-only",
                    "--feedback-json",
                    str(self.feedback_path),
                    "--package-dir",
                    str(self.package_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(feedback_sample.HOLD, code)

    def test_holds_when_feedback_contains_forbidden_literal(self):
        payload = feedback_sample.build_feedback_sample(
            package_dir=self.package_dir,
            output_path=self.feedback_path,
            repo_root=self.root,
        )
        payload["feedback"][0]["notes"] = "Bearer should never appear"
        self.feedback_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        with redirect_stdout(StringIO()):
            code = feedback_sample.run(
                [
                    "--validate-only",
                    "--feedback-json",
                    str(self.feedback_path),
                    "--package-dir",
                    str(self.package_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(feedback_sample.HOLD, code)

    def test_holds_when_boundary_is_true(self):
        self.write_trial_status(boundary_overrides={"real_data": True})

        with redirect_stdout(StringIO()):
            code = feedback_sample.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--output-path",
                    str(self.feedback_path),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(feedback_sample.HOLD, code)

    def test_kpi_report_consumes_feedback_sample(self):
        feedback_sample.build_feedback_sample(
            package_dir=self.package_dir,
            output_path=self.feedback_path,
            repo_root=self.root,
        )

        report = kpi_report.build_report(
            package_dir=self.package_dir,
            output_dir=self.package_dir / "trial_output",
            repo_root=self.root,
            feedback_json=self.feedback_path,
        )

        self.assertEqual("INTERNAL_TRIAL_FEEDBACK_MEASURED", report["status"])
        self.assertEqual("MEASURED", report["feedback"]["measurement_status"])
        self.assertEqual(3, report["feedback"]["feedback_count"])
        self.assertEqual(100.0, report["feedback"]["understanding_rate_percent"])
        self.assertEqual(66.67, report["feedback"]["usefulness_rate_percent"])
        self.assertEqual(2, report["feedback"]["missing_information_count"])
        self.assertEqual("GOAL-MVP-77_PRIVATE_DEPLOYMENT_PREREQ_AND_SIZING_DRAFT", report["next_unlock"])


if __name__ == "__main__":
    unittest.main()
