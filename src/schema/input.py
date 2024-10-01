import datetime

from pydantic import BaseModel, conint, constr

from src.enums import LevelEnum, DomainEnum, CostTypeEnum, TimeCommitmentEnum


class InputBase(BaseModel):
    domain: DomainEnum | str
    level: LevelEnum = LevelEnum.beginner
    age: conint(gt=0) = 25  # Age should be positive
    goal: constr(max_length=255) | None = None
    learning_style: list[str] = []
    cost_type: CostTypeEnum = CostTypeEnum.both
    need_certificate: bool = False
    learning_language: str = "English"
    join_community: bool = False
    time_commitment: TimeCommitmentEnum = TimeCommitmentEnum._10_20
    deadline: conint(gt=14) = 28  # Deadline should be more than 14 days


class InputOut(InputBase):
    id: int
    user_id: int
    updated_at: datetime.datetime
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class InputIn(InputBase):
    ...