import asyncio

from daemon.schedule_fetcher import get_updated_schedules

DAEMON_INTERVAL = 60


async def start_daemon():
    while True:
        await get_updated_schedules()
        await asyncio.sleep(DAEMON_INTERVAL)


asyncio.run(start_daemon())
