from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "eci_vfe_fixture_analyze.py"
FIXTURE_DIR = ROOT / "mock_data" / "eci_vfe"


def run_analyzer(fixture_dir: Path, output_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--fixture-dir",
            str(fixture_dir),
            "--output",
            str(output_dir),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class EciVfeFixtureAnalyzeTests(unittest.TestCase):
    def test_generates_expected_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "run"
            result = run_analyzer(FIXTURE_DIR, output_dir)

            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "PASS")
            self.assertEqual(payload["assessment_count"], 6)
            self.assertEqual(payload["forecast_count"], 5)
            self.assertEqual(payload["correlation_count"], 6)

            chain = read_json(output_dir / "chain_assessment.json")
            self.assertEqual(chain["assessment_count"], 6)
            lateral = next(item for item in chain["assessments"] if item["case_id"] == "ECI-FIX-003")
            self.assertEqual(lateral["stage_number"]["value"], 5)
            self.assertEqual(lateral["stage_status"]["value"], "HIGH_STAGE_SUSPECTED_SHORT_OBSERVATION")

            for assessment in chain["assessments"]:
                self.assertFalse(assessment["automatic_containment_allowed"])
                for gap in assessment["evidence_gaps"]:
                    self.assertTrue(gap["urgency"])
                    self.assertTrue(gap["window_closes_in"])
                    self.assertTrue(gap["deadline_basis"])
                    self.assertTrue(gap["fallback_if_missed"])

            forecasts = read_json(output_dir / "forecast_candidates.json")
            self.assertEqual(forecasts["forecast_count"], 5)
            for candidate in forecasts["candidates"]:
                context = candidate["query_context"]
                self.assertFalse(context["bulk_export"])
                self.assertTrue(context["audit_required"])

            correlation = read_json(output_dir / "correlation_result.json")
            self.assertEqual(correlation["correlation_count"], 6)
            for record in correlation["correlations"]:
                self.assertFalse(record["case_upgrade_allowed"])
                if not record["hard_match"] and not record["bounded_fuzzy_match"]:
                    self.assertIn(
                        record["correlation_decision"],
                        {"WEAK_MATCH", "NO_MATCH", "HOLD_INSUFFICIENT_EVIDENCE"},
                    )

            run_record = read_json(output_dir / "run_record.json")
            self.assertEqual(run_record["status"], "PASS")
            self.assertFalse(run_record["boundaries"]["live_qwen_api"])
            self.assertFalse(run_record["boundaries"]["production_writeback"])

    def test_hold_when_vfe_query_context_is_bulk(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture_copy = Path(temp_dir) / "fixture_copy"
            shutil.copytree(FIXTURE_DIR, fixture_copy)

            bad_vfe = fixture_copy / "vfe_cases" / "vfe_case_001_config_risk_candidate.json"
            payload = read_json(bad_vfe)
            payload["query_context"]["asset_scope"] = "bulk"
            bad_vfe.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            result = run_analyzer(fixture_copy, Path(temp_dir) / "run_bad")
            self.assertEqual(result.returncode, 20)
            hold = json.loads(result.stdout)
            self.assertEqual(hold["status"], "HOLD")
            self.assertIn("asset_scope bulk is forbidden", hold["error"])

    def test_hold_when_gap_field_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            fixture_copy = Path(temp_dir) / "fixture_copy_gap"
            shutil.copytree(FIXTURE_DIR, fixture_copy)

            bad_eci = fixture_copy / "eci_cases" / "eci_case_001_early_stage_recon.json"
            payload = read_json(bad_eci)
            del payload["expected_evidence_gaps"][0]["urgency"]
            bad_eci.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            result = run_analyzer(fixture_copy, Path(temp_dir) / "run_gap")
            self.assertEqual(result.returncode, 20)
            hold = json.loads(result.stdout)
            self.assertEqual(hold["status"], "HOLD")
            self.assertIn("evidence gap missing urgency", hold["error"])


if __name__ == "__main__":
    unittest.main()
