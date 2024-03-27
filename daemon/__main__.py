import asyncio
import logging
from datetime import date

import orjson
from aiohttp import ClientSession, TCPConnector

from daemon.env import BASE_SCHEMA_API_URL, SCHEMA_API_TOKEN
from schedule_parser.study_day import StudyDay

logging.basicConfig(level=logging.DEBUG)


async def get_page(url: str, params: dict[str, str | int]) -> bytes:
    headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
    }
    async with ClientSession(headers=headers, connector=TCPConnector(ssl=False)) as session:
        logging.debug("Make request to %s", url)
        async with session.get(url, params=params) as resp:
            logging.debug("Get response (%s) with code: %s", resp.url, resp.status)
            return await resp.read()


async def get_study_day_data(date: date) -> bytes:
    return await get_page(
        f"{BASE_SCHEMA_API_URL}/modules/scheduleeditor/scheduledata.php",
        {
            "date": date.strftime("%Y-%m-%d"),
            "apikey": SCHEMA_API_TOKEN,
            "actdate": "now",
            "area": 1,
        },
    )


async def get_bells_data(id: int) -> bytes:
    return await get_page(
        f"{BASE_SCHEMA_API_URL}/modules/bellsscheduleeditor/bellsscheduledata.php",
        {"id": id, "apikey": SCHEMA_API_TOKEN, "actdate": "now", "area": 1},
    )


async def main():
    study_day_data = await get_study_day_data(date.today())
    study_day = StudyDay(**orjson.loads(study_day_data))
    print(study_day)


if __name__ == "__main__":
    asyncio.run(main())
