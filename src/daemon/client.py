from zoneinfo import ZoneInfo

import edgedb

TIMEZONE = ZoneInfo("Europe/Moscow")

db_client = edgedb.create_async_client()
