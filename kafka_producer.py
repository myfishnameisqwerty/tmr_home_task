import logging
from aiokafka import AIOKafkaProducer
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaEventProducer:
    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    async def start(self):
        await self.producer.start()
        logging.info("Producer started")

    async def send_event(self, topic, event):
        try:
            await self.producer.send_and_wait(topic, event)
            logging.info(f"Producer sent {event=}")
        except Exception as e:
            logging.error(f"Failed to send event: {e}", exc_info=True)

    async def stop(self):
        await self.producer.stop()
        logging.info("Producer stopped")

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.stop()
