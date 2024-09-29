# from sqlalchemy import ARRAY, Enum, String
# from sqlalchemy.orm import Mapped, mapped_column, validates

# from src.core.database.base import SQLBase
# from src.core.database.mixin import TimestampMixin, IdMixin

# from typing import Annotated

# from src.enums import (
#     LevelEnum,
#     LearningStyleEnum,
#     CostTypeEnum,
#     TimeCommitmentEnum,
#     DomainEnum,
# )


# class Roadmap(SQLBase, IdMixin, TimestampMixin):
#     __tablename__ = "inputs"

#     domain: Mapped[DomainEnum] = mapped_column(default=DomainEnum.others)
#     level: Mapped[LevelEnum] = mapped_column(default=LevelEnum.beginner)
#     age: Mapped[int]
#     goal: Mapped[str | None]
#     learnig_style: Mapped[str | list] = mapped_column(ARRAY(String()), default=[])
#     cost_type: Mapped[Annotated[CostTypeEnum, Enum(CostTypeEnum)]] = mapped_column(
#         default=CostTypeEnum.both
#     )
#     need_certificate: Mapped[bool] = mapped_column(default=False)
#     learning_language: Mapped[str] = mapped_column(default="English")
#     join_community: Mapped[bool] = mapped_column(default=False)
#     time_commitment: Mapped[TimeCommitmentEnum] = mapped_column(
#         default=TimeCommitmentEnum._10_20
#     )  # Time commitment for learning per week
#     deadline: Mapped[int] = mapped_column(default=28)

#     @validates("deadline")
#     def validate_age(self, key, value):
#         if value <= 14:
#             raise ValueError(f"The deadline should be more than 14 days!")
#         return value