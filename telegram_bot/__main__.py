import asyncio
from datetime import datetime

from telegram_bot.handlers import register_start_handlers
from telegram_bot.middlewares import register_all_middlewares
from telegram_bot.misc.loader import dp, bot
from telegram_bot.misc.utils import set_bot_commands


async def main() -> None:
    register_all_middlewares(dp=dp)
    register_start_handlers(dp=dp)
    await set_bot_commands(bot=bot)

    bot_info = await bot.me()
    print(f'Hi {bot_info.username}. Bot started OK!\n «««  {datetime.now().replace(microsecond=0)}  »»»')

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        quit(0)
