from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models import Base

if TYPE_CHECKING:
    from backend.models import User, LinkClick


class Link(Base):
    """
    Класс со сокращёнными ссылками пользователей.
    """
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)

    url: Mapped[str] = mapped_column(index=True)
    short_code: Mapped[str] = mapped_column(String(8), index=True, unique=True)

    active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="links",
        lazy="joined"
    )
    link_clicks: Mapped[list["LinkClick"]] = relationship(
        "LinkClick",
        back_populates="link",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
