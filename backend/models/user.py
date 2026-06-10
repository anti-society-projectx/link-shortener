from typing import TYPE_CHECKING

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models import Base

if TYPE_CHECKING:
    from backend.models import Link


class User(Base):
    """
    Класс пользователей.
    """
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)

    username: Mapped[str | None] = mapped_column(unique=True, index=True)

    links: Mapped[list["Link"]] = relationship(
        "Link",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
