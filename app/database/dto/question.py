from typing import Optional
from pydantic import BaseModel


class QuestionCreate(BaseModel):
    user_message_id: int
    admin_message_id: int
    answered: Optional[bool] = False


class QuestionUpdate(BaseModel):
    user_message_id: Optional[int] = None
    admin_message_id: Optional[int] = None
    answered: Optional[bool] = False


class QuestionDTO(BaseModel):
    user_message_id: int
    admin_message_id: int
    answered: Optional[bool] = False
