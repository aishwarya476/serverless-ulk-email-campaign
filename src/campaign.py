from collections import Counter


class CampaignStore:
    """Local simulation of DynamoDB campaign status."""

    def __init__(self, campaign_id):
        self.campaign_id = campaign_id
        self.events = []

    def record(self, status):
        self.events.append(status)

    def summary(self):
        counts = Counter(self.events)
        return {
            "campaign_id": self.campaign_id,
            "SENT": counts.get("SENT", 0),
            "FAILED": counts.get("FAILED", 0),
            "REJECTED": counts.get("REJECTED", 0),
        }
