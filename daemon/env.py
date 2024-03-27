import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()
BASE_SCHEMA_API_URL: Final[str] = os.getenv("BASE_SCHEMA_API_URL", "")
SCHEMA_API_TOKEN: Final[str] = os.getenv("SCHEMA_API_TOKEN", "")
