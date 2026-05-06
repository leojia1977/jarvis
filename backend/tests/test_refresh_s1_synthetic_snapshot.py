import json
import tempfile
import unittest
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import refresh_s1_synthetic_snapshot as refresh  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
INPUT_DIR = REPO_ROOT / "mock_data" / "s0_synthetic" / "qwen_fact_bundle"


class RefreshS1SyntheticSnapshotTests(unittest.TestCase):
    def test_refresh_snapshot_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "snapshot"

            code = refresh.run(
                [
                    "--input",
                    str(INPUT_DIR),
                    "--output",
                    str(output_dir),
                    "--provider",
                    "fixture",
                    "--no-writeback",
                    "--no-customer-visible",
                ]
            )

            self.assertEqual(refresh.PASS, code)
            for name in (
                "run_record.json",
                "safety_scan.json",
                "case_summary.json",
                "final_status.json",
                "artifact_manifest.json",
                "RUN_RECORD.md",
            ):
                self.assertTrue((output_dir / name).exists(), name)

            final_status = json.loads((output_dir / "final_status.json").read_text(encoding="utf-8"))
            self.assertFalse(final_status["boundaries_preserved"]["customer_visible_output"])
            self.assertFalse(final_status["boundaries_preserved"]["writeback"])

    def test_missing_input_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = refresh.run(
                [
                    "--input",
                    str(Path(tmp) / "missing"),
                    "--output",
                    str(Path(tmp) / "snapshot"),
                    "--provider",
                    "fixture",
                    "--no-writeback",
                    "--no-customer-visible",
                ]
            )

            self.assertEqual(refresh.HOLD, code)

    def test_no_writeback_assertion_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = refresh.run(
                [
                    "--input",
                    str(INPUT_DIR),
                    "--output",
                    str(Path(tmp) / "snapshot"),
                    "--provider",
                    "fixture",
                    "--no-customer-visible",
                ]
            )

            self.assertEqual(refresh.HOLD, code)

    def test_no_customer_visible_assertion_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = refresh.run(
                [
                    "--input",
                    str(INPUT_DIR),
                    "--output",
                    str(Path(tmp) / "snapshot"),
                    "--provider",
                    "fixture",
                    "--no-writeback",
                ]
            )

            self.assertEqual(refresh.HOLD, code)


if __name__ == "__main__":
    unittest.main()
