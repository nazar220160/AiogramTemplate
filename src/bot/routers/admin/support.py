from aiogram import F, types
from aiogram.exceptions import TelegramBadRequest

from src.bot.common.filters import IsAdmin
from src.bot.common.middlewares.i18n import gettext as _
from src.bot.routers.admin.router import admin_router
from src.bot.utils.texts import admin as texts
from src.common.dto import QuestionUpdate
from src.database.core.gateway import DatabaseGateway
from src.utils.enums import Status


@admin_router.message(F.reply_to_message, IsAdmin())
async def answer_the_question(message: types.Message, db: DatabaseGateway):
    message_id = message.reply_to_message.message_id

    database_message = await db.question.reader.select(admin_message_id=message_id)
    if database_message is None:
        await message.reply(_(texts.MESSAGE_NOT_FOUND))
        return
    if database_message.status == Status.SUCCESS:
        await message.reply(_(texts.MESSAGE_ALREADY_ANSWERED))
        return
    elif database_message.status == Status.IN_PROGRESS:
        await message.reply(_(texts.MESSAGE_ALREADY_ANSWERED))
        return
    try:
        await message.send_copy(
            chat_id=message.reply_to_message.forward_from.id,
            reply_to_message_id=database_message.user_message_id,
        )
    except TelegramBadRequest:
        await message.reply(_(texts.USER_BLOCKED_BOT_OR_DELETE_MESSAGE))
        return
    except AttributeError:
        await message.reply(_(texts.ERROR))
        return

    await db.question.writer.update(
        admin_message_id=message_id, query=QuestionUpdate(answered=True)
    )
    await message.reply(_(texts.REPLY_SEND))
