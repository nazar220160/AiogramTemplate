from typing import Type

from src.database.models import Session
from src.database.repositories.base import BaseRepository
from src.database.repositories.session.reader import SessionReader
from src.database.repositories.session.writer import SessionWriter


class SessionRepository(BaseRepository[Session]):
    model: Type[Session] = Session

    @property
    def reader(self) -> SessionReader:
        return SessionReader(self)

    @property
    def writer(self) -> SessionWriter:
        return SessionWriter(self)
