import logging
import os
import pytest
from fastapi.testclient import TestClient
from cloudtrail_ingestion_service import Item, app
from s3_hooks import DynamoDBClient


logging.basicConfig(level=logging.INFO)

client = TestClient(app)

test_subject = {
    "request_id": "123",
    "event_id": "456",
    "role_id": "789",
    "event_type": "test_event",
    "event_timestamp": "2024-07-18T23:45:51.475Z",
    "affected_assets": ["asset1", "asset2"],
}


@pytest.fixture
def sample_item():
    return Item(**test_subject)



def test_init_request(sample_item, mocker):
    os.environ["KAFKA_SERVERS"] = os.getenv("KAFKA_SERVERS")
    mock_producer = mocker.patch("kafka_producer.KafkaEventProducer")
    mock_producer.return_value.__aenter__.return_value.send_event.return_value = None
    response = client.post("/", json=test_subject)
    logging.warning(f"Response content: {response.content}")
    assert response.status_code == 200
    assert response.json().get("request_id") == sample_item.request_id
