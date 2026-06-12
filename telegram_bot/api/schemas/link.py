import datetime

from pydantic import BaseModel, ConfigDict, AnyHttpUrl


class ResponseReadLinkClick(BaseModel):
    id: int
    link_id: int
    clicked_at: datetime.datetime
    country_code: str | None
    city: str | None
    os: str | None
    device_type: str | None
    browser: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class ResponseReadLink(BaseModel):
    id: int
    user_id: int
    url: AnyHttpUrl
    short_code: str
    active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class ResponseReadLinks(BaseModel):
    items: list[ResponseReadLink]
    total: int
    page: int
    page_size: int
    pages: int


class ResponseReadLinkClicks(BaseModel):
    items: list[ResponseReadLinkClick]
    total: int
    page: int
    page_size: int
    pages: int
