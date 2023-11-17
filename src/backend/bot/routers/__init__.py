from aiogram import Router

from src.backend.bot.routers.admin import admin_router
from src.backend.bot.routers.client import client_router
from src.backend.bot.routers.error import error_router
from src.backend.bot.routers.other import other_router

router = Router(name='main')
router.include_routers(
    admin_router,
    client_router,
    other_router,
    error_router,
)
