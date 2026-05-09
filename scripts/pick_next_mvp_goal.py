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
BACKLOG_PRE_QUEUE_MAX_RANK = PRIORITY_RANK["P2"]
BACKLOG_POST_QUEUE_MAX_RANK = PRIORITY_RANK["P3"]
BACKLOG_ITEM_ATTEMPT_LIMIT = {"P2": 2, "P3": 1}

QUEUE_ITEMS = (
    {
        "queue_key": "GOAL-ECIVFE-33_LOCAL_RULE_ENGINE",
        "goal_id": "GOAL-ECIVFE-33_LOCAL_RULE_ENGINE",
        "suffix": "LOCAL_RULE_ENGINE",
        "match": "GOAL-ECIVFE-33_LOCAL_RULE_ENGINE",
        "requires_all": ("GOAL-ECIVFE-30_FIXTURE_MODEL",),
        "goal_type": "script",
        "profile": "ECIVFE_LOCAL_RULE_ENGINE",
        "statement": "Implement the local/offline deterministic ECI/VFE fixture analyzer that consumes metadata-only fixtures and emits structured chain, forecast, and correlation artifacts.",
    },
    {
        "queue_key": "GOAL-ECIVFE-34_OUTPUT_GUARD",
        "goal_id": "GOAL-ECIVFE-34_OUTPUT_GUARD",
        "suffix": "OUTPUT_GUARD",
        "match": "GOAL-ECIVFE-34_OUTPUT_GUARD",
        "requires_all": ("GOAL-ECIVFE-30_FIXTURE_MODEL", "GOAL-ECIVFE-33_LOCAL_RULE_ENGINE"),
        "goal_type": "validator",
        "profile": "ECIVFE_OUTPUT_GUARD",
        "statement": "Implement the ECI/VFE output guard for schema validation, forbidden content scan, topology disclosure scan, prompt-injection propagation scan, and VFE query-control validation.",
    },
    {
        "queue_key": "GOAL-ECIVFE-31_CHAIN_INDICATOR_UI",
        "goal_id": "GOAL-ECIVFE-31_CHAIN_INDICATOR_UI",
        "suffix": "CHAIN_INDICATOR_UI",
        "match": "GOAL-ECIVFE-31_CHAIN_INDICATOR_UI",
        "requires_all": (
            "GOAL-ECIVFE-30_FIXTURE_MODEL",
            "GOAL-ECIVFE-33_LOCAL_RULE_ENGINE",
            "GOAL-ECIVFE-34_OUTPUT_GUARD",
        ),
        "goal_type": "page",
        "profile": "ECIVFE_CHAIN_INDICATOR_UI",
        "statement": "Render guard-passed ECI chain indicators in the incident workbench as operator-readable stage, confidence, and evidence-gap summaries without exposing raw evidence or attacker-readable details.",
    },
    {
        "queue_key": "GOAL-ECIVFE-32_FORECAST_CARD_UI",
        "goal_id": "GOAL-ECIVFE-32_FORECAST_CARD_UI",
        "suffix": "FORECAST_CARD_UI",
        "match": "GOAL-ECIVFE-32_FORECAST_CARD_UI",
        "requires_all": (
            "GOAL-ECIVFE-30_FIXTURE_MODEL",
            "GOAL-ECIVFE-33_LOCAL_RULE_ENGINE",
            "GOAL-ECIVFE-34_OUTPUT_GUARD",
            "GOAL-ECIVFE-31_CHAIN_INDICATOR_UI",
        ),
        "goal_type": "page",
        "profile": "ECIVFE_FORECAST_CARD_UI",
        "statement": "Render guard-passed VFE forecast cards as defensive summaries with urgency, collection-window guidance, and no attacker-readable attack path or topology detail.",
    },
    {
        "queue_key": "GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE",
        "goal_id": "GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE",
        "suffix": "LOCAL_REVIEW_PACKAGE",
        "match": "GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE",
        "requires_all": (
            "GOAL-ECIVFE-30_FIXTURE_MODEL",
            "GOAL-ECIVFE-33_LOCAL_RULE_ENGINE",
            "GOAL-ECIVFE-34_OUTPUT_GUARD",
            "GOAL-ECIVFE-31_CHAIN_INDICATOR_UI",
            "GOAL-ECIVFE-32_FORECAST_CARD_UI",
        ),
        "goal_type": "package",
        "profile": "ECIVFE_LOCAL_REVIEW_PACKAGE",
        "statement": "Build a self-contained local/offline ECI/VFE review package with guard scan, UI screenshots, manifest, and reviewer handoff, still fixture-only and metadata-only.",
    },
    {
        "queue_key": "GOAL-RC018_CUSTOMER_READABLE_PACKAGE",
        "suffix": "RC018_CUSTOMER_READABLE_PACKAGE",
        "match": "RC018_CUSTOMER_READABLE_PACKAGE",
        "requires_all": (
            "GOAL-ECIVFE-30_FIXTURE_MODEL",
            "GOAL-ECIVFE-33_LOCAL_RULE_ENGINE",
            "GOAL-ECIVFE-34_OUTPUT_GUARD",
            "GOAL-ECIVFE-31_CHAIN_INDICATOR_UI",
            "GOAL-ECIVFE-32_FORECAST_CARD_UI",
            "GOAL-ECIVFE-35_LOCAL_REVIEW_PACKAGE",
        ),
        "goal_type": "package",
        "profile": "RC018_CUSTOMER_READABLE_PACKAGE",
        "statement": "Build LOCAL_OFFLINE_TRIAL_RC_018_CN as a customer-readable local/offline review package that starts from the product path, not raw artifact tables.",
    },
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
    {
        "queue_key": "GOAL-MVP-95_PRIVATE_PREVIEW_LAUNCH_SHELL",
        "suffix": "PRIVATE_PREVIEW_LAUNCH_SHELL",
        "match": "PRIVATE_PREVIEW_LAUNCH_SHELL",
        "goal_type": "script",
        "profile": "PRIVATE_PREVIEW_LAUNCH_SHELL",
        "statement": "Refresh the private-preview launch shell so RC-019 opens as a product preview entry with current package paths, local-only boundaries, and check-only verification.",
    },
    {
        "queue_key": "GOAL-MVP-96_PRIVATE_PREVIEW_ROUTE_MAP_INDEX",
        "suffix": "PRIVATE_PREVIEW_ROUTE_MAP_INDEX",
        "match": "PRIVATE_PREVIEW_ROUTE_MAP_INDEX",
        "goal_type": "test-report",
        "profile": "PRIVATE_PREVIEW_ROUTE_MAP_INDEX",
        "statement": "Generate a product route-map index from the latest private preview package so reviewers see journeys and pages instead of evidence-package internals.",
    },
    {
        "queue_key": "GOAL-MVP-97_PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW",
        "suffix": "PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW",
        "match": "PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW",
        "goal_type": "page",
        "profile": "PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW",
        "statement": "Add a customer-readable private preview task flow that guides engineer, manager, and CTO users through the product without exposing debug fixtures.",
    },
    {
        "queue_key": "GOAL-MVP-98_PRIVATE_PREVIEW_RC_PACKAGE_REFRESH",
        "suffix": "PRIVATE_PREVIEW_RC_PACKAGE_REFRESH",
        "match": "PRIVATE_PREVIEW_RC_PACKAGE_REFRESH",
        "goal_type": "package",
        "profile": "PRIVATE_PREVIEW_RC_PACKAGE_REFRESH",
        "statement": "Refresh the local/private preview RC package after product route-map changes, including validators, screenshots, consistency checks, and zip manifest.",
    },
    {
        "queue_key": "GOAL-MVP-101_PRIVATE_PREVIEW_HEALTHCHECK",
        "suffix": "PRIVATE_PREVIEW_HEALTHCHECK",
        "match": "PRIVATE_PREVIEW_HEALTHCHECK",
        "goal_type": "validator",
        "profile": "PRIVATE_PREVIEW_HEALTHCHECK",
        "statement": "Add a private-preview healthcheck that verifies the local package, launch metadata, route map, and local-only boundaries before reviewers open the trial.",
    },
    {
        "queue_key": "GOAL-MVP-102_HOME_TO_INCIDENT_E2E_SMOKE",
        "suffix": "HOME_TO_INCIDENT_E2E_SMOKE",
        "match": "HOME_TO_INCIDENT_E2E_SMOKE",
        "goal_type": "page",
        "profile": "HOME_TO_INCIDENT_E2E_SMOKE",
        "statement": "Add a product-path smoke test proving a reviewer can move from the customer-first home to the incident workbench without seeing debug fixtures.",
    },
    {
        "queue_key": "GOAL-MVP-103_CUSTOMER_TASK_FLOW_REPORT",
        "suffix": "CUSTOMER_TASK_FLOW_REPORT",
        "match": "CUSTOMER_TASK_FLOW_REPORT",
        "goal_type": "test-report",
        "profile": "CUSTOMER_TASK_FLOW_REPORT",
        "statement": "Generate a customer task-flow report that lists engineer, manager, and CTO journeys, expected actions, and current PASS/HOLD state.",
    },
    {
        "queue_key": "GOAL-MVP-104_FEEDBACK_TO_BACKLOG_SYNC",
        "suffix": "FEEDBACK_TO_BACKLOG_SYNC",
        "match": "FEEDBACK_TO_BACKLOG_SYNC",
        "goal_type": "script",
        "profile": "FEEDBACK_TO_BACKLOG_SYNC",
        "statement": "Sync local reviewer feedback into a prioritized product backlog and action list so notes do not remain trapped in review text.",
    },
    {
        "queue_key": "GOAL-MVP-105_PRIVATE_DEPLOY_PRECHECK_REPORT",
        "suffix": "PRIVATE_DEPLOY_PRECHECK_REPORT",
        "match": "PRIVATE_DEPLOY_PRECHECK_REPORT",
        "goal_type": "test-report",
        "profile": "PRIVATE_DEPLOY_PRECHECK_REPORT",
        "statement": "Generate a Windows/local private-deployment precheck report from the dry precheck script without deploying or touching customer systems.",
    },
    {
        "queue_key": "GOAL-MVP-106_QWEN_DRY_ERROR_STATE_UI",
        "suffix": "QWEN_DRY_ERROR_STATE_UI",
        "match": "QWEN_DRY_ERROR_STATE_UI",
        "goal_type": "page",
        "profile": "QWEN_DRY_ERROR_STATE_UI",
        "statement": "Add product-readable dry model timeout, fallback, and error states in the UI without any live Qwen call or API key.",
    },
    {
        "queue_key": "GOAL-MVP-107_TRIAL_SCREENSHOT_PACKAGE_BUILDER",
        "suffix": "TRIAL_SCREENSHOT_PACKAGE_BUILDER",
        "match": "TRIAL_SCREENSHOT_PACKAGE_BUILDER",
        "goal_type": "package",
        "profile": "TRIAL_SCREENSHOT_PACKAGE_BUILDER",
        "statement": "Build a reviewer screenshot package from current product routes with screenshot safety validation and a small index.",
    },
    {
        "queue_key": "GOAL-MVP-108_PRODUCT_COPY_BOUNDARY_SCANNER",
        "suffix": "PRODUCT_COPY_BOUNDARY_SCANNER",
        "match": "PRODUCT_COPY_BOUNDARY_SCANNER",
        "goal_type": "validator",
        "profile": "PRODUCT_COPY_BOUNDARY_SCANNER",
        "statement": "Add a product-copy boundary scanner that catches debug labels, stale RC wording, secrets, and unauthorized launch language in reviewer-facing text.",
    },
    {
        "queue_key": "GOAL-MVP-109_RC_REVIEW_HANDOFF_AUTOBUILDER",
        "suffix": "RC_REVIEW_HANDOFF_AUTOBUILDER",
        "match": "RC_REVIEW_HANDOFF_AUTOBUILDER",
        "goal_type": "package",
        "profile": "RC_REVIEW_HANDOFF_AUTOBUILDER",
        "statement": "Generate an RC review handoff package that combines route screenshots, safety scans, decision template, and product checklist.",
    },
    {
        "queue_key": "GOAL-MVP-110_WINDOWS_START_STOP_SCRIPT_VALIDATOR",
        "suffix": "WINDOWS_START_STOP_SCRIPT_VALIDATOR",
        "match": "WINDOWS_START_STOP_SCRIPT_VALIDATOR",
        "goal_type": "validator",
        "profile": "WINDOWS_START_STOP_SCRIPT_VALIDATOR",
        "statement": "Validate Windows local start and stop scripts in dry-run mode so private-preview operators get clear launch and shutdown instructions.",
    },
    {
        "queue_key": "GOAL-MVP-111_CUSTOMER_README_PRODUCT_COPY_REFRESH",
        "suffix": "CUSTOMER_README_PRODUCT_COPY_REFRESH",
        "match": "CUSTOMER_README_PRODUCT_COPY_REFRESH",
        "goal_type": "script",
        "profile": "CUSTOMER_README_PRODUCT_COPY_REFRESH",
        "statement": "Refresh the customer trial README and START_HERE copy so it reads as a product preview, not an evidence package.",
    },
    {
        "queue_key": "GOAL-MVP-112_PRODUCT_BACKLOG_PRIORITIZER",
        "suffix": "PRODUCT_BACKLOG_PRIORITIZER",
        "match": "PRODUCT_BACKLOG_PRIORITIZER",
        "goal_type": "script",
        "profile": "PRODUCT_BACKLOG_PRIORITIZER",
        "statement": "Add a backlog prioritizer that ranks reviewer notes by product impact, customer-visible risk, and implementation size.",
    },
    {
        "queue_key": "GOAL-MVP-113_CLOUD_MODEL_LATENCY_REPORT",
        "suffix": "CLOUD_MODEL_LATENCY_REPORT",
        "match": "CLOUD_MODEL_LATENCY_REPORT",
        "goal_type": "test-report",
        "profile": "CLOUD_MODEL_LATENCY_REPORT",
        "statement": "Generate a dry cloud-model latency and fallback report from mock timings and configured sentinels without any network call.",
    },
    {
        "queue_key": "GOAL-MVP-114_PRIVATE_PREVIEW_ROUTE_COVERAGE_REPORT",
        "suffix": "PRIVATE_PREVIEW_ROUTE_COVERAGE_REPORT",
        "match": "PRIVATE_PREVIEW_ROUTE_COVERAGE_REPORT",
        "goal_type": "test-report",
        "profile": "PRIVATE_PREVIEW_ROUTE_COVERAGE_REPORT",
        "statement": "Generate a route coverage report showing which product paths have desktop/mobile screenshots, tests, and reviewer-ready handoff evidence.",
    },
    {
        "queue_key": "GOAL-MVP-115_INCIDENT_WORKBENCH_RC_PACKAGE",
        "suffix": "INCIDENT_WORKBENCH_RC_PACKAGE",
        "match": "INCIDENT_WORKBENCH_RC_PACKAGE",
        "goal_type": "package",
        "profile": "INCIDENT_WORKBENCH_RC_PACKAGE",
        "statement": "Package the incident workbench UX evidence for the next local RC with first-load, expanded evidence, technical reconciliation, and mobile screenshots.",
    },
)

