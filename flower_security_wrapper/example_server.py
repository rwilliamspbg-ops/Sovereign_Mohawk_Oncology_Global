"""
Example Flower server wiring with security wrapper.

This file is intentionally lightweight and can be adapted to your runtime.
"""

import os

from security_wrapper import build_secure_fedavg
from security_wrapper.policy import resolve_policy_path


def build_secure_strategy(policy_path: str | None = None):
    selected_policy = policy_path or resolve_policy_path("policy.rare_disease.json")
    return build_secure_fedavg(
        policy_path=selected_policy,
        fraction_fit=1.0,
        fraction_evaluate=0.0,
        min_fit_clients=2,
        min_available_clients=2,
    )


if __name__ == "__main__":
    strategy = build_secure_strategy(os.getenv("FLWR_POLICY_FILE"))
    print("Secure strategy wrapper ready:", strategy)
