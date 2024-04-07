import time
from aws import get_s3_client, get_sqs_client
from typing import TYPE_CHECKING
from config import get_config
import json
import logging
from debts_simplifier import calculate_balances, calculate_min_payments

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_sqs import SQSClient

logger = logging.getLogger("__main__")
config = get_config()


def is_debt_message(response):
    return "debts_id" in response and isinstance(response["debts_id"], str)


def receive_debt_from_s3(debtId, s3_client):
    debts_object = s3_client.get_object(
        Bucket=config.debts_bucket_name,
        Key=debtId,
    )
    debts_data = map(
        lambda x: x.split(","), debts_object["Body"].read().decode("utf-8").splitlines()
    )
    return debts_data


def send_result_to_s3(debtId, payments, s3_client):
    key = debtId + "_results"
    s3_client.put_object(Bucket=config.debts_bucket_name, Key=key, Body=payments)


def prepare_message_for_s3(payments):
    csv_lines = [",".join(map(str, row)) for row in payments]
    return "\n".join(csv_lines)


if __name__ == "__main__":
    sqs_client: "SQSClient" = get_sqs_client()
    s3_client: "S3Client" = get_s3_client()
    while True:
        response = sqs_client.receive_message(
            QueueUrl=config.worker_queue_url,
        )
        messages = response.get("Messages", [])
        for message in messages:
            try:
                body = json.loads(message["Body"])
                if is_debt_message(body):
                    debtId = body["debts_id"]
                    debts = receive_debt_from_s3(debtId, s3_client)
                    balances = calculate_balances(debts)
                    payments = calculate_min_payments(balances)
                    payload = prepare_message_for_s3(payments)

                    send_result_to_s3(debtId, payload, s3_client)

                    receipt_handle = message["ReceiptHandle"]
                    sqs_client.delete_message(
                        QueueUrl=config.worker_queue_url,
                        ReceiptHandle=receipt_handle,
                    )
            except json.JSONDecodeError:
                print("Error decoding message JSON.")
        time.sleep(5)
