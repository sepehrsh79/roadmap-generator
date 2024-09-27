from typing import Type

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from ..config import settings
from .base import SQLBase


class DBManager:
    def __init__(
        self, model_base: Type[DeclarativeBase], db_url: str | URL, **kwargs  # type: ignore
    ) -> None:
        self.model_base = model_base
        self.db_url = db_url

        if "sqlite" in db_url:
            kwargs = {}

        self.engine = create_async_engine(
            db_url,
            **kwargs,
        )

        self.session_maker = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
        )

    async def drop_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.model_base.metadata.drop_all)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.model_base.metadata.create_all)

    def get_session(self):
        return self.session_maker()

    def begin(self):
        return self.session_maker.begin()


SQL_DB = DBManager(
    model_base=SQLBase,
    db_url=settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
)


async def get_db():
    async with SQL_DB.begin() as session:
        yield session