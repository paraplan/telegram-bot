import asyncio
import datetime

from .database.couple import CoupleRepository

# print(asyncio.run(CabinetRepository().get_by_id(3)))
now = datetime.datetime.now(datetime.UTC)
asyncio.run(CoupleRepository().add(0, 1, now, now + datetime.timedelta(minutes=60), []))
