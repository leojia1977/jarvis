"""
SecuPilot Host Identity Resolver

Sprint 4 A-3 目标：
- 从静态资产快照构建一个权威主机身份解析器
- 为 SIEM、T3 主机选择和 blast-radius 目标选择提供统一 canonical asset id
- 在身份歧义时显式返回 partial，而不是静默猜测
"""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from typing import Iterable, Optional

from app.tools.siem_adapter import AdapterResult
from app.tools.static_data_sources import (
    AssetInventorySnapshot,
    HostIdentityRecord,
    HostIdentityResolverProtocol,
)


def _normalize_text(value: str) -> str:
    return str(value or "").strip().lower()


def _normalize_ip(value: str) -> str:
    return str(value or "").strip()


def _unique_strings(values: Iterable[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text:
            continue
        lowered = text.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        ordered.append(text)
    return ordered


class AssetInventoryHostIdentityResolver(HostIdentityResolverProtocol):
    """
    基于 AssetInventorySnapshot 构建的本地 resolver。

    `resolve_any` 的优先级：
    asset_id -> hostname -> fqdn -> ip_address -> aliases
    """

    def __init__(self, snapshot: AssetInventorySnapshot):
        self.snapshot = snapshot
        self._records: dict[str, HostIdentityRecord] = {}
        self._asset_ids: dict[str, set[str]] = defaultdict(set)
        self._hostnames: dict[str, set[str]] = defaultdict(set)
        self._fqdns: dict[str, set[str]] = defaultdict(set)
        self._ips: dict[str, set[str]] = defaultdict(set)
        self._aliases: dict[str, set[str]] = defaultdict(set)
        self._index_snapshot(snapshot)

    def _index_snapshot(self, snapshot: AssetInventorySnapshot) -> None:
        for asset in snapshot.assets:
            canonical_asset_id = str(asset.asset_id or "").strip()
            if not canonical_asset_id:
                continue

            fqdn = str(asset.extra.get("fqdn", "") or "").strip()
            aliases = _unique_strings(asset.aliases)
            source_refs = [f"asset_inventory:{canonical_asset_id}"]
            source_refs.extend(str(value) for value in asset.extra.get("source_refs", []) if value)

            record = HostIdentityRecord(
                canonical_asset_id=canonical_asset_id,
                hostname=str(asset.hostname or "").strip(),
                fqdn=fqdn,
                ip_addresses=_unique_strings(asset.ip_addresses),
                aliases=aliases,
                source_refs=_unique_strings(source_refs),
                confidence=1.0,
                extra=deepcopy(asset.extra),
            )
            self._records[canonical_asset_id] = record

            self._asset_ids[_normalize_text(canonical_asset_id)].add(canonical_asset_id)
            if record.hostname:
                self._hostnames[_normalize_text(record.hostname)].add(canonical_asset_id)
            if record.fqdn:
                self._fqdns[_normalize_text(record.fqdn)].add(canonical_asset_id)
            for ip_address in record.ip_addresses:
                self._ips[_normalize_ip(ip_address)].add(canonical_asset_id)
            for alias in record.aliases:
                self._aliases[_normalize_text(alias)].add(canonical_asset_id)

    def _result_from_candidates(
        self,
        *,
        match_kind: str,
        identifier: str,
        candidates: set[str],
    ) -> AdapterResult[Optional[HostIdentityRecord]]:
        candidate_ids = sorted(candidates)
        metadata = {
            "matched_by": match_kind,
            "identifier": identifier,
            "candidate_asset_ids": candidate_ids,
        }

        if not candidate_ids:
            return AdapterResult.ok(None, metadata=metadata)

        if len(candidate_ids) > 1:
            return AdapterResult.partial(
                None,
                gap_reason=f"identity_ambiguous:{match_kind}:{identifier}",
                metadata=metadata,
            )

        record = self._records[candidate_ids[0]]
        return AdapterResult.ok(record, metadata=metadata)

    async def resolve_asset_id(self, asset_id: str) -> AdapterResult[Optional[HostIdentityRecord]]:
        normalized = _normalize_text(asset_id)
        return self._result_from_candidates(
            match_kind="asset_id",
            identifier=str(asset_id or "").strip(),
            candidates=self._asset_ids.get(normalized, set()),
        )

    async def resolve_ip(self, ip_address: str) -> AdapterResult[Optional[HostIdentityRecord]]:
        normalized = _normalize_ip(ip_address)
        return self._result_from_candidates(
            match_kind="ip_address",
            identifier=normalized,
            candidates=self._ips.get(normalized, set()),
        )

    async def resolve_hostname(self, hostname: str) -> AdapterResult[Optional[HostIdentityRecord]]:
        text = str(hostname or "").strip()
        normalized = _normalize_text(text)

        for match_kind, index in (
            ("hostname", self._hostnames),
            ("fqdn", self._fqdns),
        ):
            result = self._result_from_candidates(
                match_kind=match_kind,
                identifier=text,
                candidates=index.get(normalized, set()),
            )
            if result.data is not None or result.status != "ok":
                return result

        return AdapterResult.ok(
            None,
            metadata={"matched_by": "hostname", "identifier": text, "candidate_asset_ids": []},
        )

    async def resolve_any(self, identifier: str) -> AdapterResult[Optional[HostIdentityRecord]]:
        text = str(identifier or "").strip()
        if not text:
            return AdapterResult.ok(
                None,
                metadata={"matched_by": "none", "identifier": "", "candidate_asset_ids": []},
            )

        for resolver in (
            self.resolve_asset_id,
            self.resolve_hostname,
            self.resolve_ip,
        ):
            result = await resolver(text)
            if result.data is not None or result.status != "ok":
                return result

        alias_result = self._result_from_candidates(
            match_kind="aliases",
            identifier=text,
            candidates=self._aliases.get(_normalize_text(text), set()),
        )
        if alias_result.data is not None or alias_result.status != "ok":
            return alias_result

        return AdapterResult.ok(
            None,
            metadata={"matched_by": "none", "identifier": text, "candidate_asset_ids": []},
        )


def build_asset_inventory_host_identity_resolver(
    snapshot: AssetInventorySnapshot,
) -> HostIdentityResolverProtocol:
    return AssetInventoryHostIdentityResolver(snapshot)
