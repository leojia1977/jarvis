import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import validate_local_trial_rc_consistency as validator  # noqa: E402


PNG_STUB = b"\x89PNG\r\n\x1a\nsecupilot"


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ValidateLocalTrialRcConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "artifacts" / "local_demo_packages" / "local-offline-trial-rc-099-cn-review"
        self.package_arg = validator.normalize_path(self.package_dir)
        self.zip_path = self.root / "artifacts" / "local_demo_packages" / "local-offline-trial-rc-099-cn-review-package-20260507.zip"
        self.output_json = self.root / "scan.json"
        self.candidate = "LOCAL_OFFLINE_TRIAL_RC_099_CN"
        self.source_candidate = "LOCAL_OFFLINE_TRIAL_RC_098_CN"
        self.zip_name = self.zip_path.name
        self.write_package()

    def tearDown(self):
        self.tmpdir.cleanup()

    def rel(self, rel_path: str) -> Path:
        return self.package_dir / rel_path

    def package_text(self) -> str:
        return (
            f"Candidate: {self.candidate}\n"
            f"Source candidate: {self.source_candidate}\n"
            f"Package: {self.package_arg}\n"
            f"Zip: {self.zip_name}\n"
        )

    def write_file(self, rel_path: str, content: bytes | str) -> None:
        path = self.rel(rel_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")

    def manifest_entry(self, rel_path: str) -> dict[str, object]:
        path = self.rel(rel_path)
        return {
            "file_name": path.name,
            "path": rel_path,
            "bytes": path.stat().st_size,
            "sha256": validator.file_sha256(path),
            "contains_raw_payload": False,
            "contains_secret_or_token": False,
            "contains_customer_visible_artifact": False,
            "retention_class": "S1_LOCAL_OFFLINE_CHINESE_REVIEW_PACKAGE",
        }

    def write_package(self) -> None:
        for rel_path in validator.REQUIRED_REVIEWER_FILES:
            self.write_file(rel_path, self.package_text())
        for rel_path in validator.REQUIRED_EVIDENCE_FILES:
            write_json(self.rel(rel_path), {"schema_version": rel_path, "status": "fixture"})
        for rel_path in validator.REQUIRED_SCREENSHOTS:
            self.write_file(rel_path, PNG_STUB)

        screenshot_index = {
            "candidate": self.candidate,
            "source_candidate": self.source_candidate,
            "boundaries": {key: False for key in validator.BOUNDARY_FALSE_KEYS},
            "screenshots": [
                {
                    "file_name": Path(rel_path).name,
                    "path": rel_path,
                    "bytes": self.rel(rel_path).stat().st_size,
                    "sha256": validator.file_sha256(self.rel(rel_path)),
                    "route": "/s1-run",
                    "viewport": "fixture",
                }
                for rel_path in validator.REQUIRED_SCREENSHOTS
            ],
        }
        write_json(self.rel("SCREENSHOT_INDEX.json"), screenshot_index)

        package_index = {
            "candidate": self.candidate,
            "source_candidate": self.source_candidate,
            "package_dir": self.package_arg,
            "zip_name": self.zip_name,
            "evidence_files": list(validator.REQUIRED_EVIDENCE_FILES),
            "screenshot_files": list(validator.REQUIRED_SCREENSHOTS),
            "boundaries": {key: False for key in validator.BOUNDARY_FALSE_KEYS},
        }
        write_json(self.rel("PACKAGE_INDEX_中文.json"), package_index)

        manifest_paths = (
            list(validator.REQUIRED_REVIEWER_FILES)
            + [rel_path for rel_path in validator.REQUIRED_JSON_FILES if rel_path != "package_manifest.json"]
            + list(validator.REQUIRED_EVIDENCE_FILES)
            + list(validator.REQUIRED_SCREENSHOTS)
        )
        manifest = {
            "candidate": self.candidate,
            "source_candidate": self.source_candidate,
            "package_dir": self.package_arg,
            "zip_name": self.zip_name,
            "boundaries": {key: False for key in validator.BOUNDARY_FALSE_KEYS},
            "package_files": [self.manifest_entry(rel_path) for rel_path in manifest_paths],
        }
        write_json(self.rel("package_manifest.json"), manifest)
        self.zip_path.parent.mkdir(parents=True, exist_ok=True)
        self.zip_path.write_bytes(b"zip-fixture")

    def run_validator(self) -> int:
        with redirect_stdout(StringIO()):
            return validator.run(
                [
                    "--package-dir",
                    str(self.package_dir),
                    "--candidate",
                    self.candidate,
                    "--source-candidate",
                    self.source_candidate,
                    "--zip-name",
                    self.zip_name,
                    "--zip-path",
                    str(self.zip_path),
                    "--output-json",
                    str(self.output_json),
                ]
            )

    def labels(self) -> set[str]:
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        return {finding["label"] for finding in payload["blocking_findings"]}

    def test_passes_consistent_rc_package(self):
        code = self.run_validator()

        self.assertEqual(validator.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("PASS", payload["status"])
        self.assertEqual(0, payload["blocking_finding_count"])

    def test_holds_on_candidate_mismatch(self):
        package_index = json.loads(self.rel("PACKAGE_INDEX_中文.json").read_text(encoding="utf-8"))
        package_index["candidate"] = "LOCAL_OFFLINE_TRIAL_RC_001_CN"
        write_json(self.rel("PACKAGE_INDEX_中文.json"), package_index)

        code = self.run_validator()

        self.assertEqual(validator.HOLD, code)
        self.assertIn("PACKAGE_INDEX_中文.json:candidate_mismatch", self.labels())

    def test_holds_on_stale_package_slug_in_reviewer_doc(self):
        self.write_file(
            "REVIEWER_START_HERE_中文.md",
            self.package_text() + "Old package: local-offline-trial-rc-006-cn-review\n",
        )

        code = self.run_validator()

        self.assertEqual(validator.HOLD, code)
        self.assertIn("unexpected_package_slug", self.labels())

    def test_holds_on_manifest_sha_mismatch(self):
        manifest = json.loads(self.rel("package_manifest.json").read_text(encoding="utf-8"))
        manifest["package_files"][0]["sha256"] = "0" * 64
        write_json(self.rel("package_manifest.json"), manifest)

        code = self.run_validator()

        self.assertEqual(validator.HOLD, code)
        self.assertIn("manifest_sha256_mismatch", self.labels())


if __name__ == "__main__":
    unittest.main()
