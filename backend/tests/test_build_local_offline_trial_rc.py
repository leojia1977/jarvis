import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import build_local_offline_trial_rc as builder  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class BuildLocalOfflineTrialRcTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.source_package = self.root / "source-rc"
        self.screenshot_dir = self.root / "screens"
        self.output_dir = self.root / "out" / "local-offline-trial-rc-099-cn-review"
        self.zip_path = self.root / "out" / "local-offline-trial-rc-099-cn-review-package.zip"
        self.validation_scan = self.root / "validation" / "screenshot_safety_scan.json"
        self.write_source_package()
        self.write_screenshots()
        self.write_validation_scan()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_source_package(self, finding_count: int = 0) -> None:
        evidence = self.source_package / "evidence"
        write_json(
            evidence / "final_status.json",
            {
                "can_deploy_to_customer_production": False,
                "boundaries_preserved": {
                    "customer_visible_output": False,
                    "production_connectors": False,
                    "qwen_autonomous_action": False,
                    "raw_payload_retention": False,
                    "secret_retention": False,
                    "writeback": False,
                },
            },
        )
        write_json(
            evidence / "safety_scan.json",
            {"summary": {"finding_count": finding_count, "no_go_count": 0}},
        )
        write_json(evidence / "artifact_manifest.json", {"artifacts": []})
        write_json(evidence / "case_summary.json", {"case_count": 20, "cases": []})

    def write_screenshots(self) -> None:
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        png_stub = b"\x89PNG\r\n\x1a\nsecupilot-test"
        for file_name, _, _ in builder.SCREENSHOT_SPECS:
            (self.screenshot_dir / file_name).write_bytes(png_stub)

    def write_validation_scan(self) -> None:
        write_json(
            self.validation_scan,
            {
                "schema_version": "secupilot.s1.review_screenshot_safety_scan.v1",
                "status": "PASS",
                "blocking_finding_count": 0,
            },
        )

    def run_builder(self) -> int:
        with redirect_stdout(StringIO()):
            return builder.run(
                [
                    "--candidate",
                    "LOCAL_OFFLINE_TRIAL_RC_099_CN",
                    "--source-candidate",
                    "LOCAL_OFFLINE_TRIAL_RC_098_CN",
                    "--source-package",
                    str(self.source_package),
                    "--screenshot-dir",
                    str(self.screenshot_dir),
                    "--output-dir",
                    str(self.output_dir),
                    "--zip-path",
                    str(self.zip_path),
                    "--source-commit",
                    "testcommit",
                    "--repo-root",
                    str(self.root),
                ]
        )

    def run_builder_with_validation(self) -> int:
        with redirect_stdout(StringIO()):
            return builder.run(
                [
                    "--candidate",
                    "LOCAL_OFFLINE_TRIAL_RC_099_CN",
                    "--source-candidate",
                    "LOCAL_OFFLINE_TRIAL_RC_098_CN",
                    "--source-package",
                    str(self.source_package),
                    "--screenshot-dir",
                    str(self.screenshot_dir),
                    "--output-dir",
                    str(self.output_dir),
                    "--zip-path",
                    str(self.zip_path),
                    "--source-commit",
                    "testcommit",
                    "--repo-root",
                    str(self.root),
                    "--screenshot-safety-scan",
                    str(self.validation_scan),
                ]
            )

    def test_builds_self_contained_package_and_zip(self):
        code = self.run_builder()

        self.assertEqual(builder.PASS, code)
        self.assertTrue((self.output_dir / "REVIEWER_START_HERE_中文.md").exists())
        self.assertTrue((self.output_dir / "REVIEWER_CHECKLIST_中文.md").exists())
        self.assertTrue((self.output_dir / "FEEDBACK_TEMPLATE_中文.md").exists())
        self.assertTrue((self.output_dir / "PACKAGE_INDEX_中文.json").exists())
        self.assertTrue((self.output_dir / "SCREENSHOT_INDEX.json").exists())
        self.assertTrue((self.output_dir / "package_manifest.json").exists())
        self.assertTrue(self.zip_path.exists())

        manifest = json.loads((self.output_dir / "package_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("LOCAL_OFFLINE_TRIAL_RC_099_CN", manifest["candidate"])
        self.assertEqual("LOCAL_OFFLINE_TRIAL_RC_098_CN", manifest["source_candidate"])
        self.assertEqual(False, manifest["boundaries"]["customer_visible_output"])
        self.assertEqual(13, len(manifest["package_files"]))
        self.assertTrue(all(item["sha256"] for item in manifest["package_files"]))
        self.assertIn("RC-099", (self.output_dir / "REVIEWER_START_HERE_中文.md").read_text(encoding="utf-8"))

    def test_includes_validation_artifact_when_supplied(self):
        code = self.run_builder_with_validation()

        self.assertEqual(builder.PASS, code)
        self.assertTrue((self.output_dir / "validation" / "screenshot_safety_scan.json").exists())
        package_index = json.loads((self.output_dir / "PACKAGE_INDEX_中文.json").read_text(encoding="utf-8"))
        self.assertEqual(["validation/screenshot_safety_scan.json"], package_index["validation_files"])
        manifest = json.loads((self.output_dir / "package_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(14, len(manifest["package_files"]))

    def test_holds_when_safety_scan_has_findings(self):
        self.write_source_package(finding_count=1)

        code = self.run_builder()

        self.assertEqual(builder.HOLD, code)
        self.assertFalse(self.zip_path.exists())


if __name__ == "__main__":
    unittest.main()
