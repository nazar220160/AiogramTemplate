from typing import Type

from src.database.models import Question
from src.database.repositories.base import BaseRepository
from src.database.repositories.question.reader import QuestionReader
from src.database.repositories.question.writer import QuestionWriter


class QuestionRepository(BaseRepository[Question]):
    model: Type[Question] = Question

    @property
    def reader(self) -> QuestionReader:
        return QuestionReader(self)

    @property
    def writer(self) -> QuestionWriter:
        return QuestionWriter(self)
