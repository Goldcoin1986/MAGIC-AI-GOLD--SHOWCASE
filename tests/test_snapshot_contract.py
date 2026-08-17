from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from magic_ai_showcase.snapshot_contract import (  # noqa: E402
    Freshness,
    SnapshotValidationError,
    normalize_snapshot,
)


class SnapshotContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = {
            "account": {"id": "DEMO-01", "alias": "DEMO ACCOUNT"},
            "runtime": {"terminal_connected": True, "source_updated_at_ms": 1_000_000},
            "metrics": {"balance": 3208.10, "equity": 3199.25, "positions_open": 2},
        }

    def test_normalizes_valid_external_data(self) -> None:
        result = normalize_snapshot(self.payload)
        self.assertEqual(result.account_id, "DEMO-01")
        self.assertEqual(result.positions_open, 2)
        self.assertEqual(len(result.change_token), 20)

    def test_same_payload_has_stable_change_token(self) -> None:
        first = normalize_snapshot(self.payload)
        second = normalize_snapshot(copy.deepcopy(self.payload))
        self.assertEqual(first.change_token, second.change_token)

    def test_metric_change_produces_new_token(self) -> None:
        first = normalize_snapshot(self.payload)
        self.payload["metrics"]["equity"] = 3250.00
        second = normalize_snapshot(self.payload)
        self.assertNotEqual(first.change_token, second.change_token)

    def test_freshness_uses_source_update_time(self) -> None:
        result = normalize_snapshot(self.payload)
        self.assertEqual(result.freshness(1_002_000), Freshness.ONLINE)
        self.assertEqual(result.freshness(1_006_000), Freshness.STALE)
        self.assertEqual(result.freshness(1_020_000), Freshness.OFFLINE)

    def test_rejects_malformed_external_snapshot(self) -> None:
        self.payload["metrics"]["positions_open"] = "two"
        with self.assertRaises(SnapshotValidationError):
            normalize_snapshot(self.payload)


if __name__ == "__main__":
    unittest.main()