PRODUCT_ACCELERATION_RESET_MARKERS = ("PRIVATE_PREVIEW_SHELL_ROUTE_MAP",)
LEGACY_QUEUE_MATCHES = {
    "RC016_SCREENSHOT_EXPECTED_CANDIDATE",
    "ZIP_TAMPER_NEGATIVE_TEST",
    "PRODUCT_ACCELERATION_POOL_PICKER",
    "CLIENT_TRIAL_HOME_PRODUCTIZATION",
    "LOCAL_OFFLINE_TRIAL_REPORT",
    "RC_PACKAGE_SELF_REVIEW_REPORT",
    "ROLE_BASED_TRIAL_HOME",
    "INCIDENT_DETAIL_PRODUCT_PAGE",
    "RECOMMENDED_ACTION_CARDS",
    "USER_FEEDBACK_LOOP",
    "QWEN_DRY_PROVIDER_UI",
    "QWEN_CLOUD_CONTRACT_MOCK",
    "PRIVATE_DEPLOY_PACKAGE_STRUCTURE",
    "CUSTOMER_TRIAL_README_AND_LAUNCHER",
    "INTERNAL_TRIAL_KPI_REPORT",
}


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
    return sorted(repo_root.glob("docs/goals/GOAL-*.md"))


def next_goal_index(goal_cards: list[Path]) -> int:
    max_index = 0
    pattern = re.compile(r"GOAL-MVP-(\d+)_")
    for path in goal_cards:
        match = pattern.search(path.stem.upper())
        if match:
            max_index = max(max_index, int(match.group(1)))
    return max_index + 1 if max_index else 1


