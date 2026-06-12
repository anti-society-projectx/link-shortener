from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.core.config import settings


class Database:
    def __init__(
            self,
            async_url: str,
            echo: bool = False
    ):
        self.async_engine = create_async_engine(
            url=async_url,
            echo=echo
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        """
        Закрыть асинхронный движок при завершении работы приложения.
        """

        await self.async_engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Асинхронный генератор сессии для FastAPI-зависимостей.
        """
        async with self.async_session_factory() as session:
            yield session


db_util = Database(
    async_url=settings.db.url
)
