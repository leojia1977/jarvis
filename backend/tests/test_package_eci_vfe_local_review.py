import json
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import package_eci_vfe_local_review as builder  # noqa: E402


def write_json(path: Path, payload: object) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class PackageEciVfeLocalReviewTests(unittest.TestCase):
  def setUp(self):
    self.tmpdir = tempfile.TemporaryDirectory()
    self.root = Path(self.tmpdir.name)
    self.run_dir = self.root / "run"
    self.output_dir = self.root / "pkg" / "eci-vfe-local-offline-rc-001"
    self.zip_output = self.root / "pkg" / "eci-vfe-local-offline-rc-001-review-package.zip"
    self._write_inputs()

  def tearDown(self):
    self.tmpdir.cleanup()

  def _write_inputs(self):
    write_json(
      self.run_dir / "output_guard_scan.json",
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
        },
      },
    )
    write_json(self.run_dir / "chain_assessment.json", {"assessments": []})
    write_json(self.run_dir / "forecast_candidates.json", {"candidates": []})
    write_json(self.run_dir / "correlation_result.json", {"correlations": []})

    screenshots = self.run_dir / "screenshots"
    screenshots.mkdir(parents=True, exist_ok=True)
    png_stub = b"\x89PNG\r\n\x1a\nsecupilot"
    for name, _, _ in builder.SCREENSHOT_SPECS:
      (screenshots / name).write_bytes(png_stub)

  def _run_builder(self) -> int:
    argv = [
      "--run-dir",
      str(self.run_dir),
      "--output-dir",
      str(self.output_dir),
      "--zip-output",
      str(self.zip_output),
      "--repo-root",
      str(self.root),
    ]
    with redirect_stdout(StringIO()):
      return builder.run(argv)

  def test_builds_package_and_zip_with_manifest(self):
    code = self._run_builder()

    self.assertEqual(builder.PASS, code)
    self.assertTrue((self.output_dir / "REVIEWER_START_HERE_中文.md").exists())
    self.assertTrue((self.output_dir / "package_manifest.json").exists())
    self.assertTrue((self.output_dir / "SCREENSHOT_INDEX_中文.json").exists())
    self.assertTrue((self.output_dir / "output_guard_scan.json").exists())
    self.assertTrue((self.output_dir / "chain_assessment.json").exists())
    self.assertTrue((self.output_dir / "forecast_candidates.json").exists())
    self.assertTrue((self.output_dir / "correlation_result.json").exists())
    self.assertTrue(self.zip_output.exists())

    manifest = json.loads((self.output_dir / "package_manifest.json").read_text(encoding="utf-8"))
    self.assertEqual(builder.CANDIDATE, manifest["candidate"])
    self.assertEqual(builder.SOURCE_CANDIDATE, manifest["source_candidate"])
    self.assertGreaterEqual(len(manifest["package_files"]), 7)
    for entry in manifest["package_files"]:
      self.assertRegex(entry["sha256"], r"^[0-9a-f]{64}$")
      self.assertGreater(entry["bytes"], 0)
      self.assertEqual("ECI_VFE_LOCAL_OFFLINE_REVIEW_ARTIFACT", entry["safety_class"])

    screenshot_index = json.loads((self.output_dir / "SCREENSHOT_INDEX_中文.json").read_text(encoding="utf-8"))
    self.assertEqual(4, len(screenshot_index["screenshots"]))
    for screenshot in screenshot_index["screenshots"]:
      self.assertRegex(screenshot["sha256"], r"^[0-9a-f]{64}$")
      self.assertEqual("ECI_VFE_REVIEWER_SAFE_SCREENSHOT", screenshot["safety_class"])

    with zipfile.ZipFile(self.zip_output, "r") as archive:
      names = set(archive.namelist())
    self.assertIn("package_manifest.json", names)
    self.assertIn("SCREENSHOT_INDEX_中文.json", names)
    self.assertIn("screenshots/eci-chain-indicator-desktop.png", names)
    self.assertIn("screenshots/vfe-forecast-card-mobile.png", names)

  def test_holds_when_guard_not_pass(self):
    write_json(
      self.run_dir / "output_guard_scan.json",
      {
        "status": "HOLD",
        "blocking_finding_count": 1,
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
    code = self._run_builder()
    self.assertEqual(builder.HOLD, code)
    self.assertFalse(self.zip_output.exists())


if __name__ == "__main__":
  unittest.main()
