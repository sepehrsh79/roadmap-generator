import sqlalchemy as sa
from sqlalchemy.future import select

from src.core.database import DBManager
from src.models import Input
from src.schema.user import UserQuery


class InputCRUD:
    @staticmethod
    async def get_query(db_session: DBManager, user_id: int):
        result = await db_session.execute(select(Input).filter(Input.user_id == user_id))
        inputs = result.scalars().all()
        return inputs

    @staticmethod
    async def get_by_id(db_session: DBManager, input_id: int, user_id: int):
        result = await db_session.execute(select(Input).filter(Input.id == input_id & Input.user_id == user_id))
        input = result.scalars().first()
        return input

    @staticmethod
    async def create(db_session: DBManager, **kwargs):
        db_input = Input(**kwargs)
        db_session.add(db_input)
        await db_session.flush()
        return db_input
