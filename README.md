# Serverless Bulk Email Campaign – Middleware Technologies

## Purpose
This project is a local, runnable academic simulation of the AWS architecture:

S3 -> EventBridge -> Validation Lambda -> SQS -> Sender Lambda -> SES
                                              |
                                              -> DynamoDB
                                              |
                                              -> CloudWatch

The local version uses Python standard-library simulations for SQS, SES and DynamoDB.
This lets you demonstrate the logic and collect real execution output before connecting
to AWS.

## Requirements
- Python 3.9 or later
- No external Python package is required.

## Run the demo

From the project root:

```bash
python run_demo.py
```

## Run unit tests

```bash
python -m unittest discover -s tests -v
```

## Expected demo behaviour

The sample CSV contains:
- valid recipients
- an invalid email
- a no-consent recipient
- a suppressed/bounced recipient
- a duplicate
- another valid recipient

The output should show validation counts, queueing, controlled sender runs,
final campaign status and `STATUS: SUCCESS`.

## Screenshots to capture for the report

1. Terminal showing the complete `python run_demo.py` output.
2. Terminal showing all unit tests passing.
3. Later, after AWS deployment: S3 object, Lambda result/logs, SQS queue,
   SES test result, DynamoDB status and CloudWatch metrics.

## Academic note
Use only test/authorized recipients. Do not use real personal email lists without
documented consent. The local MockSES does not send actual email.
