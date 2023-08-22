from aiogram import types
from aiogram.filters import BaseFilter

from database import db


class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        if not db.get_all_admins():
            db.add_admin(user_id=message.from_user.id, owner_id=1)
        return db.check_admin(user_id=message.from_user.id)
