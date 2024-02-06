import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher

from src.bot.common.middlewares import register_middlewares
from src.bot.core import (
    load_bot,
    load_dispatcher,
    load_storage,
)
from src.bot.routers import router
from src.bot.utils.other import set_bot_commands
from src.config import load_settings
from src.database.core.connection import create_sa_engine, create_sa_session_factory
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


async def main() -> None:
    settings = load_settings()
    bot = load_bot(settings=settings)
    storage = load_storage(settings=settings)
    dp = load_dispatcher(storage=storage)

    engine = create_sa_engine(url=settings.db_url)
    session_factory = create_sa_session_factory(engine)

    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    register_middlewares(dp=dp, session_factory=session_factory)

    await dp.start_polling(
        bot,
        settings=settings,
        allowed_updates=dp.resolve_used_update_types()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
