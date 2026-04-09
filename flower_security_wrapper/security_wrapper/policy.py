from dataclasses import dataclass, field
import json
import os
from typing import Dict, List


@dataclass
class SecurityPolicy:
    allowed_client_ids: List[str] = field(default_factory=list)
    client_public_keys: Dict[str, str] = field(default_factory=dict)
    client_public_keys_env: str = ""
    require_client_public_key_allowlist: bool = False
    require_attestation: bool = True
    attestation_mode: str = "metric_flag"
    attestation_signature_mode: str = "any"
    allow_attestation_metric_fallback: bool = True
    attestation_public_keys: Dict[str, str] = field(default_factory=dict)
    attestation_public_keys_env: str = ""
    require_attestation_public_key_allowlist: bool = False
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
    governance_readiness_signals: List[str] = field(default_factory=list)
    slashing_enabled: bool = True
    initial_stake: int = 100
    strike_quarantine_threshold: int = 3
    slash_amounts: Dict[str, int] = field(default_factory=dict)
    siem_webhook_url: str = ""
    siem_webhook_url_env: str = ""
    siem_timeout_seconds: int = 2
    siem_strike_alert_threshold: int = 3
    emit_round_benchmarks: bool = True
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


def _load_json_env_map(env_var: str) -> Dict[str, str]:
    raw = os.getenv(env_var, "{}")
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return {str(k): str(v) for k, v in parsed.items()}
    except json.JSONDecodeError:
        pass
    return {}


def _apply_env_overrides(data: Dict) -> None:
    nonce_mode = os.getenv("FLWR_NONCE_STORE_TYPE", "").strip()
    if nonce_mode:
        data["nonce_store_mode"] = nonce_mode

    sqlite_path = os.getenv("FLWR_NONCE_STORE_PATH", "").strip()
    if sqlite_path:
        data["nonce_sqlite_path"] = sqlite_path

    redis_url = os.getenv("FLWR_NONCE_REDIS_URL", "").strip()
    if redis_url:
        data["nonce_redis_url"] = redis_url

    pg_dsn = os.getenv("FLWR_NONCE_POSTGRES_DSN", "").strip()
    if pg_dsn:
        data["nonce_postgres_dsn"] = pg_dsn

    pg_table = os.getenv("FLWR_NONCE_POSTGRES_TABLE", "").strip()
    if pg_table:
        data["nonce_postgres_table"] = pg_table


def resolve_policy_path(default_path: str = "policy.rare_disease.json") -> str:
    return (
        os.getenv("FLWR_POLICY_FILE", "").strip()
        or os.getenv("FLWR_RD_POLICY_FILE", "").strip()
        or default_path
    )


def load_policy_from_json(path: str) -> SecurityPolicy:
    with open(path, "r", encoding="utf-8") as f:
        data: Dict = json.load(f)

    key_env = str(data.get("client_public_keys_env", "")).strip()
    if key_env:
        data["client_public_keys"] = _load_json_env_map(key_env)

    attest_env = str(data.get("attestation_public_keys_env", "")).strip()
    if attest_env:
        data["attestation_public_keys"] = _load_json_env_map(attest_env)

    siem_env = str(data.get("siem_webhook_url_env", "")).strip()
    if siem_env:
        data["siem_webhook_url"] = os.getenv(
            siem_env, str(data.get("siem_webhook_url", ""))
        )

    _apply_env_overrides(data)

    return SecurityPolicy(**data)


def load_policy(path: str | None = None) -> SecurityPolicy:
    return load_policy_from_json(path or resolve_policy_path())
