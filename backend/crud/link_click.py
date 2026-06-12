from typing import Any, Sequence

from sqlalchemy import ColumnElement, select
from sqlalchemy.orm import InstrumentedAttribute

from backend.crud.base import BaseRepository
from backend.models import LinkClick


class LinkClickRepository(BaseRepository[LinkClick]):
    model = LinkClick

    async def read_by_link_id(
            self,
            link_id: int,
            page: int,
            page_size: int,
            order_by: ColumnElement[Any] | InstrumentedAttribute[Any] = LinkClick.clicked_at.desc()
    ) -> tuple[int, Sequence[LinkClick]]:
        query = (
            select(LinkClick)
            .where(LinkClick.link_id == link_id)
        )

        return await self.paginate(query, page, page_size, order_by)
