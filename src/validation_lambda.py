import csv
import re
from config import SUPPRESSION_LIST

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_csv(csv_path):
    """Simulate the Validation Lambda.

    Returns:
        approved: recipients that passed validation
        rejected: list of dictionaries containing a reason
        summary: counts suitable for reporting
    """
    approved = []
    rejected = []
    seen = set()

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        required = {"campaign_id", "email", "consent"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(
                f"CSV must contain columns: {', '.join(sorted(required))}"
            )

        for row_no, row in enumerate(reader, start=2):
            email = (row.get("email") or "").strip().lower()
            consent = (row.get("consent") or "").strip().lower() == "true"

            if not EMAIL_RE.match(email):
                rejected.append({"row": row_no, "reason": "INVALID_EMAIL"})
                continue

            if not consent:
                rejected.append({"row": row_no, "reason": "NO_CONSENT"})
                continue

            if email in SUPPRESSION_LIST:
                rejected.append({"row": row_no, "reason": "SUPPRESSED"})
                continue

            if email in seen:
                rejected.append({"row": row_no, "reason": "DUPLICATE"})
                continue

            seen.add(email)
            approved.append({
                "campaign_id": row.get("campaign_id"),
                "email": email
            })

    summary = {
        "total": len(approved) + len(rejected),
        "approved": len(approved),
        "rejected": len(rejected),
    }
    return approved, rejected, summary
