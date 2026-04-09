"""
SecuPilot Static Data Adapter Baseline

S4-A-2 目标：
- 用显式 adapter 替换 T1 / T4 / T5 的静态数据直读
- 让 local_files 和未来 production-shaped source 共享 AdapterResult 信封
- 保持现有算法输入形状不变，只替换数据进入方式
"""

from __future__ import annotations

import asyncio
import json
import threading
import time
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import Settings, settings
from app.tools.siem_adapter import AdapterResult
from app.tools.static_data_sources import (
    AssetInventorySnapshot,
    AssetInventorySourceProtocol,
    AssetRecord,
    BaselineRecord,
    BaselineSnapshot,
    BaselineSourceProtocol,
    StaticRefreshPolicy,
    StaticSourceMetadata,
    ThreatIntelSeedRecord,
    ThreatIntelSeedSnapshot,
    ThreatIntelSeedSourceProtocol,
    TopologySnapshot,
    TopologySourceProtocol,
)


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _build_metadata(
    *,
    source_kind: str,
    source_name: str,
    source_mode: str,
    ownership: str,
    record_count: int,
    refresh_seconds: int,
) -> StaticSourceMetadata:
    return StaticSourceMetadata(
        source_kind=source_kind,
        source_name=source_name,
        source_mode=source_mode,
        ownership=ownership,
        refreshed_at_utc=_iso_utc_now(),
        record_count=record_count,
        refresh_policy=StaticRefreshPolicy(
            strategy="ttl",
            ttl_seconds=refresh_seconds,
            notes="Sprint 4 local-files baseline",
        ),
    )


def _effective_source_mode(global_mode: str, source_mode: str) -> str:
    return str(source_mode or global_mode or "local_files").strip().lower() or "local_files"


