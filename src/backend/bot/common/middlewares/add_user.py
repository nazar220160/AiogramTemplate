from typing import (
    Any,
    Awaitable,
    Callable,
    Dict
)

from aiogram import BaseMiddleware
from aiogram import types
from src.backend.database.core import Database
from src.backend.common.dto import UserCreate


class AddUserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        db: Database = data['db']

        user_info = await db.user.select(user_id=event.from_user.id)
        if not user_info:
            await db.user.create(query=UserCreate(
                user_id=event.from_user.id,
                **event.from_user.model_dump(exclude_none=False, exclude='id')
            ))

        return await handler(event, data)
