import sys
from pathlib import Path
import unittest
import tempfile
import csv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from validation_lambda import validate_csv


class ValidationTests(unittest.TestCase):

    def make_csv(self, rows):
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False,
            newline="", encoding="utf-8"
        )
        writer = csv.DictWriter(
            f, fieldnames=["campaign_id", "email", "consent"]
        )
        writer.writeheader()
        writer.writerows(rows)
        f.close()
        return f.name

    def test_valid_recipient(self):
        path = self.make_csv([{
            "campaign_id": "C1",
            "email": "valid@example.com",
            "consent": "true"
        }])
        approved, rejected, summary = validate_csv(path)
        self.assertEqual(len(approved), 1)
        self.assertEqual(len(rejected), 0)

    def test_invalid_email(self):
        path = self.make_csv([{
            "campaign_id": "C1",
            "email": "wrong-email",
            "consent": "true"
        }])
        approved, rejected, summary = validate_csv(path)
        self.assertEqual(len(approved), 0)
        self.assertEqual(rejected[0]["reason"], "INVALID_EMAIL")

    def test_no_consent(self):
        path = self.make_csv([{
            "campaign_id": "C1",
            "email": "person@example.com",
            "consent": "false"
        }])
        approved, rejected, summary = validate_csv(path)
        self.assertEqual(rejected[0]["reason"], "NO_CONSENT")

    def test_duplicate(self):
        path = self.make_csv([
            {"campaign_id": "C1", "email": "same@example.com", "consent": "true"},
            {"campaign_id": "C1", "email": "same@example.com", "consent": "true"},
        ])
        approved, rejected, summary = validate_csv(path)
        self.assertEqual(len(approved), 1)
        self.assertEqual(rejected[0]["reason"], "DUPLICATE")

    def test_suppression(self):
        path = self.make_csv([{
            "campaign_id": "C1",
            "email": "bounced@example.com",
            "consent": "true"
        }])
        approved, rejected, summary = validate_csv(path)
        self.assertEqual(rejected[0]["reason"], "SUPPRESSED")


if __name__ == "__main__":
    unittest.main()
