import unittest

from security_wrapper.checks import evaluate_update
from security_wrapper.policy import SecurityPolicy
from security_wrapper.rejection_codes import RejectionCode


class TestChecks(unittest.TestCase):
    def setUp(self):
        self.policy = SecurityPolicy(
            allowed_client_ids=["site-1"],
            signature_mode="metric_flag",
            required_metrics=[
                "client_id",
                "attestation_ok",
                "epsilon_spent",
                "payload_size_bytes",
                "nonce",
                "payload_hash",
                "gradient_zscore",
            ],
        )

    def test_accept_valid_update(self):
        metrics = {
            "client_id": "site-1",
            "signature_verified": True,
            "attestation_ok": True,
            "epsilon_spent": 0.4,
            "payload_size_bytes": 1000,
            "nonce": "abc-1",
            "payload_hash": "deadbeef",
            "gradient_zscore": 0.3,
        }
        ok, code = evaluate_update(metrics, self.policy, set(), server_round=1)
        self.assertTrue(ok)
        self.assertIsNone(code)

    def test_reject_replayed_nonce(self):
        metrics = {
            "client_id": "site-1",
            "signature_verified": True,
            "attestation_ok": True,
            "epsilon_spent": 0.4,
            "payload_size_bytes": 1000,
            "nonce": "dup",
            "payload_hash": "deadbeef",
            "gradient_zscore": 0.3,
        }
        seen = {(1, "dup")}
        ok, code = evaluate_update(metrics, self.policy, seen, server_round=1)
        self.assertFalse(ok)
        self.assertEqual(code, RejectionCode.NONCE_REPLAY)

    def test_reject_gradient_anomaly(self):
        metrics = {
            "client_id": "site-1",
            "signature_verified": True,
            "attestation_ok": True,
            "epsilon_spent": 0.2,
            "payload_size_bytes": 900,
            "nonce": "n-zscore",
            "payload_hash": "deadbeef",
            "gradient_zscore": 9.2,
        }
        ok, code = evaluate_update(metrics, self.policy, set(), server_round=2)
        self.assertFalse(ok)
        self.assertEqual(code, RejectionCode.POISONING_ANOMALY)

    def test_reject_missing_allowlisted_client_public_key(self):
        strict_policy = SecurityPolicy(
            allowed_client_ids=["site-1"],
            signature_mode="ed25519",
            require_attestation=False,
            require_client_public_key_allowlist=True,
            required_metrics=[
                "client_id",
                "epsilon_spent",
                "payload_size_bytes",
                "nonce",
                "payload_hash",
                "gradient_zscore",
                "signature_hex",
            ],
        )
        metrics = {
            "client_id": "site-1",
            "epsilon_spent": 0.2,
            "payload_size_bytes": 900,
            "nonce": "strict-nonce",
            "payload_hash": "deadbeef",
            "gradient_zscore": 0.1,
            "signature_hex": "abcd",
            "public_key_hex": "beef",
        }
        ok, code = evaluate_update(metrics, strict_policy, set(), server_round=2)
        self.assertFalse(ok)
        self.assertEqual(code, RejectionCode.SIGNATURE_INVALID)

    def test_reject_missing_allowlisted_attestation_key(self):
        strict_policy = SecurityPolicy(
            allowed_client_ids=["site-1"],
            signature_mode="metric_flag",
            attestation_mode="ed25519_quote",
            require_attestation=True,
            require_attestation_public_key_allowlist=True,
            required_metrics=[
                "client_id",
                "attestation_ok",
                "signature_verified",
                "epsilon_spent",
                "payload_size_bytes",
                "nonce",
                "payload_hash",
                "gradient_zscore",
                "attestation_quote_json",
                "attestation_signature_hex",
            ],
        )
        metrics = {
            "client_id": "site-1",
            "attestation_ok": True,
            "signature_verified": True,
            "epsilon_spent": 0.2,
            "payload_size_bytes": 900,
            "nonce": "strict-attest-nonce",
            "payload_hash": "deadbeef",
            "gradient_zscore": 0.1,
            "attestation_quote_json": "{}",
            "attestation_signature_hex": "abcd",
        }
        ok, code = evaluate_update(metrics, strict_policy, set(), server_round=2)
        self.assertFalse(ok)
        self.assertEqual(code, RejectionCode.ATTESTATION_FAILED)


if __name__ == "__main__":
    unittest.main()
