import datetime

from sqlalchemy import DateTime, func, MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Базовая модель SQLAlchemy.
    """
    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),
    }

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_N_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )
