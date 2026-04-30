import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from _project_bootstrap import bootstrap

bootstrap()

from scripts import s0_qwen_readiness as readiness  # noqa: E402
from scripts import s0_qwen_synthetic_run as runner  # noqa: E402


class S0QwenReadinessTests(unittest.TestCase):
    def test_current_qwen_fact_bundles_are_preflight_ready(self):
        rows, global_findings = readiness._preflight_rows(
            runner.DEFAULT_BUNDLE_DIR,
            max_input_chars=runner.DEFAULT_MAX_INPUT_CHARS,
            max_input_tokens_estimate=runner.DEFAULT_MAX_INPUT_TOKENS_ESTIMATE,
        )
        self.assertEqual([], global_findings)
        self.assertEqual(20, len(rows))
        self.assertEqual(set(readiness.EXPECTED_UAT_IDS), {row.uat_id for row in rows})
        self.assertTrue(all(row.synthetic_valid for row in rows))
        self.assertTrue(all(row.budget_valid for row in rows))
        self.assertLessEqual(max(row.estimated_tokens for row in rows), runner.DEFAULT_MAX_INPUT_TOKENS_ESTIMATE)

    def test_preflight_writes_json_and_markdown_without_qwen_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            args = SimpleNamespace(
                bundle_dir=runner.DEFAULT_BUNDLE_DIR,
                max_input_chars=runner.DEFAULT_MAX_INPUT_CHARS,
                max_input_tokens_estimate=runner.DEFAULT_MAX_INPUT_TOKENS_ESTIMATE,
                output_json=root / "preflight.json",
                output_md=root / "preflight.md",
            )
            exit_code = readiness.run_preflight(args)
            self.assertEqual(0, exit_code)
            payload = json.loads((root / "preflight.json").read_text(encoding="utf-8"))
            self.assertEqual("S0_002_PREFLIGHT_PASS_WAITING_FOR_CLOUD_RECOVERY", payload["decision"])
            self.assertIn("S0-002", (root / "preflight.md").read_text(encoding="utf-8"))

    def test_artifact_validator_detects_complete_synthetic_run_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "outputs").mkdir()
            (run_dir / "scoring").mkdir()
            (run_dir / "metrics").mkdir()
            (run_dir / "notes").mkdir()
            (run_dir / "manifest.json").write_text('{"synthetic_only": true}', encoding="utf-8")
            (run_dir / "scoring" / "s0_scorecard.csv").write_text("uat_id,decision\n", encoding="utf-8")
            (run_dir / "scoring" / "action_command_scan.csv").write_text("uat_id,pass\n", encoding="utf-8")
            (run_dir / "scoring" / "prompt_injection_verdicts.csv").write_text("uat_id,pass\n", encoding="utf-8")
            (run_dir / "metrics" / "latency_summary.json").write_text('{"count": 20}', encoding="utf-8")
            (run_dir / "notes" / "operator_notes.md").write_text("synthetic only", encoding="utf-8")
            (run_dir / "notes" / "reviewer_notes.md").write_text("reviewer pending", encoding="utf-8")
            for uat_id in readiness.EXPECTED_UAT_IDS:
                (run_dir / "outputs" / f"{uat_id}.json").write_text('{"scoring": {"decision": "PASS"}}', encoding="utf-8")

            args = SimpleNamespace(run_dir=run_dir, output_json=run_dir / "artifact.json", output_md=run_dir / "artifact.md")
            exit_code = readiness.run_artifact_validate(args)
            self.assertEqual(0, exit_code)
            payload = json.loads((run_dir / "artifact.json").read_text(encoding="utf-8"))
            self.assertEqual("S0_ARTIFACT_COMPLETENESS_PASS", payload["decision"])

    def test_artifact_validator_holds_on_missing_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            args = SimpleNamespace(run_dir=run_dir, output_json=run_dir / "artifact.json", output_md=run_dir / "artifact.md")
            exit_code = readiness.run_artifact_validate(args)
            self.assertEqual(1, exit_code)
            payload = json.loads((run_dir / "artifact.json").read_text(encoding="utf-8"))
            self.assertEqual("HOLD_ARTIFACT_COMPLETENESS_FAILURE", payload["decision"])


if __name__ == "__main__":
    unittest.main()
