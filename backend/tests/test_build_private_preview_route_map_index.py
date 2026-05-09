import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import build_private_preview_route_map_index as builder  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class BuildPrivatePreviewRouteMapIndexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "artifacts" / "local_demo_packages" / "local-offline-trial-rc-019-cn-review"
        self.output_md = self.root / "artifacts" / "product_route_maps" / "local-offline-trial-rc-019-cn-review" / "route_map_index.md"
        self.output_json = self.root / "artifacts" / "product_route_maps" / "local-offline-trial-rc-019-cn-review" / "route_map_index.json"
        self.write_package()

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def write_package(self, include_s1_run: bool = True, boundary_value: bool = False) -> None:
        write_json(
            self.package_dir / "PACKAGE_INDEX_中文.json",
            {
                "candidate": "LOCAL_OFFLINE_TRIAL_RC_019_CN",
                "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_018_CN",
                "package_dir": "artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review",
                "zip_name": "local-offline-trial-rc-019-cn-review-package-20260508.zip",
                "route": ["/s1-trial", "/s1-run"],
                "start_here": "REVIEWER_START_HERE_中文.md",
                "checklist": "REVIEWER_CHECKLIST_中文.md",
                "feedback_template": "FEEDBACK_TEMPLATE_中文.md",
                "evidence_files": ["evidence/final_status.json"],
                "validation_files": ["validation/screenshot_safety_scan.json"],
                "boundaries": {
                    "real_data": boundary_value,
                    "masked_real_data": False,
                    "live_qwen_api": False,
                    "live_connectors": False,
                    "production_writeback": False,
                    "customer_visible_output": False,
                    "push": False,
                },
            },
        )
        screenshots = [
            {"route": "/s1-trial", "path": "screenshots/s1-trial-desktop.png", "viewport": "1440x1100"},
            {"route": "/s1-trial", "path": "screenshots/s1-trial-mobile.png", "viewport": "390x1000"},
        ]
        if include_s1_run:
            screenshots.extend(
                [
                    {"route": "/s1-run", "path": "screenshots/s1-run-desktop.png", "viewport": "1440x1100"},
                    {"route": "/s1-run", "path": "screenshots/s1-run-mobile.png", "viewport": "390x1000"},
                ]
            )
        write_json(
            self.package_dir / "SCREENSHOT_INDEX.json",
            {
                "screenshots": screenshots,
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
        write_json(
            self.package_dir / "package_manifest.json",
            {
                "package_files": [{"path": "REVIEWER_START_HERE_中文.md"}],
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

    def run_builder(self) -> int:
        with redirect_stdout(StringIO()):
            return builder.run(
                [
                    "--package-dir",
                    str(self.package_dir.relative_to(self.root)),
                    "--output-md",
                    str(self.output_md.relative_to(self.root)),
                    "--output-json",
                    str(self.output_json.relative_to(self.root)),
                    "--repo-root",
                    str(self.root),
                ]
            )

    def test_builds_route_map_index_with_persona_coverage(self) -> None:
        code = self.run_builder()
        self.assertEqual(builder.PASS, code)
        payload = json.loads(self.output_json.read_text(encoding="utf-8"))
        self.assertEqual("LOCAL_OFFLINE_TRIAL_RC_019_CN", payload["candidate"])
        self.assertEqual(2, len(payload["route_entries"]))
        persona_names = [item["persona_name"] for item in payload["persona_route_coverage"]]
        self.assertIn("工程师评审路径", persona_names)
        self.assertIn("经理评审路径", persona_names)
        self.assertIn("CTO评审路径", persona_names)
        md = self.output_md.read_text(encoding="utf-8")
        self.assertIn("## 产品旅程总览", md)
        self.assertIn("## 角色路径覆盖", md)

    def test_holds_when_route_has_no_screenshot_coverage(self) -> None:
        self.write_package(include_s1_run=False)
        code = self.run_builder()
        self.assertEqual(builder.HOLD, code)
        self.assertFalse(self.output_json.exists())

    def test_holds_when_boundary_is_not_false(self) -> None:
        self.write_package(boundary_value=True)
        code = self.run_builder()
        self.assertEqual(builder.HOLD, code)
        self.assertFalse(self.output_json.exists())


if __name__ == "__main__":
    unittest.main()
