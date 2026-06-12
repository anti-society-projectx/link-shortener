import datetime

from pydantic import BaseModel, ConfigDict, field_validator, AnyHttpUrl


class CreateLink(BaseModel):
    user_id: int
    url: AnyHttpUrl

    @field_validator('url', mode='before')
    @classmethod
    def validate_url_format(cls, value: str) -> str:
        if isinstance(value, str) and not value.startswith(('http://', 'https://')):
            raise ValueError("Проверьте правильно ли набрана ссылка.")
        return value


class ReadLink(BaseModel):
    id: int
    user_id: int
    url: AnyHttpUrl
    short_code: str
    active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class ReadLinks(BaseModel):
    items: list[ReadLink]
    total: int
    page: int
    page_size: int
    pages: int
