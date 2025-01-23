import asyncio
from datetime import datetime
from typing import List

from aiogram import Bot, Dispatcher
from telethon.sessions import StringSession

from src.apps.telethon import TelegramApplication, TelegramAppManager
from src.bot.common.middlewares import register_middlewares
from src.bot.core import (
    load_bot,
    load_dispatcher,
    load_storage,
)
from src.bot.routers import router
from src.bot.utils.other import set_bot_commands
from src.core.config import load_config
from src.database.core.connection import (
    create_sa_engine,
    create_sa_session,
    create_sa_session_factory,
)
from src.database.core.gateway import DatabaseGateway
from src.database.core.unit_of_work import SQLAlchemyUnitOfWork
from src.utils.logger import Logger

logger = Logger()


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    await set_bot_commands(bot=bot)
    await bot.delete_webhook(drop_pending_updates=True)

    bot_info = await bot.me()
    logger.info(
        f"Hi {bot_info.username}. Bot started OK! {datetime.now().replace(microsecond=0)}"
    )


async def on_shutdown(bot: Bot) -> None:
    bot_info = await bot.me()
    logger.info(
        f"Hi {bot_info.username}. Bot shutdown OK! {datetime.now().replace(microsecond=0)}"
    )


async def start_apps(apps: List[TelegramApplication], start: bool = True):
    for app in apps:
        try:
            if start:
                await app.connect()
            logger.info(f"{app.phone_number} | is Started...🍃")
        except Exception as e:
            logger.error(str(e))


async def main() -> None:
    config = load_config()
    bot = load_bot(config=config)
    storage = load_storage(config=config)
    dp = load_dispatcher(storage=storage)

    engine = create_sa_engine(url=config.db.url)
    session_factory = create_sa_session_factory(engine)

    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    register_middlewares(dp=dp, session_factory=session_factory)

    database_sessions = create_sa_session(session_factory=session_factory)
    database_session = await database_sessions.__anext__()

    async with DatabaseGateway(
        unit_of_work=SQLAlchemyUnitOfWork(session=database_session)
    ) as database:
        telegram_sessions = await database.session.reader.select_many()

    apps = []

    for telegram_session in telegram_sessions:
        client = TelegramApplication(
            user_id=telegram_session.user_id,
            session=StringSession(telegram_session.session),
            config=config,
            database_id=telegram_session.id,
            phone_number=telegram_session.phone_number,
            session_factory=session_factory,
            bot=bot,
            test_net=telegram_session.test_net
        )

        apps.append(client)

    sessions = TelegramAppManager(apps=apps)
    await start_apps(apps=apps, start=False)

    await dp.start_polling(
        bot,
        config=config,
        session_factory=session_factory,
        sessions=sessions,
        allowed_updates=dp.resolve_used_update_types(),
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
