from src.database.repositories.user import UserRepository
from src.database.repositories.question import QuestionRepository
from src.database.repositories.settings import ComSubChatsRepository

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
