from typing import (
    Any,
    Awaitable,
    Callable,
    Dict
)

from aiogram import BaseMiddleware
from aiogram import types
from src.database.core.gateway import DatabaseGateway
from src.common.dto import UserCreate


class AddUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        db: DatabaseGateway = data["db"]

        user_info = await db.user.reader.select(user_id=event.from_user.id)
        if not user_info:
            await db.user.writer.create(query=UserCreate(
                **event.from_user.model_dump(exclude_none=False)
            ))

        return await handler(event, data)
