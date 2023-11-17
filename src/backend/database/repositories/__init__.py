from src.backend.database.repositories.user import UserRepository
from src.backend.database.repositories.question import QuestionRepository
from src.backend.database.repositories.settings import ComSubChatsRepository

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
