import asyncio
from datetime import datetime

from app.common.middlewares import register_middlewares
from app.utils.other import set_bot_commands
from app.routers import router
from app.core import (
    load_bot,
    load_dispatcher,
    load_storage,
    load_settings,
)


async def on_startup(dp, bot) -> None:
    register_middlewares(dp=dp)
    dp.include_router(router)
    await set_bot_commands(bot=bot)
    await bot.delete_webhook(drop_pending_updates=True)


async def main() -> None:
    settings = load_settings()
    bot = load_bot(settings=settings)
    storage = load_storage(settings=settings)
    dp = load_dispatcher(storage=storage)

    await on_startup(bot=bot, dp=dp)

    bot_info = await bot.me()
    print(f'Hi {bot_info.username}. Bot started OK!\n «««  {datetime.now().replace(microsecond=0)}  »»»')
    await dp.start_polling(
        bot, settings=settings,
        allowed_updates=dp.resolve_used_update_types()
    )


if __name__ == '__main__':
    asyncio.run(main())
