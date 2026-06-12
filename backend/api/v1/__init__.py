from fastapi import APIRouter

from backend.api.v1.users import router as user_router
from backend.api.v1.links import router as link_router
from backend.core.config import settings

router = APIRouter(
    prefix=settings.api.version,
)
router.include_router(user_router, prefix=settings.api.users)
router.include_router(link_router, prefix=settings.api.links)
