import io
from datetime import datetime
from database.databases import User, Session, Base, engine

Base.metadata.create_all(engine)


def check_user(user_id: int) -> bool:
    with Session() as session:
        result = session.query(User).filter_by(user_id=int(user_id)).first()
        return bool(result)


def get_all_admins() -> list[User]:
    with Session() as session:
        result = session.query(User).filter(User.is_admin != 0).all()
        return result


def check_admin(user_id: int) -> bool:
    with Session() as session:
        result = session.query(User).filter_by(user_id=int(user_id)).filter(User.is_admin != 0).first()
        return bool(result)


def add_admin(user_id: int, owner_id: int):
    with Session() as session:
        session.query(User).filter(User.user_id == user_id).update({'is_admin': owner_id},
                                                                   synchronize_session="fetch")
        session.commit()


def remove_admin(user_id: int):
    with Session() as session:
        session.query(User).filter(User.user_id == user_id).update({'is_admin': 0},
                                                                   synchronize_session="fetch")
        session.commit()


def add_user(user_id: int, lang: str, first_name, last_name, username, ref_id=None) -> User:
    with Session() as session:
        result = session.query(User).filter_by(user_id=int(user_id)).first()
        if result is None:
            new_user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username,
                            ref_id=ref_id, lang=lang, register_datetime=datetime.now())
            session.add(new_user)
            session.commit()
        return result


def edit_user_info(user_id: int, setting: str, new_value: str):
    with Session() as session:
        session.query(User).filter(User.user_id == user_id).update({setting: new_value},
                                                                   synchronize_session="fetch")
        session.commit()


def get_user_by_user_id(user_id: int) -> User:
    with Session() as session:
        result = session.query(User).filter_by(user_id=int(user_id)).first()
        return result


def get_user_by_id(id_user: int) -> User:
    with Session() as session:
        result = session.query(User).filter_by(id=id_user).first()
        return result


def get_ref_count(user_id: int) -> int:
    with Session() as session:
        users = [i[0] for i in session.query(User.ref_id)]
    return int(users.count(user_id))


def get_all_ref() -> list[User]:
    with Session() as session:
        users = [i for i in session.query(User) if i.ref_id is not None]
    return users


def get_all_users() -> list[User]:
    with Session() as session:
        result = session.query(User).all()
        return result


def add_balance(user_id, summ):
    with Session() as session:
        user_info = session.query(User).filter_by(user_id=int(user_id)).first()
        session.query(User).filter(User.user_id == user_id).update({"balance": user_info.balance + summ},
                                                                   synchronize_session="fetch")
        session.commit()


def add_ref_balance(user_id, summ):
    with Session() as session:
        user_info = session.query(User).filter_by(user_id=int(user_id)).first()
        session.query(User).filter(User.user_id == user_id).update({"ref_earned": user_info.ref_earned + summ},
                                                                   synchronize_session="fetch")

        session.commit()
