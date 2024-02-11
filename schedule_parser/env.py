from os import getenv
from typing import Final

from dotenv import load_dotenv

load_dotenv()
FILE: Final[str] = getenv("FILE_NAME", "den-sso.xlsx")
START_COLUMN: Final[int] = int(getenv("START_COLUMN", 3))
START_ROW: Final[int] = int(getenv("START_ROW", 5))
