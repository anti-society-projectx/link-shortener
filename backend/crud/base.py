from __future__ import annotations

from typing import Generic, TypeVar, Sequence, Any, Tuple

from pydantic import BaseModel
from sqlalchemy import select, Select, ColumnElement, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from backend.models import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, obj_in: BaseModel) -> T:
        obj = self.model(**obj_in.model_dump())
        self.db.add(obj)

        await self.db.flush()
        return obj

    async def get_by_id(self, obj_id: Any) -> T | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        return await self.db.scalar(stmt)

    async def list(
            self,
            *filters: Any,
            order_by: Any | None = None,
            limit: int | None = None,
            offset: int | None = None,
    ) -> Sequence[T]:
        stmt = select(self.model)

        if filters:
            stmt = stmt.where(*filters)

        if order_by is not None:
            stmt = stmt.order_by(order_by)

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        return (await self.db.scalars(stmt)).all()

    async def patch(self, obj: T, obj_in: BaseModel) -> T:
        data = obj_in.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(obj, key, value)

        await self.db.flush()
        return obj

    async def patch_by_id(self, obj_id: Any, obj_in: BaseModel) -> T | None:
        obj = await self.get_by_id(obj_id)
        if not obj:
            return None

        return await self.patch(obj, obj_in)

    async def delete(self, obj: T) -> None:
        await self.db.delete(obj)
        await self.db.flush()

    async def delete_by_id(self, obj_id: Any) -> bool:
        obj = await self.get_by_id(obj_id)
        if not obj:
            return False

        await self.delete(obj)
        return True

    async def exists(self, *filters: Any) -> bool:
        stmt = select(self.model).where(*filters).exists()
        return bool(await self.db.scalar(select(stmt)))

    async def paginate(
            self,
            base_q: Select[Tuple[T]],
            page: int,
            page_size: int,
            order_by: ColumnElement[Any] | InstrumentedAttribute[Any],
    ) -> Tuple[int, Sequence[T]]:
        """
        Считает total и возвращает страницу items.
        """
        # logger.info(
        #     "Пагинация: страница=%d, размер_страницы=%d, сортировка=%s", page, page_size, order_by
        # )
        total_subq = select(func.count()).select_from(
            base_q.order_by(None).subquery()
        )
        total = await self.db.scalar(total_subq) or 0
        # logger.debug("Всего записей: %d", total)

        items_q = base_q.order_by(order_by).offset((page - 1) * page_size).limit(page_size)
        items = (await self.db.execute(items_q)).scalars().all()
        # logger.debug("Получено элементов: %d", len(items))

        return total, items
