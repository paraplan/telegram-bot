import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()
TOKEN: Final[str] = os.getenv("TOKEN", "123456:supercooltoken")
