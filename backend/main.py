from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from starlette import status
from starlette.responses import RedirectResponse

from backend.api import routers
from backend.api.v1.dependencies import get_link_service, get_client_info
from backend.core.config import settings
from backend.core.database import db_util
from backend.exceptions.link import LinkNotFoundError
from backend.models import Base
from backend.schemas.link_click import ClientInfo, CreateLinkClick
from backend.services.link import LinkService
from backend.utils.client import parse_ip_address_info, parse_user_agent


@asynccontextmanager
async def lifespan(_app: FastAPI):
    import backend.models
    async with db_util.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    docs_url="/docs" if not settings.fastapi.prod else None,
    redoc_url="/redoc" if not settings.fastapi.prod else None,
    openapi_url="/openapi.json" if not settings.fastapi.prod else None,
    lifespan=lifespan
)

app.include_router(routers)


@app.get("/{short_code}", status_code=status.HTTP_302_FOUND)
async def redirect_url(
        short_code: str,
        client: ClientInfo = Depends(get_client_info),
        link_service: LinkService = Depends(get_link_service)
):
    try:
        link = await link_service.read_by_short_id(short_code)
        ua_data = parse_user_agent(client.user_agent)
        # ip_data = parse_ip_address_info(client.ip)
        ip_data = parse_ip_address_info("8.8.8.8")

        data_link_click = CreateLinkClick(
            link_id=link.id,
            country_code=ip_data["country_code"],
            city=ip_data["city"],
            os=ua_data["os"],
            device_type=ua_data["device_type"],
            browser=ua_data["browser"]
        )

        await link_service.create_click(data_link_click)

        return RedirectResponse(
            url=link.url,
            status_code=302,
        )
    except LinkNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проверьте актуальность ссылки."
        )


if __name__ == '__main__':
    uvicorn.run(
        "backend.main:app",
        reload=not settings.fastapi.prod,
        host=settings.fastapi.ip_address,
        port=settings.fastapi.port,
        workers=settings.fastapi.workers,
    )
