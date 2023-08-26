from datetime import datetime
from telegram_bot.database.models import User, Session, Base, engine, Question
import sqlalchemy as sa


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def check_user(user_id: int) -> bool:
    async with Session() as session:
        result = await session.execute(sa.select(User).filter_by(user_id=int(user_id)))
        result = result.scalars().first()
        return bool(result)


async def get_all_admins() -> list[User]:
    async with Session() as session:
        result = await session.execute(sa.select(User).filter(User.is_admin != 0))
        result = result.scalars().all()

        return result


async def check_admin(user_id: int) -> bool:
    async with Session() as session:
        result = await session.execute(sa.select(User).filter_by(user_id=int(user_id)).filter(User.is_admin != 0))
        result = result.scalars().first()
        return bool(result)


async def add_admin(user_id: int, owner_id: int):
    async with Session() as session:
        await session.execute(sa.update(User).where(User.user_id == user_id).values(is_admin=owner_id))
        await session.commit()


async def remove_admin(user_id: int):
    async with Session() as session:
        await session.execute(sa.update(User).where(User.user_id == user_id).values(is_admin=0))
        await session.commit()


async def add_user(user_id: int, lang: str, first_name, last_name, username, ref_id=None) -> User:
    async with Session() as session:
        result = await session.execute(sa.select(User).filter(User.user_id == int(user_id)))
        existing_user = result.scalar_one_or_none()

        if existing_user is None:
            new_user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                            ref_id=ref_id, lang=lang, register_datetime=datetime.now())
            session.add(new_user)
            await session.commit()

        return existing_user


async def get_user_by_user_id(user_id: int) -> User:
    async with Session() as session:
        result = await session.execute(sa.select(User).filter_by(user_id=int(user_id)))
        result = result.scalars().first()
        return result


async def get_user_by_id(id_user: int) -> User:
    async with Session() as session:
        result = await session.execute(sa.select(User).filter_by(id=id_user))
        result = result.scalars().first()
        return result


async def get_all_users() -> list[User]:
    async with Session() as session:
        result = await session.execute(sa.select(User))
        result = result.scalars().all()
        return result


async def get_question(admin_message_id) -> Question:
    async with Session() as session:
        result = await session.execute(sa.select(Question).filter_by(admin_message_id=admin_message_id))
        result = result.scalars().first()
        return result


async def add_question(user_message_id: int, admin_message_id: int):
    async with Session() as session:
        new_user = Question(user_message_id=user_message_id, admin_message_id=admin_message_id)
        session.add(new_user)
        await session.commit()
