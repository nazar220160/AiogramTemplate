from typing import Any, List, Optional, Union

from aiogram.filters import Filter
from aiogram import types

from src.config.settings import load_settings
from src.database.core import Database
from src.bot.utils import is_admin


class IsAdmin(Filter):

    def __init__(self, admins: Optional[List[int]] = None) -> None:
        if admins is None:
            admins = load_settings().admins
        self.admins = admins or []

    async def __call__(
            self, event: Union[types.CallbackQuery, types.Message], db: Database
    ) -> Any:
        return await is_admin(user_id=event.from_user.id, admins=self.admins, db=db)
