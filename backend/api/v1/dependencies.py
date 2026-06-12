from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import db_util
from backend.schemas.link_click import ClientInfo
from backend.services.link import LinkService
from backend.services.user import UserService


def get_user_service(db: Annotated[AsyncSession, Depends(db_util.session_getter)]) -> UserService:
    return UserService(db)

def get_link_service(db: Annotated[AsyncSession, Depends(db_util.session_getter)]) -> LinkService:
    return LinkService(db)


async def get_client_info(
    request: Request,
) -> ClientInfo:

    forwarded = request.headers.get("x-forwarded-for")

    ip = (
        forwarded.split(",")[0].strip()
        if forwarded
        else request.client.host
    )

    ua = request.headers.get("user-agent")

    return ClientInfo(
        ip=ip,
        user_agent=ua,
    )
