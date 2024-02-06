from typing import Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.interfaces.repository import Repository
from src.database.repositories.crud import ModelType, SQLAlchemyCRUDRepository


class BaseRepository(Repository, Generic[ModelType]):
    """
    Base repository class for interacting with a specific SQLAlchemy model using asynchronous sessions.

    Args:
        session (AsyncSession): The SQLAlchemy asynchronous session to be used for database operations.

    Attributes:
        _session (AsyncSession): The SQLAlchemy asynchronous session associated with the repository.
        _crud (SQLAlchemyCRUDRepository[ModelType]): The CRUD repository for the specific model.
    """

    model: Type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the repository with the provided asynchronous session.

        Args:
            session (AsyncSession): The SQLAlchemy asynchronous session to be used for database operations.
        """
        self._session = session
        self._crud = SQLAlchemyCRUDRepository(session, self.model)


class BaseInteractor(Generic[ModelType]):
    """
    Base interactor class for interacting with a specific SQLAlchemy model through a repository.

    Args:
        repo (BaseRepository[ModelType]): The repository associated with the interactor.
    """

    __slots__ = ("_repo",)

    def __init__(self, repo: BaseRepository[ModelType]) -> None:
        """
        Initialize the interactor with the provided repository.

        Args:
            repo (BaseRepository[ModelType]): The repository associated with the interactor.
        """
        self._repo = repo

    @property
    def session(self) -> AsyncSession:
        """
        Get the SQLAlchemy asynchronous session associated with the interactor.

        Returns:
            AsyncSession: The SQLAlchemy asynchronous session.
        """
        return self._repo._session

    @property
    def crud(self) -> SQLAlchemyCRUDRepository[ModelType]:
        """
        Get the CRUD repository associated with the interactor.

        Returns:
            SQLAlchemyCRUDRepository[ModelType]: The CRUD repository.
        """
        return self._repo._crud

    @property
    def model(self) -> Type[ModelType]:
        """
        Get the SQLAlchemy model associated with the interactor.

        Returns:
            Type[ModelType]: The SQLAlchemy model class.
        """
        return self._repo.model
