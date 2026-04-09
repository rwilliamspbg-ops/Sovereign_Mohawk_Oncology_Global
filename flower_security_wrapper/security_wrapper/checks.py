from typing import Any, Dict, Optional, Set, Tuple

from .attestation import AttestationVerifier
from .crypto import Ed25519Verifier, build_signature_message
from .nonce_store import NonceStore
from .policy import SecurityPolicy
from .rejection_codes import RejectionCode


def check_required_metrics(
    metrics: Dict[str, Any], policy: SecurityPolicy
) -> Optional[RejectionCode]:
    for key in policy.required_metrics:
        if key not in metrics:
            return RejectionCode.MISSING_REQUIRED_METRIC
    return None


def check_client_allowlist(
    metrics: Dict[str, Any], policy: SecurityPolicy
) -> Optional[RejectionCode]:
    if not policy.allowed_client_ids:
        return None
    if str(metrics.get("client_id")) not in policy.allowed_client_ids:
        return RejectionCode.CLIENT_NOT_ALLOWED
    return None


def check_signature(
    metrics: Dict[str, Any],
    policy: SecurityPolicy,
    server_round: int,
    verifier: Ed25519Verifier,
) -> Optional[RejectionCode]:
    if not policy.require_signature:
        return None

    if policy.signature_mode == "metric_flag":
        if not bool(metrics.get("signature_verified", False)):
            return RejectionCode.SIGNATURE_INVALID
        return None

    if policy.signature_mode != "ed25519":
        return RejectionCode.POLICY_ERROR

    client_id = str(metrics.get("client_id", ""))
    nonce = str(metrics.get("nonce", ""))
    payload_hash = str(metrics.get("payload_hash", ""))
    signature_hex = str(metrics.get("signature_hex", ""))
    allowlisted_key = policy.client_public_keys.get(client_id)
    if policy.require_client_public_key_allowlist and not allowlisted_key:
        return RejectionCode.SIGNATURE_INVALID
    public_key_hex = allowlisted_key or str(metrics.get("public_key_hex", ""))

    if (
        not client_id
        or not nonce
        or not payload_hash
        or not signature_hex
        or not public_key_hex
    ):
        return RejectionCode.SIGNATURE_INVALID

    message = build_signature_message(
        client_id=client_id,
        server_round=server_round,
        nonce=nonce,
        payload_hash=payload_hash,
    )
    if not verifier.verify_hex(
        public_key_hex=public_key_hex, message=message, signature_hex=signature_hex
    ):
        return RejectionCode.SIGNATURE_INVALID
    return None


def check_attestation(
    metrics: Dict[str, Any],
    policy: SecurityPolicy,
    verifier: AttestationVerifier,
) -> Optional[RejectionCode]:
    if not policy.require_attestation:
        return None
    client_id = str(metrics.get("client_id", ""))
    pubkey = policy.attestation_public_keys.get(client_id)
    if policy.require_attestation_public_key_allowlist and not pubkey:
        return RejectionCode.ATTESTATION_FAILED
    if not verifier.verify(
        metrics=metrics, client_id=client_id, attestation_public_key_hex=pubkey
    ):
        return RejectionCode.ATTESTATION_FAILED
    return None


def check_nonce_replay(
    metrics: Dict[str, Any],
    policy: SecurityPolicy,
    seen_round_nonces: Set[Tuple[int, str]],
    server_round: int,
    nonce_store: Optional[NonceStore] = None,
) -> Optional[RejectionCode]:
    if not policy.require_nonce:
        return None
    nonce = str(metrics.get("nonce", ""))
    if not nonce:
        return RejectionCode.NONCE_REPLAY

    if nonce_store is not None:
        if nonce_store.seen(server_round, nonce):
            return RejectionCode.NONCE_REPLAY
        return None

    if (server_round, nonce) in seen_round_nonces:
        return RejectionCode.NONCE_REPLAY
    return None


def check_poisoning_anomaly(
    metrics: Dict[str, Any], policy: SecurityPolicy
) -> Optional[RejectionCode]:
    try:
        z = float(metrics.get("gradient_zscore", 0.0))
    except (TypeError, ValueError):
        return RejectionCode.POISONING_ANOMALY
    if abs(z) > policy.max_gradient_zscore:
        return RejectionCode.POISONING_ANOMALY
    return None


def check_dp_budget(
    metrics: Dict[str, Any], policy: SecurityPolicy
) -> Optional[RejectionCode]:
    try:
        epsilon = float(metrics.get("epsilon_spent", 999))
    except (TypeError, ValueError):
        return RejectionCode.DP_BUDGET_EXCEEDED
    if epsilon > policy.max_epsilon_spent_per_round:
        return RejectionCode.DP_BUDGET_EXCEEDED
    return None


def check_payload_size(
    metrics: Dict[str, Any], policy: SecurityPolicy
) -> Optional[RejectionCode]:
    try:
        payload_size = int(
            metrics.get("payload_size_bytes", policy.max_payload_bytes + 1)
        )
    except (TypeError, ValueError):
        return RejectionCode.PAYLOAD_TOO_LARGE
    if payload_size > policy.max_payload_bytes:
        return RejectionCode.PAYLOAD_TOO_LARGE
    return None


def evaluate_update(
    metrics: Dict[str, Any],
    policy: SecurityPolicy,
    seen_round_nonces: Set[Tuple[int, str]],
    server_round: int,
    verifier: Optional[Ed25519Verifier] = None,
    attestation_verifier: Optional[AttestationVerifier] = None,
    nonce_store: Optional[NonceStore] = None,
) -> Tuple[bool, Optional[RejectionCode]]:
    verifier = verifier or Ed25519Verifier()
    attestation_verifier = attestation_verifier or AttestationVerifier(
        mode=policy.attestation_mode,
        max_age_seconds=policy.attestation_max_age_seconds,
        signature_mode=policy.attestation_signature_mode,
        allow_metric_fallback=policy.allow_attestation_metric_fallback,
    )

    checks = [
        check_required_metrics,
        check_client_allowlist,
        check_dp_budget,
        check_payload_size,
        check_poisoning_anomaly,
    ]

    for check in checks:
        code = check(metrics, policy)
        if code is not None:
            return False, code

    attestation_code = check_attestation(metrics, policy, verifier=attestation_verifier)
    if attestation_code is not None:
        return False, attestation_code

    signature_code = check_signature(
        metrics, policy, server_round=server_round, verifier=verifier
    )
    if signature_code is not None:
        return False, signature_code

    nonce_code = check_nonce_replay(
        metrics, policy, seen_round_nonces, server_round, nonce_store=nonce_store
    )
    if nonce_code is not None:
        return False, nonce_code

    nonce = str(metrics["nonce"])
    if nonce_store is not None:
        nonce_store.add(server_round, nonce)
    else:
        seen_round_nonces.add((server_round, nonce))
    return True, None
