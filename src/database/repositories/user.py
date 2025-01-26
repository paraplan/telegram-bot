from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload

from src.database.models import User
from src.database.repositories.abc import BaseRepository


class UserRepository(BaseRepository[User]):
    async def select_or_insert(self, id: int) -> User:
        statement = (
            insert(User)
            .values(id=id)
            .on_conflict_do_update(
                index_elements=["id"],
                set_=dict(id=id),
            )
            .returning(User)
            .options(selectinload(User.group), selectinload(User.settings))
        )
        result = await self._execute(statement, commit=True)
        return result.scalar_one()

    async def update_group(self, user_id: int, group_id: int):
        statement = update(User).where(User.id == user_id).values(group_id=group_id)
        async with self.sessionmaker() as session:
            await session.execute(statement)
            await session.commit()
