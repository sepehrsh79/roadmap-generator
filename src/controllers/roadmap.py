from src.core.database import DBManager
from src.crud.roadmap import RoadmapCRUD
from src.schema.roadmap import RoadmapOut, LearningDayOut

from src.schema.user import UserOut


class RoadmapController:
    roadmap_crud = RoadmapCRUD()

    def __init__(
            self,
            db_session: DBManager,
            current_user: UserOut,
            roadmap_crud: RoadmapCRUD | None = None,
    ):
        self.roadmap_crud = roadmap_crud or self.roadmap_crud
        self.db_session = db_session
        self.current_user = current_user

    async def get_user_roadmaps(self) -> list[RoadmapOut]:
        roadmaps = await self.roadmap_crud.get_roadmaps(self.db_session, user_id=self.current_user.id)
        roadmap_out_list = [RoadmapOut.from_orm(roadmap_instance) for roadmap_instance in roadmaps]
        return roadmap_out_list

    async def get_user_roadmap(self, roadmap_id: int) -> RoadmapOut:
        roadmap = await self.roadmap_crud.get_roadmap_by_id(
            self.db_session, roadmap_id=roadmap_id, user_id=self.current_user.id)
        assert roadmap is not None
        return RoadmapOut.from_orm(roadmap)

    async def get_user_roadmap_learning_days(self, roadmap_id: int) -> list[LearningDayOut]:
        inputs = await self.roadmap_crud.get_learning_days_by_roadmap_id(
            self.db_session, roadmap_id=roadmap_id, user_id=self.current_user.id)
        input_out_list = [LearningDayOut.from_orm(input_instance) for input_instance in inputs]
        return input_out_list

    async def check_user_roadmap_learning_day(self, roadmap_id: int, day_id: int) -> LearningDayOut:
        learning_day = await self.roadmap_crud.get_learning_day_by_id(
            db_session=self.db_session, roadmap_id=roadmap_id, day_id=day_id, user_id=self.current_user.id)
        assert learning_day is not None

        learning_day = await self.roadmap_crud.check_or_uncheck(db_session=self.db_session, learning_day=learning_day)
        return LearningDayOut.from_orm(learning_day)
