from typing import Optional

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)


def async_engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url)


def create_session_factory(db_url: str, engine: Optional[AsyncEngine] = None) -> async_sessionmaker[AsyncSession]:
    if engine is None:
        engine = async_engine(db_url=db_url)

    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


def async_session(db_url: str, session_factory: Optional[async_sessionmaker[AsyncSession]] = None) -> AsyncSession:
    if session_factory is None:
        session_factory = create_session_factory(db_url=db_url)
    return session_factory()
