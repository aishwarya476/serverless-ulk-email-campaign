from config import MAX_SENDS_PER_RUN


class MockSES:
    """Local simulation of Amazon SES."""

    def __init__(self):
        self.sent = []
        self.failed = []

    def send_email(self, recipient):
        # Simulated successful SES submission.
        self.sent.append(recipient)
        return True


def process_queue(queue, ses, max_sends=MAX_SENDS_PER_RUN):
    """Simulate the Sender Lambda with a controlled sending rate."""
    batch = queue.receive_batch(max_sends)
    results = []

    for message in batch:
        recipient = message["email"]
        try:
            ses.send_email(recipient)
            results.append({
                "email": recipient,
                "status": "SENT"
            })
        except Exception as exc:
            results.append({
                "email": recipient,
                "status": "FAILED",
                "reason": str(exc)
            })

    return results
