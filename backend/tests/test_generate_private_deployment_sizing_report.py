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
from scripts import generate_private_deployment_precheck as precheck_builder  # noqa: E402
from scripts import generate_private_deployment_prereq_sizing_draft as draft_builder  # noqa: E402
from scripts import generate_private_deployment_sizing_report as sizing_report  # noqa: E402


class GeneratePrivateDeploymentSizingReportTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "artifacts" / "private" / "secupilot-private"
        self.output_dir = self.package_dir / "trial_output"
        self.feedback_path = self.output_dir / feedback_sample.DEFAULT_OUTPUT_NAME
        self.draft_json = self.output_dir / draft_builder.DEFAULT_JSON_NAME
        self.precheck_json = self.output_dir / "private_deployment_precheck_result.json"
        package_builder.build_package(
            package_id="secupilot-private-test",
            output_dir=self.package_dir,
            repo_root=self.root,
        )
        self.write_trial_status()
        feedback_sample.build_feedback_sample(
            package_dir=self.package_dir,
            output_path=self.feedback_path,
            repo_root=self.root,
        )
        draft_builder.build_draft(
            package_dir=self.package_dir,
            feedback_json=self.feedback_path,
            output_dir=self.output_dir,
            repo_root=self.root,
        )
        self.write_precheck_result()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_trial_status(self):
        manifest = json.loads((self.package_dir / "package_manifest.json").read_text(encoding="utf-8"))
        payload = {
            "schema_version": "secupilot.local_trial_start_result.v1",
            "generated_at_utc": "2026-05-08T00:00:00Z",
            "package_id": manifest["package_id"],
            "package_type": manifest["package_type"],
            "status": "LOCAL_TRIAL_ENTRY_READY",
            "mode": "local_offline_dry_run",
            "entry_document": "CUSTOMER_TRIAL_START_HERE_中文.md",
            "entry_script": "START_SECUPILOT_LOCAL_TRIAL.cmd",
            "boundaries": manifest["boundaries"],
            "boundary_check": {"status": "PASS", "output": ["BOUNDARY_CHECK_PASS"]},
        }
        status_path = self.output_dir / "customer_trial_status.json"
        status_path.parent.mkdir(parents=True, exist_ok=True)
        status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def write_precheck_result(self, *, status="PRIVATE_DEPLOYMENT_PRECHECK_PASS", boundary_overrides=None, failed=False):
        boundaries = {
            "deploy_executed": False,
            "network_request": False,
            "live_qwen_api": False,
            "live_connectors": False,
            "production_writeback": False,
            "customer_visible_output": False,
            "real_data": False,
            "masked_real_data": False,
        }
        if boundary_overrides:
            boundaries.update(boundary_overrides)
        payload = {
            "schema_version": "secupilot.private_deployment_precheck_result.v1",
            "generated_at_utc": "2026-05-08T00:00:00Z",
            "package_root": "secupilot-private-test",
            "status": status,
            "checks": [
                {"id": "WIN-PREQ-01", "name": "Windows 本地执行环境", "passed": not failed, "observed": "platform=Win32NT"},
                {"id": "WIN-PREQ-02", "name": "PowerShell 执行能力", "passed": True, "observed": "powershell_version=5.1"},
                {"id": "WIN-PREQ-03", "name": "Python 启动器", "passed": True, "observed": "Python 3.14.2"},
                {"id": "WIN-PREQ-04", "name": "本地文件权限", "passed": True, "observed": "trial_output writable"},
            ],
            "boundaries": boundaries,
        }
        self.precheck_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_generates_sizing_report_from_draft_and_precheck(self):
        report = sizing_report.build_report(
            package_dir=self.package_dir,
            draft_json=self.draft_json,
            precheck_json=self.precheck_json,
            output_dir=self.output_dir,
            repo_root=self.root,
        )

        self.assertEqual(sizing_report.SCHEMA_VERSION, report["schema_version"])
        self.assertEqual("SIZING_DRAFT_READY_NOT_BENCHMARKED", report["status"])
        self.assertEqual("GOAL-MVP-80_MODEL_PROVIDER_SETUP_FLOW_DRY_RUN", report["next_unlock"])
        self.assertEqual("PRIVATE_DEPLOYMENT_PRECHECK_PASS", report["observed_precheck"]["status"])
        self.assertEqual(4, report["observed_precheck"]["passed_count"])
        self.assertEqual(3, len(report["sizing_profiles"]))
        self.assertTrue(all(item["measurement_status"] == "NOT_BENCHMARKED_DRAFT_ONLY" for item in report["sizing_profiles"]))
        self.assertTrue(all(item["production_claim"] is False for item in report["sizing_profiles"]))
        self.assertIn("No production benchmark", report["non_authorization"])
        self.assertTrue((self.output_dir / sizing_report.DEFAULT_JSON_NAME).exists())
        self.assertTrue((self.output_dir / sizing_report.DEFAULT_MD_NAME).exists())

    def test_cli_returns_pass(self):
        with redirect_stdout(StringIO()):
            code = sizing_report.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--draft-json",
                    str(self.draft_json),
                    "--precheck-json",
                    str(self.precheck_json),
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(sizing_report.PASS, code)

    def test_holds_when_precheck_did_not_pass(self):
        self.write_precheck_result(status="PRIVATE_DEPLOYMENT_PRECHECK_HOLD")

        with redirect_stdout(StringIO()):
            code = sizing_report.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--draft-json",
                    str(self.draft_json),
                    "--precheck-json",
                    str(self.precheck_json),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(sizing_report.HOLD, code)

    def test_holds_when_precheck_has_failed_check(self):
        self.write_precheck_result(failed=True)

        with redirect_stdout(StringIO()):
            code = sizing_report.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--draft-json",
                    str(self.draft_json),
                    "--precheck-json",
                    str(self.precheck_json),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(sizing_report.HOLD, code)

    def test_holds_when_boundary_is_true(self):
        self.write_precheck_result(boundary_overrides={"network_request": True})

        with redirect_stdout(StringIO()):
            code = sizing_report.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--draft-json",
                    str(self.draft_json),
                    "--precheck-json",
                    str(self.precheck_json),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(sizing_report.HOLD, code)

    def test_holds_when_draft_claims_benchmark(self):
        draft = json.loads(self.draft_json.read_text(encoding="utf-8"))
        draft["resource_sizing"]["status"] = "BENCHMARKED"
        self.draft_json.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        with redirect_stdout(StringIO()):
            code = sizing_report.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--draft-json",
                    str(self.draft_json),
                    "--precheck-json",
                    str(self.precheck_json),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(sizing_report.HOLD, code)

    def test_holds_when_output_is_outside_repo(self):
        outside = self.root.parent / "outside-sizing-report"

        with redirect_stdout(StringIO()):
            code = sizing_report.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--draft-json",
                    str(self.draft_json),
                    "--precheck-json",
                    str(self.precheck_json),
                    "--output-dir",
                    str(outside),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(sizing_report.HOLD, code)
        self.assertFalse(outside.exists())

    def test_holds_when_report_text_contains_forbidden_literal(self):
        draft = json.loads(self.draft_json.read_text(encoding="utf-8"))
        draft["resource_sizing"]["profiles"][0]["notes"] = "Bearer should never appear"
        self.draft_json.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        with redirect_stdout(StringIO()):
            code = sizing_report.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--draft-json",
                    str(self.draft_json),
                    "--precheck-json",
                    str(self.precheck_json),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(sizing_report.HOLD, code)


if __name__ == "__main__":
    unittest.main()
