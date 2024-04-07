import boto3
import pytest
from moto import mock_aws

TEST_BUCKET_NAME = "test-debts-bucket"
TEST_WORKER_QUEUE_NAME = "test-worker-queue"


@pytest.fixture(scope="session", autouse=True)
def s3_client():
    with mock_aws():
        # mock clients
        s3_client = boto3.client("s3")

        # setup bucket
        s3_client.create_bucket(Bucket=TEST_BUCKET_NAME)

        yield s3_client
