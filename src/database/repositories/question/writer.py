from typing import Any, Optional, overload

from src.common.dto import QuestionCreate, QuestionUpdate
from src.database.exceptions import InvalidParamsError
from src.database.models import Question
from src.database.repositories.base import BaseInteractor


class QuestionWriter(BaseInteractor[Question]):

    async def create(self, query: QuestionCreate) -> Optional[Question]:
        return await self.crud.create(**query.model_dump(exclude_none=True))

    @overload
    async def update(
        self, *, question_id: int, query: QuestionUpdate
    ) -> Optional[Question]: ...

    @overload
    async def update(
        self, *, user_message_id: int, query: QuestionUpdate
    ) -> Optional[Question]: ...

    @overload
    async def update(
        self, *, admin_message_id: int, query: QuestionUpdate
    ) -> Optional[Question]: ...

    async def update(
        self, *, query: QuestionUpdate, **kwargs: Any
    ) -> Optional[Question]:
        if question_id := kwargs.get("question_id"):
            result = await self.crud.update(
                self.model.id == question_id, **query.model_dump(exclude_none=True)
            )
        elif user_message_id := kwargs.get("user_message_id"):
            result = await self.crud.update(
                self.model.user_message_id == user_message_id,
                **query.model_dump(exclude_none=True),
            )
        elif admin_message_id := kwargs.get("admin_message_id"):
            result = await self.crud.update(
                self.model.admin_message_id == admin_message_id,
                **query.model_dump(exclude_none=True),
            )
        else:
            raise InvalidParamsError(f"{tuple(kwargs.keys())} is not valid params")

        return result[0] if result else None
