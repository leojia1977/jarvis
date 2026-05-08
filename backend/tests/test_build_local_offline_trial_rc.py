import json
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import build_local_offline_trial_rc as builder  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class BuildLocalOfflineTrialRcTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.source_package = self.root / "source-rc"
        self.screenshot_dir = self.root / "screens"
        self.output_dir = self.root / "out" / "local-offline-trial-rc-099-cn-review"
        self.zip_path = self.root / "out" / "local-offline-trial-rc-099-cn-review-package.zip"
        self.validation_scan = self.root / "validation" / "screenshot_safety_scan.json"
        self.validation_report = self.root / "validation" / "qwen_provider_stub_report.json"
        self.write_source_package()
        self.write_screenshots()
        self.write_validation_scan()
        self.write_validation_report()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_source_package(self, finding_count: int = 0) -> None:
        evidence = self.source_package / "evidence"
        write_json(
            evidence / "final_status.json",
            {
                "can_deploy_to_customer_production": False,
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
            evidence / "safety_scan.json",
            {"summary": {"finding_count": finding_count, "no_go_count": 0}},
        )
        write_json(evidence / "artifact_manifest.json", {"artifacts": []})
        write_json(
            evidence / "case_summary.json",
            {
                "case_count": 20,
                "cases": [
                    {
                        "case_id": "UAT-19",
                        "title": "P3 manager summary without host raw evidence",
                        "summary": (
                            "S1 fixture summary for UAT-19: "
                            "P3 manager summary without host raw evidence. "
                            "Metadata-only review required."
                        ),
                    }
                ],
            },
        )

    def write_screenshots(self) -> None:
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        png_stub = b"\x89PNG\r\n\x1a\nsecupilot-test"
        for file_name, _, _ in builder.SCREENSHOT_SPECS:
            (self.screenshot_dir / file_name).write_bytes(png_stub)

    def write_validation_scan(self) -> None:
        write_json(
            self.validation_scan,
            {
                "schema_version": "secupilot.s1.review_screenshot_safety_scan.v1",
                "status": "PASS",
                "blocking_finding_count": 0,
            },
        )

    def write_validation_report(self) -> None:
        write_json(
            self.validation_report,
            {
                "schema_version": "secupilot.qwen.synthetic_provider_stub_report.v1",
                "status": "PASS",
                "live_network_call": False,
                "secret_value_read": False,
            },
        )

    def run_builder(self, extra_args: list[str] | None = None) -> int:
        argv = [
            "--candidate",
            "LOCAL_OFFLINE_TRIAL_RC_099_CN",
            "--source-candidate",
            "LOCAL_OFFLINE_TRIAL_RC_098_CN",
            "--source-package",
            str(self.source_package),
            "--screenshot-dir",
            str(self.screenshot_dir),
            "--output-dir",
            str(self.output_dir),
            "--zip-path",
            str(self.zip_path),
            "--source-commit",
            "testcommit",
            "--repo-root",
            str(self.root),
        ]
        if extra_args:
            argv.extend(extra_args)
        with redirect_stdout(StringIO()):
            return builder.run(argv)

    def run_builder_with_validation(self) -> int:
        with redirect_stdout(StringIO()):
            return builder.run(
                [
                    "--candidate",
                    "LOCAL_OFFLINE_TRIAL_RC_099_CN",
                    "--source-candidate",
                    "LOCAL_OFFLINE_TRIAL_RC_098_CN",
                    "--source-package",
                    str(self.source_package),
                    "--screenshot-dir",
                    str(self.screenshot_dir),
                    "--output-dir",
                    str(self.output_dir),
                    "--zip-path",
                    str(self.zip_path),
                    "--source-commit",
                    "testcommit",
                    "--repo-root",
                    str(self.root),
                    "--screenshot-safety-scan",
                    str(self.validation_scan),
                    "--validation-artifact",
                    str(self.validation_report),
                ]
            )

    def default_outer_manifest_path(self) -> Path:
        return Path(str(self.zip_path) + ".outer_zip_manifest.json")

    def test_builds_self_contained_package_and_zip(self):
        code = self.run_builder()

        self.assertEqual(builder.PASS, code)
        self.assertTrue((self.output_dir / "REVIEWER_START_HERE_中文.md").exists())
        self.assertTrue((self.output_dir / "REVIEWER_CHECKLIST_中文.md").exists())
        self.assertTrue((self.output_dir / "FEEDBACK_TEMPLATE_中文.md").exists())
        self.assertTrue((self.output_dir / "PACKAGE_INDEX_中文.json").exists())
        self.assertTrue((self.output_dir / "SCREENSHOT_INDEX.json").exists())
        self.assertTrue((self.output_dir / "package_manifest.json").exists())
        self.assertTrue(self.zip_path.exists())

        manifest = json.loads((self.output_dir / "package_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("LOCAL_OFFLINE_TRIAL_RC_099_CN", manifest["candidate"])
        self.assertEqual("LOCAL_OFFLINE_TRIAL_RC_098_CN", manifest["source_candidate"])
        self.assertEqual(False, manifest["boundaries"]["customer_visible_output"])
        self.assertEqual(
            {
                "folded_state_screenshot_files": ["screenshots/s1-run-first-load-folded-desktop.png"],
                "folded_state_screenshot_required": True,
                "folded_state_submission_gate": "REQUIRED_PRE_SUBMISSION",
                "folded_state_submission_gate_reason": "AI_ADVICE_SOURCE_SECTION_MUST_BE_FOLDED_ON_FIRST_LOAD",
                "folded_state_assertion_code": "AI_ADVICE_SOURCE_FIRST_LOAD_FOLDED",
                "folded_state_expected_state": "FOLDED",
                "folded_state_expected_section": "AI 建议来源",
                "folded_state_capture_phase": "FIRST_LOAD",
                "folded_state_capture_policy": "FIRST_LOAD_NO_INTERACTION",
                "folded_state_expected_interaction_count": 0,
                "folded_state_expected_route": "/s1-run",
                "folded_state_expected_viewport": "1440x1100",
                "folded_state_primary_screenshot": "screenshots/s1-run-first-load-folded-desktop.png",
                "folded_state_primary_sha256": builder.file_sha256(
                    self.output_dir / "screenshots" / "s1-run-first-load-folded-desktop.png"
                ),
                "folded_state_screenshot_sha256": {
                    "screenshots/s1-run-first-load-folded-desktop.png": builder.file_sha256(
                        self.output_dir / "screenshots" / "s1-run-first-load-folded-desktop.png"
                    )
                },
                "folded_state_proof": {
                    "screenshot_path": "screenshots/s1-run-first-load-folded-desktop.png",
                    "route": "/s1-run",
                    "viewport": "1440x1100",
                    "expected_state": "FOLDED",
                    "expected_section": "AI 建议来源",
                    "interaction_count": 0,
                    "interaction_policy": "FIRST_LOAD_NO_INTERACTION",
                    "sha256": builder.file_sha256(
                        self.output_dir / "screenshots" / "s1-run-first-load-folded-desktop.png"
                    ),
                },
            },
            manifest["required_archive_evidence"],
        )
        self.assertRegex(manifest["manifest_self_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(manifest["manifest_self_sha256"], builder.manifest_self_sha256(manifest))
        self.assertEqual(14, len(manifest["package_files"]))
        self.assertTrue(all(item["sha256"] for item in manifest["package_files"]))
        package_index = json.loads((self.output_dir / "PACKAGE_INDEX_中文.json").read_text(encoding="utf-8"))
        required_archive = package_index["required_archive_evidence"]
        self.assertEqual(True, required_archive["folded_state_screenshot_required"])
        self.assertEqual(
            ["screenshots/s1-run-first-load-folded-desktop.png"],
            required_archive["folded_state_screenshot_files"],
        )
        self.assertEqual("REQUIRED_PRE_SUBMISSION", required_archive["folded_state_submission_gate"])
        self.assertEqual(
            "AI_ADVICE_SOURCE_SECTION_MUST_BE_FOLDED_ON_FIRST_LOAD",
            required_archive["folded_state_submission_gate_reason"],
        )
        self.assertEqual("FIRST_LOAD_NO_INTERACTION", required_archive["folded_state_capture_policy"])
        self.assertEqual(
            "AI_ADVICE_SOURCE_FIRST_LOAD_FOLDED",
            required_archive["folded_state_assertion_code"],
        )
        self.assertEqual("FOLDED", required_archive["folded_state_expected_state"])
        self.assertEqual("AI 建议来源", required_archive["folded_state_expected_section"])
        self.assertEqual("FIRST_LOAD", required_archive["folded_state_capture_phase"])
        self.assertEqual(0, required_archive["folded_state_expected_interaction_count"])
        self.assertEqual("/s1-run", required_archive["folded_state_expected_route"])
        self.assertEqual("1440x1100", required_archive["folded_state_expected_viewport"])
        self.assertEqual(
            "screenshots/s1-run-first-load-folded-desktop.png",
            required_archive["folded_state_primary_screenshot"],
        )
        self.assertEqual(
            manifest["required_archive_evidence"]["folded_state_primary_sha256"],
            required_archive["folded_state_primary_sha256"],
        )
        self.assertEqual(
            manifest["required_archive_evidence"]["folded_state_screenshot_sha256"],
            required_archive["folded_state_screenshot_sha256"],
        )
        self.assertEqual(
            manifest["required_archive_evidence"]["folded_state_proof"],
            required_archive["folded_state_proof"],
        )
        with zipfile.ZipFile(self.zip_path, "r") as archive:
            archived_paths = set(archive.namelist())
        self.assertIn("package_manifest.json", archived_paths)

        outer_zip_manifest_path = self.default_outer_manifest_path()
        self.assertTrue(outer_zip_manifest_path.exists())
        outer_manifest = json.loads(outer_zip_manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(self.zip_path.name, outer_manifest["zip_name"])
        self.assertEqual(
            str(self.zip_path.relative_to(self.root)).replace("\\", "/"),
            outer_manifest["zip_path"],
        )
        self.assertRegex(outer_manifest["zip_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(outer_manifest["package_manifest_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(manifest["manifest_self_sha256"], outer_manifest["manifest_self_sha256"])
        self.assertEqual(
            builder.file_sha256(self.output_dir / "package_manifest.json"),
            outer_manifest["package_manifest_sha256"],
        )
        self.assertIn("RC-099", (self.output_dir / "REVIEWER_START_HERE_中文.md").read_text(encoding="utf-8"))
        case_summary = json.loads(
            (self.output_dir / "evidence" / "case_summary.json").read_text(encoding="utf-8")
        )
        case = case_summary["cases"][0]
        self.assertEqual(
            "P3 manager summary (metadata-only evidence scope)",
            case["title"],
        )
        self.assertNotIn("without host raw evidence", case["summary"])

    def test_includes_validation_artifact_when_supplied(self):
        code = self.run_builder_with_validation()

        self.assertEqual(builder.PASS, code)
        self.assertTrue((self.output_dir / "validation" / "screenshot_safety_scan.json").exists())
        self.assertTrue((self.output_dir / "validation" / "qwen_provider_stub_report.json").exists())
        package_index = json.loads((self.output_dir / "PACKAGE_INDEX_中文.json").read_text(encoding="utf-8"))
        self.assertEqual(
            [
                "validation/screenshot_safety_scan.json",
                "validation/qwen_provider_stub_report.json",
            ],
            package_index["validation_files"],
        )
        manifest = json.loads((self.output_dir / "package_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(16, len(manifest["package_files"]))

    def test_supports_explicit_outer_zip_manifest_path(self):
        explicit_outer_manifest = self.root / "out" / "manifests" / "rc099.outer.json"

        code = self.run_builder(
            [
                "--outer-zip-manifest",
                str(explicit_outer_manifest.relative_to(self.root)).replace("\\", "/"),
            ]
        )

        self.assertEqual(builder.PASS, code)
        self.assertTrue(explicit_outer_manifest.exists())
        outer_manifest = json.loads(explicit_outer_manifest.read_text(encoding="utf-8"))
        self.assertEqual(self.zip_path.name, outer_manifest["zip_name"])
        self.assertRegex(outer_manifest["zip_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(outer_manifest["package_manifest_sha256"], r"^[0-9a-f]{64}$")
        manifest = json.loads((self.output_dir / "package_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["manifest_self_sha256"], outer_manifest["manifest_self_sha256"])
        self.assertEqual(
            builder.file_sha256(self.output_dir / "package_manifest.json"),
            outer_manifest["package_manifest_sha256"],
        )

    def test_holds_when_outer_manifest_path_is_outside_repo(self):
        code = self.run_builder(["--outer-zip-manifest", "../../outside/outer.json"])

        self.assertEqual(builder.HOLD, code)
        self.assertFalse(self.zip_path.exists())
        self.assertFalse((self.root.parent / "outside" / "outer.json").exists())

    def test_holds_when_safety_scan_has_findings(self):
        self.write_source_package(finding_count=1)

        code = self.run_builder()

        self.assertEqual(builder.HOLD, code)
        self.assertFalse(self.zip_path.exists())
        self.assertFalse(self.default_outer_manifest_path().exists())

    def test_requires_folded_state_screenshot_archive_evidence(self):
        folded_name = "s1-run-first-load-folded-desktop.png"
        folded_path = self.screenshot_dir / folded_name
        folded_path.unlink()
        code = self.run_builder()

        self.assertEqual(builder.HOLD, code)
        self.assertFalse((self.output_dir / "package_manifest.json").exists())

    def test_includes_folded_state_screenshot_in_package_index(self):
        code = self.run_builder()

        self.assertEqual(builder.PASS, code)
        folded_name = "s1-run-first-load-folded-desktop.png"
        folded_path = self.output_dir / "screenshots" / folded_name
        self.assertTrue(folded_path.exists())
        package_index = json.loads((self.output_dir / "PACKAGE_INDEX_中文.json").read_text(encoding="utf-8"))
        self.assertIn(f"screenshots/{folded_name}", package_index["screenshot_files"])
        screenshot_index = json.loads((self.output_dir / "SCREENSHOT_INDEX.json").read_text(encoding="utf-8"))
        screenshot_names = {item["file_name"] for item in screenshot_index["screenshots"]}
        self.assertIn(folded_name, screenshot_names)
        folded_entry = next(
            item for item in screenshot_index["screenshots"] if item["file_name"] == folded_name
        )
        self.assertEqual(
            {
                "evidence_schema_version": "secupilot.s1.folded_state_archive_evidence.v1",
                "assertion_code": "AI_ADVICE_SOURCE_FIRST_LOAD_FOLDED",
                "evidence_role": "AI_ADVICE_SOURCE_FOLDED_STATE",
                "submission_gate": "REQUIRED_PRE_SUBMISSION",
                "submission_gate_reason": "AI_ADVICE_SOURCE_SECTION_MUST_BE_FOLDED_ON_FIRST_LOAD",
                "capture_phase": "FIRST_LOAD",
                "capture_policy": "FIRST_LOAD_NO_INTERACTION",
                "sha256": builder.file_sha256(
                    self.output_dir / "screenshots" / "s1-run-first-load-folded-desktop.png"
                ),
                "interaction_count": 0,
                "expected_interaction_count": 0,
                "expected_state": "FOLDED",
                "expected_section": "AI 建议来源",
                "expected_route": "/s1-run",
                "expected_viewport": "1440x1100",
            },
            folded_entry["archive_evidence"],
        )


if __name__ == "__main__":
    unittest.main()
