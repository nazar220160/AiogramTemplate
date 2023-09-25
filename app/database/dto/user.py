from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    user_id: int
    first_name: str
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    admin: Optional[bool] = False


class UserUpdate(BaseModel):
    first_name: Optional[bool] = None
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    admin: Optional[bool] = False


class UserDTO(BaseModel):
    user_id: int
    first_name: str
    username: Optional[str] = None
    last_name: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    admin: Optional[bool] = False

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name or ''}"
