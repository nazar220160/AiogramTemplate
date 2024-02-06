from typing import Any, List, Optional, Union

from aiogram import types
from aiogram.filters import Filter

from src.bot.utils import is_admin
from src.core.config import load_config
from src.database.core.gateway import DatabaseGateway


class IsAdmin(Filter):

    def __init__(self, admins: Optional[List[int]] = None) -> None:
        if admins is None:
            admins = load_config().bot.admins
        self.admins = admins or []

    async def __call__(
        self, event: Union[types.CallbackQuery, types.Message], db: DatabaseGateway
    ) -> Any:
        return await is_admin(user_id=event.from_user.id, admins=self.admins, db=db)
