from database.repositories.user import UserRepository
from database.repositories.question import QuestionRepository
from database.repositories.settings import ComSubChatsRepository

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
