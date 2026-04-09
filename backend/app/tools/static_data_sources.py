"""
SecuPilot Static Data Source Contracts

S4-A-1 目标：
- 冻结 T1 / T4 / T5 仍在使用的静态数据源契约
- 让后续 A-2 / A-3 能直接围绕显式 source contract 实现
- 保持当前算法不变，只先冻结输入与 ownership / refresh 语义
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Optional, Protocol

from app.tools.siem_adapter import AdapterResult


StaticSourceMode = Literal["local_files", "api", "bundle", "hybrid"]
StaticSourceKind = Literal[
    "asset_inventory",
    "baseline",
    "intel_seed",
    "topology",
    "host_identity",
]
RefreshStrategy = Literal["startup", "ttl", "manual"]


@dataclass(frozen=True)
class StaticRefreshPolicy:
    strategy: RefreshStrategy
    ttl_seconds: int = 300
    notes: str = ""


@dataclass(frozen=True)
class StaticSourceMetadata:
    source_kind: StaticSourceKind
    source_name: str
    source_mode: StaticSourceMode
    ownership: str
    refreshed_at_utc: Optional[str] = None
    record_count: int = 0
    refresh_policy: StaticRefreshPolicy = field(
        default_factory=lambda: StaticRefreshPolicy(strategy="startup", ttl_seconds=300)
    )


@dataclass(frozen=True)
class AssetRecord:
    asset_id: str
    hostname: str
    ip_addresses: list[str]
    business_unit: str = ""
    owner: str = ""
    network_segment: str = ""
    role: str = ""
    os: str = ""
    criticality_weight: int = 0
    aliases: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AssetInventorySnapshot:
    metadata: StaticSourceMetadata
    assets: list[AssetRecord]


@dataclass(frozen=True)
class BaselineRecord:
    baseline_id: str
    category: str
    pattern_description: str
    confidence: float
    scope_asset_ids: list[str] = field(default_factory=list)
    activity_names: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BaselineSnapshot:
    metadata: StaticSourceMetadata
    baselines: list[BaselineRecord]


@dataclass(frozen=True)
class ThreatIntelSeedRecord:
    indicator: str
    indicator_type: Literal["ip", "domain", "hash"]
    threat_type: str = ""
    actor: str = ""
    confidence: float = 0.0
    country: str = ""
    tags: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ThreatIntelSeedSnapshot:
    metadata: StaticSourceMetadata
    records: list[ThreatIntelSeedRecord]


@dataclass(frozen=True)
class TopologySnapshot:
    metadata: StaticSourceMetadata
    nodes: dict[str, Any]
    edges: list[dict[str, Any]]


@dataclass(frozen=True)
class HostIdentityRecord:
    canonical_asset_id: str
    hostname: str = ""
    fqdn: str = ""
    ip_addresses: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)
    confidence: float = 1.0
    extra: dict[str, Any] = field(default_factory=dict)


class AssetInventorySourceProtocol(Protocol):
    async def load_asset_inventory(self) -> AdapterResult[AssetInventorySnapshot]:
        ...


class BaselineSourceProtocol(Protocol):
    async def load_baselines(self) -> AdapterResult[BaselineSnapshot]:
        ...


class ThreatIntelSeedSourceProtocol(Protocol):
    async def load_threat_intel_seed(self) -> AdapterResult[ThreatIntelSeedSnapshot]:
        ...


class TopologySourceProtocol(Protocol):
    async def load_topology(self) -> AdapterResult[TopologySnapshot]:
        ...


class HostIdentityResolverProtocol(Protocol):
    async def resolve_any(self, identifier: str) -> AdapterResult[Optional[HostIdentityRecord]]:
        ...

    async def resolve_asset_id(self, asset_id: str) -> AdapterResult[Optional[HostIdentityRecord]]:
        ...

    async def resolve_ip(self, ip_address: str) -> AdapterResult[Optional[HostIdentityRecord]]:
        ...

    async def resolve_hostname(self, hostname: str) -> AdapterResult[Optional[HostIdentityRecord]]:
        ...
