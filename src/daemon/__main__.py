import asyncio
import datetime

from loguru import logger

from src.daemon.db_bridge import update_schedules
from src.daemon.schedule_fetcher import get_updated_schedules
from src.env import DAEMON_INTERVAL, LOGGER_LEVEL, MODE

logger = logger.bind(name="daemon", level=LOGGER_LEVEL)


async def start_daemon():
    while True:
        await sleep_until()
        schedules = await get_updated_schedules()
        await update_schedules(schedules)
        logger.debug(f"daemon will go sleep for {DAEMON_INTERVAL} seconds")
        await asyncio.sleep(DAEMON_INTERVAL)


async def sleep_until():
    if MODE != "RELEASE":
        return
    now = datetime.datetime.now()
    target_time = now.replace(hour=15, minute=0, second=0)
    if now.hour >= 21:
        target_time = target_time + datetime.timedelta(days=1)
    delta = target_time - now
    if delta < datetime.timedelta(0):
        logger.debug("skipping hours sleep, target time is in the past")
        return
    sleep_seconds = delta.total_seconds()
    logger.debug(f"sleeping for {sleep_seconds} seconds until {target_time}")
    await asyncio.sleep(sleep_seconds)


asyncio.run(start_daemon())
