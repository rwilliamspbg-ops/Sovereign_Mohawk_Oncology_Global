import unittest
from typing import Any, Dict, List

from security_wrapper.policy import SecurityPolicy
from security_wrapper.replay import replay_semantic_updates
from security_wrapper.rejection_codes import RejectionCode


class TestSemanticReplayDeterminism(unittest.TestCase):
    def _build_policy(self) -> SecurityPolicy:
        return SecurityPolicy(
            allowed_client_ids=["site-1"],
            signature_mode="metric_flag",
            enable_governance_contract=False,
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

    def test_replay_is_deterministic(self):
        policy = self._build_policy()
        updates: List[Dict[str, Any]] = [
            {
                "client_id": "site-1",
                "signature_verified": True,
                "attestation_ok": True,
                "irb_approved": True,
                "dpo_reviewed": True,
                "data_deidentified": True,
                "epsilon_spent": 0.2,
                "dp_limit": 0.25,
                "payload_size_bytes": 1024,
                "nonce": "n-1",
                "payload_hash": "h-1",
                "gradient_zscore": 0.1,
                "alignment_tags": [
                    "categorical_alignment",
                    "closure_verified",
                    "oncology_safe",
                    "privacy_preserved",
                    "irb_validated",
                    "dpo_reviewed",
                ],
                "semantic_fragment": {
                    "entity": "tumor_grade",
                    "relation": "supports",
                    "role": "feature",
                    "confidence": 0.95,
                    "provenance": "site-1-cohort-2026q2",
                },
            },
            {
                "client_id": "site-1",
                "signature_verified": True,
                "attestation_ok": False,
                "irb_approved": True,
                "dpo_reviewed": True,
                "data_deidentified": True,
                "epsilon_spent": 0.3,
                "dp_limit": 0.25,
                "payload_size_bytes": 1024,
                "nonce": "n-2",
                "payload_hash": "h-2",
                "gradient_zscore": 0.2,
                "alignment_tags": [
                    "categorical_alignment",
                    "closure_verified",
                    "oncology_safe",
                ],
                "semantic_fragment": {
                    "entity": "tumor_grade",
                    "relation": "supports",
                    "role": "feature",
                    "confidence": 0.91,
                    "provenance": "site-1-cohort-2026q2",
                },
            },
        ]

        first = replay_semantic_updates(updates, policy, server_round=7)
        second = replay_semantic_updates(updates, policy, server_round=7)

        self.assertEqual(first, second)
        self.assertEqual(first[0], (True, None))
        self.assertEqual(
            first[1], (False, RejectionCode.CONSTRAINT_CLOSURE_FAILED.value)
        )


if __name__ == "__main__":
    unittest.main()
