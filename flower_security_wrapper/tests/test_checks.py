import unittest
from typing import Any, Dict

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
        metrics: Dict[str, Any] = {
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
        metrics: Dict[str, Any] = {
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
        metrics: Dict[str, Any] = {
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
        metrics: Dict[str, Any] = {
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
        metrics: Dict[str, Any] = {
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

    def test_accept_semantic_fragment_with_constraint_closure(self):
        semantic_policy = SecurityPolicy(
            allowed_client_ids=["site-1"],
            signature_mode="metric_flag",
            enable_semantic_validation=True,
            require_constraint_closure=True,
            constraint_required_tags=["categorical_alignment", "closure_verified"],
            constraint_forbidden_tags=["unaligned"],
            required_metrics=[
                "client_id",
                "attestation_ok",
                "epsilon_spent",
                "payload_size_bytes",
                "nonce",
                "payload_hash",
                "gradient_zscore",
                "semantic_fragment",
                "alignment_tags",
            ],
        )
        metrics: Dict[str, Any] = {
            "client_id": "site-1",
            "signature_verified": True,
            "attestation_ok": True,
            "epsilon_spent": 0.1,
            "payload_size_bytes": 700,
            "nonce": "semantic-ok",
            "payload_hash": "deadbeef",
            "gradient_zscore": 0.1,
            "alignment_tags": ["categorical_alignment", "closure_verified"],
            "semantic_fragment": {
                "entity": "tumor_subtype",
                "relation": "supports",
                "role": "feature",
                "confidence": 0.93,
                "provenance": "trial-cohort-a",
            },
        }

        ok, code = evaluate_update(metrics, semantic_policy, set(), server_round=3)
        self.assertTrue(ok)
        self.assertIsNone(code)

    def test_reject_semantic_fragment_when_closure_missing_required_tag(self):
        semantic_policy = SecurityPolicy(
            allowed_client_ids=["site-1"],
            signature_mode="metric_flag",
            enable_semantic_validation=True,
            require_constraint_closure=True,
            constraint_required_tags=["categorical_alignment", "closure_verified"],
            required_metrics=[
                "client_id",
                "attestation_ok",
                "epsilon_spent",
                "payload_size_bytes",
                "nonce",
                "payload_hash",
                "gradient_zscore",
                "semantic_fragment",
                "alignment_tags",
            ],
        )
        metrics: Dict[str, Any] = {
            "client_id": "site-1",
            "signature_verified": True,
            "attestation_ok": True,
            "epsilon_spent": 0.1,
            "payload_size_bytes": 700,
            "nonce": "semantic-fail",
            "payload_hash": "deadbeef",
            "gradient_zscore": 0.1,
            "alignment_tags": ["categorical_alignment"],
            "semantic_fragment": {
                "entity": "tumor_subtype",
                "relation": "supports",
                "role": "feature",
                "confidence": 0.93,
                "provenance": "trial-cohort-a",
            },
        }

        ok, code = evaluate_update(metrics, semantic_policy, set(), server_round=4)
        self.assertFalse(ok)
        self.assertEqual(code, RejectionCode.CONSTRAINT_CLOSURE_FAILED)

    def test_constraint_compiler_core_alignment_profile_autofills_required_tags(self):
        semantic_policy = SecurityPolicy(
            allowed_client_ids=["site-1"],
            signature_mode="metric_flag",
            enable_semantic_validation=True,
            require_constraint_closure=True,
            constraint_compiler_profile="core_alignment_v1",
            constraint_required_tags=["oncology_safe"],
            required_metrics=[
                "client_id",
                "attestation_ok",
                "signature_verified",
                "irb_approved",
                "dpo_reviewed",
                "data_deidentified",
                "epsilon_spent",
                "payload_size_bytes",
                "nonce",
                "payload_hash",
                "gradient_zscore",
                "semantic_fragment",
                "alignment_tags",
            ],
        )

        metrics: Dict[str, Any] = {
            "client_id": "site-1",
            "signature_verified": True,
            "attestation_ok": True,
            "irb_approved": True,
            "dpo_reviewed": True,
            "data_deidentified": True,
            "epsilon_spent": 0.2,
            "dp_limit": 0.25,
            "payload_size_bytes": 700,
            "nonce": "compiled-ok",
            "payload_hash": "deadbeef",
            "gradient_zscore": 0.1,
            "alignment_tags": ["oncology_safe"],
            "semantic_fragment": {
                "entity": "tumor_subtype",
                "relation": "supports",
                "role": "feature",
                "confidence": 0.93,
                "provenance": "trial-cohort-a",
            },
        }

        ok, code = evaluate_update(metrics, semantic_policy, set(), server_round=5)
        self.assertTrue(ok)
        self.assertIsNone(code)

    def test_constraint_compiler_blocks_forbidden_tag_state(self):
        semantic_policy = SecurityPolicy(
            allowed_client_ids=["site-1"],
            signature_mode="metric_flag",
            enable_semantic_validation=True,
            require_constraint_closure=True,
            constraint_compiler_profile="core_alignment_v1",
            constraint_required_tags=["oncology_safe"],
            required_metrics=[
                "client_id",
                "attestation_ok",
                "signature_verified",
                "irb_approved",
                "dpo_reviewed",
                "data_deidentified",
                "epsilon_spent",
                "payload_size_bytes",
                "nonce",
                "payload_hash",
                "gradient_zscore",
                "semantic_fragment",
                "alignment_tags",
            ],
        )

        metrics: Dict[str, Any] = {
            "client_id": "site-1",
            "signature_verified": True,
            "attestation_ok": False,
            "irb_approved": True,
            "dpo_reviewed": True,
            "data_deidentified": True,
            "epsilon_spent": 0.2,
            "dp_limit": 0.25,
            "payload_size_bytes": 700,
            "nonce": "compiled-fail",
            "payload_hash": "deadbeef",
            "gradient_zscore": 0.1,
            "alignment_tags": [
                "oncology_safe",
                "categorical_alignment",
                "closure_verified",
                "privacy_preserved",
                "irb_validated",
                "dpo_reviewed",
            ],
            "semantic_fragment": {
                "entity": "tumor_subtype",
                "relation": "supports",
                "role": "feature",
                "confidence": 0.93,
                "provenance": "trial-cohort-a",
            },
        }

        ok, code = evaluate_update(metrics, semantic_policy, set(), server_round=6)
        self.assertFalse(ok)
        self.assertEqual(code, RejectionCode.CONSTRAINT_CLOSURE_FAILED)


if __name__ == "__main__":
    unittest.main()
