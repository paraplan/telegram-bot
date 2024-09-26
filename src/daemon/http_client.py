import logging
from datetime import date

from aiohttp import ClientSession, TCPConnector

from src.env import SCHEDULE_ENDPOINT, SCHEDULE_TOKEN

logger = logging.getLogger(__name__)


class FetchError(Exception): ...


async def get_schedule_data(date: date) -> str:
    async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        url = f"{SCHEDULE_ENDPOINT}/modules/scheduleeditor/export.php"
        params = {"apikey": SCHEDULE_TOKEN, "actdate": "now", "date": str(date)}
        logger.debug("Fetching schedule data from %s with params %s", url, params)
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise FetchError(f"Failed to fetch schedule data: {response.status}")
            return await response.text()
