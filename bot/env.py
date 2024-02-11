import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()
TOKEN: Final[str] = os.getenv("TOKEN", "123456:supercooltoken")

POSTGRES_USER: Final[str] = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: Final[str] = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST: Final[str] = os.getenv("POSTGRES_HOST", "db")
POSTGRES_DB: Final[str] = os.getenv("POSTGRES_DB", "vgpk_bot")

POSTGRES_DATA: Final[str] = f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"

POSTGRES_SYNC_CONNECT: Final[str] = f"postgresql+psycopg://{POSTGRES_DATA}"
