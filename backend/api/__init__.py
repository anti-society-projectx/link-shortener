from fastapi import APIRouter

from backend.api.v1 import router as routers_v1
from backend.core.config import settings

routers = APIRouter(
    prefix=settings.api.prefix,
)
routers.include_router(routers_v1)
