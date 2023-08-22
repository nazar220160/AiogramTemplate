from sqlalchemy import create_engine, Column, BigInteger, Text, Integer, Float, DateTime, update, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config import CREATE_ENGINE

Base = declarative_base()
engine = create_engine(CREATE_ENGINE)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger)
    first_name = Column(Text)
    last_name = Column(Text)
    username = Column(Text)
    ref_id = Column(BigInteger, default=None)
    balance = Column(Float, default=0)
    lang = Column(Text)
    is_admin = Column(BigInteger, default=0)
    register_datetime = Column(DateTime)

    def edit_info(self, column_name, new_value):
        with Session() as session:
            table = self.__table__

            # Создаем объект запроса для обновления записи
            update_query = (
                update(table)
                .where(table.c.user_id == self.user_id)
                .values({column_name: new_value})
            )

            # Выполняем запрос к базе данных
            session.execute(update_query)
            session.commit()


class Question(Base):
    __tablename__ = "question"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_message_id = Column(BigInteger)
    admin_message_id = Column(BigInteger)
    answered = Column(Boolean, default=False)

    def is_answer(self):
        with Session() as session:
            table = self.__table__

            # Создаем объект запроса для обновления записи
            update_query = (
                update(table)
                .where(table.c.id == self.id)
                .values({'answered': True})
            )

            # Выполняем запрос к базе данных
            session.execute(update_query)
            session.commit()
