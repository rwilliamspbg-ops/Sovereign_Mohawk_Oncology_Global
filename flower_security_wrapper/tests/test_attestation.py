import json
import time
import unittest

from security_wrapper.attestation import AttestationVerifier


class TestAttestationVerifier(unittest.TestCase):
    def test_metric_flag_mode(self):
        verifier = AttestationVerifier(mode="metric_flag")
        self.assertTrue(verifier.verify({"attestation_ok": True}, "site-1"))
        self.assertFalse(verifier.verify({"attestation_ok": False}, "site-1"))

    def test_ed25519_quote_fails_without_valid_signature(self):
        verifier = AttestationVerifier(
            mode="ed25519_quote",
            expected_pcrs={"0": "abc"},
            require_nonce_binding=True,
        )
        quote = {
            "client_id": "site-1",
            "quote_ts": int(time.time()),
            "nonce": "n-1",
            "pcrs": {"0": "abc"},
        }
        metrics = {
            "nonce": "n-1",
            "attestation_quote_json": json.dumps(quote),
            "attestation_signature_hex": "00",
            "attestation_public_key_hex": "00",
        }
        self.assertFalse(verifier.verify(metrics, "site-1"))


if __name__ == "__main__":
    unittest.main()
