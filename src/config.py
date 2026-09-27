QUEUE_NAME = "bulk-email-queue"
CAMPAIGN_ID = "CMP-2026-001"

# Academic/demo sending limit. This simulates a controlled rate.
MAX_SENDS_PER_RUN = 2

# Addresses that must never be sent to.
SUPPRESSION_LIST = {
    "bounced@example.com",
    "unsubscribed@example.com",
    "complaint@example.com",
}
