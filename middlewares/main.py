from aiogram import BaseMiddleware, Bot
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject, User, Message, CallbackQuery

import keyboards

from database import db
from misc.loader import dp
from misc.utils import extract_unique_code, check_sub


class DatabaseCheck(BaseMiddleware):
    async def __call__(
            self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):
        from_user: User = data['event_from_user']
        if isinstance(event, Message):
            if not db.check_user(from_user.id):
                ref_id = extract_unique_code(event.text) if event.text else None
                if ref_id is None or not ref_id.isdigit() or not db.check_user(user_id=int(ref_id)):
                    ref_id = None
                db.add_user(user_id=from_user.id, first_name=from_user.first_name,
                            last_name=from_user.last_name, username=from_user.username,
                            lang=from_user.language_code, ref_id=ref_id)

        user_info = db.get_user_by_user_id(user_id=from_user.id)
        data['user_info'] = user_info

        if user_info.username != from_user.username:
            db.edit_user_info(user_id=user_info.user_id, setting="username", new_value=from_user.username)
        if user_info.first_name != from_user.first_name:
            db.edit_user_info(user_id=user_info.user_id, setting="first_name", new_value=from_user.first_name)
        if user_info.last_name != from_user.last_name:
            db.edit_user_info(user_id=user_info.user_id, setting="last_name", new_value=from_user.last_name)

        bot: Bot = data['bot']
        not_sub_list = await check_sub(bot=bot, user_id=from_user.id)

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


class CheckSubscribe(BaseMiddleware):
    async def __call__(
            self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):
        from_user: User = data['event_from_user']

        bot: Bot = data['bot']
        not_sub_list = await check_sub(bot=bot, user_id=from_user.id)

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
