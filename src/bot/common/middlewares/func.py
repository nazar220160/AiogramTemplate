from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
)

from aiogram import BaseMiddleware, types
from aiogram.types import CallbackQuery, Message, User

from src.bot import keyboards
from src.bot.core.models import MyBot
from src.bot.utils.other import check_com_sub
from src.core.config import Config
from src.database.core.gateway import DatabaseGateway


class ComSubMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        config: Config = data["config"]
        from_user: User = data["event_from_user"]
        if from_user.id in config.bot.admins:
            result = await handler(event, data)
            return result
        db: DatabaseGateway = data["db"]
        bot: MyBot = data["bot"]
        chats = await db.bot_chats.reader.select_many(sub=True)
        not_sub_list = await check_com_sub(
            bot=bot, user_id=from_user.id, sub_list=chats
        )

        if not not_sub_list:
            result = await handler(event, data)
            return result
        else:
            reply_markup = keyboards.subscribe_chats(chat_list=not_sub_list)
            if isinstance(event, Message):
                await event.answer(
                    text="<b>Чтобы пользоваться ботом нужно подписаться на чаты</b>",
                    reply_markup=reply_markup,
                )
            elif isinstance(event, CallbackQuery):
                message: Message = event.message
                await message.delete()
                await message.answer(
                    text="<b>Чтобы пользоваться ботом нужно подписаться на чаты</b>",
                    reply_markup=reply_markup,
                )
