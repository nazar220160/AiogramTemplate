from typing import Optional

from src.common.dto import UserCreate, UserUpdate
from src.database.models import User
from src.database.repositories.base import BaseInteractor


class UserWriter(BaseInteractor[User]):
    async def create(self, query: UserCreate) -> Optional[User]:
        return await self.crud.create(**query.model_dump(exclude_none=True))

    async def update(self, user_id: int, query: UserUpdate) -> Optional[User]:
        result = await self.crud.update(
            self.model.id == user_id, **query.model_dump(exclude_none=True)
        )
        return result[0] if result else None
