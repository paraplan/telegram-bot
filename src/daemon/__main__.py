import asyncio
import datetime
from typing import Any

from croniter import croniter
from loguru import logger

from src.daemon.db_bridge import update_schedules
from src.daemon.schedule_fetcher import get_schedules_for_updating
from src.env import DAEMON_CRONTAB, LOGGER_LEVEL, TIMEZONE

logger = logger.bind(name="daemon", level=LOGGER_LEVEL)


async def start_daemon():
    base_time = datetime.datetime.now(tz=TIMEZONE)
    cron = croniter(DAEMON_CRONTAB, base_time)
    while True:
        next_time: Any = cron.get_next(datetime.datetime)
        logger.info(f"Next crontab time: {next_time}")
        seconds_to_sleep = (next_time - datetime.datetime.now(tz=TIMEZONE)).total_seconds()
        logger.info(f"Daemon will go to sleep for {seconds_to_sleep:.2f} seconds")
        await asyncio.sleep(seconds_to_sleep)
        schedules = await get_schedules_for_updating()
        await update_schedules(schedules)


asyncio.run(start_daemon())
