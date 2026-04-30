import copy
import json
import tempfile
import unittest
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import s1_artifact_validate as validator  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = REPO_ROOT / "artifacts" / "s1_closed_shadow_runs" / "2026-04-30-001"


class S1ArtifactValidateTests(unittest.TestCase):
    def _copy_fixture(self, target: Path) -> None:
        target.mkdir(parents=True, exist_ok=True)
        for name in validator.REQUIRED_FILES:
            source = FIXTURE_DIR / name
            target.joinpath(name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    def test_validate_repo_fixture_passes(self):
        code, errors = validator.validate_artifact_dir(FIXTURE_DIR)
        self.assertEqual(validator.PASS, code)
        self.assertEqual([], errors)

    def test_missing_required_file_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifacts"
            self._copy_fixture(artifact_dir)
            (artifact_dir / "safety_scan.json").unlink()

            code, errors = validator.validate_artifact_dir(artifact_dir)

            self.assertEqual(validator.HOLD, code)
            self.assertTrue(any("missing required artifact: safety_scan.json" in err for err in errors))

    def test_unknown_retention_class_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            artifact_dir = Path(tmp) / "artifacts"
            self._copy_fixture(artifact_dir)

            manifest_path = artifact_dir / "artifact_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            broken = copy.deepcopy(manifest)
            broken["artifacts"][0]["retention_class"] = "UNKNOWN_CLASS"
            manifest_path.write_text(json.dumps(broken, ensure_ascii=False, indent=2), encoding="utf-8")

            code, errors = validator.validate_artifact_dir(artifact_dir)

            self.assertEqual(validator.HOLD, code)
            self.assertTrue(any("unknown retention_class" in err for err in errors))


if __name__ == "__main__":
    unittest.main()
