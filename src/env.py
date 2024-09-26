import os
from typing import Final, Literal

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN", "123546:supercooltoken")
SCHEDULE_ENDPOINT: Final[str] = os.getenv("SCHEDULE_ENDPOINT", "https://example.com")
SCHEDULE_TOKEN: Final[str] = os.getenv("SCHEDULE_TOKEN", "123546:supercooltoken")

EDGEDB_INSTANCE: Final[str] = os.getenv("EDGEDB_INSTANCE", "edgedb")
EDGEDB_DSN: Final[str] = os.getenv("EDGEDB_DSN", "edgedb://edgedb:5656")

DAEMON_INTERVAL: Final[int] = int(os.getenv("DAEMON_INTERVAL", 600))

ValidLogLevels = Literal["DEBUG", "INFO", "WARNING", "ERROR"]

LOGGER_LEVEL: Final[ValidLogLevels] = os.getenv("LOGGER_LEVEL", "INFO")  # type: ignore
