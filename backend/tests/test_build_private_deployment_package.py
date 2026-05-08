import json
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import build_private_deployment_package as builder  # noqa: E402


class BuildPrivateDeploymentPackageTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.output_dir = self.root / "artifacts" / "private" / "secupilot-private"
        self.zip_path = self.root / "artifacts" / "private" / "secupilot-private.zip"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_builds_windows_local_first_structure(self):
        manifest = builder.build_package(
            package_id="secupilot-private-test",
            output_dir=self.output_dir,
            repo_root=self.root,
            zip_path=self.zip_path,
        )

        self.assertEqual(builder.SCHEMA_VERSION, manifest["schema_version"])
        self.assertEqual("STRUCTURE_ONLY_NOT_DEPLOYED", manifest["status"])
        self.assertFalse(manifest["boundaries"]["real_data"])
        self.assertFalse(manifest["boundaries"]["live_qwen_api"])
        self.assertFalse(manifest["boundaries"]["network_request"])
        self.assertFalse(manifest["boundaries"]["production_writeback"])
        self.assertTrue((self.output_dir / "README_PRIVATE_DEPLOYMENT_中文.md").exists())
        self.assertTrue((self.output_dir / "CUSTOMER_TRIAL_START_HERE_中文.md").exists())
        self.assertTrue((self.output_dir / "START_SECUPILOT_LOCAL_TRIAL.cmd").exists())
        self.assertTrue((self.output_dir / "configs" / "secupilot.env.template").exists())
        self.assertTrue((self.output_dir / "configs" / "provider.dry-run.json").exists())
        self.assertTrue((self.output_dir / "scripts" / "START_CUSTOMER_TRIAL.ps1").exists())
        self.assertTrue((self.output_dir / "scripts" / "START_LOCAL_DRY_RUN.ps1").exists())
        self.assertTrue((self.output_dir / "scripts" / "VERIFY_BOUNDARIES.ps1").exists())
        self.assertTrue((self.output_dir / "trial_output" / "README_TRIAL_OUTPUT_中文.md").exists())
        self.assertTrue((self.output_dir / "package_manifest.json").exists())
        self.assertTrue(self.zip_path.exists())

        manifest_from_disk = json.loads((self.output_dir / "package_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("secupilot-private-test", manifest_from_disk["package_id"])
        self.assertEqual("CUSTOMER_TRIAL_START_HERE_中文.md", manifest_from_disk["entry_points"]["start_here"])
        self.assertEqual("START_SECUPILOT_LOCAL_TRIAL.cmd", manifest_from_disk["entry_points"]["one_click_cmd"])
        self.assertEqual("scripts/START_CUSTOMER_TRIAL.ps1", manifest_from_disk["entry_points"]["powershell_script"])
        self.assertEqual("GOAL-MVP-75_INTERNAL_TRIAL_KPI_REPORT", manifest_from_disk["next_unlock"])
        self.assertEqual(self.zip_path.name, manifest_from_disk["zip"]["zip_name"])
        self.assertRegex(manifest_from_disk["zip"]["zip_sha256"], r"^[0-9a-f]{64}$")
        self.assertFalse(Path(manifest_from_disk["package_dir"]).is_absolute())
        self.assertTrue(all(not Path(item["path"]).is_absolute() for item in manifest_from_disk["files"]))
        self.assertTrue(all(item["contains_secret"] is False for item in manifest_from_disk["files"]))
        self.assertTrue(all(item["customer_visible"] is False for item in manifest_from_disk["files"]))

        with zipfile.ZipFile(self.zip_path, "r") as archive:
            names = set(archive.namelist())
        self.assertIn("package_manifest.json", names)
        self.assertIn("CUSTOMER_TRIAL_START_HERE_中文.md", names)
        self.assertIn("START_SECUPILOT_LOCAL_TRIAL.cmd", names)
        self.assertIn("configs/secupilot.env.template", names)
        self.assertIn("scripts/START_CUSTOMER_TRIAL.ps1", names)
        self.assertIn("scripts/VERIFY_BOUNDARIES.ps1", names)

    def test_customer_trial_script_writes_status_file(self):
        shell = shutil.which("powershell.exe") or shutil.which("pwsh")
        if shell is None:
            self.skipTest("PowerShell is required for customer trial script verification")

        builder.build_package(
            package_id="secupilot-private-test",
            output_dir=self.output_dir,
            repo_root=self.root,
            zip_path=self.zip_path,
        )

        script_path = self.output_dir / "scripts" / "START_CUSTOMER_TRIAL.ps1"
        completed = subprocess.run(
            [shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)],
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        self.assertIn("LOCAL_TRIAL_ENTRY_READY", completed.stdout)
        self.assertIn("BOUNDARY_CHECK_PASS", completed.stdout)

        status_path = self.output_dir / "trial_output" / "customer_trial_status.json"
        self.assertTrue(status_path.exists())
        status = json.loads(status_path.read_text(encoding="utf-8-sig"))
        self.assertEqual("secupilot.local_trial_start_result.v1", status["schema_version"])
        self.assertEqual("LOCAL_TRIAL_ENTRY_READY", status["status"])
        self.assertEqual("local_offline_dry_run", status["mode"])
        self.assertEqual("PASS", status["boundary_check"]["status"])
        self.assertFalse(status["boundaries"]["real_data"])
        self.assertFalse(status["boundaries"]["live_qwen_api"])
        self.assertFalse(status["boundaries"]["network_request"])
        self.assertFalse(status["boundaries"]["production_writeback"])

    def test_cli_returns_pass(self):
        with redirect_stdout(StringIO()):
            code = builder.run(
                [
                    "--package-id",
                    "secupilot-private-test",
                    "--output-dir",
                    str(self.output_dir),
                    "--repo-root",
                    str(self.root),
                    "--zip-path",
                    str(self.zip_path),
                ]
            )

        self.assertEqual(builder.PASS, code)
        self.assertTrue((self.output_dir / "package_manifest.json").exists())

    def test_holds_when_output_outside_repo(self):
        outside = self.root.parent / "outside-private-package"

        with redirect_stdout(StringIO()):
            code = builder.run(
                [
                    "--output-dir",
                    str(outside),
                    "--repo-root",
                    str(self.root),
                ]
            )

        self.assertEqual(builder.HOLD, code)
        self.assertFalse(outside.exists())

    def test_generated_text_has_no_forbidden_literals(self):
        manifest = builder.build_package(
            package_id="secupilot-private-test",
            output_dir=self.output_dir,
            repo_root=self.root,
        )

        for item in manifest["files"]:
            path = self.output_dir / item["path"]
            if path.name == "package_manifest.json":
                manifest_payload = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(
                    all(file_item["contains_raw_payload"] is False for file_item in manifest_payload["files"])
                )
                continue
            if path.suffix.lower() in {".md", ".ps1", ".json", ".template"}:
                text = path.read_text(encoding="utf-8").lower()
                self.assertNotIn("authorization:", text)
                self.assertNotIn("bearer ", text)
                self.assertNotIn("refresh_token", text)
                self.assertNotIn("access_token", text)
                self.assertNotIn("api_key=", text)
                self.assertNotIn("raw_payload", text)
                self.assertNotIn("writeback_action", text)


if __name__ == "__main__":
    unittest.main()