def backlog_item_token(item: dict[str, Any]) -> str:
    item_id = str(item.get("id", "UNKNOWN")).upper()
    return item_id.replace("-", "_")


def backlog_attempt_count(goal_cards: list[Path], item: dict[str, Any]) -> int:
    token = backlog_item_token(item)
    return sum(1 for path in goal_cards if token in path.stem.upper())


def backlog_item_can_preempt(item: dict[str, Any], goal_cards: list[Path], max_rank: int) -> bool:
    priority = str(item.get("priority", "P3")).upper()
    rank = PRIORITY_RANK.get(priority, 99)
    if rank > max_rank:
        return False
    limit = BACKLOG_ITEM_ATTEMPT_LIMIT.get(priority)
    if limit is None:
        return True
    return backlog_attempt_count(goal_cards, item) < limit


def choose_open_item(
    items: list[dict[str, Any]],
    goal_cards: list[Path],
    *,
    max_rank: int = BACKLOG_PRE_QUEUE_MAX_RANK,
) -> dict[str, Any] | None:
    open_items = []
    for item in items:
        status = str(item.get("status", "")).upper()
        if status in OPEN_STATUSES and backlog_item_can_preempt(item, goal_cards, max_rank):
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


def private_preview_pool_contract(profile: str, goal_card: str, closeout: str) -> dict[str, Any] | None:
    if profile == "PRIVATE_PREVIEW_HEALTHCHECK":
        report_json = "artifacts/private_preview/healthcheck/local-offline-trial-rc-020-healthcheck.json"
        return {
            "goal_type": "validator",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/check_private_preview_health.py",
                "backend/tests/test_check_private_preview_health.py",
                report_json,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_check_private_preview_health",
                f"py -3 scripts/check_private_preview_health.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review --route-map artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json --output-json {report_json} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "healthcheck cannot find package, route map, launch metadata, or local-only boundary text",
                "healthcheck reports live Qwen/API, connector, production write-back, customer-visible deploy, or secret exposure",
                "unit test or healthcheck command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "HOME_TO_INCIDENT_E2E_SMOKE":
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/App.tsx",
                "frontend/src/App.css",
                "frontend/src/App.test.tsx",
                "frontend/tests/e2e/private-preview-product-path.spec.ts",
                "artifacts/product_experience/private_preview_path/home-to-incident-desktop.png",
                "artifacts/product_experience/private_preview_path/home-to-incident-mobile.png",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/private-preview-product-path.spec.ts",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "home-to-incident path exposes P1/P2/P3, Mock Fixture, Expert Mode, or stale RC wording",
                "route path does not let engineer, manager, and CTO users reach the incident workbench",
                "frontend unit/build/playwright fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "CUSTOMER_TASK_FLOW_REPORT":
        report_md = "artifacts/product_reports/customer_task_flow_report.md"
        report_json = "artifacts/product_reports/customer_task_flow_report.json"
        return {
            "goal_type": "test-report",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_customer_task_flow_report.py",
                "backend/tests/test_build_customer_task_flow_report.py",
                report_md,
                report_json,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_customer_task_flow_report",
                f"py -3 scripts/build_customer_task_flow_report.py --route-map artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json --output-md {report_md} --output-json {report_json} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "report omits engineer, manager, or CTO journey",
                "report reads like artifact inventory rather than product tasks and expected user actions",
                "report grants live Qwen/API, deploy, connector, production write-back, or customer-visible launch authority",
                "unit test or report command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "FEEDBACK_TO_BACKLOG_SYNC":
        output_json = "artifacts/product_backlog/private-preview/feedback_backlog_sync.json"
        output_md = "artifacts/product_backlog/private-preview/feedback_backlog_sync.md"
        return {
            "goal_type": "script",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/sync_feedback_to_product_backlog.py",
                "backend/tests/test_sync_feedback_to_product_backlog.py",
                output_json,
                output_md,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_sync_feedback_to_product_backlog",
                f"py -3 scripts/sync_feedback_to_product_backlog.py --feedback-root artifacts/product_backlog --output-json {output_json} --output-md {output_md} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "sync fabricates reviewer decisions or claims customer usage that did not happen",
                "output omits source feedback references or priority reasoning",
                "script command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "PRIVATE_DEPLOY_PRECHECK_REPORT":
        report_md = "artifacts/private_deployment/precheck/private_deployment_precheck_report.md"
        report_json = "artifacts/private_deployment/precheck/private_deployment_precheck_report.json"
        return {
            "goal_type": "test-report",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/private_deployment_precheck.ps1",
                "scripts/build_private_deployment_precheck_report.py",
                "backend/tests/test_build_private_deployment_precheck_report.py",
                report_md,
                report_json,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_private_deployment_precheck_report",
                "powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/private_deployment_precheck.ps1 -DryRun -OutputJson artifacts/private_deployment/precheck/precheck_raw.json",
                f"py -3 scripts/build_private_deployment_precheck_report.py --input-json artifacts/private_deployment/precheck/precheck_raw.json --output-md {report_md} --output-json {report_json} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "precheck attempts installation, deployment, network access, or customer-system mutation",
                "report omits Windows prerequisites, resource sizing, or model-provider path",
                "PowerShell or report command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "QWEN_DRY_ERROR_STATE_UI":
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/App.tsx",
                "frontend/src/App.css",
                "frontend/src/App.test.tsx",
                "frontend/tests/e2e/incident-product-page.spec.ts",
                "artifacts/product_experience/qwen_dry_error_states/incident-product-error-state.png",
                "artifacts/product_experience/qwen_dry_error_states/incident-product-error-state.text.json",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/incident-product-page.spec.ts",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "UI implies live Qwen/API call, API key entry, connector access, or autonomous action",
                "error state is technical stack trace rather than operator-readable fallback guidance",
                "frontend unit/build/playwright fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "TRIAL_SCREENSHOT_PACKAGE_BUILDER":
        package_dir = "artifacts/product_screenshot_packages/local-offline-trial-rc-020"
        return {
            "goal_type": "package",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_product_screenshot_package.py",
                "backend/tests/test_build_product_screenshot_package.py",
                package_dir,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_product_screenshot_package",
                f"py -3 scripts/build_product_screenshot_package.py --screenshot-root artifacts/product_experience --output-dir {package_dir} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "package includes screenshots with P1/P2/P3, Mock Fixture, Expert Mode, stale RC wording, or secrets",
                "package omits index, route labels, or screenshot safety status",
                "unit test or package command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "PRODUCT_COPY_BOUNDARY_SCANNER":
        scan_json = "artifacts/product_copy_boundary/product_copy_boundary_scan.json"
        return {
            "goal_type": "validator",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/scan_product_copy_boundaries.py",
                "backend/tests/test_scan_product_copy_boundaries.py",
                scan_json,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_scan_product_copy_boundaries",
                f"py -3 scripts/scan_product_copy_boundaries.py --paths frontend/src artifacts/product_experience docs/goals --output-json {scan_json} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "scanner misses seeded P1/P2/P3, Mock Fixture, Expert Mode, secret, token, or production launch language",
                "scanner blocks only on historical non-reviewer evidence outside configured paths",
                "unit test or scanner command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "RC_REVIEW_HANDOFF_AUTOBUILDER":
        package_dir = "artifacts/reviews/local_rc_handoff/rc-021"
        return {
            "goal_type": "package",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_rc_review_handoff.py",
                "backend/tests/test_build_rc_review_handoff.py",
                package_dir,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_rc_review_handoff",
                f"py -3 scripts/build_rc_review_handoff.py --candidate LOCAL_OFFLINE_TRIAL_RC_021_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --screenshot-root artifacts/product_experience --output-dir {package_dir} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "handoff package omits review prompt, screenshots, safety scan, decision template, or checklist",
                "handoff package grants live API, connector, production write-back, customer-visible deploy, or external pilot authority",
                "unit test or handoff command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "WINDOWS_START_STOP_SCRIPT_VALIDATOR":
        result_json = "artifacts/private_preview/windows_start_stop_validation.json"
        return {
            "goal_type": "validator",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/validate_windows_private_preview_scripts.py",
                "backend/tests/test_validate_windows_private_preview_scripts.py",
                "scripts/launch_customer_trial_local.ps1",
                "scripts/stop_customer_trial_local.ps1",
                result_json,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_validate_windows_private_preview_scripts",
                f"py -3 scripts/validate_windows_private_preview_scripts.py --launch-script scripts/launch_customer_trial_local.ps1 --stop-script scripts/stop_customer_trial_local.ps1 --output-json {result_json} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "validator allows public tunnel, deploy, service install, live API, connector, or production write-back commands",
                "launch/stop scripts omit dry-run, local-only, or stop instructions",
                "unit test or validator command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "CUSTOMER_README_PRODUCT_COPY_REFRESH":
        scan_json = "artifacts/product_copy_boundary/customer_readme_boundary_scan.json"
        return {
            "goal_type": "script",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "artifacts/private_trial_package/README_中文.md",
                "artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review/REVIEWER_START_HERE_中文.md",
                "scripts/scan_product_copy_boundaries.py",
                scan_json,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                f"py -3 scripts/scan_product_copy_boundaries.py --paths artifacts/private_trial_package/README_中文.md artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review/REVIEWER_START_HERE_中文.md --output-json {scan_json} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "README copy reads like evidence reconciliation instead of product preview instructions",
                "copy grants customer-visible deploy, live API, connector, production write-back, or external pilot authority",
                "copy scanner finds stale RC wording, debug labels, secrets, or unauthorized launch language",
                "scope expands beyond listed files",
            ],
        }
    if profile == "PRODUCT_BACKLOG_PRIORITIZER":
        output_json = "artifacts/product_backlog/private-preview/prioritized_backlog.json"
        output_md = "artifacts/product_backlog/private-preview/prioritized_backlog.md"
        return {
            "goal_type": "script",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/prioritize_product_backlog.py",
                "backend/tests/test_prioritize_product_backlog.py",
                output_json,
                output_md,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_prioritize_product_backlog",
                f"py -3 scripts/prioritize_product_backlog.py --backlog-root artifacts/product_backlog --output-json {output_json} --output-md {output_md} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "prioritizer drops source references or invents reviewer decisions",
                "output lacks product impact, customer-visible risk, or implementation-size rationale",
                "unit test or prioritizer command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "CLOUD_MODEL_LATENCY_REPORT":
        report_md = "artifacts/model_contract/cloud_model_latency_report.md"
        report_json = "artifacts/model_contract/cloud_model_latency_report.json"
        return {
            "goal_type": "test-report",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_cloud_model_latency_report.py",
                "backend/tests/test_build_cloud_model_latency_report.py",
                report_md,
                report_json,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_cloud_model_latency_report",
                f"py -3 scripts/build_cloud_model_latency_report.py --config artifacts/qwen_live_synthetic/config_validation.json --output-md {report_md} --output-json {report_json} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "report requires API key, network access, live Qwen call, or connector output",
                "report omits timeout, retry, fallback, and user-facing error state",
                "unit test or report command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "PRIVATE_PREVIEW_ROUTE_COVERAGE_REPORT":
        report_md = "artifacts/product_reports/private_preview_route_coverage.md"
        report_json = "artifacts/product_reports/private_preview_route_coverage.json"
        return {
            "goal_type": "test-report",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_private_preview_route_coverage_report.py",
                "backend/tests/test_build_private_preview_route_coverage_report.py",
                report_md,
                report_json,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_private_preview_route_coverage_report",
                f"py -3 scripts/build_private_preview_route_coverage_report.py --screenshot-root artifacts/product_experience --goal-root docs/goals --output-md {report_md} --output-json {report_json} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "report omits product home, incident workbench, trial entry, or model-readiness route",
                "report treats missing screenshots or tests as PASS",
                "unit test or report command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "INCIDENT_WORKBENCH_RC_PACKAGE":
        package_dir = "artifacts/reviews/incident_workbench_rc/rc-017"
        return {
            "goal_type": "package",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_incident_workbench_review_package.py",
                "backend/tests/test_build_incident_workbench_review_package.py",
                package_dir,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_incident_workbench_review_package",
                f"py -3 scripts/build_incident_workbench_review_package.py --candidate RC-017 --screenshot-root artifacts/product_experience/ux03 --decision-doc docs/S6_RC016_UX02_INCIDENT_AI_ADVICE_REVIEW_DECISION_2026_05_08.md --output-dir {package_dir} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "package omits first-load, expanded evidence, technical reconciliation, or mobile screenshot evidence",
                "package includes debug controls, stale RC wording, secrets, live API, connector, production write-back, or deploy language",
                "unit test or package command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    return None


def profile_contract(
    profile: str,
    goal_id: str,
    date_tag: str,
    backlog_path: str | None,
) -> dict[str, Any]:
    goal_card = f"docs/goals/{goal_id}.md"
    closeout = f"docs/S6_FAST_MVP_{goal_id.replace('-', '_')}_{date_tag}.md"
    private_preview_contract = private_preview_pool_contract(profile, goal_card, closeout)
    if private_preview_contract:
        return private_preview_contract
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
    if profile == "PRIVATE_PREVIEW_LAUNCH_SHELL":
        return {
            "goal_type": "script",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/launch_s1_local_offline_trial.ps1",
                "backend/tests/test_s1_local_offline_launcher_contract.py",
                "artifacts/local_trial_launches/local-offline-trial-rc-019/launch_info.json",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_s1_local_offline_launcher_contract",
                "powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/launch_s1_local_offline_trial.ps1 -PackageDir artifacts\\local_demo_packages\\local-offline-trial-rc-019-cn-review -DeliveryDir artifacts\\local_trial_packages\\local-offline-trial-rc-006 -Route /s1-trial -CheckOnly -SkipBuild -NoServer",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "launcher references RC-006 or RC-004 as the current candidate",
                "launcher starts a server, opens a browser, deploys, or calls live Qwen/API/connectors during check-only verification",
                "launcher omits local-only, no-writeback, no-customer-visible, or stop instructions",
                "unit test or check-only command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "ECIVFE_LOCAL_RULE_ENGINE":
        run_dir = "artifacts/eci_vfe_fixture_runs/rc001"
        return {
            "goal_type": "script",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/eci_vfe_fixture_analyze.py",
                "backend/tests/test_eci_vfe_fixture_analyze.py",
                f"{run_dir}/chain_assessment.json",
                f"{run_dir}/forecast_candidates.json",
                f"{run_dir}/correlation_result.json",
                f"{run_dir}/run_record.json",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                f"py -3 scripts/eci_vfe_fixture_analyze.py --fixture-dir mock_data\\eci_vfe --output {run_dir}",
                "py -3 -m pytest backend\\tests\\test_eci_vfe_fixture_analyze.py",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "semantic similarity alone upgrades a case",
                "high-stage label is emitted below the required threshold without suspected-state downgrade",
                "evidence_gaps omit urgency, window_closes_in, deadline_basis, or fallback_if_missed",
                "output contains raw prompt-injection text",
                "VFE query_context is missing or loses audit-required non-bulk controls",
                "script requires live Qwen/API/connectors, network access, secret, or API key",
                "scope expands beyond listed files",
            ],
        }
    if profile == "ECIVFE_OUTPUT_GUARD":
        run_dir = "artifacts/eci_vfe_fixture_runs/rc001"
        guard_scan = f"{run_dir}/output_guard_scan.json"
        return {
            "goal_type": "validator",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/validate_eci_vfe_output.py",
                "backend/tests/test_validate_eci_vfe_output.py",
                guard_scan,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                f"py -3 scripts/validate_eci_vfe_output.py --input {run_dir}",
                "py -3 -m pytest backend\\tests\\test_validate_eci_vfe_output.py",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "output_guard_scan.json is missing or not PASS",
                "schema-invalid output passes",
                "forbidden content passes",
                "private CIDR plus reachability plus port/control semantics passes",
                "bulk_export=true passes",
                "prompt injection text propagates into narrative, watch_for, or remediation",
                "scope expands beyond listed files",
            ],
        }
    if profile == "ECIVFE_CHAIN_INDICATOR_UI":
        screenshots_dir = "artifacts/eci_vfe_fixture_runs/rc001/screenshots"
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/eciVfe/EciChainIndicator.tsx",
                "frontend/src/secupilot/eciVfe/EciEvidenceGapPanel.tsx",
                "frontend/src/secupilot/eciVfe/eciVfeUiModel.ts",
                "frontend/src/secupilot/eciVfe/eciVfeUi.test.tsx",
                "frontend/src/App.tsx",
                "frontend/tests/e2e/eci-vfe-chain-indicator.spec.ts",
                f"{screenshots_dir}/eci-chain-indicator-desktop.png",
                f"{screenshots_dir}/eci-chain-indicator-mobile.png",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- --run eciVfe",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/eci-vfe-chain-indicator.spec.ts",
                f"py -3 scripts/validate_review_screenshots.py --screenshot-dir {screenshots_dir}",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "UI renders ECI output before output_guard_scan.json is PASS",
                "UI exposes raw evidence, raw logs, PoC, exploit steps, payload, credentials, token, auth header, or attacker-readable topology",
                "semantic similarity alone upgrades a case or changes the recommended action",
                "high-stage ECI labels appear without stricter confidence or suspected-state downgrade",
                "evidence gaps omit urgency or collection-window guidance",
                "screenshot safety scan finds P1/P2/P3, Mock Fixture, Expert Mode, stale RC wording, or forbidden content",
                "scope expands beyond listed files",
            ],
        }
    if profile == "ECIVFE_FORECAST_CARD_UI":
        screenshots_dir = "artifacts/eci_vfe_fixture_runs/rc001/screenshots"
        return {
            "goal_type": "page",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "frontend/src/secupilot/eciVfe/VfeForecastCard.tsx",
                "frontend/src/secupilot/eciVfe/eciVfeUiModel.ts",
                "frontend/src/secupilot/eciVfe/eciVfeUi.test.tsx",
                "frontend/src/App.tsx",
                "frontend/tests/e2e/eci-vfe-forecast-card.spec.ts",
                f"{screenshots_dir}/vfe-forecast-card-desktop.png",
                f"{screenshots_dir}/vfe-forecast-card-mobile.png",
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- --run eciVfe",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npm run test:e2e -- tests/e2e/eci-vfe-forecast-card.spec.ts",
                f"py -3 scripts/validate_review_screenshots.py --screenshot-dir {screenshots_dir}",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "VFE card renders before schema validation and output guard PASS",
                "VFE card exposes attacker-readable attack_path, exploit steps, PoC, payload, raw logs, credentials, auth headers, or internal topology reachability",
                "VFE forecast independently upgrades a case or authorizes containment/remediation",
                "attack_path_defensive_summary is missing or replaced by attacker-readable wording",
                "evidence_gaps omit urgency, collection window, deadline basis, or fallback guidance",
                "screenshot safety scan finds P1/P2/P3, Mock Fixture, Expert Mode, stale RC wording, or forbidden content",
                "scope expands beyond listed files",
            ],
        }
    if profile == "ECIVFE_LOCAL_REVIEW_PACKAGE":
        package_dir = "artifacts/local_demo_packages/eci-vfe-local-offline-rc-001"
        zip_path = "artifacts/local_demo_packages/eci-vfe-local-offline-rc-001-review-package.zip"
        return {
            "goal_type": "package",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/package_eci_vfe_local_review.py",
                "backend/tests/test_package_eci_vfe_local_review.py",
                f"{package_dir}/REVIEWER_START_HERE_中文.md",
                f"{package_dir}/package_manifest.json",
                f"{package_dir}/output_guard_scan.json",
                f"{package_dir}/chain_assessment.json",
                f"{package_dir}/forecast_candidates.json",
                f"{package_dir}/correlation_result.json",
                f"{package_dir}/SCREENSHOT_INDEX_中文.json",
                zip_path,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m pytest backend\\tests\\test_package_eci_vfe_local_review.py",
                f"py -3 scripts/package_eci_vfe_local_review.py --run-dir artifacts\\eci_vfe_fixture_runs\\rc001 --output-dir {package_dir} --zip-output {zip_path}",
                f"py -3 scripts/validate_local_trial_rc_consistency.py --package-dir {package_dir} --expected-candidate ECI_VFE_LOCAL_OFFLINE_RC_001",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "package includes raw evidence, raw logs, PoC, exploit steps, payload, credentials, token, auth header, action command, or attacker-readable topology",
                "package includes ECI/VFE output that did not pass output guard",
                "package implies real data, live Qwen/API/connectors, production write-back, customer-visible deploy, or autonomous remediation",
                "package manifest omits SHA256, bytes, safety class, or screenshot index entries",
                "candidate/source/package path wording is inconsistent",
                "scope expands beyond listed files",
            ],
        }
    if profile == "RC018_CUSTOMER_READABLE_PACKAGE":
        package_dir = "artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review"
        zip_path = "artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-package-20260509.zip"
        consistency = "artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-consistency-check.json"
        screenshot_scan = "artifacts/local_demo_packages/local-offline-trial-rc-018-cn-review-screenshot-safety-scan.json"
        return {
            "goal_type": "package",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_rc018_customer_review_package.py",
                "backend/tests/test_build_rc018_customer_review_package.py",
                f"{package_dir}/REVIEWER_START_HERE_中文.md",
                f"{package_dir}/01_REVIEW_PROMPT.md",
                f"{package_dir}/02_PRODUCT_ROUTE_MAP_中文.md",
                f"{package_dir}/03_REVIEWER_CHECKLIST_中文.md",
                f"{package_dir}/04_FEEDBACK_TEMPLATE_中文.md",
                f"{package_dir}/package_manifest.json",
                f"{package_dir}/SCREENSHOT_INDEX_中文.json",
                f"{package_dir}/safety_scan.json",
                f"{package_dir}/eci_vfe/output_guard_scan.json",
                f"{package_dir}/eci_vfe/chain_assessment_summary.json",
                f"{package_dir}/eci_vfe/forecast_candidate_summary.json",
                zip_path,
                f"{zip_path}.outer_zip_manifest.json",
                consistency,
                screenshot_scan,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_rc018_customer_review_package",
                f"py -3 scripts/build_rc018_customer_review_package.py --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --output-dir {package_dir} --zip-path {zip_path} --repo-root .",
                f"py -3 scripts/validate_review_screenshots.py --screenshot-dir {package_dir}/screenshots --output-json {screenshot_scan}",
                f"py -3 scripts/validate_local_trial_rc_consistency.py --package-dir {package_dir} --candidate LOCAL_OFFLINE_TRIAL_RC_018_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_017_CN --zip-name local-offline-trial-rc-018-cn-review-package-20260509.zip --zip-path {zip_path} --output-json {consistency}",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "package starts from artifact tables instead of product route map",
                "required customer-path screenshots are missing",
                "ECI/VFE appears as standalone technical route instead of product explanation",
                "package or screenshots expose P1/P2/P3, Mock Fixture, Expert Mode, provider/stub/dry-run language, stale RC wording, raw payloads, secrets, auth headers, PoC, exploit steps, or attacker-readable topology",
                "output_guard_scan.json is missing, not PASS, or has blocking findings",
                "VFE output exposes attacker-readable attack_path instead of defensive summary",
                "manifest, screenshot safety scan, RC consistency, or outer zip manifest reports blocking findings",
                "package grants real data, live Qwen/API/connectors, production write-back, customer-visible deploy/publish/output, external pilot, production launch, or autonomous action authority",
                "scope expands beyond listed files",
            ],
        }
    if profile == "PRIVATE_PREVIEW_ROUTE_MAP_INDEX":
        report_path = "artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.md"
        report_json = "artifacts/product_route_maps/local-offline-trial-rc-019-cn-review/route_map_index.json"
        return {
            "goal_type": "test-report",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                "scripts/build_private_preview_route_map_index.py",
                "backend/tests/test_build_private_preview_route_map_index.py",
                report_path,
                report_json,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "py -3 -m unittest backend.tests.test_build_private_preview_route_map_index",
                f"py -3 scripts/build_private_preview_route_map_index.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review --output-md {report_path} --output-json {report_json} --repo-root .",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "route map index is dominated by artifact file tables instead of product journeys",
                "route map grants customer-visible deploy, live Qwen/API, connector, or production write-back authority",
                "report omits engineer, manager, or CTO route coverage",
                "unit test or report command fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "PRIVATE_PREVIEW_CUSTOMER_TASK_FLOW":
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
                "customer task flow exposes P1/P2/P3, Mock Fixture, Expert Mode, or stale RC wording",
                "first screen is dominated by evidence paths instead of product tasks and next actions",
                "engineer, manager, or CTO path is missing",
                "frontend unit/build/playwright fails twice in the same way",
                "scope expands beyond listed files",
            ],
        }
    if profile == "PRIVATE_PREVIEW_RC_PACKAGE_REFRESH":
        package_dir = "artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review"
        zip_path = "artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip"
        consistency = "artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-consistency-check.json"
        screenshot_scan = "artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json"
        return {
            "goal_type": "package",
            "goal_card_path": goal_card,
            "closeout_path": closeout,
            "exact_files": [
                goal_card,
                package_dir,
                zip_path,
                f"{zip_path}.outer_zip_manifest.json",
                consistency,
                screenshot_scan,
                closeout,
            ],
            "acceptance_commands": [
                f"py -3 scripts/validate_codex_goal_card.py {goal_card}",
                "Set-Location -LiteralPath frontend; npm run test -- src/App.test.tsx",
                "Set-Location -LiteralPath frontend; npm run build",
                "Set-Location -LiteralPath frontend; npx playwright test tests/e2e/s1-artifact-viewer.spec.ts tests/e2e/s1-artifact-viewer.visual.spec.ts",
                "py -3 scripts/validate_review_screenshots.py --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --expected-candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --output-json artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json",
                "py -3 scripts/build_local_offline_trial_rc.py --candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_019_CN --source-package artifacts/local_demo_packages/local-offline-trial-rc-019-cn-review --screenshot-dir artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright --output-dir artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review --zip-path artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip --repo-root . --screenshot-safety-scan artifacts/s1_closed_shadow_runs/2026-04-30-001/playwright/screenshot_safety_scan.json --outer-zip-manifest artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip.outer_zip_manifest.json",
                "py -3 scripts/validate_local_trial_rc_consistency.py --package-dir artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review --candidate LOCAL_OFFLINE_TRIAL_RC_020_CN --source-candidate LOCAL_OFFLINE_TRIAL_RC_019_CN --zip-name local-offline-trial-rc-020-cn-review-package-20260508.zip --zip-path artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-package-20260508.zip --output-json artifacts/local_demo_packages/local-offline-trial-rc-020-cn-review-consistency-check.json",
                "git -c core.quotepath=false diff --check",
            ],
            "hold_conditions": [
                "package or screenshots contain stale RC-019-as-current after RC-020 refresh",
                "manifest, screenshot safety, RC consistency, or outer zip manifest reports blocking findings",
                "package grants customer-visible deploy, live Qwen/API, connector, or production write-back authority",
                "frontend/package command fails twice in the same way",
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
    product_lane_reset_seen = any(
        reset_marker in name
        for reset_marker in PRODUCT_ACCELERATION_RESET_MARKERS
        for name in existing_names
    )
    for item in QUEUE_ITEMS:
        required_matches = tuple(item.get("requires_all", ()))
        if required_matches and not all(
            any(required_match in name for name in existing_names) for required_match in required_matches
        ):
            continue
        if product_lane_reset_seen and item["match"] in LEGACY_QUEUE_MATCHES:
            continue
        if any(item["match"] in name for name in existing_names):
            continue
        goal_id = str(item.get("goal_id") or f"GOAL-MVP-{goal_index:02d}_{item['suffix']}")
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
            selected = choose_open_item(items, goal_cards)
            if selected:
                picked = backlog_candidate(repo_root, goal_index, latest_backlog, selected)
            else:
                picked = queue_candidate(repo_root, goal_index, goal_cards)
                if picked["candidate_goal"]["queue_key"] == "QUEUE_EXHAUSTED_REQUIRE_NEW_PRODUCT_GOAL":
                    selected = choose_open_item(items, goal_cards, max_rank=BACKLOG_POST_QUEUE_MAX_RANK)
                    if selected:
                        picked = backlog_candidate(repo_root, goal_index, latest_backlog, selected)
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
