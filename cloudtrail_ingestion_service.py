import asyncio
import logging
import os
import sys

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import datetime
from health import retry_check_service
from kafka_producer import KafkaEventProducer
from s3_hooks import DynamoDBClient


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DYNAMODB_URL = os.getenv("DYNAMODB_URL")
KAFKA_URL = os.getenv("KAFKA_SERVERS")
DYNAMODB_HEALTH_CHECK_URL = os.getenv(
    "DYNAMODB_HEALTH_CHECK_URL", "http://localstack:4566/_localstack/health"
)


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    if not await retry_check_service(
        "DynamoDB", DYNAMODB_HEALTH_CHECK_URL
    ):
        sys.exit(1)
    global db
    db = DynamoDBClient()
    await db.create_table_if_not_exists()
    logging.info("DynamoDB setup completed.")


class Item(BaseModel):
    request_id: str
    event_id: str
    role_id: str
    event_type: str
    event_timestamp: datetime.datetime
    affected_assets: List[str]


@app.post("/")
async def init_request(item: Item):
    logging.debug("running init_request")
    async with KafkaEventProducer(os.getenv("KAFKA_SERVERS")) as producer:
        await producer.send_event("events", item.model_dump_json())
    logging.debug("finished init_request")
    return item
