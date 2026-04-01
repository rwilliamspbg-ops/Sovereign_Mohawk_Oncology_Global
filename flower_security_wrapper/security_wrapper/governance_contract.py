from dataclasses import dataclass
from typing import Dict, List, Optional

from .rejection_codes import RejectionCode


@dataclass
class GovernanceDecision:
    accepted: bool
    reason: str
    gates: Dict[str, bool]


class GovernanceGateContract:
    """Smart-contract-like gate evaluator and slashing ledger.

    This contract codifies governance checks so update admission is deterministic
    and does not depend on synchronous human review during a training round.
    """

    def __init__(
        self,
        required_gates: Optional[List[str]] = None,
        initial_stake: int = 100,
        slash_amounts: Optional[Dict[str, int]] = None,
        strike_quarantine_threshold: int = 3,
    ) -> None:
        self.required_gates = required_gates or [
            "irb_approved",
            "dpo_reviewed",
            "data_deidentified",
            "attestation_ok",
            "signature_verified",
            "dp_within_budget",
        ]
        self.default_stake = initial_stake
        self.stakes: Dict[str, int] = {}
        self.strikes: Dict[str, int] = {}
        self.quarantined: Dict[str, bool] = {}
        self.strike_quarantine_threshold = strike_quarantine_threshold
        self.slash_amounts = slash_amounts or {
            RejectionCode.SIGNATURE_INVALID.value: 20,
            RejectionCode.ATTESTATION_FAILED.value: 25,
            RejectionCode.NONCE_REPLAY.value: 15,
            RejectionCode.DP_BUDGET_EXCEEDED.value: 10,
            RejectionCode.POISONING_ANOMALY.value: 30,
            RejectionCode.CLIENT_NOT_ALLOWED.value: 12,
        }

    def _ensure_client(self, client_id: str) -> None:
        if client_id not in self.stakes:
            self.stakes[client_id] = self.default_stake
            self.strikes[client_id] = 0
            self.quarantined[client_id] = False

    def evaluate(self, client_id: str, metrics: Dict[str, object], dp_limit: float) -> GovernanceDecision:
        self._ensure_client(client_id)
        if self.quarantined.get(client_id, False):
            return GovernanceDecision(False, "client_quarantined", {"client_quarantined": True})

        gates: Dict[str, bool] = {
            "irb_approved": bool(metrics.get("irb_approved", False)),
            "dpo_reviewed": bool(metrics.get("dpo_reviewed", False)),
            "data_deidentified": bool(metrics.get("data_deidentified", False)),
            "attestation_ok": bool(metrics.get("attestation_ok", False)),
            "signature_verified": bool(metrics.get("signature_verified", False)),
            "dp_within_budget": float(metrics.get("epsilon_spent", 999)) <= dp_limit,
            # Human reviewer is asynchronous evidence and not a hard gate.
            "human_review_async": True,
        }

        failed = [name for name in self.required_gates if not gates.get(name, False)]
        if failed:
            return GovernanceDecision(False, f"failed_gates:{','.join(failed)}", gates)

        return GovernanceDecision(True, "accepted", gates)

    def slash(self, client_id: str, rejection_code: RejectionCode) -> Dict[str, int | bool]:
        self._ensure_client(client_id)
        reason = rejection_code.value
        penalty = self.slash_amounts.get(reason, 5)
        self.stakes[client_id] = max(0, self.stakes[client_id] - penalty)
        self.strikes[client_id] += 1
        if self.strikes[client_id] >= self.strike_quarantine_threshold:
            self.quarantined[client_id] = True

        return {
            "stake": self.stakes[client_id],
            "strikes": self.strikes[client_id],
            "quarantined": self.quarantined[client_id],
        }

    def reward(self, client_id: str, amount: int = 1) -> Dict[str, int | bool]:
        self._ensure_client(client_id)
        self.stakes[client_id] += amount
        return {
            "stake": self.stakes[client_id],
            "strikes": self.strikes[client_id],
            "quarantined": self.quarantined[client_id],
        }
