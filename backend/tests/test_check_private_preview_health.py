import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from _project_bootstrap import bootstrap

bootstrap()

from scripts import check_private_preview_health as healthcheck  # noqa: E402


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class PrivatePreviewHealthcheckTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.package_dir = self.root / "artifacts" / "local_demo_packages" / "local-offline-trial-rc-020-cn-review"
        self.route_map = (
            self.root
            / "artifacts"
            / "product_route_maps"
            / "local-offline-trial-rc-019-cn-review"
            / "route_map_index.json"
        )
        self.launch_info = (
            self.root / "artifacts" / "local_trial_launches" / "local-offline-trial-rc-020" / "launch_info.json"
        )
        self.output_json = self.root / "artifacts" / "private_preview" / "healthcheck" / "health.json"
        self.write_fixtures()

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_fixtures(self) -> None:
        write_json(
            self.package_dir / "package_manifest.json",
            {
                "candidate": "LOCAL_OFFLINE_TRIAL_RC_020_CN",
                "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_019_CN",
                "package_dir": "artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review",
                "boundaries": {key: False for key in healthcheck.BOUNDARY_FALSE_KEYS},
            },
        )
        write_json(
            self.package_dir / "evidence" / "final_status.json",
            {
                "can_deploy_to_customer_production": False,
                "boundaries_preserved": {key: False for key in healthcheck.FINAL_STATUS_FALSE_KEYS},
            },
        )
        (self.package_dir / "REVIEWER_START_HERE_中文.md").parent.mkdir(parents=True, exist_ok=True)
        (self.package_dir / "REVIEWER_START_HERE_中文.md").write_text(
            "本包仅用于本地离线内部评审。\n", encoding="utf-8"
        )

        write_json(
            self.route_map,
            {
                "schema_version": "secupilot.private_preview.route_map_index.v1",
                "candidate": "LOCAL_OFFLINE_TRIAL_RC_019_CN",
                "source_candidate": "LOCAL_OFFLINE_TRIAL_RC_018_CN",
                "route_entries": [{"route": "/s1-trial", "title": "入口", "objective": "fixture", "screenshot_count": 1}],
                "boundaries": {key: False for key in healthcheck.BOUNDARY_FALSE_KEYS},
                "non_authorization": {
                    "customer_visible_or_deploy_go": False,
                    "live_qwen_api": False,
                    "production_writeback": False,
                },
            },
        )
        write_json(
            self.launch_info,
            {
                "schema_version": "secupilot.s1.local_offline_trial_launcher.v1",
                "candidate": "LOCAL_OFFLINE_TRIAL_RC_020_CN",
                "operator_notice": "Local/offline private-preview shell only.",
                "server_started": False,
                "boundaries": {key: False for key in healthcheck.BOUNDARY_FALSE_KEYS},
            },
        )

    def run_healthcheck(self) -> int:
        with redirect_stdout(StringIO()):
            return healthcheck.run(
                [
                    "--package-dir",
                    "artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review",
                    "--route-map",
                    "artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json",
                    "--launch-info",
                    "artifacts/local_trial_launches/local-offline-trial-rc-020/launch_info.json",
                    "--output-json",
                    "artifacts/private_preview/healthcheck/health.json",
                    "--repo-root",
                    str(self.root),
                ]
            )

    def load_output(self) -> dict:
        return json.loads(self.output_json.read_text(encoding="utf-8"))

    def labels(self) -> set[str]:
        return {item["label"] for item in self.load_output()["blocking_findings"]}

    def test_passes_with_complete_private_preview_materials(self):
        code = self.run_healthcheck()

        self.assertEqual(healthcheck.PASS, code)
        payload = self.load_output()
        self.assertEqual("PASS", payload["status"])
        self.assertEqual(0, payload["blocking_finding_count"])

    def test_accepts_powershell_bom_launch_metadata(self):
        payload = json.loads(self.launch_info.read_text(encoding="utf-8"))
        self.launch_info.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8-sig")

        code = self.run_healthcheck()

        self.assertEqual(healthcheck.PASS, code)

    def test_holds_when_package_is_missing(self):
        for path in sorted(self.package_dir.glob("**/*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        self.package_dir.rmdir()

        code = self.run_healthcheck()

        self.assertEqual(healthcheck.HOLD, code)
        self.assertIn("package_dir_missing", self.labels())

    def test_holds_when_launch_metadata_boundary_breaks(self):
        launch_info = json.loads(self.launch_info.read_text(encoding="utf-8"))
        launch_info["boundaries"]["live_qwen_api"] = True
        write_json(self.launch_info, launch_info)

        code = self.run_healthcheck()

        self.assertEqual(healthcheck.HOLD, code)
        self.assertIn("boundary_not_false", self.labels())


if __name__ == "__main__":
    unittest.main()
