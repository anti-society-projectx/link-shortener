from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.user import UserRepository
from backend.exceptions.user import UserNotFoundError, UserAlreadyExistsError
from backend.schemas.user import CreateUser, ReadUser, ReadUserWithOptions, ReadUsers


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)

    async def create(self, data: CreateUser) -> ReadUser:
        async with self.db.begin():
            try:
                return await self.user_repo.create(data)
            except IntegrityError:
                await self.db.rollback()
                raise UserAlreadyExistsError(tg_id=data.tg_id)

    async def read_by_id(self, user_id: int) -> ReadUser:
        user = await self.user_repo.get_by_id(user_id)

        if not user:
            raise UserNotFoundError(user_id=user_id)

        return user

    async def read_by_tg_id(self, tg_id: int) -> ReadUser:
        user = await self.user_repo.get_by_tg_id(tg_id)

        if not user:
            raise UserNotFoundError(tg_id=tg_id)

        return user

    async def reads(self, page: int, page_size: int) -> ReadUsers:
        total, items = await self.user_repo.lists_users(page, page_size)
        pages = (total + page_size - 1) // page_size if total else 0

        return ReadUsers(
            items=[ReadUser.model_validate(i) for i in items],
            total=total,
            page=page,
            page_size=page_size,
            pages=pages
        )
