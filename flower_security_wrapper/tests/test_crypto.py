import unittest

from security_wrapper.crypto import Ed25519Verifier, build_signature_message


class TestCryptoHelpers(unittest.TestCase):
    def test_message_format(self):
        msg = build_signature_message("site-1", 7, "nonce-1", "abcd")
        self.assertEqual(msg.decode("utf-8"), "site-1|7|nonce-1|abcd")

    def test_verifier_unavailable_or_invalid_input_fails_closed(self):
        verifier = Ed25519Verifier()
        ok = verifier.verify_hex("00", b"msg", "00")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
