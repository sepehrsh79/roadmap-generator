import datetime

from pydantic import BaseModel

from src.enums import StatusEnum


class RoadmapBase(BaseModel):
    topic: str
    description: str | None = None
    status: StatusEnum = StatusEnum.learning


class RoadmapOut(RoadmapBase):
    id: int
    user_id: int
    updated_at: datetime.datetime
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class LearningDayBase(BaseModel):
    title: str
    description: str | None = None
    course_link: str | None = None
    checked: bool = False


class LearningDayOut(LearningDayBase):
    id: int
    roadmap_id: int
    user_id: int
    updated_at: datetime.datetime
    created_at: datetime.datetime

    class Config:
        from_attributes = True
