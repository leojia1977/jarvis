import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import build_client_trial_readiness_report as readiness  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class BuildClientTrialReadinessReportTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "artifacts" / "local_demo_packages" / "local-offline-trial-rc-099-cn-review"
        self.feedback_json = self.package_dir / "reviewer_feedback.json"
        self.output_report = self.root / "docs" / "readiness.md"
        self.write_package()
        self.write_feedback()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_package(self, finding_count: int = 0) -> None:
        write_json(
            self.package_dir / "package_manifest.json",
            {
                "candidate": "LOCAL_OFFLINE_TRIAL_RC_099_CN",
                "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_098_CN",
                "boundaries": {
                    "real_data": False,
                    "masked_real_data": False,
                    "live_qwen_api": False,
                    "live_connectors": False,
                    "production_writeback": False,
                    "customer_visible_output": False,
                },
            },
        )
        write_json(
            self.package_dir / "evidence" / "final_status.json",
            {
                "final_outcome": "S1_CLOSED_SHADOW_PASS_WITH_NOTES",
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
            self.package_dir / "evidence" / "safety_scan.json",
            {"summary": {"finding_count": finding_count, "no_go_count": 0}},
        )
        screenshots = []
        for name in ("a.png", "b.png", "c.png", "d.png"):
            path = self.package_dir / "screenshots" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"png")
            screenshots.append({"path": f"screenshots/{name}"})
        write_json(self.package_dir / "SCREENSHOT_INDEX.json", {"screenshots": screenshots})

    def write_feedback(self, decision: str = "PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL") -> None:
        write_json(
            self.feedback_json,
            {
                "candidate": "LOCAL_OFFLINE_TRIAL_RC_099_CN",
                "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_098_CN",
                "decision": decision,
                "next_round_suggestions": ["Clean source candidate wording."],
                "non_blocking_observations": ["Source candidate wording is non-blocking."],
            },
        )

    def run_report(self) -> int:
        with redirect_stdout(StringIO()):
            return readiness.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--feedback-json",
                    str(self.feedback_json),
                    "--output-report",
                    str(self.output_report),
                    "--repo-root",
                    str(self.root),
                ]
            )

    def test_builds_internal_local_trial_readiness_report(self):
        code = self.run_report()

        self.assertEqual(readiness.PASS, code)
        text = self.output_report.read_text(encoding="utf-8")
        self.assertIn("READY_FOR_INTERNAL_LOCAL_TRIAL_ONLY", text)
        self.assertIn("customer_trial_ready = false", text)
        self.assertIn("customer-visible publish/deploy/output", text)

    def test_holds_on_failed_feedback_decision(self):
        self.write_feedback(decision="HOLD_FOR_UI_OR_PACKAGE_FIXES")

        code = self.run_report()

        self.assertEqual(readiness.HOLD, code)
        self.assertIn("HOLD", self.output_report.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
