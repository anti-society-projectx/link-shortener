from typing import Sequence, Any

from sqlalchemy import select, ColumnElement
from sqlalchemy.orm import selectinload, InstrumentedAttribute

from backend.crud.base import BaseRepository
from backend.models import Link
from backend.schemas.link import CreateLink
from backend.utils.helper import generate_string


class LinkRepository(BaseRepository[Link]):
    model = Link

    async def create(self, data: CreateLink) -> Link:
        db_model = Link(**data.model_dump(), short_code=generate_string())
        self.db.add(db_model)

        await self.db.flush()
        return db_model

    async def read_by_short_id(self, short_id: int) -> Link | None:
        stmt = (
            select(Link)
            .where(Link.short_code == short_id)
        )

        return await self.db.scalar(stmt)

    async def reads(
            self,
            page: int,
            page_size: int,
            order_by: ColumnElement[Any] | InstrumentedAttribute[Any] = Link.created_at.desc()
    ) -> tuple[int, Sequence[Link]]:
        stmt = (
            select(Link)
        )

        return await self.paginate(stmt, page, page_size, order_by)

    async def reads_by_user_id(
            self,
            user_id: int,
            page: int, page_size: int,
            order_by: ColumnElement[Any] | InstrumentedAttribute[Any] = Link.created_at.desc()
    ) -> tuple[int, Sequence[Link]]:
        query = (
            select(Link)
            .where(Link.user_id == user_id)
        )

        return await self.paginate(query, page, page_size, order_by)
