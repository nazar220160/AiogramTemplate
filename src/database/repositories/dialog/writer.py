from typing import List, Optional, Sequence

from src.common.dto import DialogCreate, DialogUpdate
from src.database.models import Dialog
from src.database.repositories.base import BaseInteractor


class DialogWriter(BaseInteractor[Dialog]):

    async def create(self, query: DialogCreate) -> Optional[Dialog]:
        return await self.crud.create(**query.model_dump(exclude_none=True))

    async def create_many(self, data: List[DialogCreate]) -> Sequence[Dialog]:
        data = [i.model_dump(exclude_none=True) for i in data]
        return await self.crud.create_many(data)

    async def update(self, user_id: int, query: DialogUpdate) -> Optional[Dialog]:
        result = await self.crud.update(
            self.model.id == user_id, **query.model_dump(exclude_none=True)
        )
        return result[0] if result else None

    async def delete(self, session_id: int) -> Sequence[Dialog]:
        return await self.crud.delete(self.model.session_id == session_id)
