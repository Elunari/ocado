from src.main import is_debt_message, receive_debt_from_s3, send_result_to_s3

TEST_BUCKET_NAME = "test-debts-bucket"
TEST_WORKER_QUEUE_URL = "http://example.com/test-worker-queue"


def test_valid_debt_message():
    message = {"debts_id": "12345"}
    assert is_debt_message(message)


def test_invalid_debt_message():
    message = {"debts_id": 12345}
    assert not is_debt_message(message)


def test_missing_debts_id():
    message = {"some_other_key": "value"}
    assert not is_debt_message(message)


def test_receive_debt_from_s3(s3_client):
    s3_client.put_object(
        Bucket=TEST_BUCKET_NAME,
        Key="debt123",
        Body=b"Logan,Jessica,574\nLogan,Mary,45\nLogan,Jessica,177",
    )

    expected_result = [
        ["Logan", "Jessica", "574"],
        ["Logan", "Mary", "45"],
        ["Logan", "Jessica", "177"],
    ]
    result = list(receive_debt_from_s3("debt123", s3_client, TEST_BUCKET_NAME))
    print(result)
    print(expected_result)
    assert result == expected_result


def test_send_result_to_s3(s3_client):
    payments = "1,10\n2,20\n3,30"
    debtId = "debt123"
    send_result_to_s3(debtId, payments, s3_client, TEST_BUCKET_NAME)

    response = s3_client.get_object(Bucket=TEST_BUCKET_NAME, Key=f"{debtId}_results")
    body = response["Body"].read().decode()
    assert body == payments
