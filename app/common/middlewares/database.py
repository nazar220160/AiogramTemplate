from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Optional,
)

from aiogram import BaseMiddleware
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncEngine

from app.database.core.connection import (
    async_engine,
    create_session_factory,
    async_session,
)
from app.database.core import Database


class DatabaseMiddleware(BaseMiddleware):

    def __init__(self, engine: Optional[AsyncEngine] = None) -> None:
        self._session_factory = create_session_factory(engine or async_engine())

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with Database(async_session(self._session_factory)) as db:
            data['db'] = db
            return await handler(event, data)
