from sqlalchemy.future import select

from src.core.database import DBManager
from src.models import Roadmap, LearningDay


class RoadmapCRUD:
    @staticmethod
    async def get_roadmaps(db_session: DBManager, user_id: int) -> list[Roadmap] | None:
        result = await db_session.execute(select(Roadmap).filter(Roadmap.user_id == user_id))
        roadmaps = result.scalars().all()
        return roadmaps

    @staticmethod
    async def get_roadmap_by_id(db_session: DBManager, roadmap_id: int, user_id: int):
        result = await db_session.execute(select(Roadmap).filter(Roadmap.id == roadmap_id & Roadmap.user_id == user_id))
        roadmap = result.scalars().first()
        return roadmap

    @staticmethod
    async def get_learning_days_by_roadmap_id(db_session: DBManager, roadmap_id: int, user_id: int):
        result = await db_session.execute(select(LearningDay).join(LearningDay.roadmap).filter(
            LearningDay.roadmap_id == roadmap_id & Roadmap.user_id == user_id))
        learning_days = result.scalars().all()
        return learning_days

    @staticmethod
    async def get_learning_day_by_id(db_session: DBManager, roadmap_id:int, day_id: int, user_id: int):
        result = await db_session.execute(select(LearningDay).join(LearningDay.roadmap).filter(
            LearningDay.id == day_id & LearningDay.roadmap_id == roadmap_id & Roadmap.user_id == user_id))
        learning_day = result.scalars().first()
        return learning_day

    @staticmethod
    async def check_or_uncheck(db_session: DBManager, learning_day):
        learning_day.checked = ~learning_day.checked
        db_session.commit(learning_day)
        return learning_day
