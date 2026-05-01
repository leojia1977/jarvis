import json
import tempfile
import unittest
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import package_s1_local_demo as packager  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = REPO_ROOT / "artifacts" / "s1_closed_shadow_runs" / "2026-04-30-001"


class PackageS1LocalDemoTests(unittest.TestCase):
    def _copy_fixture(self, target: Path) -> None:
        target.mkdir(parents=True, exist_ok=True)
        for name in packager.REQUIRED_ARTIFACT_FILES:
            source = FIXTURE_DIR / name
            target.joinpath(name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    def test_package_repo_fixture_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "package"
            code, errors = packager.package_artifacts(FIXTURE_DIR, output_dir)

            self.assertEqual(packager.PASS, code)
            self.assertEqual([], errors)
            for name in packager.REQUIRED_ARTIFACT_FILES:
                self.assertTrue((output_dir / name).exists(), name)
            manifest_path = output_dir / "package_manifest.json"
            self.assertTrue(manifest_path.exists())
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(
                "secupilot.s1.local_demo_package_manifest.v1",
                manifest["schema_version"],
            )
            self.assertEqual(len(packager.REQUIRED_ARTIFACT_FILES), len(manifest["package_artifacts"]))

    def test_missing_required_artifact_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifact"
            output_dir = Path(tmp) / "package"
            self._copy_fixture(artifact_dir)
            (artifact_dir / "run_record.json").unlink()

            code, errors = packager.package_artifacts(artifact_dir, output_dir)

            self.assertEqual(packager.HOLD, code)
            self.assertTrue(any("missing required artifact: run_record.json" in err for err in errors))

    def test_forbidden_field_key_in_source_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifact"
            output_dir = Path(tmp) / "package"
            self._copy_fixture(artifact_dir)

            case_summary_path = artifact_dir / "case_summary.json"
            case_summary = json.loads(case_summary_path.read_text(encoding="utf-8"))
            case_summary["token"] = "do-not-keep"
            case_summary_path.write_text(
                json.dumps(case_summary, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            code, errors = packager.package_artifacts(artifact_dir, output_dir)

            self.assertEqual(packager.HOLD, code)
            self.assertTrue(any("forbidden field key" in err for err in errors))


if __name__ == "__main__":
    unittest.main()
