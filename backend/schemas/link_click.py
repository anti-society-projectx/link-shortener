from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel, ConfigDict


@dataclass
class ClientInfo:
    ip: str | None
    user_agent: str | None


class CreateLinkClick(BaseModel):
    link_id: int
    # clicked_at: datetime
    country_code: str | None
    city: str | None
    os: str | None
    device_type: str | None
    browser: str | None


class ReadLinkClick(BaseModel):
    id: int
    link_id: int
    clicked_at: datetime
    country_code: str | None
    city: str | None
    os: str | None
    device_type: str | None
    browser: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReadLinkClicks(BaseModel):
    items: list[ReadLinkClick]
    total: int
    page: int
    page_size: int
    pages: int
