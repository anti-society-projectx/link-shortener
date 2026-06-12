import datetime

from pydantic import BaseModel


class ResponseReadUser(BaseModel):
    id: int
    tg_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
