from aiogram import types
from aiogram.filters import BaseFilter

from telegram_bot.database import base


class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if not await base.get_all_admins():
            await base.add_admin(user_id=message.from_user.id, owner_id=1)
        return await base.check_admin(user_id=message.from_user.id)
