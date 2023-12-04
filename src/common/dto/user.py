from datetime import datetime
from typing import Optional, TYPE_CHECKING, List
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.common.dto.question import QuestionDTO


class UserCreate(BaseModel):
    user_id: int
    first_name: str
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    blocked: Optional[bool] = False
    admin: Optional[bool] = False


class UserUpdate(BaseModel):
    first_name: Optional[bool] = None
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    blocked: Optional[bool] = None
    admin: Optional[bool] = None


class UserDTO(BaseModel):
    user_id: int
    first_name: str
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    blocked: bool
    admin: bool

    questions: List['QuestionDTO']

    created_at: datetime
    updated_at: datetime

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name or ''}"
