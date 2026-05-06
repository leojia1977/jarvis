import json
import tempfile
import unittest
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import package_s1_local_demo as packager  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = REPO_ROOT / "artifacts" / "s1_closed_shadow_runs" / "2026-04-30-001"


class PackageS1LocalDemoTests(unittest.TestCase):
    def _copy_fixture(self, target: Path) -> None:
        target.mkdir(parents=True, exist_ok=True)
        for name in packager.REQUIRED_ARTIFACT_FILES:
            source = FIXTURE_DIR / name
            target.joinpath(name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    def test_package_repo_fixture_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "package"
            code, errors = packager.package_artifacts(FIXTURE_DIR, output_dir)

            self.assertEqual(packager.PASS, code)
            self.assertEqual([], errors)
            for name in packager.REQUIRED_ARTIFACT_FILES:
                self.assertTrue((output_dir / name).exists(), name)
            manifest_path = output_dir / "package_manifest.json"
            self.assertTrue(manifest_path.exists())
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(
                "secupilot.s1.local_demo_package_manifest.v1",
                manifest["schema_version"],
            )
            self.assertEqual(len(packager.REQUIRED_ARTIFACT_FILES), len(manifest["package_artifacts"]))

    def test_missing_required_artifact_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifact"
            output_dir = Path(tmp) / "package"
            self._copy_fixture(artifact_dir)
            (artifact_dir / "run_record.json").unlink()

            code, errors = packager.package_artifacts(artifact_dir, output_dir)

            self.assertEqual(packager.HOLD, code)
            self.assertTrue(any("missing required artifact: run_record.json" in err for err in errors))

    def test_forbidden_field_key_in_source_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifact"
            output_dir = Path(tmp) / "package"
            self._copy_fixture(artifact_dir)

            case_summary_path = artifact_dir / "case_summary.json"
            case_summary = json.loads(case_summary_path.read_text(encoding="utf-8"))
            case_summary["token"] = "do-not-keep"
            case_summary_path.write_text(
                json.dumps(case_summary, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            code, errors = packager.package_artifacts(artifact_dir, output_dir)

            self.assertEqual(packager.HOLD, code)
            self.assertTrue(any("forbidden field key" in err for err in errors))

    def test_manifest_raw_payload_flag_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifact"
            output_dir = Path(tmp) / "package"
            self._copy_fixture(artifact_dir)

            manifest_path = artifact_dir / "artifact_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["artifacts"][0]["contains_raw_payload"] = True
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            code, errors = packager.package_artifacts(artifact_dir, output_dir)

            self.assertEqual(packager.HOLD, code)
            self.assertTrue(any("contains_raw_payload=true" in err for err in errors))

    def test_forbidden_markdown_pattern_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifact"
            output_dir = Path(tmp) / "package"
            self._copy_fixture(artifact_dir)
            (artifact_dir / "RUN_RECORD.md").write_text(
                "operator note\nAuthorization: Bearer not-for-demo-token\n",
                encoding="utf-8",
            )

            code, errors = packager.package_artifacts(artifact_dir, output_dir)

            self.assertEqual(packager.HOLD, code)
            self.assertTrue(any("RUN_RECORD.md: forbidden text pattern" in err for err in errors))

    def test_invalid_json_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifact"
            output_dir = Path(tmp) / "package"
            self._copy_fixture(artifact_dir)
            (artifact_dir / "run_record.json").write_text("{", encoding="utf-8")

            code, errors = packager.package_artifacts(artifact_dir, output_dir)

            self.assertEqual(packager.HOLD, code)
            self.assertTrue(any("run_record.json: invalid JSON" in err for err in errors))

    def test_manifest_paths_are_portable(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "package"
            code, errors = packager.package_artifacts(FIXTURE_DIR, output_dir)

            self.assertEqual(packager.PASS, code)
            self.assertEqual([], errors)
            manifest = json.loads((output_dir / "package_manifest.json").read_text(encoding="utf-8"))
            self.assertFalse(Path(manifest["source_artifact_dir"]).is_absolute())
            self.assertFalse(Path(manifest["package_dir"]).is_absolute())
            for item in manifest["package_artifacts"]:
                self.assertFalse(Path(item["path"]).is_absolute())

    def test_run_cli_returns_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "package"

            code = packager.run(
                [
                    "--artifact-dir",
                    str(FIXTURE_DIR),
                    "--output-dir",
                    str(output_dir),
                ]
            )

            self.assertEqual(packager.PASS, code)
            self.assertTrue((output_dir / "package_manifest.json").exists())

    def test_include_reviewer_readme_adds_manifest_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "package"

            code, errors = packager.package_artifacts(
                FIXTURE_DIR,
                output_dir,
                include_reviewer_readme=True,
            )

            self.assertEqual(packager.PASS, code)
            self.assertEqual([], errors)
            readme_path = output_dir / packager.REVIEWER_README_FILE
            self.assertTrue(readme_path.exists())
            readme = readme_path.read_text(encoding="utf-8")
            self.assertIn("local/offline reviewer inspection only", readme)
            self.assertIn("live Qwen/API calls", readme)
            self.assertIn("local browser review decision preview", readme)
            self.assertIn("does not write artifacts or call external systems", readme)
            manifest = json.loads((output_dir / "package_manifest.json").read_text(encoding="utf-8"))
            readme_entries = [
                item
                for item in manifest["package_artifacts"]
                if item["file_name"] == packager.REVIEWER_README_FILE
            ]
            self.assertEqual(1, len(readme_entries))
            self.assertEqual(packager.DEFAULT_RETENTION_CLASS, readme_entries[0]["retention_class"])
            self.assertFalse(readme_entries[0]["contains_raw_payload"])

    def test_run_cli_can_include_reviewer_readme(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "package"

            code = packager.run(
                [
                    "--artifact-dir",
                    str(FIXTURE_DIR),
                    "--output-dir",
                    str(output_dir),
                    "--include-reviewer-readme",
                ]
            )

            self.assertEqual(packager.PASS, code)
            self.assertTrue((output_dir / packager.REVIEWER_README_FILE).exists())

    def test_include_screenshots_adds_manifest_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "package"

            code, errors = packager.package_artifacts(
                FIXTURE_DIR,
                output_dir,
                include_reviewer_readme=True,
                include_screenshots=True,
            )

            self.assertEqual(packager.PASS, code)
            self.assertEqual([], errors)
            self.assertTrue((output_dir / "playwright" / "s1-run-desktop.png").exists())
            self.assertTrue((output_dir / "playwright" / "s1-run-mobile.png").exists())
            manifest = json.loads((output_dir / "package_manifest.json").read_text(encoding="utf-8"))
            screenshot_paths = {
                item["path"]
                for item in manifest["package_artifacts"]
                if item["path"].startswith("playwright/")
            }
            self.assertEqual(
                {"playwright/s1-run-desktop.png", "playwright/s1-run-mobile.png"},
                screenshot_paths,
            )
            readme = (output_dir / packager.REVIEWER_README_FILE).read_text(encoding="utf-8")
            self.assertIn("Visual screenshots are packaged under `playwright/`", readme)

    def test_include_screenshots_holds_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifact"
            output_dir = Path(tmp) / "package"
            self._copy_fixture(artifact_dir)

            code, errors = packager.package_artifacts(
                artifact_dir,
                output_dir,
                include_screenshots=True,
            )

            self.assertEqual(packager.HOLD, code)
            self.assertTrue(any("no screenshots found under playwright/" in err for err in errors))


if __name__ == "__main__":
    unittest.main()
