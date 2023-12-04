from datetime import datetime
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

from src.utils.enums import Status

if TYPE_CHECKING:
    from src.common.dto.user import UserDTO


class QuestionCreate(BaseModel):
    user_message_id: int
    admin_message_id: int
    status: Optional[Status] = Status.PENDING
    user_id: int


class QuestionUpdate(BaseModel):
    user_message_id: Optional[int] = None
    admin_message_id: Optional[int] = None
    status: Optional[Status] = None
    user_id: Optional[int] = None


class QuestionDTO(BaseModel):
    id: int
    user_message_id: int
    admin_message_id: int
    status: Optional[Status]
    user_id: int
    user: Optional['UserDTO']

    created_at: datetime
    updated_at: datetime
