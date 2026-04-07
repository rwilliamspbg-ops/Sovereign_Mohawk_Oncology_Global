import json
import time
from typing import Dict

from .crypto import Ed25519Verifier


class AttestationVerifier:
    """Attestation verifier with mode-based enforcement.

    Modes:
    - metric_flag: trusts boolean `attestation_ok`
    - ed25519_quote: verifies signed quote payload and freshness
    """

    def __init__(
        self,
        mode: str = "metric_flag",
        max_age_seconds: int = 300,
        expected_pcrs: Dict[str, str] | None = None,
        require_nonce_binding: bool = True,
    ) -> None:
        self.mode = mode
        self.max_age_seconds = max_age_seconds
        self.expected_pcrs = expected_pcrs or {}
        self.require_nonce_binding = require_nonce_binding
        self.signature_verifier = Ed25519Verifier()

    def _parse_and_validate_tpm_quote(
        self, quote_json: str, client_id: str, round_nonce: str
    ) -> bool:
        try:
            parsed = json.loads(quote_json)
            ts = int(parsed.get("quote_ts", 0))
            quote_client = str(parsed.get("client_id", ""))
            quote_nonce = str(parsed.get("nonce", ""))
            quote_pcrs = parsed.get("pcrs", {})
            if not isinstance(quote_pcrs, dict):
                return False
        except Exception:
            return False

        if quote_client != client_id:
            return False
        if abs(int(time.time()) - ts) > self.max_age_seconds:
            return False
        if self.require_nonce_binding and (
            not quote_nonce or quote_nonce != round_nonce
        ):
            return False

        for pcr_idx, expected_value in self.expected_pcrs.items():
            if str(quote_pcrs.get(pcr_idx, "")) != str(expected_value):
                return False
        return True

    def verify(
        self,
        metrics: Dict[str, object],
        client_id: str,
        attestation_public_key_hex: str | None = None,
    ) -> bool:
        if self.mode == "metric_flag":
            return bool(metrics.get("attestation_ok", False))

        if self.mode != "ed25519_quote":
            return False

        quote_json = str(metrics.get("attestation_quote_json", ""))
        sig_hex = str(metrics.get("attestation_signature_hex", ""))
        key_hex = attestation_public_key_hex or str(
            metrics.get("attestation_public_key_hex", "")
        )
        round_nonce = str(metrics.get("nonce", ""))

        if not quote_json or not sig_hex or not key_hex:
            return False

        if not self._parse_and_validate_tpm_quote(quote_json, client_id, round_nonce):
            return False

        return self.signature_verifier.verify_hex(
            public_key_hex=key_hex,
            message=quote_json.encode("utf-8"),
            signature_hex=sig_hex,
        )
