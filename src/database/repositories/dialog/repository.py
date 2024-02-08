from typing import Type

from src.database.models import Dialog
from src.database.repositories.base import BaseRepository
from src.database.repositories.dialog.reader import DialogReader
from src.database.repositories.dialog.writer import DialogWriter


class DialogRepository(BaseRepository[Dialog]):
    model: Type[Dialog] = Dialog

    @property
    def reader(self) -> DialogReader:
        return DialogReader(self)

    @property
    def writer(self) -> DialogWriter:
        return DialogWriter(self)
