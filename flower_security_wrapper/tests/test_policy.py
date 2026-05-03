import json
import os
import tempfile
import unittest
from typing import Any, Dict

from security_wrapper.policy import load_policy_from_json, resolve_policy_path


class TestPolicyLoading(unittest.TestCase):
    def test_load_policy_json(self):
        data: Dict[str, Any] = {
            "allowed_client_ids": ["a"],
            "client_public_keys": {"a": "00"},
            "require_attestation": True,
            "attestation_signature_mode": "xmss",
            "require_signature": True,
            "signature_mode": "ed25519",
            "require_nonce": True,
            "max_payload_bytes": 10,
            "max_epsilon_spent_per_round": 0.7,
            "governance_readiness_signals": ["go_live_approved"],
            "emit_round_benchmarks": False,
            "required_metrics": ["client_id", "payload_hash"],
        }
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            json.dump(data, f)
            path = f.name

        policy = load_policy_from_json(path)
        self.assertEqual(policy.allowed_client_ids, ["a"])
        self.assertEqual(policy.client_public_keys["a"], "00")
        self.assertEqual(policy.signature_mode, "ed25519")
        self.assertEqual(policy.max_payload_bytes, 10)
        self.assertEqual(policy.max_epsilon_spent_per_round, 0.7)
        self.assertEqual(policy.attestation_signature_mode, "xmss")
        self.assertEqual(policy.governance_readiness_signals, ["go_live_approved"])
        self.assertFalse(policy.emit_round_benchmarks)

    def test_load_policy_with_env_key_injection(self):
        os.environ["TEST_CLIENT_KEYS_JSON"] = json.dumps({"site-a": "abc123"})
        os.environ["TEST_ATTEST_KEYS_JSON"] = json.dumps({"site-a": "def456"})
        os.environ["TEST_SIEM_URL"] = "http://127.0.0.1:9999/hook"

        data: Dict[str, Any] = {
            "allowed_client_ids": ["site-a"],
            "client_public_keys": {},
            "client_public_keys_env": "TEST_CLIENT_KEYS_JSON",
            "attestation_public_keys": {},
            "attestation_public_keys_env": "TEST_ATTEST_KEYS_JSON",
            "siem_webhook_url": "",
            "siem_webhook_url_env": "TEST_SIEM_URL",
        }
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            json.dump(data, f)
            path = f.name

        policy = load_policy_from_json(path)
        self.assertEqual(policy.client_public_keys["site-a"], "abc123")
        self.assertEqual(policy.attestation_public_keys["site-a"], "def456")
        self.assertEqual(policy.siem_webhook_url, "http://127.0.0.1:9999/hook")

    def test_nonce_store_env_overrides(self):
        os.environ["FLWR_NONCE_STORE_TYPE"] = "sqlite"
        os.environ["FLWR_NONCE_STORE_PATH"] = "./dev_nonce.db"

        data: Dict[str, Any] = {
            "allowed_client_ids": ["site-a"],
            "nonce_store_mode": "memory",
            "nonce_sqlite_path": "nonce_cache.db",
        }
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            json.dump(data, f)
            path = f.name

        policy = load_policy_from_json(path)
        self.assertEqual(policy.nonce_store_mode, "sqlite")
        self.assertEqual(policy.nonce_sqlite_path, "./dev_nonce.db")

    def test_resolve_policy_path_prefers_strict_env(self):
        os.environ["FLWR_POLICY_FILE"] = "policy.rare_disease.json"
        self.assertEqual(resolve_policy_path("fallback.json"), "policy.rare_disease.json")

    def test_load_policy_semantic_runtime_fields(self):
        data: Dict[str, Any] = {
            "allowed_client_ids": ["site-a"],
            "enable_semantic_validation": True,
            "semantic_fragment_metric_key": "semantic_fragment",
            "semantic_required_fields": [
                "entity",
                "relation",
                "role",
                "confidence",
                "provenance",
            ],
            "semantic_min_confidence": 0.8,
            "require_constraint_closure": True,
            "constraint_alignment_metric_key": "alignment_tags",
            "constraint_compiler_profile": "core_alignment_v1",
            "constraint_required_tags": ["categorical_alignment"],
            "constraint_forbidden_tags": ["unaligned"],
            "benchmark_client_eval_p95_budget_ms": 25.0,
        }
        with tempfile.NamedTemporaryFile("w", delete=False) as f:
            json.dump(data, f)
            path = f.name

        policy = load_policy_from_json(path)
        self.assertTrue(policy.enable_semantic_validation)
        self.assertEqual(policy.semantic_fragment_metric_key, "semantic_fragment")
        self.assertEqual(policy.semantic_min_confidence, 0.8)
        self.assertTrue(policy.require_constraint_closure)
        self.assertEqual(policy.constraint_compiler_profile, "core_alignment_v1")
        self.assertEqual(policy.constraint_required_tags, ["categorical_alignment"])
        self.assertEqual(policy.constraint_forbidden_tags, ["unaligned"])
        self.assertEqual(policy.benchmark_client_eval_p95_budget_ms, 25.0)

    def test_rare_disease_profile_includes_semantic_slashing(self):
        policy_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "policy.rare_disease.json",
        )
        policy = load_policy_from_json(policy_path)
        self.assertEqual(policy.constraint_compiler_profile, "core_alignment_v1")
        self.assertIn("semantic_fragment", policy.required_metrics)
        self.assertIn("alignment_tags", policy.required_metrics)
        self.assertEqual(
            policy.slash_amounts.get("SEMANTIC_FRAGMENT_INVALID"),
            20,
        )
        self.assertEqual(
            policy.slash_amounts.get("CONSTRAINT_CLOSURE_FAILED"),
            25,
        )


if __name__ == "__main__":
    unittest.main()
