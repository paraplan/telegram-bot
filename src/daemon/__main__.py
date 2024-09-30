import asyncio
import datetime
import logging

from src.daemon.db_bridge import update_schedules
from src.daemon.schedule_fetcher import get_updated_schedules
from src.env import DAEMON_INTERVAL, LOGGER_LEVEL

logging.basicConfig(level=LOGGER_LEVEL)
logger = logging.getLogger(__name__)


async def start_daemon():
    while True:
        await sleep_until(datetime.datetime.now())
        schedules = await get_updated_schedules()
        await update_schedules(schedules)
        logger.debug("daemon will go sleep for %s seconds", DAEMON_INTERVAL)
        await asyncio.sleep(DAEMON_INTERVAL)


async def sleep_until(time: datetime.datetime):
    now = datetime.datetime.now()
    target_time = now.replace(hour=16, minute=0, second=0)
    if now.hour >= 21:
        target_time = target_time + datetime.timedelta(days=1)
    delta = target_time - now
    if delta < datetime.timedelta(0):
        logger.debug("skipping hours sleep, target time is in the past")
        return
    sleep_seconds = delta.total_seconds()
    logger.debug("sleeping for %s seconds until %s", sleep_seconds, target_time)
    await asyncio.sleep(sleep_seconds)


asyncio.run(start_daemon())
