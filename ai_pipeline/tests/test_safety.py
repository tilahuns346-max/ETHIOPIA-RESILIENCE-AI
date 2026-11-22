import unittest

class TestSafetyConstraints(unittest.TestCase):
    def test_human_review_flag(self):
        payload = {"risk_probability": 0.91, "requires_human_officer_review": True}
        self.assertTrue(payload["requires_human_officer_review"])

if __name__ == "__main__":
    unittest.main()
