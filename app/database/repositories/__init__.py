from app.database.repositories.base import BaseRepository
from app.database.repositories.user import UserRepository

__all__ = (
    'UserRepository',
)

REPOSITORIES = (
    UserRepository,
)
