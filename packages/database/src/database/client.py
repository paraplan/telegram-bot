from sqlalchemy.ext.asyncio import create_async_engine

from env import POSTGRES_DSN

engine = create_async_engine(POSTGRES_DSN)
