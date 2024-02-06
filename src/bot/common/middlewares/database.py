from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)

from aiogram import BaseMiddleware, types

from src.database.core.connection import SessionFactoryType, create_sa_session
from src.database.core.gateway import DatabaseGateway
from src.database.core.unit_of_work import SQLAlchemyUnitOfWork


class DatabaseMiddleware(BaseMiddleware):

    def __init__(self, session_factory: SessionFactoryType) -> None:
        self._session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        sessions = create_sa_session(session_factory=self._session_factory)
        async for session in sessions:
            uow = SQLAlchemyUnitOfWork(session=session)
            async with DatabaseGateway(uow) as database:
                data["db"] = database
                return await handler(event, data)
