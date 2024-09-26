import os
from typing import Final, Literal

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN", "123546:supercooltoken")
SCHEDULE_ENDPOINT: Final[str] = os.getenv("SCHEDULE_ENDPOINT", "https://example.com")
SCHEDULE_TOKEN: Final[str] = os.getenv("SCHEDULE_TOKEN", "123546:supercooltoken")

DATABASE_HOST: Final[str] = os.getenv("DATABASE_HOST", "edgedb")

ValidLogLevels = Literal["DEBUG", "INFO", "WARNING", "ERROR"]

LOGGER_LEVEL: Final[ValidLogLevels] = os.getenv("LOGGER_LEVEL", "INFO")  # type: ignore
