import logging
import os
import aioboto3


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DynamoDBClient:
    def __init__(self, table_name="AnomalyDetections"):
        self.session = aioboto3.Session()
        self.endpoint_url = os.getenv("DYNAMODB_URL")
        self.region_name = os.getenv("REGION")
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.table_name = table_name
        logger.info("DynamoDB session started")

    async def get_table(self, table_name):
        async with self.session.resource(
            "dynamodb",
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as dynamodb:
            return await dynamodb.Table(table_name)

    async def create_table_if_not_exists(self, table_name=None):
        table_name = table_name or self.table_name
        async with self.session.resource(
            "dynamodb",
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        ) as dynamodb:
            table = await dynamodb.Table(table_name)
            try:
                await dynamodb.meta.client.describe_table(TableName=table_name)
                logger.info("DynamoDB table loaded")
            except dynamodb.meta.client.exceptions.ResourceNotFoundException:
                logger.info(f"Creating table {table_name}...")
                table = await dynamodb.create_table(
                    TableName=table_name,
                    KeySchema=[
                        {"AttributeName": "event_id", "KeyType": "HASH"},
                    ],
                    AttributeDefinitions=[
                        {"AttributeName": "event_id", "AttributeType": "S"},
                    ],
                    ProvisionedThroughput={
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                )
                await table.meta.client.get_waiter("table_exists").wait(
                    TableName=table_name
                )
                logger.info(f"Table {table_name} created successfully.")
