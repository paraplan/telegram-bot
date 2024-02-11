import asyncio
import logging
import re
import typing

from aiohttp import ClientSession
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
SCHEDULE_URL: typing.Final[str] = "https://vgke.by/raspisanie-zanjatij/"


async def get_page(url: str) -> bytes:
    headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0"
    }
    async with ClientSession(headers=headers) as session:
        logging.debug("Make request to %s", url)
        async with session.get(url) as resp:
            logging.debug("Get response with code: %s", resp.status)
            return await resp.read()


async def get_schedules_links() -> list[str]:
    data = await get_page(SCHEDULE_URL)
    bs = BeautifulSoup(data, features="html.parser")
    elements = bs.find_all(
        "iframe",
        {
            "src": re.compile(r"sso"),
            "width": "900px",
            "height": "900px",
            "frameborder": 0,
        },
    )
    logging.debug("Found elements: %s", elements)
    schedules = [re.sub(r".*src=", "", element["src"]) for element in elements]
    logging.debug("Schedules links: %s", schedules)
    return schedules


async def get_schedules() -> list[bytes]:
    return [await get_page(schedule_url) for schedule_url in await get_schedules_links()]


async def main():
    print(await get_schedules())


if __name__ == "__main__":
    asyncio.run(main())
