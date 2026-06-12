from typing import Any

from sqlalchemy import select, Sequence, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, selectinload
from sqlalchemy.orm.interfaces import ORMOption

from backend.crud.base import BaseRepository
from backend.models import User


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        query = (
            select(User)
            .where(User.tg_id == tg_id)
        )

        return await self.db.scalar(query)

    async def lists_users(
            self,
            page: int,
            page_size: int,
            order_by: ColumnElement[Any] | InstrumentedAttribute[Any] = User.created_at.desc()
    ) -> tuple[int, Sequence[User]]:
        stmt = (
            select(User)
        )

        return await self.paginate(stmt, page, page_size, order_by)
