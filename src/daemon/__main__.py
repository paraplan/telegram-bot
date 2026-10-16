import asyncio
import datetime
import logging
from typing import Any

from croniter import croniter

from src.daemon.db_bridge import update_schedules
from src.daemon.schedule_fetcher import get_schedules_for_updating
from src.env import DAEMON_CRONTAB, TIMEZONE
from src.logging_configure import configure_logging

logger = logging.getLogger(__name__)


async def start_daemon() -> None:
    base_time = datetime.datetime.now(tz=TIMEZONE)
    cron = croniter(DAEMON_CRONTAB, base_time)
    while True:
        next_time: Any = cron.get_next(datetime.datetime)
        logger.info("Next crontab time: %s", next_time)
        seconds_to_sleep = (next_time - datetime.datetime.now(tz=TIMEZONE)).total_seconds()
        logger.debug("Daemon will go to sleep for %s seconds", seconds_to_sleep)
        await asyncio.sleep(seconds_to_sleep)
        schedules = await get_schedules_for_updating()
        await update_schedules(schedules)


if __name__ == "__main__":
    configure_logging()
    asyncio.run(start_daemon())
