"""
Example Flower server wiring with security wrapper.

This file is intentionally lightweight and can be adapted to your runtime.
"""

from security_wrapper import build_secure_fedavg


def build_secure_strategy(policy_path: str = "policy.example.json"):
    return build_secure_fedavg(
        policy_path=policy_path,
        fraction_fit=1.0,
        fraction_evaluate=0.0,
        min_fit_clients=2,
        min_available_clients=2,
    )


if __name__ == "__main__":
    strategy = build_secure_strategy()
    print("Secure strategy wrapper ready:", strategy)
