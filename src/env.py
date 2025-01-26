import os
from typing import Final, Literal

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN", "123546:supercooltoken")
SCHEDULE_ENDPOINT: Final[str] = os.getenv("SCHEDULE_ENDPOINT", "https://example.com")
SCHEDULE_TOKEN: Final[str] = os.getenv("SCHEDULE_TOKEN", "123546:supercooltoken")

POSTGRES_USER: Final[str] = os.getenv("POSTGRES_USER", "paraplan")
POSTGRES_PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD", "paraplan")
POSTGRES_HOST: Final[str] = os.getenv("POSTGRES_HOST", "db")
POSTGRES_PORT: Final[str] = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB: Final[str] = os.getenv("POSTGRES_DB", "paraplan")

POSTGRES_DSN: Final[str] = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}?prepared_statement_cache_size=500"
)


DAEMON_INTERVAL: Final[int] = int(os.getenv("DAEMON_INTERVAL", 600))

ValidLogLevels = Literal["DEBUG", "INFO", "WARNING", "ERROR"]

LOGGER_LEVEL: Final[ValidLogLevels] = os.getenv("LOGGER_LEVEL", "INFO")  # type: ignore
MODE: Final[Literal["RELEASE", "DEV", "STAGE"]] = os.getenv("MODE", "RELEASE")  # type: ignore
STAGE_ALLOWED_USERS: Final[list[int]] = list(
    map(int, os.getenv("STAGE_ALLOWED_USERS", "").split(","))
)
