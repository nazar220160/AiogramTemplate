from aiogram import F, types
from aiogram.fsm.context import FSMContext
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import MemorySession, StringSession
from src.apps.telethon import TelegramAppManager, TelegramApplication

from src.bot import keyboards
from src.bot.common.middlewares.i18n import gettext as _
from src.bot.common.states.auth import SessionCreation
from src.bot.routers.client.router import client_router
from src.bot.utils.callback import CallbackData as Cd
from src.bot.utils.other import paginate
from src.bot.utils.texts import client as texts
from src.common.dto import SessionCreate
from src.core.config import Config
from src.database.core.gateway import DatabaseGateway


@client_router.callback_query(
    lambda c: Cd.extract(c.data).data == Cd.Accounts.add()
)
async def add_account(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    mes = await callback.message.answer(
        text=_(texts.SEND_PHONE_NUMBER),
        reply_markup=keyboards.back(to=Cd.Start.accounts(), cancel=True),
    )
    await state.set_state(SessionCreation.phone_number)
    await state.set_data(data={"message_id": mes.message_id})


@client_router.message(F.text, SessionCreation.phone_number)
async def get_phone_number(
    message: types.Message,
    state: FSMContext,
    sessions: TelegramAppManager,
    settings: Config,
    session_factory,
):
    phone_number = message.text.replace("+", "").replace(" ", "")

    non_auth_session = sessions.get_client(user_id=message.from_user.id, db_id=None)
    if non_auth_session:
        sessions.apps.remove(non_auth_session)

    client = TelegramApplication(
        user_id=message.from_user.id,
        session=MemorySession(),
        settings=settings,
        phone_number=phone_number,
        session_factory=session_factory
    )
    await client.connect()

    state_data = await state.get_data()

    try:
        res = await client.send_code_request(message.text)
        await message.bot.delete_message(
            chat_id=message.chat.id, message_id=state_data["message_id"]
        )
        mes = await message.answer(
            text=_(texts.SEND_CODE).format(phone_number),
            reply_markup=keyboards.back(to=Cd.Start.accounts(), cancel=True),
        )
        await state.set_state(SessionCreation.code)
        await state.set_data(
            data={"message_id": mes.message_id, "phone_code_hash": res.phone_code_hash}
        )
        sessions.apps.append(client)
    except Exception as e:
        await message.reply(
            text=str(e),
            reply_markup=keyboards.back(to=Cd.Start.accounts(), main_menu=True),
            parse_mode=None,
        )


@client_router.message(F.text, SessionCreation.code)
async def get_code(
    message: types.Message,
    state: FSMContext,
    sessions: TelegramAppManager,
    db: DatabaseGateway,
):
    code = message.text.replace(" ", "")

    state_data = await state.get_data()
    client: TelegramApplication = sessions.get_client(
        user_id=message.from_user.id, db_id=None
    )

    try:
        res = await client.sign_in(
            phone=client.phone_number,
            code=code,
            phone_code_hash=state_data["phone_code_hash"],
        )
    except SessionPasswordNeededError:
        await state.set_state(SessionCreation.password)
        state_data["code"] = code
        await state.set_data(state_data)
        await message.reply(
            text=_(texts.SEND_2FA_CODE),
            reply_markup=keyboards.back(to=Cd.Back.main_menu(), cancel=True),
        )
        return
    except Exception as e:
        await message.reply(
            text=str(e),
            parse_mode=None,
            reply_markup=keyboards.back(to=Cd.Back.main_menu(), cancel=True),
        )
        return

    await add_account_hd(message, client, db, state, res)


@client_router.message(F.text, SessionCreation.password)
async def get_2fa_code(
    message: types.Message,
    state: FSMContext,
    sessions: TelegramAppManager,
    db: DatabaseGateway,
):
    client: TelegramApplication = sessions.get_client(
        user_id=message.from_user.id, db_id=None
    )
    try:
        res = await client.sign_in(phone=client.phone_number, password=message.text)
    except Exception as e:
        await message.reply(
            text=str(e),
            parse_mode=None,
            reply_markup=keyboards.back(to=Cd.Back.main_menu(), cancel=True),
        )
        return

    await add_account_hd(message, client, db, state, res)


async def add_account_hd(message, client: TelegramApplication, db, state, res):
    string_session = StringSession.save(client.session)

    res = await db.session.create(
        query=SessionCreate(
            user_id=message.from_user.id,
            phone_number=client.phone_number,
            session=string_session,
            first_name=res.first_name,
            last_name=res.last_name,
            username=res.username,
        )
    )
    await state.clear()

    client.db_id = res.id

    list_sessions = await db.session.select_many_with_user_id(
        user_id=message.from_user.id
    )
    pag = paginate(list_items=list_sessions, items_per_page=6)

    await message.answer(
        text=_(texts.ACCOUNT_ADDED_SUCCESS), reply_markup=keyboards.accounts_list(pag)
    )

    if client.is_connected():
        client.disconnect()
