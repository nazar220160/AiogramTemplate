from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)

from aiogram import BaseMiddleware
from aiogram import types
from aiogram.types import User, Message, CallbackQuery

from app import keyboards
from app.core.models import MyBot
from app.core.settings import Settings
from app.database.core import Database
from app.utils.other import check_com_sub


class ComSubMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        settings: Settings = data['settings']
        from_user: User = data['event_from_user']
        if from_user.id in settings.admins:
            result = await handler(event, data)
            return result
        db: Database = data['db']
        bot: MyBot = data['bot']
        chats = await db.com_sub_chats.get_chats_turn_on()
        not_sub_list = await check_com_sub(bot=bot, user_id=from_user.id,
                                           sub_list=chats)

        if not not_sub_list:
            result = await handler(event, data)
            return result
        else:
            reply_markup = keyboards.inline.subscribe_chats(chat_list=not_sub_list)
            if isinstance(event, Message):
                await event.answer(text="<b>Чтобы пользоваться ботом нужно подписаться на чаты</b>",
                                   reply_markup=reply_markup)
            elif isinstance(event, CallbackQuery):
                message: Message = event.message
                await message.delete()
                await message.answer(text="<b>Чтобы пользоваться ботом нужно подписаться на чаты</b>",
                                     reply_markup=reply_markup)
