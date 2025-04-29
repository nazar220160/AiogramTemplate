from aiogram import types
from aiogram.fsm.context import FSMContext

from src.apps.telethon import TelegramApplication, TelegramAppManager
from src.bot import keyboards
from src.bot.common.middlewares.i18n import gettext as _
from src.bot.routers.client.router import client_router
from src.bot.utils.callback import CallbackData as Cd
from src.bot.utils.other import paginate
from src.bot.utils.texts import client as texts
from src.database.core.gateway import DatabaseGateway


@client_router.callback_query(lambda c: Cd.extract(c.data).data == Cd.Start.accounts())
async def start(callback: types.CallbackQuery, db: DatabaseGateway, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    sessions = await db.session.reader.select_many(user_id=callback.from_user.id)
    pag = paginate(list_items=sessions, items_per_page=6)
    reply_markup = keyboards.accounts_list(pag)
    await callback.message.answer(
        text=_(texts.YOUR_ACCOUNTS), reply_markup=reply_markup
    )


@client_router.callback_query(lambda c: Cd.extract(c.data).data == Cd.Accounts.move())
async def account_move(callback: types.CallbackQuery, db: DatabaseGateway):
    data = Cd.extract(callback.data)
    settings = True if data.args[1] == "True" else False
    sessions = await db.session.reader.select_many(user_id=callback.from_user.id)
    pag = paginate(sessions, 6)
    reply_markup = keyboards.accounts_list(
        ls=pag, page_num=int(data.args[0]), data=data.args[-1], settings=settings
    )
    await callback.message.edit_reply_markup(reply_markup=reply_markup)


@client_router.callback_query(
    lambda c: Cd.extract(c.data).data == Cd.Accounts.settings()
)
async def account_settings(
    callback: types.CallbackQuery, sessions: TelegramAppManager, db: DatabaseGateway
):
    data = Cd.extract(callback.data)
    session_id = int(data.args[0])
    account_base = await db.session.reader.select(session_id=session_id)
    client: TelegramApplication = sessions.get_client(database_id=session_id)
    reply_markup = keyboards.session_settings(
        included=client.is_connected(), session_id=session_id
    )
    text = _(texts.SESSION_SETTING).format(
        account_base.phone_number,
        f"{account_base.first_name} {account_base.last_name if account_base.last_name else ''}",
        f"{'✅' if client.is_connected() is True else '⛔️'}",
    )
    await callback.message.edit_text(text=text, reply_markup=reply_markup)


@client_router.callback_query(
    lambda c: Cd.extract(c.data, True).data == Cd.AccountSettings()
)
async def account_setting(
    callback: types.CallbackQuery,
    sessions: TelegramAppManager,
    db: DatabaseGateway,
) -> None:
    data = Cd.extract(callback.data)
    session_id = int(data.args[0])

    client: TelegramApplication = sessions.get_client(database_id=session_id)

    if data.data == Cd.AccountSettings.remove():
        if client.is_connected():
            await client.disconnect()

        await db.session.writer.delete(session_id=session_id)

        db_sessions = await db.session.reader.select_many(user_id=callback.from_user.id)
        pag = paginate(db_sessions, 6)

        reply_markup = keyboards.accounts_list(pag)

        await callback.message.edit_text(
            text=_(texts.REMOVE_SESSION_SUCCESSFUL).format(client.phone_number),
            reply_markup=reply_markup,
        )
        sessions.apps.remove(client)

    elif data.data == Cd.AccountSettings.turn():
        if client.is_connected():
            await client.disconnect()
            info = f"{client.phone_number} | is Stopped...💣"
        else:
            await client.connect()
            info = f"{client.phone_number} | is Started...🍃"

        account_base = await db.session.reader.select(session_id=session_id)
        text = _(texts.SESSION_SETTING).format(
            account_base.phone_number,
            f"{account_base.first_name} {account_base.last_name if account_base.last_name else ''}",
            f"{'✅' if client.is_connected() is True else '⛔️'}",
        )
        reply_markup = keyboards.session_settings(
            included=client.is_connected(), session_id=session_id
        )

        await callback.message.edit_text(text=text, reply_markup=reply_markup)
        await callback.answer(text=info, show_alert=True)

    elif data.data == Cd.AccountSettings.dialogs():
        dialogs = await db.dialog.reader.select_many(session_id=session_id)
        pag = paginate(dialogs, 10)
        reply_markup = keyboards.dialogs(pag, data="none", account_id=session_id)
        await callback.message.edit_text(
            text=_(texts.DIALOGS_LIST), reply_markup=reply_markup
        )


@client_router.callback_query(lambda c: Cd.extract(c.data).data == Cd.Accounts.select())
async def account_select(
    callback: types.CallbackQuery,
):
    cb_data = Cd.extract(callback.data)
    if cb_data.args[-1] == "Callback":
        ...
