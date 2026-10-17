import os
from typing import Final
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

DAEMON_LOGGER_LEVEL: Final[str | None] = os.getenv("DAEMON_LOGGER_LEVEL")  # deprecated
LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
ENVIRONMENT: Final[str] = os.getenv("ENVIRONMENT", "production")
TIMEZONE: Final[ZoneInfo] = ZoneInfo(os.getenv("TIMEZONE", "Europe/Moscow"))

BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN", "123546:supercooltoken")

POSTGRES_USER: Final[str] = os.getenv("POSTGRES_USER", "paraplan")
POSTGRES_PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD", "paraplan")
POSTGRES_HOST: Final[str] = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT: Final[str] = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB: Final[str] = os.getenv("POSTGRES_DB", "paraplan")
POSTGRES_DSN: Final[str] = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?prepared_statement_cache_size=500"
)

SCHEDULE_ENDPOINT: Final[str] = os.getenv("SCHEDULE_ENDPOINT", "https://example.com")
SCHEDULE_TOKEN: Final[str] = os.getenv("SCHEDULE_TOKEN", "123546:supercooltoken")

DAEMON_CRONTAB: Final[str] = os.getenv("DAEMON_CRONTAB", "*/10 12-18 * * *")

ALLOWED_USERS: Final[str | None] = os.getenv("ALLOWED_USERS")
LIST_ALLOWED_USERS: Final[list[int]] = (
    list(map(int, ALLOWED_USERS.split(","))) if ALLOWED_USERS else []
)
