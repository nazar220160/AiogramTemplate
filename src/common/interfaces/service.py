import abc
from typing import Any, Generic, TypeVar

from src.common.interfaces.repository import Repository

RepositoryType = TypeVar("RepositoryType", bound=Repository)


class Service(abc.ABC, Generic[RepositoryType]):
    def __init__(self, repository: RepositoryType, **kwargs: Any) -> None:
        self._repository = repository
