import aiohttp
import asyncio
import logging
import os

# Configure environment variables
MAX_RETRIES = int(os.getenv("MAX_RETRIES_ON_START", 5))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", 5))

logger = logging.getLogger(__name__)

async def is_service_available(service_url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(service_url) as response:
                logger.info(f"{service_url} responded with status {response.status}")
                return response.status == 200
        except Exception as e:
            logger.error(f"Health check to {service_url} failed: {e}")
            return False

async def retry_check_service(service_name, service_url):
    for attempt in range(MAX_RETRIES):
        if await is_service_available(service_url):
            logger.info(f"{service_name} is available.")
            return True
        else:
            logger.warning(
                f"{service_name} not available. Attempt {attempt + 1} of {MAX_RETRIES}. Retrying in {RETRY_DELAY} seconds..."
            )
            await asyncio.sleep(RETRY_DELAY)
    logger.error(f"Max retries reached. {service_name} is not available.")
    return False
