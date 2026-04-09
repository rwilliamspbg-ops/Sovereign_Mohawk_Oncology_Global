import unittest

from security_wrapper.governance_contract import GovernanceGateContract
from security_wrapper.rejection_codes import RejectionCode


class TestGovernanceContract(unittest.TestCase):
    def test_governance_accepts_when_required_gates_pass(self):
        contract = GovernanceGateContract()
        metrics = {
            "irb_approved": True,
            "dpo_reviewed": True,
            "data_deidentified": True,
            "attestation_ok": True,
            "signature_verified": True,
            "epsilon_spent": 0.2,
        }
        decision = contract.evaluate("site-1", metrics, dp_limit=0.8)
        self.assertTrue(decision.accepted)

    def test_slashing_and_quarantine(self):
        contract = GovernanceGateContract(strike_quarantine_threshold=2)
        state1 = contract.slash("site-9", RejectionCode.SIGNATURE_INVALID)
        state2 = contract.slash("site-9", RejectionCode.NONCE_REPLAY)
        self.assertEqual(state1["strikes"], 1)
        self.assertEqual(state2["strikes"], 2)
        self.assertTrue(state2["quarantined"])

    def test_readiness_signals_can_be_required(self):
        contract = GovernanceGateContract(
            readiness_required_signals=["transport_kex_ready", "go_live_approved"]
        )
        metrics = {
            "irb_approved": True,
            "dpo_reviewed": True,
            "data_deidentified": True,
            "attestation_ok": True,
            "signature_verified": True,
            "epsilon_spent": 0.2,
            "transport_kex_ready": True,
            "go_live_approved": False,
        }
        decision = contract.evaluate("site-2", metrics, dp_limit=0.8)
        self.assertFalse(decision.accepted)
        self.assertIn("readiness:go_live_approved", decision.reason)


if __name__ == "__main__":
    unittest.main()
