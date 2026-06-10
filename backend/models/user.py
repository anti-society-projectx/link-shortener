from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base


class User(Base):
    """
    Класс пользователей.
    """
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)

    username: Mapped[str | None] = mapped_column(unique=True, index=True)
