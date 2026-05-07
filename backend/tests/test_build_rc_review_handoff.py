import json
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import build_rc_review_handoff as builder  # noqa: E402


PNG_STUB = b"\x89PNG\r\n\x1a\nsecupilot"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class BuildRcReviewHandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "package"
        self.package_zip = self.root / "package.zip"
        self.screenshot_scan = self.root / "screenshot_safety_scan.json"
        self.rc_consistency = self.root / "rc_consistency_check.json"
        self.qwen_validation = self.root / "qwen_validation.json"
        self.qwen_screenshot = self.root / "qwen_preview.png"
        self.qwen_text = self.root / "qwen_preview.text.json"
        self.output_dir = self.root / "handoff"
        self.zip_path = self.root / "handoff.zip"
        self.write_inputs()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_inputs(self, screenshot_status: str = "PASS") -> None:
        self.package_dir.mkdir(parents=True, exist_ok=True)
        for name in (
            "REVIEWER_START_HERE_中文.md",
            "REVIEWER_CHECKLIST_中文.md",
            "FEEDBACK_TEMPLATE_中文.md",
        ):
            (self.package_dir / name).write_text("LOCAL_OFFLINE_TRIAL_RC_010_CN\n", encoding="utf-8")
        package_index = {
            "candidate": "LOCAL_OFFLINE_TRIAL_RC_010_CN",
            "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_009_CN",
            "boundaries": {key: False for key in builder.BOUNDARY_FALSE_KEYS},
        }
        write_json(self.package_dir / "PACKAGE_INDEX_中文.json", package_index)
        write_json(
            self.package_dir / "package_manifest.json",
            {
                "candidate": "LOCAL_OFFLINE_TRIAL_RC_010_CN",
                "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_009_CN",
                "boundaries": {key: False for key in builder.BOUNDARY_FALSE_KEYS},
                "package_files": [],
            },
        )
        self.package_zip.write_bytes(b"zip")
        write_json(
            self.screenshot_scan,
            {"status": screenshot_status, "blocking_finding_count": 0},
        )
        write_json(
            self.rc_consistency,
            {"status": "PASS", "blocking_finding_count": 0},
        )
        write_json(
            self.qwen_validation,
            {"status": "PASS", "network_call": False, "live_qwen_api": False},
        )
        self.qwen_screenshot.write_bytes(PNG_STUB)
        write_json(
            self.qwen_text,
            {
                "provider_mode": "dry_contract_only",
                "visible_text": "SYNTHETIC_ONLY REVIEW_AND_SIGNOFF_REQUIRED",
            },
        )

    def run_builder(self) -> int:
        with redirect_stdout(StringIO()):
            return builder.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--package-zip",
                    str(self.package_zip),
                    "--screenshot-safety-scan",
                    str(self.screenshot_scan),
                    "--rc-consistency-check",
                    str(self.rc_consistency),
                    "--qwen-preview-validation",
                    str(self.qwen_validation),
                    "--qwen-preview-screenshot",
                    str(self.qwen_screenshot),
                    "--qwen-preview-text",
                    str(self.qwen_text),
                    "--output-dir",
                    str(self.output_dir),
                    "--zip-path",
                    str(self.zip_path),
                    "--repo-root",
                    str(self.root),
                ]
            )

    def test_builds_handoff_dir_and_zip(self):
        code = self.run_builder()

        self.assertEqual(builder.PASS, code)
        self.assertTrue((self.output_dir / "REVIEWER_HANDOFF_START_HERE_中文.md").exists())
        self.assertTrue((self.output_dir / "REVIEWER_PROMPT_中文.md").exists())
        self.assertTrue((self.output_dir / "HANDOFF_MANIFEST.json").exists())
        self.assertTrue((self.output_dir / "validation" / "screenshot_safety_scan.json").exists())
        self.assertTrue((self.output_dir / "qwen_preview" / "qwen_preview.png").exists())
        self.assertTrue(self.zip_path.exists())
        with zipfile.ZipFile(self.zip_path) as archive:
            self.assertIn("HANDOFF_MANIFEST.json", archive.namelist())
            self.assertIn("rc_package/package.zip", archive.namelist())

    def test_holds_when_screenshot_scan_not_pass(self):
        self.write_inputs(screenshot_status="HOLD")

        code = self.run_builder()

        self.assertEqual(builder.HOLD, code)
        self.assertFalse(self.zip_path.exists())

    def test_holds_when_boundary_is_true(self):
        package_index = json.loads((self.package_dir / "PACKAGE_INDEX_中文.json").read_text(encoding="utf-8"))
        package_index["boundaries"]["live_qwen_api"] = True
        write_json(self.package_dir / "PACKAGE_INDEX_中文.json", package_index)

        code = self.run_builder()

        self.assertEqual(builder.HOLD, code)


if __name__ == "__main__":
    unittest.main()
