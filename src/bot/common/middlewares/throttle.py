from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Final,
)

from aiogram import BaseMiddleware, types
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.utils import texts

TRIGGER_VALUE: Final[int] = 4
DEFAULT_MESSAGE_TIMEOUT: Final[int] = 10


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(
            self, storage: BaseStorage
    ) -> None:
        self._storage = storage

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.Message,
            data: Dict[str, Any]
    ) -> Any:

        if isinstance(self._storage, MemoryStorage):
            return await handler(event, data)

        user = f'user_message_{event.from_user.id}'  # type: ignore
        timeout = DEFAULT_MESSAGE_TIMEOUT

        is_throttled = await self._storage.redis.get(user)  # type: ignore
        if is_throttled:
            count = int(is_throttled.decode())
            if count == TRIGGER_VALUE:
                await self._storage.redis.set(name=user, value=count + 1, ex=timeout)  # type: ignore
                return await event.answer(texts.THROTTLED)  # type: ignore
            elif count > TRIGGER_VALUE:
                return
            else:
                await self._storage.redis.set(name=user, value=count + 1, ex=timeout)  # type: ignore
        else:
            await self._storage.redis.set(name=user, value=1, ex=timeout)  # type: ignore

        return await handler(event, data)
