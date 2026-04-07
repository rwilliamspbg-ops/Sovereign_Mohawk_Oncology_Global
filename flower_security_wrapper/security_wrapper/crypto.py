class Ed25519Verifier:
    """Ed25519 signature verification helper.

    Uses `cryptography` if available. If unavailable, verification fails closed.
    """

    def __init__(self) -> None:
        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import (
                Ed25519PublicKey,
            )
        except ImportError:
            self._public_key_cls = None
        else:
            self._public_key_cls = Ed25519PublicKey

    @property
    def available(self) -> bool:
        return self._public_key_cls is not None

    def verify_hex(
        self, public_key_hex: str, message: bytes, signature_hex: str
    ) -> bool:
        if not self.available:
            return False
        try:
            public_key_bytes = bytes.fromhex(public_key_hex)
            signature_bytes = bytes.fromhex(signature_hex)
            public_key = self._public_key_cls.from_public_bytes(public_key_bytes)
            public_key.verify(signature_bytes, message)
            return True
        except Exception:
            return False


def build_signature_message(
    client_id: str,
    server_round: int,
    nonce: str,
    payload_hash: str,
) -> bytes:
    return f"{client_id}|{server_round}|{nonce}|{payload_hash}".encode("utf-8")
