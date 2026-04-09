import json
import time
import unittest

from security_wrapper.attestation import AttestationVerifier, normalize_attestation_mode


class TestAttestationVerifier(unittest.TestCase):
    def test_mode_aliases_normalize(self):
        self.assertEqual(normalize_attestation_mode("metric"), "metric_flag")
        self.assertEqual(normalize_attestation_mode("tpm_quote"), "ed25519_quote")
        self.assertEqual(normalize_attestation_mode("unknown"), "invalid")

    def test_metric_flag_mode(self):
        verifier = AttestationVerifier(mode="metric_flag")
        self.assertTrue(verifier.verify({"attestation_ok": True}, "site-1"))
        self.assertFalse(verifier.verify({"attestation_ok": False}, "site-1"))

    def test_quote_signature_mode_mismatch_rejected(self):
        verifier = AttestationVerifier(
            mode="tpm_quote",
            signature_mode="xmss",
            expected_pcrs={"0": "abc"},
            require_nonce_binding=True,
        )
        quote = {
            "client_id": "site-1",
            "quote_ts": int(time.time()),
            "nonce": "n-1",
            "pcrs": {"0": "abc"},
            "signature_algo": "rsa",
        }
        metrics = {
            "nonce": "n-1",
            "attestation_quote_json": json.dumps(quote),
            "attestation_signature_hex": "00",
            "attestation_public_key_hex": "00",
        }
        self.assertFalse(verifier.verify(metrics, "site-1"))

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
