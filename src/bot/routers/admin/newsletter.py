from datetime import datetime
from typing import List

from aiogram import types
from aiogram.fsm.context import FSMContext

from src.bot import keyboards
from src.bot.common.filters import IsAdmin
from src.bot.common.middlewares.i18n import gettext as _
from src.bot.common.states.admin import Newsletter
from src.bot.core.models import MyBot
from src.bot.routers.admin.router import admin_router
from src.bot.utils.callback import CallbackData as Cb
from src.bot.utils.texts import admin as texts
from src.database.core.gateway import DatabaseGateway
from src.database.models import User


@admin_router.callback_query(lambda c: Cb.extract(c.data).data == Cb.Admin.ross())
async def ross_handler(
    callback: types.CallbackQuery,
    state: FSMContext,
) -> None:
    await state.set_state(Newsletter.message)
    await state.set_data({"message_id": callback.message.message_id})
    await callback.message.edit_text(
        _(texts.ENTER_MESSAGE_FOR_ROSS),
        reply_markup=keyboards.back(to=Cb.Admin.main()),
    )


@admin_router.callback_query(
    lambda c: Cb.extract(c.data).data == Cb.Admin.confirm_ross()
)
async def confirm_ross(
    callback: types.CallbackQuery,
    db: DatabaseGateway,
) -> None:
    list_users = await db.user.reader.select_many()
    await ross(callback.message, list_users=list_users)


async def ross(message: types.Message, list_users: List[User]):
    errors = []
    good = 0
    file_text = b""
    for i in list_users:
        try:
            await message.copy_to(chat_id=i.id)
            file_text += bytes(f"{i.id}: {_(texts.SUCCESSFUL)}\n", "utf-8")
            good += 1
        except Exception as e:
            errors.append(e)
            file_text += bytes(f"{i.id}: {_(texts.ERROR)} - {e}\n", "utf-8")

    text_file = types.input_file.BufferedInputFile(
        file=file_text,
        filename=_(texts.ROSS_FILE_NAME).format(date=datetime.now().date()),
    )

    await message.edit_reply_markup()
    if file_text:
        await message.reply_document(
            document=text_file,
            caption=_(texts.ROSS_DONE).format(good=good, errors=len(errors)),
            reply_markup=keyboards.back(to=Cb.Admin.main()),
        )


@admin_router.message(Newsletter.message, IsAdmin())
async def get_ross_message(message: types.Message, state: FSMContext, bot: MyBot):
    data = await state.get_data()
    await state.clear()
    await message.copy_to(
        chat_id=message.from_user.id, reply_markup=keyboards.confirm_ross()
    )
    await message.delete()
    await bot.delete_message(
        chat_id=message.from_user.id, message_id=data["message_id"]
    )
