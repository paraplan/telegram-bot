from sqlalchemy.ext.asyncio import create_async_engine

from src.env import POSTGRES_DSN

engine = create_async_engine(POSTGRES_DSN)
