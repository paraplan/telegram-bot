from zoneinfo import ZoneInfo

import edgedb

from src.env import EDGEDB_DSN

TIMEZONE = ZoneInfo("Europe/Moscow")

db_client = edgedb.create_async_client(EDGEDB_DSN, tls_security="insecure")
