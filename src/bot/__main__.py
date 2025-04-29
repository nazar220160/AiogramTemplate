import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from src.bot.common.middlewares import register_middlewares
from src.bot.core import (
    load_bot,
    load_dispatcher,
    load_storage,
)
from src.bot.routers import router
from src.bot.utils.other import set_bot_commands
from src.core.config import Config, load_config
from src.database.core.connection import create_sa_engine, create_sa_session_factory
from src.utils.logger import Logger

logger = Logger()


async def on_startup(bot: Bot, dispatcher: Dispatcher) -> None:
    await set_bot_commands(bot=bot)
    await bot.delete_webhook(drop_pending_updates=True)

    config = load_config()
    if config.bot.use_webhook:
        await bot.set_webhook(
            f"{config.bot.webhook_url}{config.bot.webhook_path}",
            secret_token=config.bot.webhook_secret,
        )

    bot_info = await bot.me()
    logger.info(
        f"Hi {bot_info.username}. Bot started OK! {datetime.now().replace(microsecond=0)}"
    )


async def on_shutdown(bot: Bot) -> None:
    bot_info = await bot.me()
    logger.info(
        f"Hi {bot_info.username}. Bot shutdown OK! {datetime.now().replace(microsecond=0)}"
    )


def init_bot() -> tuple[Bot, Dispatcher, Config]:
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
    return bot, dp, config


async def run_polling(dp: Dispatcher, bot: Bot, config: Config) -> None:
    await dp.start_polling(
        bot, config=config, allowed_updates=dp.resolve_used_update_types()
    )


def run_webhook(dp: Dispatcher, bot: Bot, config: Config) -> None:
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=config.bot.webhook_secret, config=config
    )
    webhook_requests_handler.register(app, path=config.bot.webhook_path)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=config.bot.webhook_host, port=config.bot.webhook_port)


def main():
    bot, dp, config = init_bot()
    if config.bot.use_webhook:
        run_webhook(dp, bot, config)
    else:
        try:
            asyncio.run(run_polling(dp, bot, config))
        except KeyboardInterrupt:
            ...


if __name__ == "__main__":
    main()
