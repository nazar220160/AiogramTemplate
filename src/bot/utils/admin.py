from typing import List
from src.database.core.gateway import DatabaseGateway


async def is_admin(user_id: int, admins: List, db: DatabaseGateway) -> bool:
    if user_id in admins:
        return True
    user_info = await db.user.reader.select(user_id=user_id)
    return user_info.admin
