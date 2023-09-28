import abc
from typing import (
    Any,
    Generic,
    Optional,
    Type,
    Dict,
    Iterable,
    Union,
    Sequence,
    TypeVar,
)
from sqlalchemy import ColumnExpressionArgument

EntryType = TypeVar('EntryType')


class AbstractCRUDRepository(abc.ABC, Generic[EntryType]):

    def __init__(self, model: Type[EntryType]) -> None:
        self.model = model

    @abc.abstractmethod
    async def create(self, **values: Dict[str, Any]) -> Optional[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_many(
            self,
            data: Iterable[Union[EntryType, Dict[str, Any]]]
    ) -> Sequence[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def select(
            self,
            *clauses: ColumnExpressionArgument[bool],
    ) -> Optional[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def select_many(
            self,
            *clauses: ColumnExpressionArgument[bool],
            offset: Optional[int],
            limit: Optional[int],
    ) -> Sequence[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(
            self,
            *clauses: ColumnExpressionArgument[bool],
            **values: Dict[str, Any]
    ) -> Sequence[EntryType]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_many(self, data: Iterable[Union[EntryType, Dict[str, Any]]]) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, *clauses: ColumnExpressionArgument[bool]) -> Sequence[EntryType]:
        raise NotImplementedError
