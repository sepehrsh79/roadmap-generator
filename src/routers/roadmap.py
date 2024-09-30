from fastapi import APIRouter, Depends

from src.controllers.roadmap import RoadmapController
from src.core.database import DBManager, get_db
from src.depends import get_current_user_from_db
from src.schema.roadmap import RoadmapOut, LearningDayOut
from src.schema.user import UserOut

router = APIRouter(
    prefix="/roadmap",
    tags=[
        "roadmap",
    ],
)


@router.get("/", description="get user roadmaps")
async def get_user_roadmaps(
        db_session: DBManager = Depends(get_db),
        current_user: UserOut = Depends(get_current_user_from_db),
) -> list[RoadmapOut]:
    return await RoadmapController(db_session=db_session, current_user=current_user).get_user_roadmaps()


@router.get("/{roadmap_id}", description="get user roadmap", response_model=RoadmapOut)
async def get_user_roadmap(
        roadmap_id: int,
        db_session: DBManager = Depends(get_db),
        current_user: UserOut = Depends(get_current_user_from_db),
) -> RoadmapOut:
    return await RoadmapController(db_session=db_session, current_user=current_user).get_user_roadmap(
        roadmap_id=roadmap_id
    )


@router.get("/{roadmap_id}/days", description="get user roadmap learning days")
async def get_user_roadmap_learning_days(
        roadmap_id: int,
        db_session: DBManager = Depends(get_db),
        current_user: UserOut = Depends(get_current_user_from_db),
) -> list[LearningDayOut]:
    return await RoadmapController(db_session=db_session, current_user=current_user).get_user_roadmap_learning_days(
        roadmap_id=roadmap_id)


@router.patch("/{roadmap_id}/day/{day_id}/update", description="update user roadmap learning days",
             response_model=LearningDayOut)
async def check_user_roadmap_learning_day(
        roadmap_id: int,
        day_id: int,
        db_session: DBManager = Depends(get_db),
        current_user: UserOut = Depends(get_current_user_from_db),
) -> LearningDayOut:
    return await RoadmapController(db_session=db_session, current_user=current_user).check_user_roadmap_learning_day(
        roadmap_id=roadmap_id, day_id=day_id)
