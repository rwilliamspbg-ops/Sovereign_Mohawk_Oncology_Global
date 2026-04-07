from dataclasses import dataclass, field
import json
import os
from typing import Dict, List


@dataclass
class SecurityPolicy:
    allowed_client_ids: List[str] = field(default_factory=list)
    client_public_keys: Dict[str, str] = field(default_factory=dict)
    client_public_keys_env: str = ""
    require_attestation: bool = True
    attestation_mode: str = "metric_flag"
    attestation_public_keys: Dict[str, str] = field(default_factory=dict)
    attestation_public_keys_env: str = ""
    attestation_max_age_seconds: int = 300
    attestation_expected_pcrs: Dict[str, str] = field(default_factory=dict)
    attestation_require_nonce_binding: bool = True
    require_signature: bool = True
    signature_mode: str = "ed25519"
    require_nonce: bool = True
    nonce_store_mode: str = "memory"
    nonce_sqlite_path: str = "nonce_cache.db"
    nonce_redis_url: str = "redis://localhost:6379/0"
    nonce_postgres_dsn: str = ""
    nonce_postgres_table: str = "seen_nonces"
    max_payload_bytes: int = 5_000_000
    max_epsilon_spent_per_round: float = 0.8
    max_gradient_zscore: float = 4.0
    min_gradient_cosine_similarity: float = 0.1
    max_krum_score: float = 15.0
    require_vector_consensus_checks: bool = True
    enable_governance_contract: bool = True
    governance_required_gates: List[str] = field(
        default_factory=lambda: [
            "irb_approved",
            "dpo_reviewed",
            "data_deidentified",
            "attestation_ok",
            "signature_verified",
            "dp_within_budget",
        ]
    )
    slashing_enabled: bool = True
    initial_stake: int = 100
    strike_quarantine_threshold: int = 3
    slash_amounts: Dict[str, int] = field(default_factory=dict)
    siem_webhook_url: str = ""
    siem_webhook_url_env: str = ""
    siem_timeout_seconds: int = 2
    siem_strike_alert_threshold: int = 3
    required_metrics: List[str] = field(
        default_factory=lambda: [
            "client_id",
            "attestation_ok",
            "epsilon_spent",
            "payload_size_bytes",
            "nonce",
            "payload_hash",
            "gradient_zscore",
        ]
    )


def load_policy_from_json(path: str) -> SecurityPolicy:
    with open(path, "r", encoding="utf-8") as f:
        data: Dict = json.load(f)

    key_env = str(data.get("client_public_keys_env", "")).strip()
    if key_env:
        raw = os.getenv(key_env, "{}")
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                data["client_public_keys"] = {str(k): str(v) for k, v in parsed.items()}
        except json.JSONDecodeError:
            pass

    attest_env = str(data.get("attestation_public_keys_env", "")).strip()
    if attest_env:
        raw = os.getenv(attest_env, "{}")
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                data["attestation_public_keys"] = {
                    str(k): str(v) for k, v in parsed.items()
                }
        except json.JSONDecodeError:
            pass

    siem_env = str(data.get("siem_webhook_url_env", "")).strip()
    if siem_env:
        data["siem_webhook_url"] = os.getenv(
            siem_env, str(data.get("siem_webhook_url", ""))
        )

    return SecurityPolicy(**data)
