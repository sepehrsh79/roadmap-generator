import datetime
from uuid import UUID

from pydantic import BaseModel

from src.enums import StatusEnum


class RoadmapBase(BaseModel):
    topic: str
    description: str | None = None
    status: StatusEnum = StatusEnum.learning


class RoadmapOut(RoadmapBase):
    id: int
    user_id: UUID
    updated_at: datetime.datetime
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class LearningDayBase(BaseModel):
    title: str
    description: str | None = None
    course_link: str | None = None
    checked: bool = False
    learning_methods: str | None
    online_groups_and_forums: str | None
    time_planning: str | None
    course: str | None
    course_level: str | None
    course_teacher: str | None
    course_type: str | None
    fee: str | None
    has_certificate: str | None


class LearningDayOut(LearningDayBase):
    id: int
    roadmap_id: int
    user_id: UUID
    updated_at: datetime.datetime
    created_at: datetime.datetime

    class Config:
        from_attributes = True
