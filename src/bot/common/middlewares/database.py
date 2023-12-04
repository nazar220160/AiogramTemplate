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

from src.database.core.connection import (
    async_engine,
    create_session_factory,
    async_session,
)
from src.database.core import Database


class DatabaseMiddleware(BaseMiddleware):

    def __init__(self, db_url: str, engine: Optional[AsyncEngine] = None) -> None:
        self._db_url = db_url
        self._session_factory = create_session_factory(db_url=db_url, engine=engine or async_engine(db_url=db_url))

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        session = async_session(db_url=self._db_url, session_factory=self._session_factory)
        async with Database(db_url=self._db_url, session=session) as db:
            data['db'] = db
            return await handler(event, data)
