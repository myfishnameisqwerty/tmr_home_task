import logging
import os
import sys
from aiokafka import AIOKafkaConsumer
import asyncio
import json
import random

from health import retry_check_service
from s3_hooks import DynamoDBClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DYNAMODB_HEALTH_CHECK_URL = os.getenv(
    "DYNAMODB_HEALTH_CHECK_URL", "http://localstack:4566/_localstack/health"
)
KAFKA_SERVERS = os.getenv("KAFKA_SERVERS", "http://kafka:29092")


async def get_anomaly_score(event):
    return int(random.uniform(-1, 10))


class KafkaEventConsumer:
    def __init__(self, dynamodb_table, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.consumer = AIOKafkaConsumer(
            "events",
            bootstrap_servers=self.bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        self.dynamodb_table = dynamodb_table

    async def start(self):
        await self.consumer.start()
        logging.info("Consumer started")

    async def consume_events(self):
        tasks = []
        logging.debug("on consume_events")
        async for message in self.consumer:
            event = message.value
            logging.info(f"Consumer {event=}")
            task = asyncio.create_task(self.process_event(json.loads(event)))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def process_event(self, event):
        try:
            logging.debug("On process_event")
            event_id = event["event_id"]
            request_id = event["request_id"]
            response = await self.dynamodb_table.get_item(Key={"event_id": event_id})
            logging.info(f"{response=}")
            if "Item" in response:
                logging.info(f"Event {event_id} already processed.")
                return response["Item"]["anomaly_score"]

            anomaly_score = await get_anomaly_score(event)

            if anomaly_score > 0:
                await self.dynamodb_table.put_item(
                    Item={
                        "event_id": event_id,
                        "request_id": request_id,
                        "role_id": event["role_id"],
                        "event_type": event["event_type"],
                        "event_timestamp": event["event_timestamp"],
                        "affected_assets": event["affected_assets"],
                        "anomaly_score": anomaly_score,
                    }
                )
                logging.info(
                    f"Anomaly detected for event {event_id} with score {anomaly_score}."
                )
            else:
                logging.info(f"No anomaly detected for event {event_id}.")
        except Exception as e:
            logging.exception(f"On process_event got {e}")

    async def stop(self):
        await self.consumer.stop()
        logging.info("Consumer stopped")

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()


async def main():
    if not await retry_check_service("DynamoDB", DYNAMODB_HEALTH_CHECK_URL):
        sys.exit(1)
    dynamodb = DynamoDBClient()
    dynamodb_table = await dynamodb.get_table(dynamodb.table_name)
    async with KafkaEventConsumer(dynamodb_table, KAFKA_SERVERS) as consumer:
        await consumer.consume_events()


if __name__ == "__main__":
    asyncio.run(main())
