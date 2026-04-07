from typing import Any

from .audit import AuditLogger
from .policy import SecurityPolicy, load_policy_from_json
from .wrapper import SecurityWrapperStrategy


class SecurityFedAvgStrategy(SecurityWrapperStrategy):
    """Concrete Flower FedAvg integration with security wrapper.

    Requires `flwr` at runtime. Pass FedAvg constructor kwargs to this class.
    """

    def __init__(
        self,
        policy: SecurityPolicy,
        audit_logger: AuditLogger | None = None,
        **fedavg_kwargs: Any,
    ) -> None:
        try:
            from flwr.server.strategy import FedAvg
        except ImportError as exc:
            raise ImportError("flwr is required to use SecurityFedAvgStrategy") from exc

        inner_strategy = FedAvg(**fedavg_kwargs)
        super().__init__(
            inner_strategy=inner_strategy, policy=policy, audit_logger=audit_logger
        )


def build_secure_fedavg(
    policy_path: str,
    audit_path: str = "security_audit.jsonl",
    **fedavg_kwargs: Any,
) -> SecurityFedAvgStrategy:
    policy = load_policy_from_json(policy_path)
    audit_logger = AuditLogger(audit_path)
    return SecurityFedAvgStrategy(
        policy=policy, audit_logger=audit_logger, **fedavg_kwargs
    )
