import asyncio
from telegram_bot.database.base import create_tables

loop = asyncio.get_event_loop()
loop.run_until_complete(create_tables())
