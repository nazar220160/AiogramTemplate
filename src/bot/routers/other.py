from aiogram import Router, types

from src.common.dto.core import BotChatsCreate, BotChatsUpdate
from src.database.core.gateway import DatabaseGateway

other_router = Router()


@other_router.my_chat_member()
async def my_chat_member(update: types.ChatMemberUpdated, db: DatabaseGateway) -> None:
    check_chat = await db.bot_chats.reader.exist(chat_id=update.chat.id)

    if check_chat:
        sub = None
        if update.new_chat_member.status.value != "administrator":
            sub = False
        query = BotChatsUpdate(
            permissions=update.new_chat_member.model_dump(mode="json", exclude="user"),
            sub=sub,
            **update.chat.model_dump(exclude_none=True, exclude="permissions"),
        )
        await db.bot_chats.writer.update(
            chat_id=update.chat.id,
            query=query,
        )
        return

    await db.bot_chats.writer.create(
        query=BotChatsCreate(
            permissions=update.new_chat_member.model_dump(mode="json", exclude="user"),
            **update.chat.model_dump(exclude_none=True, exclude="permissions"),
        )
    )
