import json
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import build_rc018_customer_review_package as builder  # noqa: E402


def write_json(path: Path, payload: object) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class BuildRc018CustomerReviewPackageTests(unittest.TestCase):
  def setUp(self):
    self.tmpdir = tempfile.TemporaryDirectory()
    self.root = Path(self.tmpdir.name)
    self.output_dir = self.root / "artifacts" / "local_demo_packages" / "local-offline-trial-rc-018-cn-review"
    self.zip_path = self.root / "artifacts" / "local_demo_packages" / "local-offline-trial-rc-018-cn-review-package-20260509.zip"
    self._write_source_inputs()

  def tearDown(self):
    self.tmpdir.cleanup()

  def _write_source_inputs(self):
    eci_root = self.root / "artifacts" / "eci_vfe_fixture_runs" / "rc001"
    write_json(
      eci_root / "output_guard_scan.json",
      {
        "status": "PASS",
        "blocking_finding_count": 0,
        "boundaries": {
          "real_data": False,
          "masked_real_data": False,
          "live_qwen_api": False,
          "live_connectors": False,
          "production_writeback": False,
          "customer_visible_output": False,
          "push": False,
        },
      },
    )
    write_json(eci_root / "chain_assessment.json", {"assessments": [{"stage_status": {"value": "HIGH_STAGE_SUSPECTED"}}]})
    write_json(eci_root / "forecast_candidates.json", {"candidates": [{"candidate_label": {"value": "CONFIGURATION_RISK_REVIEW"}}]})

    screenshot_dir = self.output_dir / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    png_stub = b"\x89PNG\r\n\x1a\nrc018-test"
    for file_name, *_ in builder.SCREENSHOTS:
      (screenshot_dir / file_name).write_bytes(png_stub)

  def _run_builder(self) -> int:
    argv = [
      "--candidate",
      "LOCAL_OFFLINE_TRIAL_RC_018_CN",
      "--source-candidate",
      "LOCAL_OFFLINE_TRIAL_RC_017_CN",
      "--output-dir",
      str(self.output_dir.relative_to(self.root)).replace("\\", "/"),
      "--zip-path",
      str(self.zip_path.relative_to(self.root)).replace("\\", "/"),
      "--repo-root",
      str(self.root),
    ]
    with redirect_stdout(StringIO()):
      return builder.run(argv)

  def test_builds_customer_readable_package_outputs(self):
    code = self._run_builder()
    self.assertEqual(builder.PASS, code)

    self.assertTrue((self.output_dir / "REVIEWER_START_HERE_中文.md").exists())
    self.assertTrue((self.output_dir / "01_REVIEW_PROMPT.md").exists())
    self.assertTrue((self.output_dir / "02_PRODUCT_ROUTE_MAP_中文.md").exists())
    self.assertTrue((self.output_dir / "03_REVIEWER_CHECKLIST_中文.md").exists())
    self.assertTrue((self.output_dir / "04_FEEDBACK_TEMPLATE_中文.md").exists())
    self.assertTrue((self.output_dir / "SCREENSHOT_INDEX_中文.json").exists())
    self.assertTrue((self.output_dir / "safety_scan.json").exists())
    self.assertTrue((self.output_dir / "eci_vfe" / "output_guard_scan.json").exists())
    self.assertTrue((self.output_dir / "eci_vfe" / "chain_assessment_summary.json").exists())
    self.assertTrue((self.output_dir / "eci_vfe" / "forecast_candidate_summary.json").exists())
    self.assertTrue(self.zip_path.exists())
    self.assertTrue((self.zip_path.with_suffix(".zip.outer_zip_manifest.json")).exists())
    self.assertTrue((self.output_dir.parent / "local-offline-trial-rc-018-cn-review-consistency-check.json").exists())
    self.assertTrue((self.output_dir.parent / "local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json").exists())

    screenshot_index = json.loads((self.output_dir / "SCREENSHOT_INDEX_中文.json").read_text(encoding="utf-8"))
    self.assertEqual(7, len(screenshot_index["screenshots"]))
    self.assertEqual(
      "06_eci_vfe_summary_expanded_desktop.png",
      screenshot_index["screenshots"][5]["file_name"],
    )
    self.assertEqual("eci_vfe_summary_expanded", screenshot_index["screenshots"][5]["state"])
    manifest = json.loads((self.output_dir / "package_manifest.json").read_text(encoding="utf-8"))
    self.assertGreaterEqual(len(manifest["package_files"]), 10)

    with zipfile.ZipFile(self.zip_path, "r") as archive:
      names = set(archive.namelist())
    self.assertIn("01_REVIEW_PROMPT.md", names)
    self.assertIn("eci_vfe/output_guard_scan.json", names)
    self.assertIn("screenshots/01_product_home_desktop.png", names)
    self.assertIn("screenshots/06_eci_vfe_summary_expanded_desktop.png", names)

  def test_holds_when_output_guard_not_pass(self):
    write_json(
      self.root / "artifacts" / "eci_vfe_fixture_runs" / "rc001" / "output_guard_scan.json",
      {"status": "HOLD", "blocking_finding_count": 1, "boundaries": builder.BOUNDARIES},
    )
    code = self._run_builder()
    self.assertEqual(builder.HOLD, code)


if __name__ == "__main__":
  unittest.main()
