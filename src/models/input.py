from uuid import UUID

from sqlalchemy import ARRAY, Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

from src.core.database.base import SQLBase
from src.core.database.mixin import TimestampMixin, IdMixin

from typing import Annotated

from src.enums import (
    LevelEnum,
    CostTypeEnum,
    TimeCommitmentEnum,
    DomainEnum,
)
from src.models import User


class Input(SQLBase, IdMixin, TimestampMixin):
    __tablename__ = "inputs"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user: Mapped["User"] = relationship("User", back_populates="inputs")
    domain: Mapped[DomainEnum] = mapped_column(default=DomainEnum.backend_development)
    specific_tool: Mapped[str | None] = mapped_column(default=None, nullable=True)
    level: Mapped[LevelEnum] = mapped_column(default=LevelEnum.beginner)
    age: Mapped[int]
    goal: Mapped[str | None]
    learning_style: Mapped[str | list] = mapped_column(ARRAY(String()), default=[])
    cost_type: Mapped[Annotated[CostTypeEnum, Enum[CostTypeEnum]]] = mapped_column(
        default=CostTypeEnum.both
    )
    need_certificate: Mapped[bool] = mapped_column(default=False)
    learning_language: Mapped[str] = mapped_column(default="English")
    join_community: Mapped[bool] = mapped_column(default=False)
    time_commitment: Mapped[TimeCommitmentEnum] = mapped_column(
        default=TimeCommitmentEnum._10_20
    )  # Time commitment for learning per week
    deadline: Mapped[int] = mapped_column(default=28)

    @validates("deadline")
    def validate_age(self, key, value):
        if value <= 14:
            raise ValueError(f"The deadline should be more than 14 days!")
        return value
