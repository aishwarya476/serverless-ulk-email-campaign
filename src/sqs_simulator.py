from collections import deque


class SQSQueue:
    """Small local simulation of an Amazon SQS queue."""

    def __init__(self):
        self.messages = deque()

    def send_message(self, message):
        self.messages.append(message)

    def receive_batch(self, size):
        batch = []
        while self.messages and len(batch) < size:
            batch.append(self.messages.popleft())
        return batch

    def size(self):
        return len(self.messages)
