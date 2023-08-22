import asyncio
from datetime import datetime

from aiogram.enums import UpdateType
from handlers import register_start_handlers
from middlewares import register_all_middlewares
from misc.loader import dp, bot
from misc.utils import set_bot_commands


async def bot_start():
    register_all_middlewares(dp=dp)
    register_start_handlers(dp=dp)
    await set_bot_commands(bot=bot)
    bot_info = await bot.me()
    print(f'Hi {bot_info.username}. Bot started OK!\n «««  {datetime.now().replace(microsecond=0)}  »»»')

    await dp.start_polling(bot, allowed_updates=[UpdateType.MESSAGE, UpdateType.CALLBACK_QUERY])


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(bot_start())
    except KeyboardInterrupt:
        quit(0)
