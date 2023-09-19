from typing import Optional
from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import AsyncEngine
from app.common.middlewares.database import DatabaseMiddleware


def register_middlewares(dp: Dispatcher, engine: Optional[AsyncEngine] = None) -> None:
    db_middleware = DatabaseMiddleware(engine)
    dp.message.outer_middleware.register(db_middleware)
    dp.callback_query.outer_middleware.register(db_middleware)
