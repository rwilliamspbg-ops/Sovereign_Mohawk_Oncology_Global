import unittest

from security_wrapper.poisoning import detect_poisoned_clients


class TestPoisoningDetectors(unittest.TestCase):
    def test_detect_outlier_vector(self):
        vectors = {
            "a": [0.1, 0.1, 0.1],
            "b": [0.11, 0.1, 0.09],
            "c": [0.09, 0.1, 0.1],
            "mal": [10.0, -10.0, 8.0],
        }
        poisoned = detect_poisoned_clients(vectors, min_cosine_similarity=0.2, max_krum_score=2.0)
        self.assertIn("mal", poisoned)


if __name__ == "__main__":
    unittest.main()
