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


if __name__ == "__main__":
    unittest.main()
