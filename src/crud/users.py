import sqlalchemy as sa
from sqlalchemy.future import select

from src.core.database import DBManager
from src.models import User
from src.schema.user import UserQuery


class UserCRUD:
    @staticmethod
    def get_selects():
        return [getattr(User, field) for field in UserQuery.__fields__]

    @staticmethod
    async def get_by_username(db_session: DBManager, username: str):
        user = await db_session.scalars(
            select(User).where(User.username == username)
        )
        return user.first()

    @staticmethod
    async def get_by_id(db_session: DBManager, user_id: str):
        result = await db_session.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        return user

    @staticmethod
    async def query_by_username(db_session: DBManager, username: str):
        result = await db_session.execute(
            select(*UserCRUD.get_selects()).filter(
                User.username.ilike(f"%{username}%")
            )
        )
        return result

    @staticmethod
    async def create(db_session: DBManager, username: str, password: str, gauth: str):
        db_user = User(username=username, password=password, gauth=gauth)
        db_session.add(db_user)
        # await session.flush()
        # await session.refresh(db_user)
        return db_user
