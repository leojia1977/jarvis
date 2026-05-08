#!/usr/bin/env python3
"""Pick the next executable SecuPilot MVP Goal candidate."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


PASS = 0
HOLD = 20
OPEN_STATUSES = {"OPEN", "BACKLOG_OPEN"}
PRIORITY_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

QUEUE_ITEMS = (
    {
        "queue_key": "GOAL-MVP-61_RC016_SCREENSHOT_EXPECTED_CANDIDATE",
        "suffix": "RC016_SCREENSHOT_EXPECTED_CANDIDATE",
        "match": "RC016_SCREENSHOT_EXPECTED_CANDIDATE",
        "goal_type": "package",
        "profile": "RC_SCREENSHOT_CANDIDATE",
        "statement": "Align RC-016 screenshot visible candidate text, visual assertions, and screenshot safety expected candidate so package validation no longer relies on RC-014 text.",
    },
    {
        "queue_key": "GOAL-MVP-62_ZIP_TAMPER_NEGATIVE_TEST",
        "suffix": "ZIP_TAMPER_NEGATIVE_TEST",
        "match": "ZIP_TAMPER_NEGATIVE_TEST",
        "goal_type": "validator",
        "profile": "ZIP_TAMPER_TEST",
        "statement": "Add negative tests proving local/offline package zip or manifest tampering is detected and cannot pass RC integrity validation.",
    },
    {
        "queue_key": "GOAL-MVP-63_PRODUCT_ACCELERATION_POOL_PICKER",
        "suffix": "PRODUCT_ACCELERATION_POOL_PICKER",
        "match": "PRODUCT_ACCELERATION_POOL_PICKER",
        "goal_type": "script",
        "profile": "SCRIPT_GOAL_PICKER",
        "statement": "Extend the Goal picker so queue exhaustion falls through to an explicit product acceleration pool instead of repeated exhausted closeouts.",
    },
    {
        "queue_key": "GOAL-MVP-64_CLIENT_TRIAL_HOME_PRODUCTIZATION",
        "suffix": "CLIENT_TRIAL_HOME_PRODUCTIZATION",
        "match": "CLIENT_TRIAL_HOME_PRODUCTIZATION",
        "goal_type": "page",
        "profile": "CLIENT_TRIAL_HOME",
        "statement": "Make the local/offline trial entry feel like a product trial home: clearer headline, business-readable sections, and lower technical-path prominence while preserving local-only boundaries.",
    },
    {
        "queue_key": "GOAL-MVP-65_LOCAL_OFFLINE_TRIAL_REPORT",
        "suffix": "LOCAL_OFFLINE_TRIAL_REPORT",
        "match": "LOCAL_OFFLINE_TRIAL_REPORT",
        "goal_type": "test-report",
        "profile": "LOCAL_TRIAL_REPORT",
        "statement": "Generate a local/offline trial report from the latest RC package, validation outputs, and reviewer feedback so internal readers get a single current status artifact.",
    },
    {
        "queue_key": "GOAL-MVP-66_RC_PACKAGE_SELF_REVIEW_REPORT",
        "suffix": "RC_PACKAGE_SELF_REVIEW_REPORT",
        "match": "RC_PACKAGE_SELF_REVIEW_REPORT",
        "goal_type": "test-report",
        "profile": "RC_SELF_REVIEW_REPORT",
        "statement": "Generate an automated RC package self-review report so package readiness has a machine-generated PASS/HOLD summary before human review.",
    },
    {
        "queue_key": "GOAL-MVP-67_ROLE_BASED_TRIAL_HOME",
        "suffix": "ROLE_BASED_TRIAL_HOME",
        "match": "ROLE_BASED_TRIAL_HOME",
        "goal_type": "page",
        "profile": "ROLE_BASED_HOME",
        "statement": "Turn the trial entry into a role-based product home with engineer, manager, and CTO paths while keeping one shared SecuPilot product experience.",
    },
    {
        "queue_key": "GOAL-MVP-68_INCIDENT_DETAIL_PRODUCT_PAGE",
        "suffix": "INCIDENT_DETAIL_PRODUCT_PAGE",
        "match": "INCIDENT_DETAIL_PRODUCT_PAGE",
        "goal_type": "page",
        "profile": "INCIDENT_DETAIL_PAGE",
        "statement": "Create a productized incident detail page where conclusion, risk, and next action lead while evidence stays collapsed behind a technical detail section.",
    },
    {
        "queue_key": "GOAL-MVP-69_RECOMMENDED_ACTION_CARDS",
        "suffix": "RECOMMENDED_ACTION_CARDS",
        "match": "RECOMMENDED_ACTION_CARDS",
        "goal_type": "page",
        "profile": "ACTION_CARDS",
        "statement": "Add SecuPilot recommended action cards that translate analysis into practical next steps without enabling autonomous action or write-back.",
    },
    {
        "queue_key": "GOAL-MVP-70_USER_FEEDBACK_LOOP",
        "suffix": "USER_FEEDBACK_LOOP",
        "match": "USER_FEEDBACK_LOOP",
        "goal_type": "page",
        "profile": "FEEDBACK_LOOP",
        "statement": "Add a local/offline feedback loop for accuracy, usefulness, missing information, and suggested action so trial feedback becomes structured product input.",
    },
    {
        "queue_key": "GOAL-MVP-71_QWEN_DRY_PROVIDER_UI",
        "suffix": "QWEN_DRY_PROVIDER_UI",
        "match": "QWEN_DRY_PROVIDER_UI",
        "goal_type": "page",
        "profile": "QWEN_DRY_UI",
        "statement": "Expose a cloud-Qwen dry provider preview in the product UI using mock contract data only, with no live API call, no key, and no real data.",
    },
    {
        "queue_key": "GOAL-MVP-72_QWEN_CLOUD_CONTRACT_MOCK",
        "suffix": "QWEN_CLOUD_CONTRACT_MOCK",
        "match": "QWEN_CLOUD_CONTRACT_MOCK",
        "goal_type": "interface",
        "profile": "QWEN_CLOUD_CONTRACT",
        "statement": "Define the cloud model invocation contract with mock latency, timeout, and error handling so Qwen integration can be tested without network calls or secrets.",
    },
    {
        "queue_key": "GOAL-MVP-73_PRIVATE_DEPLOY_PACKAGE_STRUCTURE",
        "suffix": "PRIVATE_DEPLOY_PACKAGE_STRUCTURE",
        "match": "PRIVATE_DEPLOY_PACKAGE_STRUCTURE",
        "goal_type": "package",
        "profile": "PRIVATE_DEPLOY_PACKAGE",
        "statement": "Draft a Windows/local-first private deployment package structure with startup, config, and offline trial handoff files, without deploying or touching customer systems.",
    },
    {
        "queue_key": "GOAL-MVP-74_CUSTOMER_TRIAL_README_AND_LAUNCHER",
        "suffix": "CUSTOMER_TRIAL_README_AND_LAUNCHER",
        "match": "CUSTOMER_TRIAL_README_AND_LAUNCHER",
        "goal_type": "script",
        "profile": "CUSTOMER_TRIAL_LAUNCHER",
        "statement": "Create a customer-trial README and one-command local launcher for the internal trial build while preserving local/offline and no-deploy boundaries.",
    },
    {
        "queue_key": "GOAL-MVP-75_INTERNAL_TRIAL_KPI_REPORT",
        "suffix": "INTERNAL_TRIAL_KPI_REPORT",
        "match": "INTERNAL_TRIAL_KPI_REPORT",
        "goal_type": "test-report",
        "profile": "TRIAL_KPI_REPORT",
        "statement": "Generate an internal trial KPI report covering understanding rate, task completion, feedback themes, and blockers from local/offline feedback artifacts.",
    },
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_latest_backlog(repo_root: Path) -> Path | None:
    candidates = sorted(
        repo_root.glob("artifacts/product_backlog/**/reviewer_backlog.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def list_goal_cards(repo_root: Path) -> list[Path]:
    return sorted(repo_root.glob("docs/goals/GOAL-MVP-*.md"))


def next_goal_index(goal_cards: list[Path]) -> int:
    max_index = 0
    pattern = re.compile(r"GOAL-MVP-(\d+)_")
    for path in goal_cards:
        match = pattern.search(path.stem.upper())
        if match:
            max_index = max(max_index, int(match.group(1)))
    return max_index + 1 if max_index else 1


def choose_open_item(items: list[dict[str, Any]]) -> dict[str, Any] | None:
    open_items = []
    for item in items:
        status = str(item.get("status", "")).upper()
        if status in OPEN_STATUSES:
            open_items.append(item)
    if not open_items:
        return None

    def sort_key(item: dict[str, Any]) -> tuple[int, str]:
        priority = str(item.get("priority", "P3")).upper()
        return (PRIORITY_RANK.get(priority, 99), str(item.get("id", "")))

    open_items.sort(key=sort_key)
    return open_items[0]


def infer_profile(item: dict[str, Any]) -> str:
    text = f"{item.get('title', '')} {item.get('description', '')}".lower()
    if any(token in text for token in ("/s1-run", "result", "first-screen", "首屏", "文案", "tooltip")):
        return "UI_PAGE"
    if any(
        token in text
        for token in ("manifest", "candidate", "source", "package", "zip", "截图", "screenshot", "case title")
    ):
        return "PACKAGE"
    return "SCRIPT_GENERIC"


def profile_contract(
    profile: str,
    goal_id: str,
    date_tag: str,
    backlog_path: str | None,
) -> dict[str, Any]:
    goal_card = f"docs/goals/{goal_id}.md"
    closeout = f"docs/S6_FAST_MVP_{goal_id.replace('-', '_')}_{date_tag}.md"
    if profile == "UI_PAGE":
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/s1/S1ArtifactView.tsx",
                "frontend/src/App.test.tsx",
                "frontend/tests/e2e/s1-artifact-viewer.spec.ts",
                "frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "target UI field remains unchanged after patch",
                "frontend unit/build/playwright fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "RC_SCREENSHOT_CANDIDATE":
        candidate = "LOCAL_OFFLINE_TRIAL_RC_016_CN"
        scan_path = "artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan_mvp61.json"
        return {
            "goal_type": "package",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts",
                "frontend/src/App.test.tsx",
                "frontend/tests/e2e/s1-artifact-viewer.spec.ts",
                "frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts",
                scan_path,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts",
                f"py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate {candidate} --output-json {scan_path}",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "screenshot visible text still contains LOCAL_OFFLINE_TRIAL_RC_014_CN as current candidate",
                "screenshot safety expected_candidate_missing finding appears",
                "frontend unit/build/playwright fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "ZIP_TAMPER_TEST":
        return {
            "goal_type": "validator",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_local_offline_trial_rc.py",
                "scripts/validate_local_trial_rc_consistency.py",
                "backend/tests/test_build_local_offline_trial_rc.py",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_local_offline_trial_rc",
                "py -3 scripts/build_local_offline_trial_rc.py --help",
                "py -3 scripts/validate_local_trial_rc_consistency.py --help",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "tampered zip or manifest can still pass validation",
                "negative test mutates repo artifacts outside a temporary directory",
                "unit test fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "PACKAGE":
        return {
            "goal_type": "package",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_local_offline_trial_rc.py",
                "backend/tests/test_build_local_offline_trial_rc.py",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_local_offline_trial_rc",
                "py -3 scripts/build_local_offline_trial_rc.py --help",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "package builder behavior changes outside selected backlog scope",
                "unit test fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "SCRIPT_GOAL_PICKER":
        return {
            "goal_type": "script",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/pick_next_mvp_goal.py",
                "backend/tests/test_pick_next_mvp_goal.py",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_pick_next_mvp_goal",
                "py -3 scripts/pick_next_mvp_goal.py --repo-root . --output-json artifacts/product_acceleration/next_goal_candidate.json --output-md artifacts/product_acceleration/next_goal_candidate.md",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "latest backlog cannot be parsed as JSON",
                "script output misses exact_files or acceptance_commands",
                "unit test fails twice in the same way",
            ],
        }
    if profile == "CLIENT_TRIAL_HOME":
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/s1/S1LocalTrialView.tsx",
                "frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts",
                "frontend/src/App.test.tsx",
                "frontend/tests/e2e/s1-artifact-viewer.spec.ts",
                "frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "trial home exposes P1/P2/P3, Mock Fixture, or Expert Mode text",
                "technical artifact paths dominate first screen",
                "frontend unit/build/playwright fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "LOCAL_TRIAL_REPORT":
        report_path = "artifacts/product_reports/local-offline-trial-rc-016-cn-review/trial_report.md"
        return {
            "goal_type": "test-report",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_client_trial_readiness_report.py",
                "backend/tests/test_build_client_trial_readiness_report.py",
                report_path,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_client_trial_readiness_report",
                "py -3 scripts/build_client_trial_readiness_report.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review --feedback-json artifacts/local_demo_packages/local-offline-trial-rc-014-cn-review/reviewer_feedback.json --output-report artifacts/product_reports/local-offline-trial-rc-016-cn-review/trial_report.md --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "report grants customer-visible deploy or pilot go",
                "report omits package, safety, or validation status",
                "unit test fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "RC_SELF_REVIEW_REPORT":
        report_path = "artifacts/rc_self_review/local-offline-trial-rc-016-cn-review/self_review_report.md"
        return {
            "goal_type": "test-report",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_rc_package_self_review.py",
                "backend/tests/test_build_rc_package_self_review.py",
                report_path,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_rc_package_self_review",
                "py -3 scripts/build_rc_package_self_review.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review --screenshot-safety-scan artifacts/review_screenshot_safety/local-offline-trial-rc-016-cn-review/screenshot_safety_scan.json --rc-consistency-check artifacts/local_trial_rc_consistency/local-offline-trial-rc-016-cn-review/rc_consistency_check.json --outer-zip-manifest artifacts/local_demo_packages/local-offline-trial-rc-016-cn-review-package-20260508.zip.outer_zip_manifest.json --output-report artifacts/rc_self_review/local-offline-trial-rc-016-cn-review/self_review_report.md --output-json artifacts/rc_self_review/local-offline-trial-rc-016-cn-review/self_review_report.json --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "self-review report marks PASS when any validator has blocking findings",
                "report includes raw payload, secret, token, auth header, or customer-visible deploy go",
                "unit test fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "ROLE_BASED_HOME":
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/s1/S1LocalTrialView.tsx",
                "frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts",
                "frontend/src/App.test.tsx",
                "frontend/tests/e2e/s1-artifact-viewer.spec.ts",
                "frontend/tests/e2e/s1-artifact-viewer.visual.spec.ts",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "role cards are generic marketing copy instead of engineer/manager/CTO trial paths",
                "P1/P2/P3, Mock Fixture, or Expert Mode appears in reviewer-facing UI",
                "frontend unit/build/playwright fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "INCIDENT_DETAIL_PAGE":
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/s1/S1ArtifactView.tsx",
                "frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts",
                "frontend/src/App.test.tsx",
                "frontend/tests/e2e/s1-artifact-viewer.spec.ts",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "incident detail first screen is dominated by evidence table or artifact paths",
                "conclusion, risk, or next action is missing from first screen",
                "raw payload, secret, token, auth header, or write-back text appears",
                "frontend unit/build/playwright fails twice in the same way",
            ],
        }
    if profile == "ACTION_CARDS":
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/s1/S1ArtifactView.tsx",
                "frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts",
                "frontend/src/App.test.tsx",
                "frontend/tests/e2e/s1-artifact-viewer.spec.ts",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "action card implies autonomous approval, remediation, write-back, or production mutation",
                "recommended action lacks human-review wording",
                "frontend unit/build/playwright fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "FEEDBACK_LOOP":
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/s1/S1ArtifactView.tsx",
                "frontend/src/secupilot/s1/s1ClosedShadowRunArtifacts.ts",
                "frontend/src/App.test.tsx",
                "frontend/tests/e2e/s1-artifact-viewer.spec.ts",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "feedback control writes to backend, network, external tracker, or customer-visible output",
                "feedback categories omit accuracy, usefulness, missing information, or suggested action",
                "frontend unit/build/playwright fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "QWEN_DRY_UI":
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/s1/s1QwenProviderDryPreview.ts",
                "frontend/src/secupilot/s1/s1QwenProviderContract.ts",
                "frontend/src/secupilot/s1/S1ArtifactView.tsx",
                "frontend/src/App.test.tsx",
                "frontend/tests/e2e/s1-artifact-viewer.spec.ts",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "UI requires API key, live Qwen call, network request, or connector output",
                "UI accepts raw payload, action_command, or autonomous approval fields",
                "frontend unit/build/playwright fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "QWEN_CLOUD_CONTRACT":
        return {
            "goal_type": "interface",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/s1/s1QwenProviderContract.ts",
                "frontend/src/secupilot/s1/s1QwenProviderDryPreview.ts",
                "frontend/src/App.test.tsx",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "contract requires network, API key, secret, token, or live Qwen service",
                "contract omits mock latency, timeout, or error-state handling",
                "contract permits autonomous action or production write-back",
                "frontend unit/build fails twice in the same way",
            ],
        }
    if profile == "PRIVATE_DEPLOY_PACKAGE":
        return {
            "goal_type": "package",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_private_trial_package.py",
                "backend/tests/test_build_private_trial_package.py",
                "artifacts/private_trial_package/README_中文.md",
                "artifacts/private_trial_package/package_manifest.json",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_private_trial_package",
                "py -3 scripts/build_private_trial_package.py --output-dir artifacts/private_trial_package --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "package attempts deploy, service installation, external network, or customer system mutation",
                "package includes secrets, tokens, auth headers, or real data",
                "unit test fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "CUSTOMER_TRIAL_LAUNCHER":
        return {
            "goal_type": "script",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/launch_customer_trial_local.ps1",
                "artifacts/private_trial_package/README_中文.md",
                "backend/tests/test_customer_trial_launcher_contract.py",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_customer_trial_launcher_contract",
                "powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/launch_customer_trial_local.ps1 -DryRun",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "launcher starts deploy, opens public tunnel, calls live API, or mutates production/customer systems",
                "dry run omits local URL, package path, or stop instructions",
                "unit test or dry run fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "TRIAL_KPI_REPORT":
        return {
            "goal_type": "test-report",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_internal_trial_kpi_report.py",
                "backend/tests/test_build_internal_trial_kpi_report.py",
                "artifacts/product_reports/internal_trial_kpi_report.md",
                "artifacts/product_reports/internal_trial_kpi_report.json",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_internal_trial_kpi_report",
                "py -3 scripts/build_internal_trial_kpi_report.py --feedback-root artifacts/product_backlog --output-md artifacts/product_reports/internal_trial_kpi_report.md --output-json artifacts/product_reports/internal_trial_kpi_report.json --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "KPI report fabricates reviewer decisions or customer usage metrics",
                "report grants customer-visible deploy or production launch",
                "unit test fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    return {
        "goal_type": "script",
        "goal_card_path": goal_card,
        "closeout_path": closeout,
        "exact_files": [goal_card, "scripts/close_reviewer_backlog_items.py", closeout],
        "acceptance_commands": [
            f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
            "py -3 scripts/close_reviewer_backlog_items.py --help",
            "git -c core.quotepath=false diff --check",
        ],
        "hold_conditions": [
            "backlog item cannot map to a bounded execution profile",
            "script command fails",
            "scope expands beyond listed files",
        ],
    }


def backlog_candidate(
    repo_root: Path,
    goal_index: int,
    backlog_path: Path,
    item: dict[str, Any],
) -> dict[str, Any]:
    item_id = str(item.get("id", "UNKNOWN")).replace("-", "_")
    goal_id = f"GOAL-MVP-{goal_index:02d}_BACKLOG_ITEM_{item_id}"
    date_tag = datetime.now().strftime("%Y_%m_%d")
    profile = infer_profile(item)
    contract = profile_contract(profile, goal_id, date_tag, backlog_path.as_posix())
    return {
        "selection_mode": "BACKLOG_OPEN_ITEM",
        "source_backlog_json": backlog_path.as_posix(),
        "selected_backlog_item": {
            "id": item.get("id"),
            "title": item.get("title"),
            "status": item.get("status"),
            "priority": item.get("priority"),
            "category": item.get("category"),
        },
        "candidate_goal": {
            "queue_key": "REVIEWER_BACKLOG_OPEN_ITEM",
            "goal_id": goal_id,
            "goal_type": contract["goal_type"],
            "statement": str(item.get("title", "")).strip(),
            "exact_files": contract["exact_files"],
            "acceptance_commands": contract["acceptance_commands"],
            "hold_conditions": contract["hold_conditions"],
            "followup_note": "If implementation commit lands, run one follow-up backlog closeout Goal for this exact item.",
        },
    }


def queue_candidate(repo_root: Path, goal_index: int, goal_cards: list[Path]) -> dict[str, Any]:
    existing_names = [path.stem.upper() for path in goal_cards]
    date_tag = datetime.now().strftime("%Y_%m_%d")
    for item in QUEUE_ITEMS:
        if any(item["match"] in name for name in existing_names):
            continue
        goal_id = f"GOAL-MVP-{goal_index:02d}_{item['suffix']}"
        contract = profile_contract(item["profile"], goal_id, date_tag, None)
        return {
            "selection_mode": "QUEUE_FALLBACK",
            "candidate_goal": {
                "queue_key": item["queue_key"],
                "goal_id": goal_id,
                "goal_type": contract["goal_type"],
                "statement": item.get(
                    "statement",
                    f"Execute {item['queue_key']} as the next bounded product-acceleration Goal.",
                ),
                "exact_files": contract["exact_files"],
                "acceptance_commands": contract["acceptance_commands"],
                "hold_conditions": contract["hold_conditions"],
            },
        }

    goal_id = f"GOAL-MVP-{goal_index:02d}_QUEUE_EXHAUSTED"
    contract = profile_contract("SCRIPT_GENERIC", goal_id, date_tag, None)
    return {
        "selection_mode": "CONCRETE_BLOCKER",
        "candidate_goal": {
            "queue_key": "QUEUE_EXHAUSTED_REQUIRE_NEW_PRODUCT_GOAL",
            "goal_id": goal_id,
            "goal_type": contract["goal_type"],
            "statement": "All predefined queue goals appear completed; require one new explicit product-acceleration goal definition.",
            "exact_files": contract["exact_files"],
            "acceptance_commands": contract["acceptance_commands"],
            "hold_conditions": contract["hold_conditions"],
        },
    }


def render_markdown(payload: dict[str, Any]) -> str:
    candidate = payload["candidate_goal"]
    selected = payload.get("selected_backlog_item")
    selected_block = ""
    if selected:
        selected_block = (
            "## Selected Backlog Item\n\n"
            f"- id: {selected.get('id')}\n"
            f"- priority: {selected.get('priority')}\n"
            f"- status: {selected.get('status')}\n"
            f"- title: {selected.get('title')}\n\n"
        )
    commands = "\n".join(f"- {line}" for line in candidate["acceptance_commands"])
    hold_conditions = "\n".join(f"- {line}" for line in candidate["hold_conditions"])
    files = "\n".join(f"- {path}" for path in candidate["exact_files"])
    return (
        "# SecuPilot Next MVP Goal Candidate\n\n"
        f"Generated at: {payload['generated_at_local']}\n\n"
        f"Selection mode: {payload['selection_mode']}\n\n"
        f"{selected_block}"
        "## Candidate Goal\n\n"
        f"- queue_key: {candidate['queue_key']}\n"
        f"- goal_id: {candidate['goal_id']}\n"
        f"- goal_type: {candidate['goal_type']}\n"
        f"- statement: {candidate['statement']}\n\n"
        "## Exact Files\n\n"
        f"{files}\n\n"
        "## Acceptance Commands\n\n"
        f"{commands}\n\n"
        "## HOLD Conditions\n\n"
        f"{hold_conditions}\n"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--output-md", required=True)
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    output_json = (repo_root / args.output_json).resolve()
    output_md = (repo_root / args.output_md).resolve()

    goal_cards = list_goal_cards(repo_root)
    goal_index = next_goal_index(goal_cards)

    latest_backlog = find_latest_backlog(repo_root)
    payload_base = {
        "schema_version": "secupilot.next_mvp_goal_candidate.v1",
        "generated_at_local": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "latest_backlog_json": latest_backlog.as_posix() if latest_backlog else None,
    }

    try:
        if latest_backlog:
            backlog_payload = read_json(latest_backlog)
            if not isinstance(backlog_payload, dict):
                raise ValueError(f"backlog is not a JSON object: {latest_backlog.as_posix()}")
            items = backlog_payload.get("items", [])
            if not isinstance(items, list):
                raise ValueError(f"backlog items is not a list: {latest_backlog.as_posix()}")
            selected = choose_open_item(items)
            if selected:
                picked = backlog_candidate(repo_root, goal_index, latest_backlog, selected)
            else:
                picked = queue_candidate(repo_root, goal_index, goal_cards)
        else:
            picked = queue_candidate(repo_root, goal_index, goal_cards)
    except Exception as exc:
        error_payload = {
            "status": "HOLD",
            "error": str(exc),
            **payload_base,
        }
        print(json.dumps(error_payload, ensure_ascii=False, indent=2))
        return HOLD

    payload = {"status": "PASS", **payload_base, **picked}
    write_json(output_json, payload)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(payload), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return PASS


if __name__ == "__main__":
    sys.exit(run())
