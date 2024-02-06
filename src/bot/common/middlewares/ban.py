from typing import (
    Any,
    Awaitable,
    Callable,
    Dict, Union,
)

from aiogram import BaseMiddleware
from aiogram import types

from src.bot.utils import texts
from src.core.config import Config
from src.database.core.gateway import DatabaseGateway
from src.bot.common.middlewares.i18n import gettext as _


class BanMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Union[types.Message, types.CallbackQuery],
            data: Dict[str, Any],
    ) -> Any:
        config: Config = data["config"]
        if event.from_user.id in config.bot.admins:
            result = await handler(event, data)
            return result
        db: DatabaseGateway = data["db"]
        check_user = await db.user.reader.select(user_id=event.from_user.id)
        if not check_user.blocked:
            result = await handler(event, data)
            return result

        if isinstance(event, types.Message):
            await event.reply(text=_(texts.USER_BLOCKED))
        if isinstance(event, types.CallbackQuery):
            await event.answer(text=_(texts.USER_BLOCKED_ALERT), show_alert=True)
