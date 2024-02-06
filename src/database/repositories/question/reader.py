from typing import Any, Optional, Sequence, overload

from sqlalchemy import select

from src.common.types import OrderByType
from src.database.exceptions import InvalidParamsError
from src.database.models import Question
from src.database.repositories.base import BaseInteractor
from src.utils.enums import Status


class QuestionReader(BaseInteractor[Question]):
    @overload
    async def select(self, *, question_id: int) -> Optional[Question]: ...

    @overload
    async def select(self, *, user_message_id: int) -> Optional[Question]: ...

    @overload
    async def select(self, *, admin_message_id: int) -> Optional[Question]: ...

    async def select(self, **kwargs: Any) -> Optional[Question]:
        if admin_message_id := kwargs.get("admin_message_id"):
            result = await self.crud.select(
                self.model.admin_message_id == admin_message_id
            )
        elif admin_message_id := kwargs.get("admin_message_id"):
            result = await self.crud.select(
                self.model.admin_message_id == admin_message_id
            )
        elif question_id := kwargs.get("question_id"):
            result = await self.crud.select(self.model.id == question_id)
        else:
            raise InvalidParamsError(f"{tuple(kwargs.keys())} is not valid params")

        return result

    @overload
    async def select_many(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[Question]: ...

    @overload
    async def select_many(
        self,
        *,
        user_id: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[Question]: ...

    @overload
    async def select_many(
        self,
        *,
        status: Status,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: OrderByType,
    ) -> Sequence[Question]: ...

    async def select_many(
        self,
        *,
        order_by: OrderByType = "ASC",
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **kwargs: Any,
    ) -> Sequence[Question]:
        if user_id := kwargs.get("user_id"):
            stmt = (
                select(self.model)
                .where(self.model.user_id == user_id)
                .offset(offset)
                .limit(limit)
                .order_by(
                    self.model.id.asc() if order_by == "ASC" else self.model.id.desc()
                )
            )
            result = (await self.session.execute(stmt)).scalars().all()
        elif status := kwargs.get("status"):
            stmt = (
                select(self.model)
                .where(self.model.status == status)
                .offset(offset)
                .limit(limit)
                .order_by(
                    self.model.id.asc() if order_by == "ASC" else self.model.id.desc()
                )
            )
            result = (await self.session.execute(stmt)).scalars().all()
        else:
            result = await self.crud.select_many(offset=offset, limit=limit)
        return result
