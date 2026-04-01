"""Adversarial exercise: 1 benign + 2 malicious hospitals.

This simulates a staging round and verifies that malicious updates are rejected,
slashed, and eventually quarantined.
"""

from dataclasses import dataclass
from typing import Dict

from security_wrapper import SecurityPolicy, SecurityWrapperStrategy


@dataclass
class DummyFitRes:
    metrics: Dict[str, object]


class DummyStrategy:
    def aggregate_fit(self, server_round, results, failures):
        return {
            "round": server_round,
            "accepted": len(results),
            "failures": len(failures),
        }


def make_policy() -> SecurityPolicy:
    return SecurityPolicy(
        allowed_client_ids=["hospital-benign", "hospital-mal-1", "hospital-mal-2"],
        signature_mode="metric_flag",
        enable_governance_contract=True,
        slashing_enabled=True,
        strike_quarantine_threshold=2,
    )


def make_metrics(
    client_id: str,
    ok: bool = True,
    replay_nonce: str | None = None,
    epsilon: float = 0.3,
    gradient_zscore: float = 0.4,
):
    nonce = replay_nonce or f"n-{client_id}"
    return {
        "client_id": client_id,
        "signature_verified": ok,
        "attestation_ok": ok,
        "irb_approved": ok,
        "dpo_reviewed": ok,
        "data_deidentified": ok,
        "epsilon_spent": epsilon,
        "payload_size_bytes": 500,
        "nonce": nonce,
        "payload_hash": "hash-001",
        "gradient_zscore": gradient_zscore,
    }


def run_exercise() -> None:
    wrapper = SecurityWrapperStrategy(DummyStrategy(), make_policy())

    round1 = [
        ("hospital-benign", DummyFitRes(make_metrics("hospital-benign", ok=True))),
        ("hospital-mal-1", DummyFitRes(make_metrics("hospital-mal-1", ok=False))),
        ("hospital-mal-2", DummyFitRes(make_metrics("hospital-mal-2", ok=True, epsilon=1.9, gradient_zscore=7.5))),
    ]

    print("Round 1:", wrapper.aggregate_fit(1, round1, []))

    # Repeat malicious behavior to trigger quarantine
    round2 = [
        ("hospital-benign", DummyFitRes(make_metrics("hospital-benign", ok=True, replay_nonce="benign-2"))),
        ("hospital-mal-1", DummyFitRes(make_metrics("hospital-mal-1", ok=False, replay_nonce="mal-1-r2"))),
        ("hospital-mal-2", DummyFitRes(make_metrics("hospital-mal-2", ok=True, epsilon=2.5, replay_nonce="mal-2-r2", gradient_zscore=8.2))),
    ]

    print("Round 2:", wrapper.aggregate_fit(2, round2, []))
    print("Contract stakes:", wrapper.governance_contract.stakes)
    print("Contract strikes:", wrapper.governance_contract.strikes)
    print("Contract quarantined:", wrapper.governance_contract.quarantined)


if __name__ == "__main__":
    run_exercise()
