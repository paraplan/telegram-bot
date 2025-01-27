from datetime import date

from aiohttp import ClientSession, TCPConnector
from loguru import logger

from src.env import SCHEDULE_ENDPOINT, SCHEDULE_TOKEN


class FetchError(Exception): ...


async def get_schedule_data(date: date) -> str:
    async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        url = f"{SCHEDULE_ENDPOINT}/modules/scheduleeditor/export.php"
        params = {"apikey": SCHEDULE_TOKEN, "actdate": "now", "date": str(date)}
        logger.debug(f"Fetching schedule data from {url} with params {params}")
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise FetchError(f"Failed to fetch schedule data: {response.status}")
            return await response.text()
