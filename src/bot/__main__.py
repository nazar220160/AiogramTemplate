import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher

from src.bot.common.middlewares import register_middlewares
from src.bot.utils.other import set_bot_commands
from src.bot.routers import router
from src.bot.utils.polling_manager import PollingManager

from src.bot.core import (
    load_bot,
    load_dispatcher,
    load_storage,
)
from src.config import load_settings
from src.utils.logger import Logger

logger = Logger()


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    await set_bot_commands(bot=bot)
    register_middlewares(dp=dispatcher)
    await bot.delete_webhook(drop_pending_updates=True)

    bot_info = await bot.me()
    logger.info(f'Hi {bot_info.username}. Bot started OK! {datetime.now().replace(microsecond=0)}')


async def on_shutdown(bot: Bot) -> None:
    bot_info = await bot.me()
    logger.info(f'Hi {bot_info.username}. Bot shutdown OK! {datetime.now().replace(microsecond=0)}')


async def main() -> None:
    settings = load_settings()
    bot = load_bot(settings=settings)
    storage = load_storage(settings=settings)
    dp = load_dispatcher(storage=storage)
    polling_manager = PollingManager()

    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(
        bot, settings=settings, polling_manager=polling_manager,
        allowed_updates=dp.resolve_used_update_types()
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        ...
