import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()

SCHEDULE_ENDPOINT: Final[str] = os.getenv("SCHEDULE_ENDPOINT", "https://example.com")
SCHEDULE_TOKEN: Final[str] = os.getenv("SCHEDULE_TOKEN", "123546:supercooltoken")
