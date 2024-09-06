from datetime import date

from aiohttp import ClientSession, TCPConnector

from src.env import SCHEDULE_ENDPOINT, SCHEDULE_TOKEN


async def get_schedule_data(date: date) -> str:
    async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        async with session.get(
            f"{SCHEDULE_ENDPOINT}/modules/scheduleeditor/export.php",
            params={"apikey": SCHEDULE_TOKEN, "actdate": "now", "date": str(date)},
        ) as response:
            return await response.text()
