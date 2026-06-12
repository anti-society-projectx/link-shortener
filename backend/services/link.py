from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.link import LinkRepository
from backend.crud.link_click import LinkClickRepository
from backend.exceptions.link import LinkAlreadyExistsError, LinkNotFoundError
from backend.schemas.link import CreateLink, ReadLink, ReadLinks
from backend.schemas.link_click import ReadLinkClicks, ReadLinkClick, CreateLinkClick


class LinkService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.link_repo = LinkRepository(db)
        self.link_clicks_repo = LinkClickRepository(db)

    async def create(self, data: CreateLink) -> ReadLink:
        try:
            async with self.db.begin():
                return await self.link_repo.create(data)
        except IntegrityError:
            raise LinkAlreadyExistsError()

    async def create_click(self, data: CreateLinkClick) -> ReadLinkClick:
        click = await self.link_clicks_repo.create(data)
        await self.db.commit()
        return click

    async def read_by_id(self, link_id: int) -> ReadLink:
        link = await self.link_repo.get_by_id(link_id)

        if not link:
            raise LinkNotFoundError()

        return link

    async def read_by_short_id(self, short_id: int) -> ReadLink:
        link = await self.link_repo.read_by_short_id(short_id)

        if not link:
            raise LinkNotFoundError()

        return link

    async def reads(self, page: int, page_size: int) -> ReadLinks:
        total, items = await self.link_repo.reads(page, page_size)
        pages = (total + page_size - 1) // page_size if total else 0

        return ReadLinks(
            items=[ReadLink.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=pages
        )

    async def reads_by_user_id(self, user_id: int, page: int, page_size: int) -> ReadLinks:
        total, items = await self.link_repo.reads_by_user_id(user_id, page, page_size)
        pages = (total + page_size - 1) // page_size if total else 0

        return ReadLinks(
            items=[ReadLink.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=pages
        )

    async def reads_link_clicks_by_id(self, link_id: int, page: int, page_size: int) -> ReadLinkClicks:
        total, items = await self.link_clicks_repo.read_by_link_id(link_id, page, page_size)
        pages = (total + page_size - 1) // page_size if total else 0

        return ReadLinkClicks(
            items=[ReadLinkClick.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=pages
        )

    async def read_link_click_by_id(self, click_id: int) -> ReadLink:
        link_click = await self.link_clicks_repo.get_by_id(click_id)

        if not link_click:
            raise LinkNotFoundError()

        return link_click
