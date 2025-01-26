import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.database import RepositoryFactory

# from src.database.models import Cabinet
from src.env import POSTGRES_DSN

engine = create_async_engine(POSTGRES_DSN)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def main():
    db = RepositoryFactory()


if __name__ == "__main__":
    asyncio.run(main())
