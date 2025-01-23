import traceback
from contextlib import suppress

from aiogram import Bot, types
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramBadRequest

from src.apps.telethon import TelegramApplication, TelegramAppManager
from src.bot import keyboards
from src.bot.routers.client.router import client_router
from src.bot.utils.callback import CallbackData as Cd
from src.bot.utils.other import paginate
from src.common.dto import DialogCreate
from src.database.core.gateway import DatabaseGateway


@client_router.callback_query(lambda c: Cd.extract(c.data).data == Cd.Dialogs.update())
async def dialogs_update(
    callback: types.CallbackQuery,
    bot: Bot,
    sessions: TelegramAppManager,
    db: DatabaseGateway,
):
    await bot.send_chat_action(callback.from_user.id, ChatAction.TYPING)
    data = Cd.extract(callback.data)
    user_id = callback.from_user.id
    account_id = int(data.args[1])

    client = sessions.get_client(database_id=account_id)

    try:
        async with client:
            await save_dialogs(
                user_id=user_id, client=client, session_id=account_id, db=db
            )
    except ConnectionError as e:
        await db.uow.rollback()
        await callback.answer(str(e), show_alert=True)
        return

    except Exception:
        await db.uow.rollback()
        file_text = traceback.format_exc().encode()
        file_text += bytes(f"\n\n{client.__dict__}", "utf-8")
        text = f"Ошибка сбора диалогов {client.phone_number}"
        text_file = types.input_file.BufferedInputFile(
            file_text, filename=text + ".txt"
        )
        await callback.message.reply_document(document=text_file, caption=text)
        await callback.answer("Unknown error...🧨", show_alert=True)
        return
    dialogs = await db.dialog.reader.select_many(session_id=account_id)
    pag = paginate(dialogs, 10)
    reply_markup = keyboards.dialogs(
        pag, page_num=int(data.args[0]), data=data.args[-1], account_id=account_id
    )
    with suppress(TelegramBadRequest):
        await callback.message.edit_reply_markup(reply_markup=reply_markup)


@client_router.callback_query(lambda c: Cd.extract(c.data).data == Cd.Dialogs.move())
async def dialogs_move(callback: types.CallbackQuery, db: DatabaseGateway):
    data = Cd.extract(callback.data)
    session_id = int(data.args[1])
    if data.args[-1] == Cd.Parser.start():
        db_dialogs = await db.dialog.reader.select_many(
            session_id=session_id, chat_type="group"
        )
    else:
        db_dialogs = await db.dialog.reader.select_many(session_id=session_id)
    pag = paginate(db_dialogs, 10)
    reply_markup = keyboards.dialogs(
        ls=pag, page_num=int(data.args[0]), data=data.args[-1], account_id=session_id
    )
    await callback.message.edit_reply_markup(reply_markup=reply_markup)


async def save_dialogs(
    user_id: int, client: TelegramApplication, session_id: int, db: DatabaseGateway
) -> int:
    await db.dialog.writer.delete(session_id=session_id)
    result = []
    async for dialog in client.iter_dialogs():
        from telethon.tl.custom.dialog import Dialog

        dialog: Dialog
        chat_id = dialog.id
        try:
            chat_username = dialog.entity.username
        except AttributeError:
            chat_username = None
        chat_title = dialog.title

        chat_type = ""
        if dialog.is_channel:
            chat_type = "channel"
        if dialog.is_group:
            chat_type = "group"
        if dialog.is_user:
            chat_type = "private"
        admin_rights = None
        participants_count = None
        if dialog.is_channel:
            admin_rights = dialog.entity.admin_rights
            with suppress(AttributeError):
                participants_count = dialog.entity.participants_count
        elif dialog.is_group:
            with suppress(AttributeError):
                participants_count = dialog.entity.participants_count
        if admin_rights:
            admin_rights = admin_rights.__dict__
        res = DialogCreate(
            user_id=user_id,
            session_id=session_id,
            chat_id=chat_id,
            chat_username=chat_username,
            chat_title=chat_title,
            chat_type=chat_type,
            admin_rights=admin_rights,
            members_count=participants_count,
        )
        result.append(res)
    await db.dialog.writer.create_many(data=result)
