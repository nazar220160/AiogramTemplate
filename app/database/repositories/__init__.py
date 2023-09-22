from app.database.repositories.base import BaseRepository
from app.database.repositories.user import UserRepository
from app.database.repositories.question import QuestionRepository

__all__ = (
    'UserRepository',
    'QuestionRepository',
)

REPOSITORIES = (
    UserRepository,
    QuestionRepository,
)
