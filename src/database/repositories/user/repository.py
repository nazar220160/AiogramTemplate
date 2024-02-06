from typing import Type

from src.database.models import User
from src.database.repositories.base import BaseRepository
from src.database.repositories.user.reader import UserReader
from src.database.repositories.user.writer import UserWriter


class UserRepository(BaseRepository[User]):
    model: Type[User] = User

    @property
    def reader(self) -> UserReader:
        return UserReader(self)

    @property
    def writer(self) -> UserWriter:
        return UserWriter(self)
