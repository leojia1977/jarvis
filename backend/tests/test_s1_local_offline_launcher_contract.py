import json
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "launch_s1_local_offline_trial.ps1"
PACKAGE_DIR = "artifacts\\local_demo_packages\\local-offline-trial-rc-019-cn-review"
DELIVERY_DIR = "artifacts\\local_trial_packages\\local-offline-trial-rc-006"
LAUNCH_INFO_PATH = (
    REPO_ROOT
    / "artifacts"
    / "local_trial_launches"
    / "local-offline-trial-rc-019"
    / "launch_info.json"
)


def run_launcher(*args: str) -> dict:
    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(SCRIPT_PATH),
        "-PackageDir",
        PACKAGE_DIR,
        "-DeliveryDir",
        DELIVERY_DIR,
        "-Route",
        "/s1-trial",
        "-SkipBuild",
        "-NoServer",
        *args,
    ]
    result = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    return json.loads(result.stdout.strip())


class S1LocalOfflineLauncherContractTests(unittest.TestCase):
    def test_check_only_contract_is_local_offline(self):
        payload = run_launcher("-CheckOnly")

        self.assertEqual("LOCAL_OFFLINE_TRIAL_RC_019_CN", payload["candidate"])
        self.assertTrue(payload["check_only"])
        self.assertFalse(payload["server_started"])
        self.assertEqual(
            "artifacts\\local_trial_launches\\local-offline-trial-rc-019\\launch_info.json",
            payload["launcher_output_path"],
        )
        self.assertEqual(
            "artifacts\\local_demo_packages\\local-offline-trial-rc-019-cn-review\\REVIEWER_START_HERE_中文.md",
            payload["reviewer_start_here"],
        )
        self.assertIn("Local/offline private-preview shell only", payload["operator_notice"])
        for key, value in payload["boundaries"].items():
            self.assertFalse(value, key)

    def test_non_check_only_writes_launch_info_file(self):
        payload = run_launcher()

        self.assertFalse(payload["check_only"])
        self.assertTrue(LAUNCH_INFO_PATH.exists())
        launch_info = json.loads(LAUNCH_INFO_PATH.read_text(encoding="utf-8-sig"))
        self.assertEqual("LOCAL_OFFLINE_TRIAL_RC_019_CN", launch_info["candidate"])
        self.assertEqual(payload["launcher_output_path"], launch_info["launcher_output_path"])
        self.assertFalse(launch_info["boundaries"]["customer_visible_output"])
        self.assertFalse(launch_info["boundaries"]["live_qwen_api"])


if __name__ == "__main__":
    unittest.main()
