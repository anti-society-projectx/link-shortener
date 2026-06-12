import datetime

from pydantic import BaseModel, Field, ConfigDict

from backend.schemas.link import ReadLink


# class UserBase(BaseModel):
#     id: int
#     tg_id: int
#     username: str | None
#     created_at: datetime.datetime
#     updated_at: datetime.datetime


class CreateUser(BaseModel):
    tg_id: int = Field(ge=1, description="Telegram ID пользователя")

class ReadUser(BaseModel):
    id: int
    tg_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class ReadUserWithOptions(ReadUser):
    links: list[ReadLink] = []

    model_config = ConfigDict(from_attributes=True)


class ReadUsers(BaseModel):
    items: list[ReadUser]
    total: int
    page: int
    page_size: int
    pages: int
