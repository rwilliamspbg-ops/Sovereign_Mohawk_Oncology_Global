from typing import Any, Dict, List, Sequence, Set, Tuple

from .checks import evaluate_update
from .policy import SecurityPolicy
from .rejection_codes import RejectionCode


def replay_semantic_updates(
    updates: Sequence[Dict[str, Any]],
    policy: SecurityPolicy,
    server_round: int,
) -> List[Tuple[bool, str | None]]:
    """Replay updates through admission checks and return deterministic outcomes."""
    seen_round_nonces: Set[Tuple[int, str]] = set()
    outcomes: List[Tuple[bool, str | None]] = []

    for metrics in updates:
        ok, rejection = evaluate_update(
            metrics,
            policy,
            seen_round_nonces,
            server_round=server_round,
        )
        code = rejection.value if isinstance(rejection, RejectionCode) else None
        outcomes.append((ok, code))

    return outcomes