def _read_json_file(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _run_sync(coro):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    result: dict[str, Any] = {}
    error: dict[str, BaseException] = {}

    def _worker() -> None:
        try:
            result["value"] = asyncio.run(coro)
        except BaseException as exc:  # pragma: no cover - defensive relay
            error["value"] = exc

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    thread.join()

    if "value" in error:
        raise error["value"]
    return result.get("value")


class _BaseLocalFileSource:
    def __init__(
        self,
        *,
        root: Path,
        source_mode: str,
        refresh_seconds: int,
        rel_path: str,
    ) -> None:
        self.root = root
        self.source_mode = source_mode
        self.refresh_seconds = refresh_seconds
        self.rel_path = Path(rel_path)

    @property
    def path(self) -> Path:
        return self.root / self.rel_path

    async def _load_json(self, source_kind: str) -> AdapterResult[Any]:
        started = time.monotonic()
        if not self.path.exists():
            return AdapterResult.unavailable(
                {},
                gap_reason=f"static_source_missing:{source_kind}:{self.path}",
                latency_ms=(time.monotonic() - started) * 1000,
            )

        try:
            payload = await asyncio.to_thread(_read_json_file, self.path)
        except json.JSONDecodeError as exc:
            return AdapterResult.unavailable(
                {},
                gap_reason=f"static_source_invalid_json:{source_kind}:{exc}",
                latency_ms=(time.monotonic() - started) * 1000,
            )
        except OSError as exc:
            return AdapterResult.unavailable(
                {},
                gap_reason=f"static_source_read_failed:{source_kind}:{exc}",
                latency_ms=(time.monotonic() - started) * 1000,
            )

        return AdapterResult.ok(payload, latency_ms=(time.monotonic() - started) * 1000)


class _UnsupportedSourceBase:
    def __init__(self, *, source_mode: str, source_kind: str, refresh_seconds: int) -> None:
        self.source_mode = source_mode
        self.source_kind = source_kind
        self.refresh_seconds = refresh_seconds

    def _metadata(self, record_count: int = 0) -> StaticSourceMetadata:
        return _build_metadata(
            source_kind=self.source_kind,
            source_name=f"{self.source_kind}:{self.source_mode}",
            source_mode=self.source_mode,
            ownership="Static source contract placeholder",
            record_count=record_count,
            refresh_seconds=self.refresh_seconds,
        )


class LocalFileAssetInventorySource(_BaseLocalFileSource):
    def __init__(self, *, root: Path, source_mode: str, refresh_seconds: int) -> None:
        super().__init__(
            root=root,
            source_mode=source_mode,
            refresh_seconds=refresh_seconds,
            rel_path="assets/asset_dictionary.json",
        )

    async def load_asset_inventory(self) -> AdapterResult[AssetInventorySnapshot]:
        raw = await self._load_json("asset_inventory")
        if raw.status != "ok":
            return AdapterResult(
                status=raw.status,
                data=AssetInventorySnapshot(
                    metadata=_build_metadata(
                        source_kind="asset_inventory",
                        source_name=str(self.rel_path).replace("\\", "/"),
                        source_mode=self.source_mode,
                        ownership="T1 scoring context and T5 topology seed",
                        record_count=0,
                        refresh_seconds=self.refresh_seconds,
                    ),
                    assets=[],
                ),
                latency_ms=raw.latency_ms,
                gap_reason=raw.gap_reason,
                metadata={"path": str(self.path)},
            )

        assets: list[AssetRecord] = []
        for row in raw.data.get("assets", []):
            ip_addresses = list(row.get("ip_addresses", []) or [])
            primary_ip = row.get("ip_address")
            if primary_ip and primary_ip not in ip_addresses:
                ip_addresses.append(str(primary_ip))

            aliases = list(row.get("aliases", []) or [])
            asset = AssetRecord(
                asset_id=str(row.get("asset_id", "")),
                hostname=str(row.get("hostname", "")),
                ip_addresses=[str(value) for value in ip_addresses if value],
                business_unit=str(row.get("business_unit", "")),
                owner=str(row.get("owner", "")),
                network_segment=str(row.get("network_segment", "")),
                role=str(row.get("role", "")),
                os=str(row.get("os", "")),
                criticality_weight=int(row.get("criticality_weight", 0) or 0),
                aliases=[str(value) for value in aliases if value],
                extra={
                    key: value
                    for key, value in row.items()
                    if key
                    not in {
                        "asset_id",
                        "hostname",
                        "ip_addresses",
                        "ip_address",
                        "business_unit",
                        "owner",
                        "network_segment",
                        "role",
                        "os",
                        "criticality_weight",
                        "aliases",
                    }
                },
            )
            if asset.asset_id:
                assets.append(asset)

        snapshot = AssetInventorySnapshot(
            metadata=_build_metadata(
                source_kind="asset_inventory",
                source_name=str(self.rel_path).replace("\\", "/"),
                source_mode=self.source_mode,
                ownership="T1 scoring context and T5 topology seed",
                record_count=len(assets),
                refresh_seconds=self.refresh_seconds,
            ),
            assets=assets,
        )
        return AdapterResult.ok(snapshot, latency_ms=raw.latency_ms, metadata={"path": str(self.path)})


class LocalFileBaselineSource(_BaseLocalFileSource):
    def __init__(self, *, root: Path, source_mode: str, refresh_seconds: int) -> None:
        super().__init__(
            root=root,
            source_mode=source_mode,
            refresh_seconds=refresh_seconds,
            rel_path="baselines/false_positive_baseline.json",
        )

    async def load_baselines(self) -> AdapterResult[BaselineSnapshot]:
        raw = await self._load_json("baseline")
        if raw.status != "ok":
            return AdapterResult(
                status=raw.status,
                data=BaselineSnapshot(
                    metadata=_build_metadata(
                        source_kind="baseline",
                        source_name=str(self.rel_path).replace("\\", "/"),
                        source_mode=self.source_mode,
                        ownership="T1 baseline dampening",
                        record_count=0,
                        refresh_seconds=self.refresh_seconds,
                    ),
                    baselines=[],
                ),
                latency_ms=raw.latency_ms,
                gap_reason=raw.gap_reason,
                metadata={"path": str(self.path)},
            )

        baselines: list[BaselineRecord] = []
        for row in raw.data.get("baselines", []):
            pattern = str(row.get("pattern_description", ""))
            record = BaselineRecord(
                baseline_id=str(row.get("baseline_id", "")),
                category=str(row.get("category", "")),
                pattern_description=pattern,
                confidence=float(row.get("confidence", 0.0) or 0.0),
                scope_asset_ids=[str(value) for value in row.get("scope_asset_ids", []) if value],
                activity_names=[
                    str(value) for value in (row.get("activity_names") or [pattern]) if value
                ],
                extra={
                    key: value
                    for key, value in row.items()
                    if key
                    not in {
                        "baseline_id",
                        "category",
                        "pattern_description",
                        "confidence",
                        "scope_asset_ids",
                        "activity_names",
                    }
                },
            )
            if record.baseline_id:
                baselines.append(record)

        snapshot = BaselineSnapshot(
            metadata=_build_metadata(
                source_kind="baseline",
                source_name=str(self.rel_path).replace("\\", "/"),
                source_mode=self.source_mode,
                ownership="T1 baseline dampening",
                record_count=len(baselines),
                refresh_seconds=self.refresh_seconds,
            ),
            baselines=baselines,
        )
        return AdapterResult.ok(snapshot, latency_ms=raw.latency_ms, metadata={"path": str(self.path)})


class LocalFileThreatIntelSeedSource(_BaseLocalFileSource):
    def __init__(self, *, root: Path, source_mode: str, refresh_seconds: int) -> None:
        super().__init__(
            root=root,
            source_mode=source_mode,
            refresh_seconds=refresh_seconds,
            rel_path="threat_intel/mock_ioc_database.json",
        )

    async def load_threat_intel_seed(self) -> AdapterResult[ThreatIntelSeedSnapshot]:
        raw = await self._load_json("intel_seed")
        if raw.status != "ok":
            return AdapterResult(
                status=raw.status,
                data=ThreatIntelSeedSnapshot(
                    metadata=_build_metadata(
                        source_kind="intel_seed",
                        source_name=str(self.rel_path).replace("\\", "/"),
                        source_mode=self.source_mode,
                        ownership="T4 intel enrichment seed",
                        record_count=0,
                        refresh_seconds=self.refresh_seconds,
                    ),
                    records=[],
                ),
                latency_ms=raw.latency_ms,
                gap_reason=raw.gap_reason,
                metadata={"path": str(self.path)},
            )

        records: list[ThreatIntelSeedRecord] = []
        for section, indicator_type, field_name in (
            ("malicious_ips", "ip", "ip"),
            ("malicious_domains", "domain", "domain"),
            ("malicious_hashes", "hash", "hash"),
        ):
            for row in raw.data.get(section, []):
                indicator = str(row.get(field_name, ""))
                if not indicator:
                    continue
                records.append(
                    ThreatIntelSeedRecord(
                        indicator=indicator,
                        indicator_type=indicator_type,
                        threat_type=str(row.get("threat_type", row.get("family", ""))),
                        actor=str(row.get("actor", row.get("family", ""))),
                        confidence=float(row.get("confidence", 0.0) or 0.0),
                        country=str(row.get("country", "")),
                        tags=[str(value) for value in row.get("tags", []) if value],
                        extra={
                            key: value
                            for key, value in row.items()
                            if key
                            not in {
                                field_name,
                                "threat_type",
                                "actor",
                                "confidence",
                                "country",
                                "tags",
                                "family",
                            }
                        },
                    )
                )

        snapshot = ThreatIntelSeedSnapshot(
            metadata=_build_metadata(
                source_kind="intel_seed",
                source_name=str(self.rel_path).replace("\\", "/"),
                source_mode=self.source_mode,
                ownership="T4 intel enrichment seed",
                record_count=len(records),
                refresh_seconds=self.refresh_seconds,
            ),
            records=records,
        )
        return AdapterResult.ok(snapshot, latency_ms=raw.latency_ms, metadata={"path": str(self.path)})


class LocalFileTopologySource(_BaseLocalFileSource):
    def __init__(self, *, root: Path, source_mode: str, refresh_seconds: int) -> None:
        super().__init__(
            root=root,
            source_mode=source_mode,
            refresh_seconds=refresh_seconds,
            rel_path="knowledge_graph/entity_relationships.json",
        )

    async def load_topology(self) -> AdapterResult[TopologySnapshot]:
        raw = await self._load_json("topology")
        if raw.status != "ok":
            return AdapterResult(
                status=raw.status,
                data=TopologySnapshot(
                    metadata=_build_metadata(
                        source_kind="topology",
                        source_name=str(self.rel_path).replace("\\", "/"),
                        source_mode=self.source_mode,
                        ownership="T5 blast-radius topology graph",
                        record_count=0,
                        refresh_seconds=self.refresh_seconds,
                    ),
                    nodes={},
                    edges=[],
                ),
                latency_ms=raw.latency_ms,
                gap_reason=raw.gap_reason,
                metadata={"path": str(self.path)},
            )

        nodes = deepcopy(raw.data.get("nodes", {}))
        edges = deepcopy(raw.data.get("relationships", raw.data.get("edges", [])))
        snapshot = TopologySnapshot(
            metadata=_build_metadata(
                source_kind="topology",
                source_name=str(self.rel_path).replace("\\", "/"),
                source_mode=self.source_mode,
                ownership="T5 blast-radius topology graph",
                record_count=len(edges),
                refresh_seconds=self.refresh_seconds,
            ),
            nodes=nodes,
            edges=edges,
        )
        return AdapterResult.ok(snapshot, latency_ms=raw.latency_ms, metadata={"path": str(self.path)})


class UnsupportedAssetInventorySource(_UnsupportedSourceBase):
    async def load_asset_inventory(self) -> AdapterResult[AssetInventorySnapshot]:
        return AdapterResult.unavailable(
            AssetInventorySnapshot(metadata=self._metadata(), assets=[]),
            gap_reason=f"static_source_mode_not_implemented:asset_inventory:{self.source_mode}",
        )


class UnsupportedBaselineSource(_UnsupportedSourceBase):
    async def load_baselines(self) -> AdapterResult[BaselineSnapshot]:
        return AdapterResult.unavailable(
            BaselineSnapshot(metadata=self._metadata(), baselines=[]),
            gap_reason=f"static_source_mode_not_implemented:baseline:{self.source_mode}",
        )


class UnsupportedThreatIntelSeedSource(_UnsupportedSourceBase):
    async def load_threat_intel_seed(self) -> AdapterResult[ThreatIntelSeedSnapshot]:
        return AdapterResult.unavailable(
            ThreatIntelSeedSnapshot(metadata=self._metadata(), records=[]),
            gap_reason=f"static_source_mode_not_implemented:intel_seed:{self.source_mode}",
        )


class UnsupportedTopologySource(_UnsupportedSourceBase):
    async def load_topology(self) -> AdapterResult[TopologySnapshot]:
        return AdapterResult.unavailable(
            TopologySnapshot(metadata=self._metadata(), nodes={}, edges=[]),
            gap_reason=f"static_source_mode_not_implemented:topology:{self.source_mode}",
        )


@dataclass(frozen=True)
class StaticDataSourceAdapters:
    asset_inventory: AssetInventorySourceProtocol
    baselines: BaselineSourceProtocol
    threat_intel_seed: ThreatIntelSeedSourceProtocol
    topology: TopologySourceProtocol


@dataclass(frozen=True)
class LoadedStaticDataRuntimePayloads:
    asset_inventory_snapshot: AssetInventorySnapshot
    baseline_snapshot: BaselineSnapshot
    threat_intel_seed_snapshot: ThreatIntelSeedSnapshot
    topology_snapshot: TopologySnapshot
    asset_inventory_payload: dict[str, Any]
    baseline_payload: dict[str, Any]
    threat_intel_seed_payload: dict[str, Any]
    topology_payload: dict[str, Any]


def asset_inventory_snapshot_to_runtime_payload(snapshot: AssetInventorySnapshot) -> dict[str, Any]:
    assets: list[dict[str, Any]] = []
    for record in snapshot.assets:
        payload = {
            "asset_id": record.asset_id,
            "hostname": record.hostname,
            "ip_address": record.ip_addresses[0] if record.ip_addresses else "",
            "ip_addresses": list(record.ip_addresses),
            "business_unit": record.business_unit,
            "owner": record.owner,
            "network_segment": record.network_segment,
            "role": record.role,
            "os": record.os,
            "criticality_weight": record.criticality_weight,
            "aliases": list(record.aliases),
            **deepcopy(record.extra),
        }
        assets.append(payload)
    return {
        "assets": assets,
        "total": len(assets),
    }


def baseline_snapshot_to_runtime_payload(snapshot: BaselineSnapshot) -> dict[str, Any]:
    baselines: list[dict[str, Any]] = []
    for record in snapshot.baselines:
        payload = {
            "baseline_id": record.baseline_id,
            "category": record.category,
            "pattern_description": record.pattern_description,
            "confidence": record.confidence,
            "scope_asset_ids": list(record.scope_asset_ids),
            "activity_names": list(record.activity_names),
            **deepcopy(record.extra),
        }
        baselines.append(payload)
    return {
        "total": len(baselines),
        "baselines": baselines,
    }


def threat_intel_seed_snapshot_to_runtime_payload(snapshot: ThreatIntelSeedSnapshot) -> dict[str, Any]:
    payload = {
        "malicious_ips": [],
        "malicious_domains": [],
        "malicious_hashes": [],
    }
    for record in snapshot.records:
        base = {
            "threat_type": record.threat_type,
            "actor": record.actor,
            "confidence": record.confidence,
            "country": record.country,
            "tags": list(record.tags),
            **deepcopy(record.extra),
        }
        if record.indicator_type == "ip":
            payload["malicious_ips"].append({"ip": record.indicator, **base})
        elif record.indicator_type == "domain":
            payload["malicious_domains"].append({"domain": record.indicator, **base})
        elif record.indicator_type == "hash":
            payload["malicious_hashes"].append({"hash": record.indicator, **base})
    return payload


def topology_snapshot_to_runtime_payload(snapshot: TopologySnapshot) -> dict[str, Any]:
    return {
        "nodes": deepcopy(snapshot.nodes),
        "relationships": deepcopy(snapshot.edges),
    }


async def load_static_data_runtime_payloads(
    adapters: StaticDataSourceAdapters,
) -> LoadedStaticDataRuntimePayloads:
    asset_result, baseline_result, intel_result, topology_result = await asyncio.gather(
        adapters.asset_inventory.load_asset_inventory(),
        adapters.baselines.load_baselines(),
        adapters.threat_intel_seed.load_threat_intel_seed(),
        adapters.topology.load_topology(),
    )

    results = {
        "asset_inventory": asset_result,
        "baseline": baseline_result,
        "intel_seed": intel_result,
        "topology": topology_result,
    }
    for source_kind, result in results.items():
        if result.status != "ok":
            detail = result.gap_reason or "static_source_unavailable"
            raise RuntimeError(f"static_source_{source_kind}_{result.status}:{detail}")

    return LoadedStaticDataRuntimePayloads(
        asset_inventory_snapshot=asset_result.data,
        baseline_snapshot=baseline_result.data,
        threat_intel_seed_snapshot=intel_result.data,
        topology_snapshot=topology_result.data,
        asset_inventory_payload=asset_inventory_snapshot_to_runtime_payload(asset_result.data),
        baseline_payload=baseline_snapshot_to_runtime_payload(baseline_result.data),
        threat_intel_seed_payload=threat_intel_seed_snapshot_to_runtime_payload(intel_result.data),
        topology_payload=topology_snapshot_to_runtime_payload(topology_result.data),
    )


def load_static_data_runtime_payloads_sync(
    adapters: StaticDataSourceAdapters,
) -> LoadedStaticDataRuntimePayloads:
    return _run_sync(load_static_data_runtime_payloads(adapters))


def build_static_data_source_adapters(
    runtime_settings: Settings = settings,
) -> StaticDataSourceAdapters:
    root = runtime_settings.get_static_data_dir()
    refresh_seconds = int(getattr(runtime_settings, "static_data_refresh_seconds", 300) or 300)
    default_mode = str(getattr(runtime_settings, "static_data_mode", "local_files") or "local_files")

    asset_mode = _effective_source_mode(default_mode, getattr(runtime_settings, "asset_source_mode", ""))
    baseline_mode = _effective_source_mode(default_mode, getattr(runtime_settings, "baseline_source_mode", ""))
    intel_mode = _effective_source_mode(default_mode, getattr(runtime_settings, "intel_seed_source_mode", ""))
    topology_mode = _effective_source_mode(default_mode, getattr(runtime_settings, "topology_source_mode", ""))

    def _asset_source():
        if asset_mode in {"local_files", "bundle"}:
            return LocalFileAssetInventorySource(root=root, source_mode=asset_mode, refresh_seconds=refresh_seconds)
        return UnsupportedAssetInventorySource(
            source_mode=asset_mode,
            source_kind="asset_inventory",
            refresh_seconds=refresh_seconds,
        )

    def _baseline_source():
        if baseline_mode in {"local_files", "bundle"}:
            return LocalFileBaselineSource(root=root, source_mode=baseline_mode, refresh_seconds=refresh_seconds)
        return UnsupportedBaselineSource(
            source_mode=baseline_mode,
            source_kind="baseline",
            refresh_seconds=refresh_seconds,
        )

    def _intel_source():
        if intel_mode in {"local_files", "bundle"}:
            return LocalFileThreatIntelSeedSource(root=root, source_mode=intel_mode, refresh_seconds=refresh_seconds)
        return UnsupportedThreatIntelSeedSource(
            source_mode=intel_mode,
            source_kind="intel_seed",
            refresh_seconds=refresh_seconds,
        )

    def _topology_source():
        if topology_mode in {"local_files", "bundle"}:
            return LocalFileTopologySource(root=root, source_mode=topology_mode, refresh_seconds=refresh_seconds)
        return UnsupportedTopologySource(
            source_mode=topology_mode,
            source_kind="topology",
            refresh_seconds=refresh_seconds,
        )

    return StaticDataSourceAdapters(
        asset_inventory=_asset_source(),
        baselines=_baseline_source(),
        threat_intel_seed=_intel_source(),
        topology=_topology_source(),
    )
