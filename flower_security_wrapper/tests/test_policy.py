import json
import os
import tempfile
import unittest

from security_wrapper.policy import load_policy_from_json, resolve_policy_path


class TestPolicyLoading(unittest.TestCase):
    def test_load_policy_json(self):
        data = {
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

        data = {
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

        data = {
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


if __name__ == "__main__":
    unittest.main()
