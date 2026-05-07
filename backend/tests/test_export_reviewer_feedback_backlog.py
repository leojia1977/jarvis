import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import export_reviewer_feedback_backlog as exporter  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ExportReviewerFeedbackBacklogTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.feedback_json = self.root / "feedback.json"
        self.output_json = self.root / "backlog.json"
        self.output_md = self.root / "backlog.md"
        self.write_feedback()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_feedback(self, **overrides):
        payload = {
            "candidate": "LOCAL_OFFLINE_TRIAL_RC_009_CN",
            "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_008_CN",
            "reviewer": "Jarvis",
            "decision": "PASS_TO_NEXT_INTERNAL_LOCAL_TRIAL",
            "timestamp": "2026-05-07",
            "non_blocking_observations": [
                "RC-008 中文评审包 字样需要下一轮清理。",
            ],
            "next_round_suggestions": [
                "清理 /s1-trial 第 02 步说明文字中的 source candidate 引用。",
                "考虑在 /s1-run 顶部增加更明确的 本轮试用范围 说明。",
            ],
            "boundaries": {
                "real_data": False,
                "masked_real_data": False,
                "live_qwen_api": False,
                "live_connectors": False,
                "production_writeback": False,
                "customer_visible_output": False,
                "push": False,
            },
            "customer_visible_or_deploy_go": False,
        }
        payload.update(overrides)
        write_json(self.feedback_json, payload)

    def run_exporter(self) -> int:
        with redirect_stdout(StringIO()):
            return exporter.run(
                [
                    "--feedback-json",
                    str(self.feedback_json),
                    "--output-json",
                    str(self.output_json),
                    "--output-md",
                    str(self.output_md),
                    "--repo-root",
                    str(self.root),
                ]
            )

    def test_exports_backlog_items_from_feedback(self):
        code = self.run_exporter()

        self.assertEqual(exporter.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("secupilot.reviewer_feedback_product_backlog.v1", payload["schema_version"])
        self.assertEqual(3, len(payload["items"]))
        self.assertEqual("BACKLOG_OPEN", payload["items"][0]["status"])
        self.assertTrue(self.output_md.exists())

    def test_holds_when_boundary_is_true(self):
        self.write_feedback(
            boundaries={
                "real_data": False,
                "masked_real_data": False,
                "live_qwen_api": True,
                "live_connectors": False,
                "production_writeback": False,
                "customer_visible_output": False,
                "push": False,
            }
        )

        code = self.run_exporter()

        self.assertEqual(exporter.HOLD, code)
        self.assertFalse(self.output_json.exists())

    def test_holds_when_feedback_grants_deploy(self):
        self.write_feedback(customer_visible_or_deploy_go=True)

        code = self.run_exporter()

        self.assertEqual(exporter.HOLD, code)


if __name__ == "__main__":
    unittest.main()
