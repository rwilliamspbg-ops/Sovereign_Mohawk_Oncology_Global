import json
import tempfile
import unittest

from security_wrapper.audit import AuditLogger
from security_wrapper.policy import SecurityPolicy
from security_wrapper.wrapper import SecurityWrapperStrategy


class _DummyInnerStrategy:
    def __init__(self) -> None:
        self.last_round = None
        self.last_accepted_count = None

    def aggregate_fit(self, server_round, results, failures):
        self.last_round = server_round
        self.last_accepted_count = len(results)
        return {"round": server_round, "accepted": len(results), "failures": len(failures)}


class _FitRes:
    def __init__(self, metrics):
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

        valid_metrics = {
            "client_id": "site-1",
            "signature_verified": True,
            "attestation_ok": True,
            "epsilon_spent": 0.2,
            "payload_size_bytes": 200,
            "nonce": "n-1",
            "payload_hash": "hash-1",
            "gradient_zscore": 0.1,
        }
        invalid_metrics = {
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
        hook_payloads = []
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


if __name__ == "__main__":
    unittest.main()
