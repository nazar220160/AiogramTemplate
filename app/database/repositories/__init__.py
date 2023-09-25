from app.database.repositories.base import BaseRepository
from app.database.repositories.user import UserRepository
from app.database.repositories.question import QuestionRepository
from app.database.repositories.settings import ComSubChatsRepository

__all__ = (
    'UserRepository',
    'QuestionRepository',
    'ComSubChatsRepository',
)

REPOSITORIES = (
    UserRepository,
    QuestionRepository,
    ComSubChatsRepository,
)
