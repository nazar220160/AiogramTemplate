import asyncio

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, async_scoped_session

from config import db_url

Base = declarative_base()
engine = create_async_engine(db_url)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Session = async_scoped_session(async_session, scopefunc=asyncio.current_task)


class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    user_id = sa.Column(sa.BigInteger)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    username = sa.Column(sa.Text)
    ref_id = sa.Column(sa.BigInteger, default=None)
    is_admin = sa.Column(sa.BigInteger, default=0)
    register_datetime = sa.Column(sa.DateTime)

    async def edit_info(self, column_name, new_value):
        async with Session() as session:
            table = self.__table__

            # Создаем объект запроса для обновления записи
            update_query = (
                sa.update(table)
                .where(table.c.user_id == self.user_id)
                .values({column_name: new_value})
            )
            # Выполняем запрос к базе данных
            await session.execute(update_query)
            await session.commit()


class Question(Base):
    __tablename__ = "question"
    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    user_message_id = sa.Column(sa.BigInteger)
    admin_message_id = sa.Column(sa.BigInteger)
    answered = sa.Column(sa.Boolean, default=False)

    async def is_answer(self):
        async with Session() as session:
            table = self.__table__

            # Создаем объект запроса для обновления записи
            update_query = (
                sa.update(table)
                .where(table.c.id == self.id)
                .values({'answered': True})
            )

            # Выполняем запрос к базе данных
            await session.execute(update_query)
            await session.commit()
