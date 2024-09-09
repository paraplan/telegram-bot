import asyncio
import logging

from src.daemon.db_bridge import update_schedules
from src.daemon.schedule_fetcher import get_updated_schedules

DAEMON_INTERVAL = 60

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def start_daemon():
    while True:
        schedules = await get_updated_schedules()
        await update_schedules(schedules)
        logger.debug("daemon will go sleep for %s seconds", DAEMON_INTERVAL)
        await asyncio.sleep(DAEMON_INTERVAL)


asyncio.run(start_daemon())
