from aiogram import Router

from .base import router as base_router
from .link import router as link_router

routers = Router()

routers.include_router(base_router)
routers.include_router(link_router)
