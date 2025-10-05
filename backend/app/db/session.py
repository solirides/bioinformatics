"""Database session management for PGIP."""

from collections.abc import AsyncIterator
from typing import Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings
from app.db.base import Base


class _BaseModel:
    """Placeholder for declarative base injection."""


engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def get_engine() -> AsyncEngine:
    if engine is None:
        raise RuntimeError("Database engine has not been initialized")
    return engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    if _session_factory is None:
        raise RuntimeError("Session factory is not configured")
    return _session_factory


def init_engine(database_url: Optional[str] = None, echo: Optional[bool] = None) -> None:
    """Initialize the async database engine and session factory."""

    global engine, _session_factory

    settings = get_settings()
    url = database_url or settings.database_url
    echo_flag = echo if echo is not None else settings.database_echo

    engine = create_async_engine(url, echo=echo_flag, future=True)
    _session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Yield an async session for request-scoped usage."""

    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session


async def create_all() -> None:
    """Create all database tables."""

    engine_instance = get_engine()
    async with engine_instance.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all() -> None:
    """Drop all database tables."""

    engine_instance = get_engine()
    async with engine_instance.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
