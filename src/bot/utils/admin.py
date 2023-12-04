from typing import List
from src.database.core import Database


async def is_admin(user_id: int, admins: List, db: Database) -> bool:
    if user_id in admins:
        return True
    user_info = await db.user.select(user_id=user_id)
    return user_info.admin
