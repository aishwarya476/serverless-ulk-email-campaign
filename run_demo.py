import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from config import CAMPAIGN_ID, MAX_SENDS_PER_RUN
from validation_lambda import validate_csv
from sqs_simulator import SQSQueue
from sender_lambda import MockSES, process_queue
from campaign import CampaignStore


def main():
    csv_path = Path(__file__).resolve().parent / "data" / "sample_campaign.csv"

    print("=" * 65)
    print("SERVERLESS BULK EMAIL CAMPAIGN - LOCAL DEMO")
    print("=" * 65)
    print(f"Campaign ID        : {CAMPAIGN_ID}")
    print(f"Input CSV          : {csv_path.name}")
    print(f"Controlled rate    : {MAX_SENDS_PER_RUN} messages/run")
    print()

    print("[1] VALIDATION LAMBDA")
    approved, rejected, validation_summary = validate_csv(csv_path)

    print(f"Total input records: {validation_summary['total']}")
    print(f"Approved records   : {validation_summary['approved']}")
    print(f"Rejected records   : {validation_summary['rejected']}")

    reason_counts = {}
    for item in rejected:
        reason_counts[item["reason"]] = reason_counts.get(item["reason"], 0) + 1

    for reason, count in sorted(reason_counts.items()):
        print(f"  - {reason}: {count}")

    print()
    print("[2] SQS BUFFER")
    queue = SQSQueue()
    for message in approved:
        queue.send_message(message)
    print(f"Messages queued    : {queue.size()}")

    print()
    print("[3] SENDER LAMBDA + MOCK SES")
    ses = MockSES()
    store = CampaignStore(CAMPAIGN_ID)

    run_number = 1
    while queue.size() > 0:
        results = process_queue(queue, ses, MAX_SENDS_PER_RUN)
        for result in results:
            store.record(result["status"])
            print(
                f"Run {run_number}: "
                f"{result['email']} -> {result['status']}"
            )
        run_number += 1

    print()
    print("[4] CAMPAIGN STATUS (DYNAMODB SIMULATION)")
    final = store.summary()
    print(f"Campaign ID       : {final['campaign_id']}")
    print(f"Sent              : {final['SENT']}")
    print(f"Failed            : {final['FAILED']}")
    print(f"Rejected           : {validation_summary['rejected']}")
    print(f"Queue remaining    : {queue.size()}")

    print()
    print("[5] FINAL RESULT")
    if final["SENT"] == validation_summary["approved"] and queue.size() == 0:
        print("STATUS: SUCCESS")
        print("All approved recipients were processed successfully.")
    else:
        print("STATUS: ATTENTION REQUIRED")

    print("=" * 65)


if __name__ == "__main__":
    main()
