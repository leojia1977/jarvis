import json
import shutil
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import build_private_deployment_package as package_builder  # noqa: E402
from scripts import capture_customer_trial_feedback_sample as feedback_sample  # noqa: E402
from scripts import generate_private_deployment_prereq_sizing_draft as draft_builder  # noqa: E402
from scripts import generate_private_deployment_precheck as precheck_builder  # noqa: E402


class GeneratePrivateDeploymentPrecheckTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "artifacts" / "private" / "secupilot-private"
        self.feedback_path = self.package_dir / "trial_output" / feedback_sample.DEFAULT_OUTPUT_NAME
        self.draft_json = self.package_dir / "trial_output" / draft_builder.DEFAULT_JSON_NAME
        self.precheck_script = self.package_dir / "scripts" / precheck_builder.DEFAULT_SCRIPT_NAME
        self.contract_path = self.package_dir / "trial_output" / precheck_builder.DEFAULT_CONTRACT_NAME
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
            output_dir=self.package_dir / "trial_output",
            repo_root=self.root,
        )

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
        status_path = self.package_dir / "trial_output" / "customer_trial_status.json"
        status_path.parent.mkdir(parents=True, exist_ok=True)
        status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_generates_precheck_script_and_contract(self):
        contract = precheck_builder.build_precheck(
            package_dir=self.package_dir,
            draft_json=self.draft_json,
            output_script=self.precheck_script,
            contract_path=self.contract_path,
            repo_root=self.root,
        )

        self.assertEqual(precheck_builder.SCHEMA_VERSION, contract["schema_version"])
        self.assertTrue(self.precheck_script.exists())
        self.assertTrue(self.contract_path.exists())
        self.assertEqual(4, len(contract["checks"]))
        self.assertEqual("GOAL-MVP-79_PRIVATE_DEPLOYMENT_SIZING_REPORT", contract["next_unlock"])
        script_text = self.precheck_script.read_text(encoding="utf-8")
        self.assertIn("WIN-PREQ-01", script_text)
        self.assertIn("PRIVATE_DEPLOYMENT_PRECHECK_PASS", script_text)
        self.assertNotIn("Authorization:", script_text)
        self.assertNotIn("Bearer ", script_text)

    def test_cli_returns_pass(self):
        with redirect_stdout(StringIO()):
            code = precheck_builder.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--draft-json",
                    str(self.draft_json),
                    "--output-script",
                    str(self.precheck_script),
                    "--contract-path",
                    str(self.contract_path),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(precheck_builder.PASS, code)
        self.assertTrue(self.precheck_script.exists())

    def test_generated_powershell_precheck_runs_and_writes_result(self):
        shell = shutil.which("powershell.exe") or shutil.which("pwsh")
        if shell is None:
            self.skipTest("PowerShell is required for precheck verification")

        precheck_builder.build_precheck(
            package_dir=self.package_dir,
            draft_json=self.draft_json,
            output_script=self.precheck_script,
            contract_path=self.contract_path,
            repo_root=self.root,
        )
        completed = subprocess.run(
            [shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(self.precheck_script)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn("PRIVATE_DEPLOYMENT_PRECHECK_PASS", completed.stdout)
        result_path = self.package_dir / "trial_output" / "private_deployment_precheck_result.json"
        self.assertTrue(result_path.exists())
        result = json.loads(result_path.read_text(encoding="utf-8-sig"))
        self.assertEqual("secupilot.private_deployment_precheck_result.v1", result["schema_version"])
        self.assertEqual("PRIVATE_DEPLOYMENT_PRECHECK_PASS", result["status"])
        self.assertEqual(4, len(result["checks"]))
        self.assertTrue(all(item["passed"] is True for item in result["checks"]))
        self.assertFalse(result["boundaries"]["deploy_executed"])
        self.assertFalse(result["boundaries"]["network_request"])
        self.assertFalse(result["boundaries"]["live_qwen_api"])

    def test_holds_when_draft_status_is_not_ready(self):
        payload = json.loads(self.draft_json.read_text(encoding="utf-8"))
        payload["status"] = "HOLD_FOR_BLOCKER_REVIEW"
        self.draft_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        with redirect_stdout(StringIO()):
            code = precheck_builder.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--draft-json",
                    str(self.draft_json),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(precheck_builder.HOLD, code)

    def test_holds_when_output_is_outside_repo(self):
        outside_script = self.root.parent / "outside-precheck.ps1"

        with redirect_stdout(StringIO()):
            code = precheck_builder.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--draft-json",
                    str(self.draft_json),
                    "--output-script",
                    str(outside_script),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(precheck_builder.HOLD, code)
        self.assertFalse(outside_script.exists())


if __name__ == "__main__":
    unittest.main()
