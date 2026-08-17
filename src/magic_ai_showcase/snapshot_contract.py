"""Sanitized example of a realtime snapshot boundary.

This module demonstrates input validation and freshness classification only.
It intentionally contains no trading signal, order-entry rule or proprietary
Expert Advisor logic.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any, Mapping


class SnapshotValidationError(ValueError):
    """Raised when an external snapshot violates the public data contract."""


class Freshness(StrEnum):
    ONLINE = "online"
    STALE = "stale"
    OFFLINE = "offline"


@dataclass(frozen=True, slots=True)
class NormalizedSnapshot:
    account_id: str
    alias: str
    terminal_connected: bool
    source_updated_at_ms: int
    balance: float
    equity: float
    positions_open: int
    change_token: str

    def freshness(self, now_ms: int, heartbeat_ms: int = 1_000) -> Freshness:
        if heartbeat_ms < 100:
            raise ValueError("heartbeat_ms must be at least 100")
        age_ms = max(0, int(now_ms) - self.source_updated_at_ms)
        online_limit = max(3_000, heartbeat_ms * 3)
        stale_limit = max(8_000, heartbeat_ms * 8)
        if age_ms <= online_limit:
            return Freshness.ONLINE
        if age_ms <= stale_limit:
            return Freshness.STALE
        return Freshness.OFFLINE

    def public_dict(self) -> dict[str, Any]:
        return asdict(self)


def _required_object(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise SnapshotValidationError(f"{key} must be an object")
    return value


def _required_text(payload: Mapping[str, Any], key: str, limit: int = 80) -> str:
    value = str(payload.get(key) or "").strip()
    if not value:
        raise SnapshotValidationError(f"{key} is required")
    return value[:limit]


def _number(payload: Mapping[str, Any], key: str) -> float:
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SnapshotValidationError(f"{key} must be numeric")
    return float(value)


def _integer(payload: Mapping[str, Any], key: str, minimum: int = 0) -> int:
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise SnapshotValidationError(f"{key} must be an integer >= {minimum}")
    return value


def normalize_snapshot(payload: Mapping[str, Any]) -> NormalizedSnapshot:
    """Validate one external snapshot and return a deterministic public model."""

    if not isinstance(payload, Mapping):
        raise SnapshotValidationError("snapshot must be an object")
    account = _required_object(payload, "account")
    runtime = _required_object(payload, "runtime")
    metrics = _required_object(payload, "metrics")

    normalized_fields = {
        "account_id": _required_text(account, "id", 64),
        "alias": _required_text(account, "alias", 60),
        "terminal_connected": runtime.get("terminal_connected") is True,
        "source_updated_at_ms": _integer(runtime, "source_updated_at_ms", 1),
        "balance": _number(metrics, "balance"),
        "equity": _number(metrics, "equity"),
        "positions_open": _integer(metrics, "positions_open"),
    }
    canonical = json.dumps(
        normalized_fields,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    normalized_fields["change_token"] = hashlib.sha256(canonical).hexdigest()[:20]
    return NormalizedSnapshot(**normalized_fields)
