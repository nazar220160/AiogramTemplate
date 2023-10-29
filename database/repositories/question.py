from typing import (
    Optional,
    Type,
    List,
)

from database.converters import convert_question_model_to_dto
from database.dto import (
    QuestionCreate,
    QuestionDTO,
    QuestionUpdate,
)
from database.interfaces.repositories.base import Repository
from database.models import Question
from database.repositories.base import BaseRepository


class QuestionRepository(
    BaseRepository[Question],
    Repository[int, QuestionDTO, QuestionCreate, QuestionUpdate]
):
    model: Type[Question] = Question

    async def create(self, query: QuestionCreate) -> Optional[QuestionDTO]:
        result = await self._crud.create(**query.model_dump(exclude_none=True))
        if not result:
            return None

        return convert_question_model_to_dto(result)

    async def select(self, admin_message_id: int) -> Optional[QuestionDTO]:
        result = await self._crud.select(self.model.admin_message_id == admin_message_id)
        if not result:
            return None

        return convert_question_model_to_dto(result)

    async def select_many(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> List[QuestionDTO]:
        result = await self._crud.select_many(offset=offset, limit=limit)
        return [convert_question_model_to_dto(model) for model in result]

    async def update(
            self, admin_message_id: int, query: QuestionUpdate, exclude_none: bool = True
    ) -> List[QuestionDTO]:
        result = await self._crud.update(
            self.model.admin_message_id == admin_message_id,
            **query.model_dump(exclude_none=exclude_none)
        )
        return [convert_question_model_to_dto(model) for model in result]

    async def delete(self, user_message_id: int) -> List[QuestionDTO]:
        result = await self._crud.delete(self.model.user_message_id == user_message_id)
        return [convert_question_model_to_dto(model) for model in result]
