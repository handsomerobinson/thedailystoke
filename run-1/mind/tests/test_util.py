import unittest

from mind.util import FakeClock, redact, redact_obj, tokenize, truncate, validate_user_id, estimate_tokens


class UtilTests(unittest.TestCase):
    def test_redact_masks_keys(self):
        s = redact("key sk-ant-abcdefgh12345678 and Bearer abcdefghijklmnop and api_key=supersecret1")
        self.assertNotIn("abcdefgh12345678", s)
        self.assertNotIn("abcdefghijklmnop", s)
        self.assertNotIn("supersecret1", s)
        self.assertIn("[REDACTED]", s)

    def test_redact_obj_masks_secret_named_fields(self):
        self.assertEqual(redact_obj({"api_key": "x", "n": 1})["api_key"], "[REDACTED]")

    def test_truncate(self):
        self.assertEqual(truncate("abc", 5), "abc")
        self.assertTrue(truncate("a" * 20, 5).startswith("aaaaa…"))

    def test_tokenize_splits_snake_case_and_drops_stopwords(self):
        toks = tokenize("Write the function is_palindrome")
        self.assertIn("is_palindrome", toks)
        self.assertIn("palindrome", toks)
        self.assertNotIn("the", toks)

    def test_fake_clock(self):
        c = FakeClock(100)
        c.sleep(5)
        self.assertEqual(c.now(), 105)

    def test_user_id_validation(self):
        self.assertEqual(validate_user_id("alice@x.org"), "alice@x.org")
        for bad in ["", "../etc", "a b", "x" * 65]:
            with self.assertRaises(ValueError):
                validate_user_id(bad)

    def test_estimate_tokens_overestimates(self):
        self.assertGreaterEqual(estimate_tokens("x" * 400), 100)


if __name__ == "__main__":
    unittest.main()
