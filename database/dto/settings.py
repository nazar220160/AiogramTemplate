from typing import Optional
from pydantic import BaseModel


class ComSubChatsCreate(BaseModel):
    chat_id: int
    username: str
    turn: Optional[bool] = True


class ComSubChatsUpdate(BaseModel):
    chat_id: Optional[int] = None
    username: Optional[str] = None
    turn: Optional[bool] = None


class ComSubChatsDTO(BaseModel):
    chat_id: int
    username: str
    turn: Optional[bool] = False
