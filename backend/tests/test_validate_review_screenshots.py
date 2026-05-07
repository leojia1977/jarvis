import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import validate_review_screenshots as validator  # noqa: E402


PNG_STUB = b"\x89PNG\r\n\x1a\nsecupilot"


class ValidateReviewScreenshotsTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.screenshot_dir = self.root / "screenshots"
        self.output_json = self.root / "scan.json"
        self.screenshot_dir.mkdir(parents=True)
        self.write_fixture()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_fixture(self, extra_text: str = ""):
        for file_name, route, viewport in validator.EXPECTED_SCREENSHOTS:
            (self.screenshot_dir / file_name).write_bytes(PNG_STUB)
            (self.screenshot_dir / file_name.replace(".png", ".text.json")).write_text(
                json.dumps(
                    {
                        "schema_version": "secupilot.s1.screenshot_text_evidence.v1",
                        "file_name": file_name,
                        "route": route,
                        "viewport": viewport,
                        "visible_text": f"LOCAL_OFFLINE_TRIAL_RC_009_CN 本地离线试用结果 {extra_text}",
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

    def run_validator(self) -> int:
        with redirect_stdout(StringIO()):
            return validator.run(
                [
                    "--screenshot-dir",
                    str(self.screenshot_dir),
                    "--expected-candidate",
                    "LOCAL_OFFLINE_TRIAL_RC_009_CN",
                    "--output-json",
                    str(self.output_json),
                ]
            )

    def test_clean_screenshot_text_passes(self):
        code = self.run_validator()

        self.assertEqual(validator.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("PASS", payload["status"])
        self.assertEqual(0, payload["blocking_finding_count"])

    def test_holds_on_debug_role_text(self):
        self.write_fixture(extra_text="P1 P2 P3 Mock Fixture Expert Mode")

        code = self.run_validator()

        self.assertEqual(validator.HOLD, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        labels = {
            finding["label"]
            for result in payload["results"]
            for finding in result["blocking_findings"]
        }
        self.assertIn("role_switch_p1_p2_p3", labels)
        self.assertIn("mock_fixture_phase", labels)
        self.assertIn("expert_mode", labels)

    def test_holds_on_stale_rc_path(self):
        self.write_fixture(extra_text="local-offline-trial-rc-006")

        code = self.run_validator()

        self.assertEqual(validator.HOLD, code)

    def test_source_candidate_phrase_is_pass_with_notes(self):
        self.write_fixture(extra_text="RC-008 中文评审包")

        code = self.run_validator()

        self.assertEqual(validator.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("PASS_WITH_NOTES", payload["status"])
        self.assertEqual(0, payload["blocking_finding_count"])
        self.assertGreater(payload["warning_count"], 0)


if __name__ == "__main__":
    unittest.main()
