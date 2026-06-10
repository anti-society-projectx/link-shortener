import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models import Base

if TYPE_CHECKING:
    from backend.models import Link


class LinkClick(Base):
    __tablename__ = "link_clicks"

    link_id: Mapped[int] = mapped_column(
        ForeignKey("links.id", ondelete="CASCADE"),
        index=True
    )

    clicked_at: Mapped[datetime.datetime] = mapped_column(index=True)

    country_code: Mapped[str | None] = mapped_column(String(3), nullable=True, index=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)

    os: Mapped[str | None] = mapped_column(String(50), nullable=True)
    device_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    browser: Mapped[str | None] = mapped_column(String(50), nullable=True)

    referrer_address: Mapped[str | None] = mapped_column(Text, default=None, index=True)

    link: Mapped["Link"] = relationship(
        "Link",
        back_populates="link_clicks"
    )
