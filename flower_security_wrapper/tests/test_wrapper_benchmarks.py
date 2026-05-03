import json
import tempfile
import unittest
from typing import Any, Dict, List, Tuple
from unittest.mock import patch

from security_wrapper.audit import AuditLogger
from security_wrapper.policy import SecurityPolicy
from security_wrapper.wrapper import SecurityWrapperStrategy


class _DummyInnerStrategy:
    def __init__(self) -> None:
        self.last_round: int | None = None
        self.last_accepted_count: int | None = None

    def aggregate_fit(
        self, server_round: int, results: List[Tuple[Any, Any]], failures: List[Any]
    ) -> Dict[str, int]:
        self.last_round = server_round
        self.last_accepted_count = len(results)
        return {"round": server_round, "accepted": len(results), "failures": len(failures)}


class _FitRes:
    def __init__(self, metrics: Dict[str, Any]) -> None:
        self.metrics = metrics


class TestWrapperBenchmarks(unittest.TestCase):
    def test_emits_round_benchmark_and_calls_hook(self):
        policy = SecurityPolicy(
            allowed_client_ids=["site-1", "site-2"],
            signature_mode="metric_flag",
            require_vector_consensus_checks=False,
            enable_governance_contract=False,
            emit_round_benchmarks=True,
        )

        valid_metrics: Dict[str, Any] = {
            "client_id": "site-1",
            "signature_verified": True,
            "attestation_ok": True,
            "epsilon_spent": 0.2,
            "payload_size_bytes": 200,
            "nonce": "n-1",
            "payload_hash": "hash-1",
            "gradient_zscore": 0.1,
        }
        invalid_metrics: Dict[str, Any] = {
            "client_id": "site-2",
            "signature_verified": True,
            "attestation_ok": True,
            "epsilon_spent": 9.9,
            "payload_size_bytes": 200,
            "nonce": "n-2",
            "payload_hash": "hash-2",
            "gradient_zscore": 0.2,
        }

        inner = _DummyInnerStrategy()
        hook_payloads: List[Dict[str, object]] = []
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            audit_path = f.name

        wrapper = SecurityWrapperStrategy(
            inner_strategy=inner,
            policy=policy,
            audit_logger=AuditLogger(audit_path, enable_wal=False),
            benchmark_hook=hook_payloads.append,
        )

        out = wrapper.aggregate_fit(
            server_round=5,
            results=[("c1", _FitRes(valid_metrics)), ("c2", _FitRes(invalid_metrics))],
            failures=[],
        )

        self.assertEqual(out["accepted"], 1)
        self.assertEqual(inner.last_accepted_count, 1)
        self.assertEqual(len(hook_payloads), 1)
        self.assertEqual(hook_payloads[0]["total_results"], 2)
        self.assertEqual(hook_payloads[0]["accepted"], 1)
        self.assertEqual(hook_payloads[0]["rejected_validation"], 1)

        with open(audit_path, "r", encoding="utf-8") as fh:
            records = [json.loads(line) for line in fh if line.strip()]

        benchmark_records = [r for r in records if r.get("event_type") == "round_benchmark"]
        self.assertEqual(len(benchmark_records), 1)
        self.assertEqual(benchmark_records[0]["payload"]["round"], 5)
        self.assertIn("p95_client_eval_ms", benchmark_records[0]["payload"])
        self.assertIn("p95_within_budget", benchmark_records[0]["payload"])

    def test_emits_p95_slo_violation_event_when_over_budget(self):
        policy = SecurityPolicy(
            allowed_client_ids=["site-1"],
            signature_mode="metric_flag",
            require_vector_consensus_checks=False,
            enable_governance_contract=False,
            emit_round_benchmarks=True,
            benchmark_client_eval_p95_budget_ms=1.0,
        )

        metrics: Dict[str, Any] = {
            "client_id": "site-1",
            "signature_verified": True,
            "attestation_ok": True,
            "epsilon_spent": 0.2,
            "payload_size_bytes": 200,
            "nonce": "n-slo",
            "payload_hash": "hash-slo",
            "gradient_zscore": 0.1,
        }

        inner = _DummyInnerStrategy()
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            audit_path = f.name

        wrapper = SecurityWrapperStrategy(
            inner_strategy=inner,
            policy=policy,
            audit_logger=AuditLogger(audit_path, enable_wal=False),
        )

        time_values = [
            100.0,
            100.002,
            100.012,
            100.015,
        ]
        with patch("security_wrapper.wrapper.time.perf_counter", side_effect=time_values):
            wrapper.aggregate_fit(
                server_round=8,
                results=[("c1", _FitRes(metrics))],
                failures=[],
            )

        with open(audit_path, "r", encoding="utf-8") as fh:
            records = [json.loads(line) for line in fh if line.strip()]

        violations = [
            r for r in records if r.get("event_type") == "round_benchmark_slo_violation"
        ]
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0]["payload"]["round"], 8)

        benchmark_records = [r for r in records if r.get("event_type") == "round_benchmark"]
        self.assertEqual(len(benchmark_records), 1)
        self.assertFalse(benchmark_records[0]["payload"]["p95_within_budget"])

    def test_no_slo_violation_when_p95_within_budget(self):
        policy = SecurityPolicy(
            allowed_client_ids=["site-1"],
            signature_mode="metric_flag",
            require_vector_consensus_checks=False,
            enable_governance_contract=False,
            emit_round_benchmarks=True,
            benchmark_client_eval_p95_budget_ms=20.0,
        )

        metrics: Dict[str, Any] = {
            "client_id": "site-1",
            "signature_verified": True,
            "attestation_ok": True,
            "epsilon_spent": 0.2,
            "payload_size_bytes": 200,
            "nonce": "n-slo-pass",
            "payload_hash": "hash-slo-pass",
            "gradient_zscore": 0.1,
        }

        inner = _DummyInnerStrategy()
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            audit_path = f.name

        wrapper = SecurityWrapperStrategy(
            inner_strategy=inner,
            policy=policy,
            audit_logger=AuditLogger(audit_path, enable_wal=False),
        )

        time_values = [
            200.0,
            200.002,
            200.004,
            200.006,
        ]
        with patch("security_wrapper.wrapper.time.perf_counter", side_effect=time_values):
            wrapper.aggregate_fit(
                server_round=9,
                results=[("c1", _FitRes(metrics))],
                failures=[],
            )

        with open(audit_path, "r", encoding="utf-8") as fh:
            records = [json.loads(line) for line in fh if line.strip()]

        violations = [
            r for r in records if r.get("event_type") == "round_benchmark_slo_violation"
        ]
        self.assertEqual(len(violations), 0)

        benchmark_records = [r for r in records if r.get("event_type") == "round_benchmark"]
        self.assertEqual(len(benchmark_records), 1)
        self.assertTrue(benchmark_records[0]["payload"]["p95_within_budget"])


if __name__ == "__main__":
    unittest.main()
