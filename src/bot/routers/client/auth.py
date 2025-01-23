from asyncio.exceptions import TimeoutError
from contextlib import suppress

from aiogram import F, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import MemorySession, StringSession

from src.apps.telethon import TelegramApplication, TelegramAppManager
from src.bot import keyboards
from src.bot.common.middlewares.i18n import gettext as _
from src.bot.common.states.auth import SessionCreation
from src.bot.core.models import MyBot
from src.bot.routers.client.router import client_router
from src.bot.utils.callback import CallbackData as Cd
from src.bot.utils.other import paginate
from src.bot.utils.texts import client as texts
from src.common.dto import SessionCreate
from src.core.config import Config
from src.database.core.gateway import DatabaseGateway
from src.utils.qr_code import generate_qr_code


@client_router.callback_query(lambda c: Cd.extract(c.data).data == Cd.Accounts.add())
async def add_account(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    mes = await callback.message.answer(
        text=_(texts.SEND_PHONE_NUMBER),
        reply_markup=keyboards.auth_account(),
    )
    await state.set_state(SessionCreation.phone_number)
    await state.set_data(data={"message_id": mes.message_id})


@client_router.callback_query(
    lambda c: Cd.extract(c.data).data == Cd.Accounts.auth_with_qr(),
    SessionCreation.phone_number,
)
async def add_account_with_qr(
    callback: types.CallbackQuery,
    state: FSMContext,
    sessions: TelegramAppManager,
    db: DatabaseGateway,
    session_factory,
    config: Config,
    bot: MyBot,
):
    await state.clear()
    await callback.message.delete()

    non_auth_session = sessions.get_client(user_id=callback.from_user.id, database_id=None)
    if non_auth_session:
        sessions.apps.remove(non_auth_session)

    client = TelegramApplication(
        user_id=callback.from_user.id,
        session=MemorySession(),
        config=config,
        session_factory=session_factory,
        bot=bot,
    )

    await client.connect()
    qr_login = await client.qr_login()
    qr_code_image = generate_qr_code(qr_login.url)

    mes = await callback.message.answer_photo(
        photo=types.BufferedInputFile(qr_code_image, filename="auth_code"),
        caption=_(texts.AUTH_QR_CODE),
        reply_markup=keyboards.back(to=Cd.Start.accounts(), cancel=True),
    )

    await state.set_state(SessionCreation.phone_number)
    await state.set_data(data={"message_id": mes.message_id})
    try:
        res = await qr_login.wait(timeout=300)
    except SessionPasswordNeededError:
        with suppress(TelegramBadRequest):
            await mes.reply(texts.SESSION_PASSWORD_NEEDED_PLS_OFF)
        return
    except TimeoutError:
        with suppress(TelegramBadRequest):
            await mes.delete()
        return

    client.phone_number = res.phone

    await mes.delete()
    await add_account_hd(
        user_id=callback.from_user.id,
        bot=bot,
        client=client,
        db=db,
        state=state,
        res=res,
    )
    sessions.apps.append(client)


@client_router.message(F.text, SessionCreation.phone_number)
async def get_phone_number(
    message: types.Message,
    state: FSMContext,
    sessions: TelegramAppManager,
    config: Config,
    session_factory,
):
    phone_number = message.text.replace("+", "").replace(" ", "")

    non_auth_session = sessions.get_client(
        user_id=message.from_user.id, database_id=None
    )
    if non_auth_session:
        sessions.apps.remove(non_auth_session)

    client = TelegramApplication(
        user_id=message.from_user.id,
        session=MemorySession(),
        config=config,
        phone_number=phone_number,
        session_factory=session_factory,
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
    bot: MyBot
):
    code = message.text.replace(" ", "")

    state_data = await state.get_data()
    client: TelegramApplication = sessions.get_client(
        user_id=message.from_user.id, database_id=None
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

    await add_account_hd(message.from_user.id, bot, client, db, state, res)


@client_router.message(F.text, SessionCreation.password)
async def get_2fa_code(
    message: types.Message,
    state: FSMContext,
    sessions: TelegramAppManager,
    db: DatabaseGateway,
    bot: MyBot
):
    client: TelegramApplication = sessions.get_client(
        user_id=message.from_user.id, database_id=None
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

    await add_account_hd(message.from_user.id, bot, client, db, state, res)


async def add_account_hd(
    user_id: int, bot: MyBot, client: TelegramApplication, db: DatabaseGateway, state, res
):
    string_session = StringSession.save(client.session)

    res = await db.session.writer.create(
        query=SessionCreate(
            user_id=user_id,
            phone_number=client.phone_number,
            session=string_session,
            first_name=res.first_name,
            last_name=res.last_name,
            username=res.username,
        )
    )
    await state.clear()

    client.database_id = res.id

    list_sessions = await db.session.reader.select_many(user_id=user_id)
    pag = paginate(list_items=list_sessions, items_per_page=6)

    await bot.send_message(
        chat_id=user_id,
        text=_(texts.ACCOUNT_ADDED_SUCCESS),
        reply_markup=keyboards.accounts_list(pag),
    )

    if client.is_connected():
        client.disconnect()
